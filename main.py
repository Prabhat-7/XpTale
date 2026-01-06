import os
import subprocess
from pathlib import Path

# ----------------------------
# CONFIGURATION
# ----------------------------
INPUT_FOLDER = "input"
TEMP_FOLDER = "temp/normalized"
FILES_TXT = "temp/files.txt"
OUTPUT_FILE = "output/merged.mp4"

# Photo video settings
PHOTO_DURATION = 3  # seconds per photo
FPS = 30
RESOLUTION = "1920:1080"
VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"
CRF = "23"
PRESET = "fast"

# Supported formats
VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv"]
PHOTO_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".heic"]

# ----------------------------
# CREATE TEMP FOLDERS IF NEEDED
# ----------------------------
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(FILES_TXT), exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def is_video(file):
    return file.suffix.lower() in VIDEO_EXTENSIONS

def is_photo(file):
    return file.suffix.lower() in PHOTO_EXTENSIONS

def normalize_video(input_path, output_path):
    """Normalize video resolution, fps, and codec"""
    filter_str = (
        "scale=w=1920:h=1080:"
        "force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
        "setsar=1"
    )
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
      "-vf", filter_str,
        "-c:v", VIDEO_CODEC, "-preset", PRESET, "-crf", CRF,
        "-c:a", AUDIO_CODEC,
        str(output_path)
    ]
    subprocess.run(cmd, check=True)

def photo_to_video(input_path, output_path):
    """Convert photo to short video (maintain aspect ratio + pad)"""
    filter_str = (
        "scale=w=1920:h=1080:"
        "force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
        "setsar=1"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-t", str(PHOTO_DURATION),
        "-i", str(input_path),
        "-vf", filter_str,
        "-c:v", VIDEO_CODEC,
        "-preset", PRESET,
        "-crf", CRF,
        "-r", str(FPS),
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
# ----------------------------
# MAIN PIPELINE
# ----------------------------
print("Scanning input folder...")
input_files = sorted(Path(INPUT_FOLDER).iterdir())  # sorted for order
print(input_files)

processed_files = []

for file in input_files:
    if is_video(file):
        print(f"Normalizing video: {file.name}")
        output_file = Path(TEMP_FOLDER) / file.name
        normalize_video(file, output_file)
        processed_files.append(output_file)
    elif is_photo(file):
        print(f"Processing photo: {file.name}")

    # Check if it's HEIC
        if file.suffix.lower() == ".heic":
        # Convert HEIC to JPEG using sips
            converted_jpeg = Path(TEMP_FOLDER) / (file.stem + ".jpeg")
            print(f"Converting HEIC to JPEG: {file.name} -> {converted_jpeg.name}")
            subprocess.run(["sips", "-s", "format", "jpeg", str(file), "--out", str(converted_jpeg)], check=True)
            photo_input = converted_jpeg
        else:
            photo_input = file

    # Convert photo (JPEG/PNG) to video
        output_file = Path(TEMP_FOLDER) / (file.stem + ".mp4")
        print(f"Converting photo to video: {photo_input.name}")
        photo_to_video(photo_input, output_file)
        processed_files.append(output_file)

    else:
        print(f"Skipping unsupported file: {file.name}")


# ----------------------------
# GENERATE files.txt
# ----------------------------
print("Generating files.txt for FFmpeg merge...")
with open(FILES_TXT, "w") as f:
    for pf in processed_files:
        f.write(f"file '{pf.as_posix().replace('temp/', '')}'\n")
# ----------------------------
# MERGE EVERYTHING
# ----------------------------
print("Merging all videos into final output...")
merge_cmd = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", FILES_TXT,
    "-c:v", VIDEO_CODEC, "-preset", PRESET, "-crf", CRF,
    "-c:a", AUDIO_CODEC,
    OUTPUT_FILE
]
subprocess.run(merge_cmd, check=True)

print(f"✅ Merge complete! Final video saved at: {OUTPUT_FILE}")