"""
Convert DICOM slices to PNG grouped by series.
Usage: python convert_to_png.py
Requires: pip install pydicom pillow numpy
"""

import os
import sys
from collections import defaultdict

try:
    import pydicom
    import numpy as np
    from PIL import Image
except ImportError:
    print("Missing dependencies. Run: pip install pydicom pillow numpy")
    sys.exit(1)

DICOM_FOLDER = r"C:\Users\jlram\OneDrive\Documents\Jose\IMAGES\DICOMS"
OUTPUT_FOLDER = r"C:\Users\jlram\mri_images"

# Save ALL slices for these series (no sampling) - critical for LCL/ACL assessment
FULL_EXPORT_SERIES = {"2_AX_T2_FS_RIGHT", "6_SAG_T2_FS_RT"}
NUM_SLICES_PER_SERIES = 30  # used for all other series


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

    # Group files by series
    series = defaultdict(list)
    for name in sorted(os.listdir(DICOM_FOLDER)):
        path = os.path.join(DICOM_FOLDER, name)
        if not os.path.isfile(path):
            continue
        try:
            ds = pydicom.dcmread(path, stop_before_pixels=True)
            series_num = str(getattr(ds, "SeriesNumber", "0"))
            series_desc = str(getattr(ds, "SeriesDescription", "unknown")).replace(" ", "_")
            instance = int(getattr(ds, "InstanceNumber", 0))
            key = f"{series_num}_{series_desc}"
            series[key].append((instance, path))
        except Exception:
            pass

    print(f"Found {len(series)} series:\n")
    for key, slices in sorted(series.items()):
        print(f"  Series {key}: {len(slices)} slices")

    print()

    for key, slices in sorted(series.items()):
        slices.sort(key=lambda x: x[0])
        out_dir = os.path.join(OUTPUT_FOLDER, key)
        os.makedirs(out_dir, exist_ok=True)

        if key in FULL_EXPORT_SERIES:
            selected = slices
            print(f"Saving ALL {len(slices)} slices for series: {key}")
        else:
            n = min(NUM_SLICES_PER_SERIES, len(slices))
            indices = np.linspace(0, len(slices) - 1, n, dtype=int)
            selected = [slices[i] for i in indices]
            print(f"Saving {n} slices for series: {key}")
        for i, (instance, path) in enumerate(selected):
            ds = pydicom.dcmread(path)
            img_array = normalize(ds.pixel_array)
            img = Image.fromarray(img_array, mode="L")
            out_path = os.path.join(out_dir, f"slice_{i+1:02d}_inst{instance}.png")
            img.save(out_path)

        print(f"  -> Saved to: {out_dir}")

    print(f"\nDone. Images saved to: {OUTPUT_FOLDER}")


if __name__ == "__main__":
    main()
