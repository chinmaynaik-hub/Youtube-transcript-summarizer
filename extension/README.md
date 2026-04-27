# YouTube Summarizer in Regional Languages - Source Code

## Description
This Firefox extension summarizes YouTube videos using Google Gemini AI in 19 different languages.

## Build Instructions

### Prerequisites
- No build tools required
- This extension uses vanilla JavaScript (no transpilation, bundling, or minification)

### Third-Party Libraries
- **marked.min.js** (v11.1.1 or latest): Markdown parser
  - Source: https://github.com/markedjs/marked
  - CDN: https://cdn.jsdelivr.net/npm/marked/marked.min.js
  - License: MIT

### Installation Steps

1. **Download marked.min.js** (if not included):
   ```bash
   curl -o marked.min.js https://cdn.jsdelivr.net/npm/marked/marked.min.js
   ```

2. **Verify file structure**:
   ```
   extension/
   ├── manifest.json
   ├── popup.html
   ├── popup.js
   ├── popup.css
   ├── marked.min.js
   ├── logo48.png
   ├── logo96.png
   └── README.md
   ```

3. **Create ZIP for submission**:
   ```bash
   cd extension
   zip -r ../youtube-summarizer-extension.zip *
   ```

### No Build Process Required
- All source files are unminified and human-readable (except third-party library marked.min.js)
- No compilation, transpilation, or bundling steps
- Extension is ready to use as-is

## Backend Requirements
This extension requires a local Flask backend running on `http://localhost:5000` with the `/process_video` endpoint.

## Supported Languages
English, Hindi, Spanish, French, German, Japanese, Korean, Chinese, Arabic, Portuguese, Russian, Kannada, Tamil, Telugu, Bengali, Marathi, Gujarati, Urdu, Malayalam

## License
MIT License

## Contact
Developer: naikchinmay345@gmail.com
