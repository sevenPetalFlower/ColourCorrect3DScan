# 🎥 White Balancing and Demosaicing with DCRAW

This guide walks you through white balancing and demosaicing a RAW `.NEF` image using DCRAW, guided by spectral measurements from a spectroradiometer.

---

## 📏 Step 1: Measure the White Point with Spectroradiometer

To obtain the accurate white point under your specific lighting conditions:

1. Place a calibrated white tile under your illumination setup.
2. Use a spectroradiometer (e.g. CS2000) to measure the reflected light.
3. Run the provided MATLAB script:

```matlab
MeasureWhitePoint.m
```

This will:

- Trigger CS2000 to measure the XYZ white point
- Save the values in a `.mat` file for further processing
- Extract the camera's color transformation matrix  
- Calculate the white balance multipliers  

---

## ⚙️ Step 2: Install DCRAW

You will need DCRAW to convert `.NEF` files to `.TIFF` while applying white balance and demosaicing.

- 📥 Download DCRAW for Windows from:  
  https://dcraw.en.softonic.com/

- 📚 Learn more about DCRAW features and parameters:  
  http://www.guillermoluijk.com/tutorial/dcraw/index_en.htm

---

## 🛠️ Step 3: Convert RAW Images with `convertNEF2tiff.bat`

This batch script simplifies calling DCRAW across an image folder.

### ✏️ Edit the script before running:

Open `convertNEF2tiff.bat` and set the following paths:

```bat
set DCRAW_PATH='Path to dcraw.exe'
set IMAGE_FOLDER='Path to your NEF images'
```

Then run the script in terminal:

```cmd
convertNEF2tiff.bat
```

This will apply white balance, demosaic, and convert all `.NEF` files to `.TIFF`.
This process ensures consistent color correction from physical measurement to image output.

➡️ **Next:** [Capture Dataset for 3D Reconstruction](captureDatasetFor3DReconstruction.md.md)
