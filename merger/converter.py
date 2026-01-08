from .cmd_runner import CmdRunner
from .config import Config


class Converter:
    @staticmethod
    def convert(input_path, output_path):
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
            "-t", str(Config.PHOTO_DURATION),
            "-i", str(input_path),
            "-vf", filter_str,
            "-c:v", Config.VIDEO_CODEC,
            "-preset", Config.PRESET,
            "-crf", Config.CRF,
            "-r", str(Config.FPS),
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        CmdRunner.run(cmd)
