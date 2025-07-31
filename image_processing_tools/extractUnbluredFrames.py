import cv2
import os
from skimage.metrics import structural_similarity as ssim
import numpy as np

# === Global variables ===
DOCUMENTS_DIR = 'C:/Users/Svitlana/Documents'
VIDEO_PATH = os.path.join(DOCUMENTS_DIR, 'test_videos', 'peach.mp4')
SAVE_FOLDER = os.path.join(DOCUMENTS_DIR, 'test_images', 'peach_new')
SSIM_THRESHOLD = 0.8
LAPLACIAN_THRESHOLD = 50.0

# === Ensure save folder exists ===
os.makedirs(SAVE_FOLDER, exist_ok=True)

def is_blurry(image, threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return lap_var < threshold

def is_similar(img1, img2, threshold):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    similarity, _ = ssim(gray1, gray2, full=True)
    return similarity > threshold

def process_video():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Failed to open video:", VIDEO_PATH)
        return

    frame_id = 0
    saved_id = 0
    prev_saved = None

    while True:
        print(frame_id)
        ret, frame = cap.read()
        if not ret:
            break

        if is_blurry(frame, LAPLACIAN_THRESHOLD):
            frame_id += 1
            continue

        if prev_saved is not None and is_similar(prev_saved, frame, SSIM_THRESHOLD):
            frame_id += 1
            continue

        filename = os.path.join(SAVE_FOLDER, f"frame_{saved_id:05d}.jpg")
        print(f'Saved {frame_id}')
        cv2.imwrite(filename, frame)
        prev_saved = frame.copy()
        saved_id += 1
        frame_id += 1

    cap.release()
    print(f"Done. Saved {saved_id} frames.")

if __name__ == "__main__":
    process_video()
