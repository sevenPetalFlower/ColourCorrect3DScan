import cv2
import os
from skimage.metrics import structural_similarity as ssim
import numpy as np

# === Global variables ===
DOCUMENTS_DIR = 'C:/Users/Svitlana/Documents'
INPUT_FOLDER = os.path.join(DOCUMENTS_DIR, 'peach frames')
SAVE_FOLDER = os.path.join(DOCUMENTS_DIR, 'test_images', 'peach_new')
DEPTH_FOLDER = os.path.join(DOCUMENTS_DIR, 'test_images', 'peach_depth_maps')
SSIM_THRESHOLD = 0.7
LAPLACIAN_THRESHOLD = 30
DEPTH_THRESHOLD = 128

# === Ensure save folder exists ===
os.makedirs(SAVE_FOLDER, exist_ok=True)

def is_blurry(image, depth_mask, depth_frame, threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    normalized_depth_frame = depth_frame/255
    # Apply mask to grayscale image
    masked_gray = gray * normalized_depth_frame

    # Compute Laplacian only in masked region
    laplacian = cv2.Laplacian(masked_gray, cv2.CV_64F)
    masked_laplacian = laplacian[depth_mask]

    # Compute variance as blurriness metric
    if masked_laplacian.size > 0:
        blur_score = masked_laplacian.var()
    else:
        blur_score = 0  # or np.nan

    return blur_score < threshold


def is_similar(img1, img2, threshold):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    similarity, _ = ssim(gray1, gray2, full=True)
    return similarity > threshold


def main():
    current_directory = os.getcwd()

    # List all files (including non-files like directories, so filter)
    file_paths = [os.path.join(INPUT_FOLDER, f) for f in os.listdir(INPUT_FOLDER)
                  if f.endswith('.png')]
    file_paths_depth = [os.path.join(DEPTH_FOLDER, f) for f in os.listdir(DEPTH_FOLDER)
                        if f.endswith('.png')]

    prev_saved = None
    for img_path, depth_path in zip(file_paths, file_paths_depth):
        filename_no_ext = os.path.splitext(os.path.basename(img_path))[0]

        frame = cv2.imread(img_path)
        depth_frame = cv2.imread(depth_path, cv2.IMREAD_GRAYSCALE)
        depth_mask = depth_frame > DEPTH_THRESHOLD

        if is_blurry(frame, depth_mask, depth_frame, LAPLACIAN_THRESHOLD):
            continue

        if prev_saved is not None and is_similar(prev_saved, frame, SSIM_THRESHOLD):
            continue

        filename = os.path.join(SAVE_FOLDER, f"{filename_no_ext}.jpg")
        print(f'Saved {filename_no_ext}')
        cv2.imwrite(filename, frame)
        prev_saved = frame.copy()

if __name__ == "__main__":
    main()
