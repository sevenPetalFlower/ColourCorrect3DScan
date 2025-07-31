# On the way to Colour correct 3D scanning

This repository contains tools and tutorials for colour correct 3d scans, including automated camera control, remote platform rotation, and image processing workflows including frame extraction, depth/disparity map generation, and NEF image handling.

---

## 📚 Tutorials

- **[Set Up Camera](docs/setUpCamera.md)**
- **[Set Up SwitchBot](docs/setUpSwitchBot.md)**
- **[Capture Dataset for 3D Reconstruction](docs/captureDatasetFor3DReconstruction.md)**
- **[Reconstruct 3D in RealityScan](docs/reconstruct3DRealityScan.md)**

---

## 📸 controlCameraUbuntu

Linux Ubuntu bash tools for capturing images with a DSLR camera via `gphoto2`, and distantly setting camera parameters.

### `camera_installs/`

- **`installs.sh`**  
  Installs necessary packages: `gphoto2`, `exiftool`, and `curl`.

  - **`connect_camera.sh`**  
  Kills `gvfs-gphoto2` processes that might interfere with camera communication. Run before connecting or capturing.
  
- **`capchure_with_camera_parameters.sh`**  
  Captures a RAW image using specified camera settings (ISO, aperture, shutter speed), renames it using `exiftool`, and saves it with camera parametrs and timestamp in the name.

- **`shoot_images.sh`**  
  Automates taking n photos and controls a remote platform (via HTTP API) between shots.

---

## 🔌 controlRemoteRotationPlatform

Contains an HTTP API server that interfaces with a SwitchBot device for remote control.

- **`botApi.py`**  
  A Python server that exposes `/connect`, `/press`, and `/disconnect` endpoints. These control a SwitchBot device to pess a button on the remote control that moves platform 1°. 
---

## 🧠 image_processing_tools

Scripts to extract, filter, analyze, and transform images or videos during post-processing stages.

- **`convertVideoToFrames.py`**  
  Extracts one frame per second from each video in a folder and saves them as JPGs.

- **`extractUnbluredFrames.py`**  
  Removes blurry or too-similar frames based on Laplacian variance and SSIM. Saves clean frames from video.

- **`extractUnbluredFramesWithDepthFiltering.py`**  
  Advanced version of the above: filters blurry frames **based on masked depth information**. Useful for focusing on regions of interest.

- **`calculate_depth_maps.py`**  
  Uses the MiDaS deep model to predict depth from RGB images. Saves normalized grayscale depth maps.

- **`calculate_disparity_maps.py`**  
  Computes disparity maps between stereo pairs using OpenCV’s `StereoSGBM`. Outputs visualizable disparity maps.

- **`nef2jpg.py`**  
  Batch converts `.NEF` raw files to `.JPG` using `rawpy` and `imageio`. Processes files in parallel.

- **`shuffle_images.py`**  
  Randomly shuffles and renames `.png` images from a source folder into a target folder.
