"""
Convert key DICOM slices to PNG for AI review.
Usage: python convert_to_png.py
Requires: pip install pydicom pillow numpy
"""

import os
import sys

try:
    import pydicom
    import numpy as np
    from PIL import Image
except ImportError:
    print("Missing dependencies. Run: pip install pydicom pillow numpy")
    sys.exit(1)

DICOM_FOLDER = r"C:\Users\jlram\OneDrive\Documents\Jose\IMAGES\DICOMS"
OUTPUT_FOLDER = r"\\wsl$\Ubuntu\home\user\stef\mri_images"
NUM_SLICES = 20


def normalize(pixel_array):
    arr = pixel_array.astype(np.float32)
    arr -= arr.min()
    if arr.max() > 0:
        arr /= arr.max()
    return (arr * 255).astype(np.uint8)


def main():
    if not os.path.isdir(DICOM_FOLDER):
        print(f"DICOM folder not found: {DICOM_FOLDER}")
        sys.exit(1)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Load all valid DICOM files
    files = []
    for name in sorted(os.listdir(DICOM_FOLDER)):
        path = os.path.join(DICOM_FOLDER, name)
        if not os.path.isfile(path):
            continue
        try:
            ds = pydicom.dcmread(path)
            instance = int(getattr(ds, "InstanceNumber", 0))
            files.append((instance, path))
        except Exception:
            pass

    files.sort(key=lambda x: x[0])
    print(f"Loaded {len(files)} DICOM slices.")

    if not files:
        print("No valid DICOM files found.")
        sys.exit(1)

    # Pick evenly spaced slices
    indices = np.linspace(0, len(files) - 1, NUM_SLICES, dtype=int)
    selected = [files[i] for i in indices]

    for i, (instance, path) in enumerate(selected):
        ds = pydicom.dcmread(path)
        img_array = normalize(ds.pixel_array)
        img = Image.fromarray(img_array, mode="L")
        out_path = os.path.join(OUTPUT_FOLDER, f"slice_{i+1:02d}_inst{instance}.png")
        img.save(out_path)
        print(f"  Saved: {out_path}")

    print(f"\nDone. {NUM_SLICES} slices saved to: {OUTPUT_FOLDER}")


if __name__ == "__main__":
    main()
