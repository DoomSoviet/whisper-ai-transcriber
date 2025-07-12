#!/usr/bin/env python3
"""
Lightweight Whisper AI Transcription Service
A simple web application for transcribing audio files using OpenAI's Whisper AI.
"""

import os
import tempfile
import shutil
from flask import Flask, request, render_template, jsonify, send_file
import logging
from datetime import datetime
import json
from werkzeug.utils import secure_filename

# Try importing whisper - will show helpful error if not installed
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("WARNING: OpenAI Whisper not available. Please install with: pip install openai-whisper")

# Try importing yt-dlp for YouTube support
try:
    import yt_dlp
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False
    print("INFO: YouTube support not available. Install yt-dlp for YouTube functionality.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TRANSCRIPTS_FOLDER'] = 'transcripts'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TRANSCRIPTS_FOLDER'], exist_ok=True)

# Supported file extensions
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'flac', 'm4a', 'ogg', 'wma', 'aac'}

# Global variable to store the Whisper model
whisper_model = None

def load_whisper_model(model_size="base"):
    """Load the Whisper model."""
    global whisper_model
    
    if not WHISPER_AVAILABLE:
        raise Exception("OpenAI Whisper is not installed. Please run: pip install openai-whisper")
    
    if whisper_model is None or getattr(whisper_model, '_model_size', None) != model_size:
        logger.info(f"Loading Whisper model: {model_size}")
        try:
            whisper_model = whisper.load_model(model_size)
            whisper_model._model_size = model_size  # Store model size for reference
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            raise
    return whisper_model

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_youtube_audio(url, output_path):
    """Download audio from YouTube video."""
    if not YOUTUBE_AVAILABLE:
        raise Exception("YouTube support not available. Please install yt-dlp: pip install yt-dlp")
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'extractaudio': True,
            'audioformat': 'mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            ydl.download([url])
            
            # Find the downloaded file
            for file in os.listdir(output_path):
                if file.endswith('.mp3'):
                    return os.path.join(output_path, file), title
                    
        return None, None
    except Exception as e:
        logger.error(f"Error downloading YouTube video: {e}")
        raise

def transcribe_audio(audio_path, model_size="base"):
    """Transcribe audio file using Whisper."""
    try:
        model = load_whisper_model(model_size)
        logger.info(f"Starting transcription of: {audio_path}")
        
        result = model.transcribe(audio_path)
        
        return {
            'text': result['text'],
            'segments': result['segments'],
            'language': result['language']
        }
    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        raise

def save_transcript(transcript_data, filename_base):
    """Save transcript to file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_filename = f"{filename_base}_{timestamp}.json"
    transcript_path = os.path.join(app.config['TRANSCRIPTS_FOLDER'], transcript_filename)
    
    with open(transcript_path, 'w', encoding='utf-8') as f:
        json.dump(transcript_data, f, ensure_ascii=False, indent=2)
    
    return transcript_path

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html', 
                         whisper_available=WHISPER_AVAILABLE,
                         youtube_available=YOUTUBE_AVAILABLE)

@app.route('/transcribe_youtube', methods=['POST'])
def transcribe_youtube():
    """Transcribe audio from YouTube video."""
    if not YOUTUBE_AVAILABLE:
        return jsonify({'error': 'YouTube support not available. Please install yt-dlp: pip install yt-dlp'}), 400
    
    try:
        data = request.get_json()
        youtube_url = data.get('url')
        model_size = data.get('model_size', 'base')
        
        if not youtube_url:
            return jsonify({'error': 'YouTube URL is required'}), 400
        
        # Create temporary directory for download
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download audio from YouTube
            audio_path, video_title = download_youtube_audio(youtube_url, temp_dir)
            
            if not audio_path:
                return jsonify({'error': 'Failed to download audio from YouTube'}), 400
            
            # Transcribe the audio
            transcript = transcribe_audio(audio_path, model_size)
            
            # Add metadata
            transcript['source'] = 'youtube'
            transcript['url'] = youtube_url
            transcript['title'] = video_title
            transcript['timestamp'] = datetime.now().isoformat()
            transcript['model_size'] = model_size
            
            # Save transcript
            safe_title = secure_filename(video_title or 'youtube_video')
            transcript_path = save_transcript(transcript, safe_title)
            
            return jsonify({
                'success': True,
                'transcript': transcript['text'],
                'language': transcript['language'],
                'title': video_title,
                'transcript_file': os.path.basename(transcript_path)
            })
            
    except Exception as e:
        logger.error(f"Error in YouTube transcription: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/transcribe_file', methods=['POST'])
def transcribe_file():
    """Transcribe uploaded audio file."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        model_size = request.form.get('model_size', 'base')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not supported. Supported formats: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Transcribe the audio
            transcript = transcribe_audio(file_path, model_size)
            
            # Add metadata
            transcript['source'] = 'file'
            transcript['filename'] = filename
            transcript['timestamp'] = datetime.now().isoformat()
            transcript['model_size'] = model_size
            
            # Save transcript
            filename_base = os.path.splitext(filename)[0]
            transcript_path = save_transcript(transcript, filename_base)
            
            return jsonify({
                'success': True,
                'transcript': transcript['text'],
                'language': transcript['language'],
                'filename': filename,
                'transcript_file': os.path.basename(transcript_path)
            })
            
        finally:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        logger.error(f"Error in file transcription: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download_transcript/<filename>')
def download_transcript(filename):
    """Download saved transcript file."""
    try:
        transcript_path = os.path.join(app.config['TRANSCRIPTS_FOLDER'], filename)
        if os.path.exists(transcript_path):
            return send_file(transcript_path, as_attachment=True)
        else:
            return jsonify({'error': 'Transcript file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    try:
        status = {
            'status': 'healthy',
            'whisper_available': WHISPER_AVAILABLE,
            'youtube_available': YOUTUBE_AVAILABLE
        }
        
        if WHISPER_AVAILABLE:
            # Try to load the model to verify everything is working
            load_whisper_model()
            status['whisper_loaded'] = True
        
        return jsonify(status)
    except Exception as e:
        return jsonify({
            'status': 'unhealthy', 
            'error': str(e),
            'whisper_available': WHISPER_AVAILABLE,
            'youtube_available': YOUTUBE_AVAILABLE
        }), 500

@app.route('/status')
def status():
    """Get application status and requirements."""
    return jsonify({
        'whisper_available': WHISPER_AVAILABLE,
        'youtube_available': YOUTUBE_AVAILABLE,
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size_mb': app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024),
        'installation_help': {
            'whisper': 'pip install openai-whisper',
            'youtube': 'pip install yt-dlp',
            'ffmpeg': 'Required for audio processing - install from https://ffmpeg.org/'
        }
    })

if __name__ == '__main__':
    print("🎤 Starting Whisper Transcription Service...")
    print("=" * 50)
    
    # Check dependencies
    if not WHISPER_AVAILABLE:
        print("❌ OpenAI Whisper not available")
        print("   Install with: pip install openai-whisper")
    else:
        print("✅ OpenAI Whisper available")
    
    if not YOUTUBE_AVAILABLE:
        print("⚠️  YouTube support not available") 
        print("   Install with: pip install yt-dlp")
    else:
        print("✅ YouTube support available")
    
    print("=" * 50)
    
    if WHISPER_AVAILABLE:
        print("Loading Whisper model (this may take a moment)...")
        try:
            load_whisper_model()
            print("✅ Whisper model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading Whisper model: {e}")
    
    print("🚀 Server starting on http://localhost:5000")
    print("📝 Open the URL in your browser to use the transcription service")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
