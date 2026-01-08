from pathlib import Path

from .config import Config
from .console import ConsoleStyle
from .normalizer import Normalizer
from .cmd_runner import CmdRunner
from .converter import Converter 

printer=ConsoleStyle()

class Merger:
    processed_files=[]
    def create_file(self):
        """Generate files.txt from a list of files"""

        printer.print_section("Merging Content")
        printer.print_step("Generating files.txt for FFmpeg merge...")
        with open(Config.FILES_TXT, "w") as f:
            for pf in self.processed_files:
                f.write(f"file '{pf.as_posix().replace('temp/', '')}'\n")
        printer.print_success(f"files.txt created at: {Config.FILES_TXT}")

    @staticmethod
    def is_video(file):
        return file.suffix.lower() in Config.VIDEO_EXTENSIONS
    
    @staticmethod
    def is_photo(file):
        return file.suffix.lower() in Config.PHOTO_EXTENSIONS
    
    def merge(self):
        """Merges all the videos together"""
        printer.print_section("Processing Pipeline Started")
        printer.print_step("Scanning input folder...")
        input_files = sorted(Path(Config.INPUT_FOLDER).iterdir())  # sorted for order

        for file in input_files:
            if Merger.is_video(file):
                printer.print_step(f"Normalizing video: [bold]{file.name}[/bold]")
                output_file = Path(Config.NORMALIZED_FOLDER) / file.name
                Normalizer.normalize_video(file, output_file)
                self.processed_files.append(output_file)
            elif Merger.is_photo(file):
                printer.print_step(f"Processing photo: [bold]{file.name}[/bold]")

            # Check if it's HEIC
                if file.suffix.lower() == ".heic":
                # Convert HEIC to JPEG using sips
                    converted_jpeg = Path(Config.CONVERTED_FOLDER) / (file.stem + ".jpeg")
                    printer.print_substep(f"Converting HEIC to JPEG: {file.name} -> {converted_jpeg.name}")
                    CmdRunner.run_cmd(["sips", "-s", "format", "jpeg", str(file), "--out", str(converted_jpeg)])
                    printer.print_success(f"Converted HEIC to JPEG: {converted_jpeg.name}\n")
                    photo_input = converted_jpeg
                else:
                    photo_input = file

            # Convert photo (JPEG/PNG) to video
                output_file = Path(Config.NORMALIZED_FOLDER) / (file.stem + ".mp4")
                printer.print_substep(f"Converting photo to video: {photo_input.name}")
                Converter.convert(photo_input, output_file)
                self.processed_files.append(output_file)
                printer.print_success(f"Converted photo to video: {output_file.name}\n")

            else:
                printer.print_warning(f"Skipping unsupported file: {file.name}")

        Merger.create_file()
        # ----------------------------
        # MERGE EVERYTHING
        # ----------------------------
        printer.print_step("Merging all videos into final output...")
        merge_cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", Config.FILES_TXT,
            "-c:v", Config.VIDEO_CODEC, "-preset", Config.PRESET, "-crf", Config.CRF,
            "-c:a", Config.AUDIO_CODEC,
            Config.OUTPUT_FILE
        ]
        CmdRunner.run_cmd(merge_cmd)

        printer.print_section("Task Completed")
        printer.print_success(f"Merge complete! Final video saved at: [bold]{Config.OUTPUT_FILE}[/bold]")

        delete_temp_cmd=[
            "rm", "-rf","temp"
        ]
        CmdRunner.run_cmd(delete_temp_cmd)