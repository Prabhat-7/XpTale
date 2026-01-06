import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

# ----------------------------
# CONFIGURATION
# ----------------------------
INPUT_FOLDER = "input"
NORMALIZED_FOLDER = "temp/normalized"   # ALL videos
CONVERTED_FOLDER = "temp/converted"     # ONLY converted images

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
os.makedirs(NORMALIZED_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

os.makedirs(os.path.dirname(FILES_TXT), exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# ----------------------------
# CLI STYLING HELPERS
# ----------------------------
def print_section(title):
    """Prints a styled box around the section title."""
    console.print(Panel(f"[bold magenta]{title}[/bold magenta]", expand=False, border_style="bold magenta"))

def print_step(msg):
    """Prints a processing step."""
    console.print(f"[cyan]  ➜ {msg}[/cyan]")

def print_substep(msg):
    """Prints a sub-step detail."""
    console.print(f"    [blue]↳ {msg}[/blue]")

def print_success(msg):
    """Prints a success message."""
    console.print(f"[green]  ✔ {msg}[/green]")

def print_warning(msg):
    """Prints a warning message."""
    console.print(f"[yellow]  ⚠ {msg}[/yellow]")

def print_error(msg):
    """Prints an error message."""
    console.print(f"[red]  ✖ {msg}[/red]")

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def run_cmd(cmd):
    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,   # hide normal output
            stderr=subprocess.PIPE,     # capture errors
            text=True
        )
    except subprocess.CalledProcessError as e:
        print_error("Command failed:")
        console.print(f"      [red]{' '.join(cmd)}[/red]")
        console.print(f"\n    [bold]--- ERROR OUTPUT ---[/bold]")
        console.print(f"    [red]{e.stderr}[/red]")
        raise  # stop the program

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
    run_cmd(cmd)

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
    run_cmd(cmd)



# ----------------------------
# MAIN PIPELINE
# ----------------------------
print_section("Processing Pipeline Started")
print_step("Scanning input folder...")
input_files = sorted(Path(INPUT_FOLDER).iterdir())  # sorted for order

processed_files = []

for file in input_files:
    if is_video(file):
        print_step(f"Normalizing video: [bold]{file.name}[/bold]")
        output_file = Path(NORMALIZED_FOLDER) / file.name
        normalize_video(file, output_file)
        processed_files.append(output_file)
    elif is_photo(file):
        print_step(f"Processing photo: [bold]{file.name}[/bold]")

    # Check if it's HEIC
        if file.suffix.lower() == ".heic":
        # Convert HEIC to JPEG using sips
            converted_jpeg = Path(CONVERTED_FOLDER) / (file.stem + ".jpeg")
            print_substep(f"Converting HEIC to JPEG: {file.name} -> {converted_jpeg.name}")
            run_cmd(["sips", "-s", "format", "jpeg", str(file), "--out", str(converted_jpeg)])
            print_success(f"Converted HEIC to JPEG: {converted_jpeg.name}\n")
            photo_input = converted_jpeg
        else:
            photo_input = file

    # Convert photo (JPEG/PNG) to video
        output_file = Path(NORMALIZED_FOLDER) / (file.stem + ".mp4")
        print_substep(f"Converting photo to video: {photo_input.name}")
        photo_to_video(photo_input, output_file)
        processed_files.append(output_file)
        print_success(f"Converted photo to video: {output_file.name}\n")

    else:
        print_warning(f"Skipping unsupported file: {file.name}")


# ----------------------------
# GENERATE files.txt
# ----------------------------
print_section("Merging Content")
print_step("Generating files.txt for FFmpeg merge...")
with open(FILES_TXT, "w") as f:
    for pf in processed_files:
        f.write(f"file '{pf.as_posix().replace('temp/', '')}'\n")
print_success(f"files.txt created at: {FILES_TXT}")
# ----------------------------
# MERGE EVERYTHING
# ----------------------------
print_step("Merging all videos into final output...")
merge_cmd = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", FILES_TXT,
    "-c:v", VIDEO_CODEC, "-preset", PRESET, "-crf", CRF,
    "-c:a", AUDIO_CODEC,
    OUTPUT_FILE
]
run_cmd(merge_cmd)

print_section("Task Completed")
print_success(f"Merge complete! Final video saved at: [bold]{OUTPUT_FILE}[/bold]")

delete_temp_cmd=[
    "rm", "-rf","temp"
]
run_cmd(delete_temp_cmd)