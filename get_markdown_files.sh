#!/bin/bash
# Helper script to download markdown files from SFTP

echo "Step 1: Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running."
    echo "   Please start Docker Desktop, then run this script again."
    exit 1
fi

echo "✓ Docker is running"
echo ""
echo "Step 2: Starting SFTP server..."
docker-compose up -d sftp-server

echo ""
echo "Step 3: Waiting for SFTP server to be ready..."
sleep 5

echo ""
echo "Step 4: Downloading markdown files..."
python3 download_markdown.py

echo ""
echo "Done! Check the 'sftp-markdown-files' folder for downloaded files."

