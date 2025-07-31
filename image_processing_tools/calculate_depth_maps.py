import os
import torch
import cv2

# === CONFIGURATION ===
DOCUMENTS_DIR = 'C:/Users/Svitlana/Documents'
INPUT_FOLDER = os.path.join(DOCUMENTS_DIR, 'peach frames')
OUTPUT_FOLDER = os.path.join(DOCUMENTS_DIR, 'test_images', 'peach_depth_maps')


def calculateDepthMap(img):
    # Load MiDaS model
    midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")  # Use "DPT_Large" for better quality
    midas.eval()

    # Move model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    midas.to(device)

    # Load transforms
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    transform = midas_transforms.small_transform  # use .dpt_transform if using DPT_Large

    input_batch = transform(img).to(device)

    # Inference
    with torch.no_grad():
        prediction = midas(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False
        ).squeeze()

    # Convert to numpy
    depth_map = prediction.cpu().numpy()

    # Normalize for visualization
    depth_min = depth_map.min()
    depth_max = depth_map.max()
    depth_vis = (depth_map - depth_min) / (depth_max - depth_min)

    return depth_vis


if __name__=="__main__":
    current_directory = os.getcwd()

    # List all files (including non-files like directories, so filter)
    file_paths = [os.path.join(INPUT_FOLDER, f) for f in os.listdir(INPUT_FOLDER)
                  if  f.endswith('.png')]

    for path in file_paths:
        filename_no_ext = os.path.splitext(os.path.basename(path))[0]

        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Load rectified grayscale stereo pair
        depth_map = calculateDepthMap(img)
        depth_file_name = f'{filename_no_ext}.png'
        save_path = os.path.join(OUTPUT_FOLDER, depth_file_name)
        cv2.imwrite(save_path, (depth_map * 255).astype('uint8'))