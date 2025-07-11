# src/app.py (updated to use templates and static folders)
from flask import Flask, request, jsonify, render_template
import whisper
import os
import tempfile
from flask_cors import CORS
import torch  # For device detection

app = Flask(__name__, 
            static_folder='../static',  # Point to static/ in project root
            template_folder='../templates')  # Point to templates/ in project root
CORS(app)

# Detect accelerator/device automatically
device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load Whisper model on the detected device
model = whisper.load_model("small.en", device=device)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp_file:
        audio_file.save(tmp_file.name)
        audio_path = tmp_file.name
    
    try:
        result = model.transcribe(audio_path)
        text = result['text'].strip()
    except Exception as e:
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500
    finally:
        if os.path.exists(audio_path):
            os.unlink(audio_path)
    
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)