// static/script.js
let mediaRecorder;
let audioChunks = [];
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const clearBtn = document.getElementById('clearBtn');
const copyBtn = document.getElementById('copyBtn');
const textOutput = document.getElementById('textOutput');
const status = document.getElementById('status');

startBtn.onclick = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        mediaRecorder.start();
        audioChunks = [];
        mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
        startBtn.disabled = true;
        stopBtn.disabled = false;
        clearBtn.disabled = true;  // Disable clear during recording
        copyBtn.disabled = true;  // Disable copy during recording
        status.textContent = 'Recording...';
    } catch (err) {
        status.textContent = `Error starting recording: ${err.message}`;
    }
};

stopBtn.onclick = () => {
    mediaRecorder.stop();
    mediaRecorder.onstop = async () => {
        status.textContent = 'Processing transcription...';
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        
        try {
            const response = await fetch('/transcribe', { method: 'POST', body: formData });
            const data = await response.json();
            if (data.text) {
                textOutput.value = data.text;
                status.textContent = 'Transcription complete. Edit the text as needed.';
                clearBtn.disabled = false;  // Enable clear after transcription
                copyBtn.disabled = false;  // Enable copy after transcription
            } else {
                status.textContent = `Error: ${data.error}`;
            }
        } catch (err) {
            status.textContent = `Fetch error: ${err.message}`;
        }
        
        startBtn.disabled = false;
        stopBtn.disabled = true;
    };
};

// Clear button functionality
clearBtn.onclick = () => {
    textOutput.value = '';
    status.textContent = 'Text cleared. Ready for next recording.';
    clearBtn.disabled = true;  // Disable after clearing until next transcription
    copyBtn.disabled = true;  // Disable copy after clearing
};

// Copy button functionality
copyBtn.onclick = async () => {
    try {
        await navigator.clipboard.writeText(textOutput.value);
        status.textContent = 'Text copied to clipboard!';
    } catch (err) {
        status.textContent = `Error copying text: ${err.message}`;
    }
};