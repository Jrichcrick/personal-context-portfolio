#!/usr/bin/env bash
# Download a single podcast episode from Spotify (or any URL yt-dlp supports)
# Usage: ./download-episode.sh <url> [output-dir]
# Example: ./download-episode.sh "https://open.spotify.com/episode/XXXX"
#
# First run: make sure you're logged into Spotify in Chrome/Chromium.
# yt-dlp will pull cookies automatically from your browser.

set -euo pipefail

URL="${1:?Usage: $0 <spotify-episode-url> [output-dir]}"
OUTPUT_DIR="${2:-$HOME/Downloads/podcasts}"
mkdir -p "$OUTPUT_DIR"

echo "Downloading: $URL"
echo "Output dir:  $OUTPUT_DIR"
echo ""

yt-dlp \
  --cookies-from-browser chrome \
  --extract-audio \
  --audio-format mp3 \
  --audio-quality 0 \
  --embed-thumbnail \
  --add-metadata \
  --output "$OUTPUT_DIR/%(uploader)s - %(title)s.%(ext)s" \
  "$URL"

echo ""
echo "Done. File saved to: $OUTPUT_DIR"
echo ""
echo "To get into Pocket Casts:"
echo "  1. Upload the MP3 to Google Drive"
echo "  2. In Pocket Casts: Files tab → + → Google Drive"
