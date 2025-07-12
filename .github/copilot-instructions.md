<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Whisper AI Transcription Service

This project is a Python Flask web application that uses OpenAI's Whisper AI for audio transcription. The application supports:

## Key Features

- YouTube video audio extraction and transcription
- Local audio file upload and transcription
- Multiple Whisper model sizes (tiny, base, small, medium, large)
- Modern responsive web interface
- Transcript download functionality
- Support for multiple audio formats (MP3, MP4, WAV, FLAC, M4A, OGG, WMA, AAC)

## Architecture

- **Backend**: Python Flask application with Whisper AI integration
- **Frontend**: HTML/CSS/JavaScript with modern responsive design
- **Audio Processing**: yt-dlp for YouTube downloads, Whisper for transcription
- **File Handling**: Secure file uploads with cleanup

## Development Guidelines

- Follow Flask best practices for route handling and error management
- Use proper logging for debugging and monitoring
- Implement secure file handling with proper validation
- Maintain clean separation between frontend and backend functionality
- Ensure proper error handling for network operations and file processing

## Dependencies

- OpenAI Whisper for transcription
- Flask for web framework
- yt-dlp for YouTube audio extraction
- Standard Python libraries for file handling and utilities
