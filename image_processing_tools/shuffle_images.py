import os
import random
import shutil

# Set your source and target folders
DOCUMENTS_DIR = 'C:/Users/Laysa/Documents/svitlana'
ROOT_FOLDER =  'phone_platform_video_test'
SOURCE_FOLDER = os.path.join(DOCUMENTS_DIR, ROOT_FOLDER, 'frames')
TARGET_FOLDER =  os.path.join(DOCUMENTS_DIR, ROOT_FOLDER, 'shuffled')

# Create target folder if it doesn't exist
os.makedirs(TARGET_FOLDER, exist_ok=True)

# Get all .png files in the source folder
png_files = [f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith('.png')]

# Shuffle the list
random.shuffle(png_files)

# Copy and rename files to target folder
for i, filename in enumerate(png_files):
    src_path = os.path.join(SOURCE_FOLDER, filename)
    dst_path = os.path.join(TARGET_FOLDER, f"{i}.png")
    shutil.copy2(src_path, dst_path)  # copy2 keeps metadata

print(f"Shuffled and copied {len(png_files)} png files to: {TARGET_FOLDER}")
