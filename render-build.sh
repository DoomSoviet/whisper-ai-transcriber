#!/usr/bin/env bash
# Install FFmpeg for Render.com
set -e

apt-get update && apt-get install -y ffmpeg

echo "FFmpeg installed successfully."
