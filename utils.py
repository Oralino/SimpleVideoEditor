import os
import shutil
import subprocess
import vlc


def check_ffmpeg_installed() -> bool:
    ffmpeg_exists = shutil.which("ffmpeg") is not None or os.path.exists(
        "ffmpeg.exe"
    )
    ffprobe_exists = shutil.which("ffprobe") is not None or os.path.exists(
        "ffprobe.exe"
    )
    return ffmpeg_exists and ffprobe_exists


def check_vlc_installed() -> bool:
    try:
        instance = vlc.Instance("--quiet")
        if instance is not None:
            instance.release()
            return True
        return False
    except Exception:
        return False


def parse_time_to_seconds(time_str: str) -> float:
    if not time_str:
        return 0.0
    parts = time_str.split(":")
    if len(parts) == 3:
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    try:
        return float(time_str)
    except ValueError:
        return 0.0


def format_time(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"


def get_video_duration(filepath: str) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        filepath,
    ]
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=creationflags,
        )
        return float(result.stdout)
    except Exception:
        return 100.0