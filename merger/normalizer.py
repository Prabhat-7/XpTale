from .config import Config
from .cmd_runner import CmdRunner


class Normalizer:
    @staticmethod
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
            "-c:v", Config.VIDEO_CODEC, "-preset", Config.PRESET, "-crf", Config.CRF,
            "-c:a", Config.AUDIO_CODEC,
            str(output_path)
        ]
        CmdRunner.run(cmd)
