#!/bin/bash

# === Configuration ===
SAVE_DIR="Write save dir location here"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
TEMPFILE="$SAVE_DIR/temp_capture.NEF"
mkdir -p "$SAVE_DIR"
killall gvfs-gphoto2-volume-monitor &>/dev/null

# === Set camera parameters ===
gphoto2 --set-config /main/imgsettings/iso=200
gphoto2 --set-config /main/capturesettings/f-number=5
gphoto2 --set-config /main/capturesettings/shutterspeed=1/50

# === Capture image ===
echo "Capturing image..."
gphoto2 --capture-image-and-download --filename "$TEMPFILE"

# === Check if capture succeeded ===
if [ $? -ne 0 ]; then
    echo "❌ Capture failed."
    exit 1
fi

# === Extract real metadata using exiftool ===
ISO_CLEAN=$(exiftool -ISO -s -s -s "$TEMPFILE")
FNUMBER_CLEAN=$(exiftool -FNumber -s -s -s "$TEMPFILE" | sed 's/^f//;s/\./p/')
EXPOSURE_CLEAN=$(exiftool -ShutterSpeed -s -s -s "$TEMPFILE" | sed 's/ /_/g;s/\//-/g;s/^-//')

# === Compose final filename ===
FILENAME="capture_iso${ISO_CLEAN}_f${FNUMBER_CLEAN}_${EXPOSURE_CLEAN}_${TIMESTAMP}.NEF"
FINALFILE="$SAVE_DIR/$FILENAME"

# === Rename the file ===
mv "$TEMPFILE" "$FINALFILE"

echo "✅ Saved as: $FINALFILE"
