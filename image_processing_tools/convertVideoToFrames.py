import cv2
import os

# Input and output paths
DOCUMENTS_DIR = 'C:/Users/Laysa/Documents/svitlana/keyboard_IPhone'
ROOT_FOLDER =  'side2'
INPUT_FOLDER = os.path.join(DOCUMENTS_DIR)
OUTPUT_FOLDER =  os.path.join(DOCUMENTS_DIR, 'frames')

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Loop through all video files
for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(('.MP4', '.mp4', '.avi', '.mov', '.mkv')):
        video_path = os.path.join(INPUT_FOLDER, filename)
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"❌ Failed to open: {filename}")
            continue

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            print(f"⚠️ Could not determine FPS for {filename}. Skipping.")
            cap.release()
            continue

        frame_interval = int(fps)  # capture 1 frame every second
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_name = os.path.splitext(filename)[0]

        frame_idx = 0
        saved_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % frame_interval == 0:
                frame_filename = f"{video_name}_frame_{saved_count:04d}.jpg"
                frame_path = os.path.join(OUTPUT_FOLDER, frame_filename)
                cv2.imwrite(frame_path, frame)
                saved_count += 1
            frame_idx += 1

        cap.release()
        print(f"✅ Extracted {saved_count} frames from {filename}")

print("🎉 Done extracting frames.")
