# Whisper AI Transcription Service

A lightweight web application that uses OpenAI's Whisper AI to transcribe audio from YouTube videos and local audio files.

## Features

- 🎥 **YouTube Video Transcription**: Simply paste a YouTube URL to extract and transcribe audio
- 📁 **Local File Support**: Upload audio files in various formats (MP3, MP4, WAV, FLAC, M4A, OGG, WMA, AAC)
- 🧠 **Multiple AI Models**: Choose from different Whisper model sizes based on your accuracy and speed needs
- 💾 **Download Transcripts**: Save transcriptions as JSON files for later use
- 🌐 **Modern Web Interface**: Clean, responsive design that works on desktop and mobile
- ⚡ **Fast Processing**: Optimized for local processing with automatic cleanup

## Quick Start

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio processing)

### Installation

1. **Clone or download this project**

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg:**

   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html) or use `winget install FFmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

4. **Run the application:**

   ```bash
   python app.py
   ```

5. **Open your browser** and go to `http://localhost:5000`

## Usage

### YouTube Transcription

1. Click the "YouTube" tab
2. Paste a YouTube video URL
3. Select your preferred Whisper model
4. Click "Transcribe YouTube Video"
5. Wait for processing to complete
6. View and download your transcript

### File Transcription

1. Click the "File Upload" tab
2. Drag and drop an audio file or click to browse
3. Select your preferred Whisper model
4. Click "Transcribe Audio File"
5. Wait for processing to complete
6. View and download your transcript

## Whisper Models

| Model  | Speed   | Accuracy | Use Case                              |
| ------ | ------- | -------- | ------------------------------------- |
| Tiny   | Fastest | Lower    | Quick drafts, real-time processing    |
| Base   | Fast    | Good     | General purpose, balanced performance |
| Small  | Medium  | Better   | Higher quality transcriptions         |
| Medium | Slower  | High     | Professional transcriptions           |
| Large  | Slowest | Highest  | Maximum accuracy needed               |

## Supported Audio Formats

- MP3, MP4, WAV, FLAC
- M4A, OGG, WMA, AAC
- Maximum file size: 500MB

## Project Structure

```
study-help/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Temporary file storage (auto-created)
├── transcripts/          # Saved transcripts (auto-created)
└── README.md            # This file
```

## API Endpoints

- `GET /` - Main web interface
- `POST /transcribe_youtube` - Transcribe YouTube video
- `POST /transcribe_file` - Transcribe uploaded file
- `GET /download_transcript/<filename>` - Download saved transcript
- `GET /health` - Health check endpoint

## Configuration

The application can be configured by modifying variables in `app.py`:

- `MAX_CONTENT_LENGTH`: Maximum upload file size (default: 500MB)
- `UPLOAD_FOLDER`: Temporary upload directory
- `TRANSCRIPTS_FOLDER`: Saved transcripts directory

## Troubleshooting

### Common Issues

1. **"FFmpeg not found" error**

   - Install FFmpeg as described in the installation section
   - Ensure FFmpeg is in your system PATH

2. **"Module not found" errors**

   - Run `pip install -r requirements.txt` to install all dependencies

3. **YouTube download fails**

   - Check if the URL is valid and publicly accessible
   - Some videos may be restricted or age-gated

4. **Large files timeout**
   - Use smaller model sizes for faster processing
   - Consider splitting large audio files

### Performance Tips

- Use the "tiny" or "base" models for faster processing
- Process shorter audio segments when possible
- Ensure sufficient disk space for temporary files
- Close other resource-intensive applications during processing

## Development

To contribute or modify the application:

1. Install development dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run in debug mode:

   ```bash
   python app.py
   ```

3. The application will reload automatically when you make changes

## License

This project uses OpenAI's Whisper AI model. Please refer to the [Whisper repository](https://github.com/openai/whisper) for licensing information.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Automatic speech recognition
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube download functionality
- [Flask](https://flask.palletsprojects.com/) - Web framework
