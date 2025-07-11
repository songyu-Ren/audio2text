# Audio-to-Text Webapp

A simple, offline webapp for recording voice (English-only), transcribing it to editable text using OpenAI's Whisper model (local processing), and features like copy/clear text. Runs in your browser via a local Flask server. No cloud APIs—everything on your machine.

## Features
- Start/Stop recording with microphone.
- Automatic transcription using Whisper (supports GPU acceleration on Apple Silicon, NVIDIA, or CPU fallback).
- Editable text output with clear and copy-to-clipboard buttons.
- Modern UI with Bootstrap.
- Configurable Whisper model (e.g., small.en for balance, medium.en for higher accuracy).

## Requirements
- Python 3.10+ (tested on 3.12).
- FFmpeg (for audio processing): Install via package manager (e.g., `brew install ffmpeg` on Mac, `apt install ffmpeg` on Linux, or Chocolatey on Windows).
- Modern browser (Chrome/Safari recommended for mic access).

## Installation
1. Clone the repo:
   ```
   git clone https://github.com/songyu-Ren/audio2text.git
   cd audio2text
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv audio  # Or any name
   source audio/bin/activate  # On Mac/Linux; on Windows: audio\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install flask openai-whisper torch flask-cors
   ```
   - Note: On Windows with NVIDIA GPU, for CUDA support: `pip install torch --index-url https://download.pytorch.org/whl/cu121`

## Running the App
1. Start the server:
   ```
   python src/app.py
   ```
   - Optional configs (set before running):
     - `export WHISPER_MODEL=medium.en` (Mac/Linux) or `set WHISPER_MODEL=medium.en` (Windows) for a more accurate model.
     - `export PORT=8080` to change the port.

2. Open in browser: http://127.0.0.1:5000/ (or your port).
3. Grant microphone permission, record, and transcribe!

## Troubleshooting
- **Model Download**: On first run, Whisper downloads the model (~244MB for small.en)—needs internet once.
- **Slow Transcription**: Use a smaller model (e.g., `tiny.en`) or ensure GPU is detected (check terminal logs).
- **Mic Issues**: Ensure browser permissions; test in incognito if blocked.
- **Errors**: Check terminal logs. For FFmpeg missing: Install it and restart.
- **Windows/Linux Notes**: FFmpeg might need manual path setup; test audio formats.

## Contributing
Fork and PR! Issues welcome.

Built with Flask, Whisper, and vanilla JS/Bootstrap.