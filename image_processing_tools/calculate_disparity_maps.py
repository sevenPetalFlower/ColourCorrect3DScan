import cv2
import os
import numpy as np

# === CONFIGURATION ===
DOCUMENTS_DIR = 'C:/Users/Svitlana/Documents'
INPUT_FOLDER = os.path.join(DOCUMENTS_DIR, 'peach frames')
OUTPUT_FOLDER = os.path.join(DOCUMENTS_DIR, 'test_images', 'peach_disparity_maps')

# === SETUP ===
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
image_files = sorted(f for f in os.listdir(INPUT_FOLDER) if f.endswith('.png'))

# === StereoSGBM SETTINGS ===
window_size = 5
min_disp = 0
num_disp = 64  # Must be divisible by 16

stereo = cv2.StereoSGBM_create(
    minDisparity=min_disp,
    numDisparities=num_disp,
    blockSize=5,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32,
    disp12MaxDiff=1,
    P1=8 * 3 * window_size ** 2,
    P2=32 * 3 * window_size ** 2,
)

# === PROCESS IMAGE PAIRS ===
for i in range(len(image_files) - 1):
    imgL = cv2.imread(os.path.join(INPUT_FOLDER, image_files[i]), cv2.IMREAD_GRAYSCALE)
    imgR = cv2.imread(os.path.join(INPUT_FOLDER, image_files[i+1]), cv2.IMREAD_GRAYSCALE)

    if imgL is None or imgR is None:
        print(f"Error reading images {image_files[i]} or {image_files[i+1]}")
        continue

    disparity = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    # Normalize for visualization
    disp_vis = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    disp_vis = np.uint8(disp_vis)

    filename = f"disparity_{i:05d}.png"
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, filename), disp_vis)
    print(f"Saved {filename}")

print("✅ Disparity map generation complete.")
