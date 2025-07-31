import os
import rawpy
import imageio
from concurrent.futures import ProcessPoolExecutor
from functools import partial

# ==== Global parameters ====
DOCUMENTS_DIR = 'C:/Users/Laysa/Documents/svitlana'
ROOT_FOLDER =  'white_object_final'
IMAGES_FOLDER = os.path.join(DOCUMENTS_DIR, ROOT_FOLDER, 'nef')
SAVE_FOLDER = os.path.join(DOCUMENTS_DIR, ROOT_FOLDER, 'jpg')

# Create save folder if it doesn't exist
os.makedirs(SAVE_FOLDER, exist_ok=True)

# List all NEF files
nef_files = [f for f in os.listdir(IMAGES_FOLDER) if f.lower().endswith('.nef')]

def convert_nef_to_jpg(nef_file, input_folder, output_folder):
    nef_path = os.path.join(input_folder, nef_file)
    jpg_name = os.path.splitext(nef_file)[0] + '.jpg'
    jpg_path = os.path.join(output_folder, jpg_name)

    try:
        with rawpy.imread(nef_path) as raw:
            rgb = raw.postprocess()
            imageio.imwrite(jpg_path, rgb)
        print(f"Converted {nef_file} -> {jpg_name}")
    except Exception as e:
        print(f"Error converting {nef_file}: {e}")

if __name__ == '__main__':
    # Wrap everything inside main
    convert_func = partial(convert_nef_to_jpg, input_folder=IMAGES_FOLDER, output_folder=SAVE_FOLDER)

    with ProcessPoolExecutor() as executor:
        executor.map(convert_func, nef_files)
