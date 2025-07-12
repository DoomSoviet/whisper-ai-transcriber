# Deployment script for Windows
@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: FFmpeg not found. Please install FFmpeg to process audio files.
    echo You can download it from: https://ffmpeg.org/download.html
    echo Or install with: winget install FFmpeg
) else (
    echo FFmpeg is installed and ready.
)

echo.
echo Starting Whisper Transcription Service...
python app.py

pause
