from flask import Flask, request, jsonify, render_template
import whisper
import os
import tempfile
from flask_cors import CORS
import torch
import logging  # Added for logging

app = Flask(__name__, 
            static_folder='../static', 
            template_folder='../templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit uploads to 16MB
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Config from env vars (default to small.en)
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'small.en')
PORT = int(os.getenv('PORT', 5000))

# Detect device
device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Using device: {device}")

# Load model
try:
    model = whisper.load_model(WHISPER_MODEL, device=device)
    logging.info(f"Loaded Whisper model: {WHISPER_MODEL}")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        logging.warning("No audio file in request")
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        logging.warning("Empty audio filename")
        return jsonify({'error': 'Empty audio file'}), 400
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp_file:
        audio_file.save(tmp_file.name)
        audio_path = tmp_file.name
    
    try:
        logging.info(f"Transcribing file: {audio_path}")
        result = model.transcribe(audio_path)
        text = result['text'].strip()
        logging.info("Transcription successful")
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500
    finally:
        if os.path.exists(audio_path):
            os.unlink(audio_path)
    
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True, port=PORT, threaded=True)  # Threaded for better perf