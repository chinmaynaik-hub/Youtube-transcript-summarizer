# YouTube Transcript Summarizer

A Flask-based web application that automatically fetches YouTube video captions and generates AI-powered summaries using Google Gemini API. Supports summarization in multiple Indian regional languages.

## Features

-  Extract captions from any YouTube video
-  AI-powered summarization using Google Gemini API
-  Multi-language support:
  - English, Hindi, Spanish, French, German, Japanese, Kannada, Korean, Chinese, Arabic, Portuguese, Russian, Tamil, Telugu, Bengali, Marathi, Gujarati, Urdu, Malayalam
-  Clean and responsive web interface
-  **Native Firefox Browser Extension** for 1-click summarization
-  Fast and efficient processing

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)
- A Google API key with Gemini API access

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/chinmaynaik-hub/youtube-transcript-summarizer.git
   cd youtube-transcript-summarizer
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Google API key**
   - Create a `.env` file in the root directory
   - Add your Google Gemini API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - 
4. ** Create virtual environment to avoid python dependency conflicts**
   - create virtual environment by running
     | OS | Command |
      |---|---|
      | Windows | `python -m venv venv` |
      | Linux | `python3 -m venv venv` |
   - enter into virtual environment
     | OS/Shell | Command |
      |---|---|
      | Windows Powershell | `.\venv\Scripts\Activate.ps1` |
      | Windows CMD | `.\venv\Scripts\activate.bat` |
      | Bash | `source venv/bin/activate` |
     

## Project Structure

```
your_project_folder/
├── .env                # Environment variables (Google API key)
├── requirements.txt    # contains all the dependencies
├── app.py              # Flask backend application
├── extension/          # Firefox Browser Extension files
│   ├── manifest.json   # Extension configuration
│   ├── popup.html      # Extension UI
│   ├── popup.css       # Extension styles
│   ├── popup.js        # Extension logic
│   └── marked.min.js   # Local markdown parsing script
├── templates/          # HTML templates
│   └── index.html     # Main web interface
└── static/            # Static assets
    └── styles.css      # Stylesheet
```

## Firefox Browser Extension

Bring the summarizer right into your browser!

1. Open Firefox and go to `about:debugging#/runtime/this-firefox`.
2. Click **"Load Temporary Add-on..."**.
3. Select the `manifest.json` file located inside the `extension/` directory.
4. Go to any YouTube video and click the new extension icon in your toolbar to instantly summarize it.

*Note: Your `app.py` Flask server must be actively running in the background for the extension to fetch data!*

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`

3. **Use the application**
   - Paste a YouTube video URL
   - Select your preferred language
   - Click "Summarize" to get the AI-generated summary

## How It Works

1. **Caption Extraction**: The application fetches video captions using the YouTube Transcript API
2. **API Request**: The transcript is sent to Google Gemini API for processing
3. **Summarization**: Gemini generates a concise summary in the selected language
4. **Display**: The summary is returned and displayed on the web interface

## Configuration

### Environment Variables

Create a `.env` file with the following:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

### Supported Languages

- English
- Hindi
- Spanish
- French
- German
- Japanese
- Kannada
- Korean
- Chinese
- Arabic
- Portuguese
- Russian
- Tamil
- Telugu
- Bengali
- Marathi
- Gujarati
- Urdu
- Malayalam

## Dependencies

- **Flask**: Web framework
- **flask-cors**: For secure communication with the browser extension
- **yt-dlp**: For fetching video captions and transcripts
- **google-generativeai**: Google Gemini API client
- **python-dotenv**: Environment variable management

## Troubleshooting

### Common Issues

1. **No captions available**: Some videos don't have captions. Try another video.
2. **API key error**: Ensure your Google API key is valid and has Gemini API access enabled.
3. **Language not supported**: The video must have captions in or translatable to the selected language.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini API for AI-powered summarization
- YouTube Transcript API for caption extraction
- Flask framework for web application development

## Contributors

This project was developed by:

- **[Bheemanagowda](https://github.com/Bheemangowda2405)**
- **[Chetan M I](https://github.com/chetan-mi)**
- **[Chinmay Naik](https://github.com/chinmaynaik-hub)**
- **[Chinmay Soratur](https://github.com/chinmayrs)**

## Contact

Project Link: [https://github.com/chinmaynaik-hub/youtube-transcript-summarizer](https://github.com/chinmaynaik-hub/youtube-transcript-summarizer)

---

⭐ If you find this project useful, please consider giving it a star!
