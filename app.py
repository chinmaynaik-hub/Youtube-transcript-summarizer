from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google import genai
import yt_dlp
import re
import logging
import tempfile
import glob

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app) # Enables CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Get the Google API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API key is missing. Please set it in the .env file.")

# Configure the Google API client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    logging.error("Failed to configure Google Generative AI client", exc_info=True)
    raise e

# Define the prompt template for Google Gemini
def get_prompt(language):
    return f"""You are a YouTube video summarizer. Given the transcript of a video, provide a concise and informative summary in {language}. Here's the transcript: """


# Function to extract transcript details from the YouTube video using yt-dlp
def extract_transcript_details(youtube_video_url):
    try:
        # Extract video ID using regex
        match = re.search(r'(?:youtube\.com\/(?:[^\/\n\s]+\/[^\n\s]+|(?:v|e(?:mbed)?)\/|\S*\?v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})', youtube_video_url)
        if not match:
            logging.error("Invalid YouTube URL")
            return None, None
        video_id = match.group(1)

        # Use a temporary directory for subtitle files
        with tempfile.TemporaryDirectory() as tmpdir:
            outtmpl = os.path.join(tmpdir, '%(id)s')
            ydl_opts = {
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'subtitlesformat': 'vtt',
                'outtmpl': outtmpl,
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

            # Find the downloaded subtitle file
            sub_files = glob.glob(os.path.join(tmpdir, '*.vtt'))
            if not sub_files:
                logging.error("No subtitles found for this video")
                return None, None

            # Parse VTT file to extract plain text
            with open(sub_files[0], 'r', encoding='utf-8') as f:
                vtt_content = f.read()

            # Remove VTT headers, timestamps, and formatting tags
            lines = vtt_content.split('\n')
            text_lines = []
            seen = set()
            for line in lines:
                # Skip headers, timestamps, and empty lines
                if re.match(r'^WEBVTT', line) or re.match(r'^Kind:', line) or re.match(r'^Language:', line):
                    continue
                if re.match(r'^\d{2}:\d{2}', line) or re.match(r'^\s*$', line):
                    continue
                if re.match(r'^\d+$', line):
                    continue
                # Remove HTML-like tags
                clean = re.sub(r'<[^>]+>', '', line).strip()
                if clean and clean not in seen:
                    seen.add(clean)
                    text_lines.append(clean)

            transcript = ' '.join(text_lines)
            if not transcript:
                logging.error("Subtitle file was empty after parsing")
                return None, None

            logging.debug(f"Transcript fetched successfully for video ID {video_id}")
            return transcript, video_id

    except Exception as e:
        logging.error("Unexpected error while fetching transcript", exc_info=True)
        return None, None

# Function to generate summary using Google Gemini
def generate_gemini_content(transcript_text, prompt, custom_api_key=None):
    try:
        # Determine which client to use
        request_client = client
        if custom_api_key:
            request_client = genai.Client(api_key=custom_api_key)

        # Use Gemini model for generating summary
        response = request_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt + transcript_text
        )
        logging.debug("Summary generated successfully")
        return response.text
    except Exception as e:
        logging.error("Error generating summary using Gemini", exc_info=True)
        return None

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle YouTube URL and fetch the summary and thumbnail
@app.route('/process_video', methods=['POST'])
def process_video():
    try:
        # Extract YouTube link from the request
        youtube_link = request.json.get('youtube_link')
        if not youtube_link:
            return jsonify({"error": "YouTube URL is required"}), 400

        # Get transcript and video ID
        transcript_text, video_id = extract_transcript_details(youtube_link)
        if not transcript_text or not video_id:
            return jsonify({"error": "Could not fetch transcript or invalid video link"}), 400

        # Generate thumbnail URL
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"

        # Get selected language (default to English)
        language = request.json.get('language', 'English')
        
        # Get custom API key if provided
        custom_api_key = request.json.get('api_key')

        # Generate summary using Google Gemini
        summary = generate_gemini_content(transcript_text, get_prompt(language), custom_api_key)
        if not summary:
            return jsonify({"error": "Failed to generate summary"}), 500

        # Return response
        return jsonify({"thumbnail_url": thumbnail_url, "summary": summary})

    except Exception as e:
        logging.error("Unexpected error in /process_video", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
