from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, VideoUnavailable, TranscriptsDisabled
import re
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Get the Google API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API key is missing. Please set it in the .env file.")

# Configure the Google API client
try:
    genai.configure(api_key=api_key)
except Exception as e:
    logging.error("Failed to configure Google Generative AI client", exc_info=True)
    raise e

# Define the prompt for Google Gemini
prompt = """You are a YouTube video summarizer. Given the transcript of a video, provide a concise and informative summary. Here's the transcript: """

# Function to extract transcript details from the YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        # Extract video ID using regex
        match = re.search(r'(?:youtube\.com\/(?:[^\/\n\s]+\/[^\n\s]+|(?:v|e(?:mbed)?)\/|\S*\?v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})', youtube_video_url)
        if not match:
            logging.error("Invalid YouTube URL")
            return None, None
        video_id = match.group(1)

        # Fetch the transcript
        transcript_segments = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([segment["text"] for segment in transcript_segments])
        logging.debug(f"Transcript fetched successfully for video ID {video_id}")
        return transcript, video_id
    except VideoUnavailable:
        logging.error("Video is unavailable")
        return None, None
    except TranscriptsDisabled:
        logging.error("Transcripts are disabled for this video")
        return None, None
    except Exception as e:
        logging.error("Unexpected error while fetching transcript", exc_info=True)
        return None, None

# Function to generate summary using Google Gemini
def generate_gemini_content(transcript_text, prompt):
    try:
        # Use Gemini model for generating summary
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
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

        # Generate summary using Google Gemini
        summary = generate_gemini_content(transcript_text, prompt)
        if not summary:
            return jsonify({"error": "Failed to generate summary"}), 500

        # Return response
        return jsonify({"thumbnail_url": thumbnail_url, "summary": summary})

    except Exception as e:
        logging.error("Unexpected error in /process_video", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

from googletrans import Translator

@app.route('/translate_summary', methods=['POST'])
def translate_summary():
    data = request.json
    text = data.get('text', '')
    language = data.get('language', '')

    if not text or not language:
        return jsonify({"error": "Text and language are required"}), 400

    try:
        translator = Translator()
        translated = translator.translate(text, dest=language)
        return jsonify({"translated_text": translated.text})
    except Exception as e:
        return jsonify({"error": "Translation failed"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5002)
