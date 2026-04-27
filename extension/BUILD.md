# Build Instructions for Firefox Reviewers

## Overview
This extension does NOT require any build process. All source code is provided as-is.

## System Requirements
- **Operating System**: Any (Windows, macOS, Linux)
- **Build Tools**: None required
- **Dependencies**: None (except third-party library marked.min.js)

## Third-Party Libraries
Only one external library is used:
- **marked.min.js**: MIT-licensed markdown parser from https://github.com/markedjs/marked

## Verification Steps

### Option 1: Use Provided Files (Recommended)
1. Extract the source code ZIP
2. All files are ready to use - no build needed
3. Load the extension in Firefox using `about:debugging`

### Option 2: Download marked.min.js Fresh
If you want to verify the third-party library:

```bash
# Download marked.min.js from official CDN
curl -o marked.min.js https://cdn.jsdelivr.net/npm/marked/marked.min.js

# Or using wget
wget -O marked.min.js https://cdn.jsdelivr.net/npm/marked/marked.min.js
```

## File Structure
```
extension/
├── manifest.json          (Extension configuration)
├── popup.html            (UI markup - unminified)
├── popup.js              (Main logic - unminified)
├── popup.css             (Styles - unminified)
├── marked.min.js         (Third-party library - MIT license)
├── logo48.png            (Icon 48x48)
├── logo96.png            (Icon 96x96)
├── README.md             (Documentation)
└── BUILD.md              (This file)
```

## Source Code Notes
- **popup.js**: 100% original, unminified JavaScript
- **popup.html**: Standard HTML5, no preprocessing
- **popup.css**: Plain CSS, no SASS/LESS/PostCSS
- **marked.min.js**: Only minified file (third-party library)

## No Build Script Needed
Since there is no build process, no build script is provided. The extension works directly from source files.

## Testing
1. Open Firefox
2. Navigate to `about:debugging#/runtime/this-firefox`
3. Click "Load Temporary Add-on"
4. Select `manifest.json` from the extension folder
5. Visit any YouTube video page
6. Click the extension icon to test

## Backend Requirement
The extension communicates with a local Flask server at `http://localhost:5000`. This is documented in the extension description and is required for functionality.
