"""
Read and summarize DICOM MRI files.
Usage: python read_mri.py <folder_path>
Requires: pip install pydicom
"""

import sys
import os

try:
    import pydicom
except ImportError:
    print("pydicom not installed. Run: pip install pydicom")
    sys.exit(1)


def tag(ds, keyword, default="N/A"):
    return str(getattr(ds, keyword, default))


def summarize_series(files):
    if not files:
        return

    # Read first file for header info
    ds = pydicom.dcmread(files[0], stop_before_pixels=True)

    print("=" * 60)
    print("PATIENT / STUDY INFO")
    print("=" * 60)
    print(f"  Patient Name    : {tag(ds, 'PatientName')}")
    print(f"  Patient ID      : {tag(ds, 'PatientID')}")
    print(f"  Date of Birth   : {tag(ds, 'PatientBirthDate')}")
    print(f"  Sex             : {tag(ds, 'PatientSex')}")
    print(f"  Study Date      : {tag(ds, 'StudyDate')}")
    print(f"  Study Time      : {tag(ds, 'StudyTime')}")
    print(f"  Study Desc      : {tag(ds, 'StudyDescription')}")
    print(f"  Referring MD    : {tag(ds, 'ReferringPhysicianName')}")
    print(f"  Institution     : {tag(ds, 'InstitutionName')}")

    print()
    print("=" * 60)
    print("ACQUISITION / SERIES INFO")
    print("=" * 60)
    print(f"  Modality        : {tag(ds, 'Modality')}")
    print(f"  Series Desc     : {tag(ds, 'SeriesDescription')}")
    print(f"  Protocol Name   : {tag(ds, 'ProtocolName')}")
    print(f"  Sequence Name   : {tag(ds, 'SequenceName')}")
    print(f"  Body Part       : {tag(ds, 'BodyPartExamined')}")
    print(f"  Patient Position: {tag(ds, 'PatientPosition')}")
    print(f"  Manufacturer    : {tag(ds, 'Manufacturer')}")
    print(f"  Model           : {tag(ds, 'ManufacturerModelName')}")
    print(f"  Field Strength  : {tag(ds, 'MagneticFieldStrength')} T")

    print()
    print("=" * 60)
    print("MRI PARAMETERS")
    print("=" * 60)
    print(f"  TR (ms)         : {tag(ds, 'RepetitionTime')}")
    print(f"  TE (ms)         : {tag(ds, 'EchoTime')}")
    print(f"  Flip Angle (deg): {tag(ds, 'FlipAngle')}")
    print(f"  Inversion Time  : {tag(ds, 'InversionTime')}")
    print(f"  Echo Train Len  : {tag(ds, 'EchoTrainLength')}")
    print(f"  Slice Thickness : {tag(ds, 'SliceThickness')} mm")
    print(f"  Spacing Between : {tag(ds, 'SpacingBetweenSlices')} mm")
    print(f"  Pixel Spacing   : {tag(ds, 'PixelSpacing')}")
    print(f"  Rows x Cols     : {tag(ds, 'Rows')} x {tag(ds, 'Columns')}")
    print(f"  Number of Slices: {len(files)}")
    print(f"  Scan Options    : {tag(ds, 'ScanOptions')}")
    print(f"  Image Type      : {tag(ds, 'ImageType')}")

    print()
    print("=" * 60)
    print(f"FILES READ: {len(files)} slices from {os.path.dirname(files[0])}")
    print("=" * 60)


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\jlram\OneDrive\Documents\Jose\IMAGES\DICOMS"

    if not os.path.isdir(folder):
        print(f"Folder not found: {folder}")
        sys.exit(1)

    entries = sorted(os.listdir(folder))
    files = [
        os.path.join(folder, f)
        for f in entries
        if not f.startswith(".")
    ]
    files = [f for f in files if os.path.isfile(f)]

    if not files:
        print("No files found in folder.")
        sys.exit(1)

    # Filter to valid DICOM files
    dicom_files = []
    for f in files:
        try:
            pydicom.dcmread(f, stop_before_pixels=True)
            dicom_files.append(f)
        except Exception:
            pass

    print(f"Found {len(dicom_files)} DICOM files.\n")
    summarize_series(dicom_files)


if __name__ == "__main__":
    main()
