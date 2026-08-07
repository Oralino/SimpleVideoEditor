import os
import re
import subprocess
import threading
from typing import Callable, Optional
from config import ENCODER_MAP, RESOLUTION_MAP
from utils import parse_time_to_seconds


def process_video(
    infile: str,
    output_dir: str,
    file_name: str,
    start_time: str,
    end_time: str,
    sys_vol: float,
    mic_vol: float,
    is_single_track: bool,
    strip_audio: bool,
    target_res: str,
    selected_encoder: str,
    video_duration: float,
    abort_event: threading.Event,
    progress_callback: Optional[Callable[[float, str], None]] = None,
) -> str:
    # 1. Resolve Target Output Directory
    if output_dir and output_dir.strip():
        target_dir = output_dir.strip()
    else:
        target_dir = os.path.dirname(infile)

    # Automatically create output directory if missing
    os.makedirs(target_dir, exist_ok=True)

    # 2. Resolve Clean File Name
    if file_name and file_name.strip():
        clean_name = file_name.strip()
        if clean_name.lower().endswith((".mp4", ".mkv", ".mov", ".avi")):
            clean_name = os.path.splitext(clean_name)[0]
    else:
        base_name = os.path.splitext(os.path.basename(infile))[0]
        clean_name = f"{base_name}_processed"

    outfile = os.path.join(target_dir, f"{clean_name}.mp4")

    cmd = ["ffmpeg", "-y"]

    start_sec = parse_time_to_seconds(start_time) if start_time else 0.0
    end_sec = parse_time_to_seconds(end_time) if end_time else video_duration
    target_duration = max(end_sec - start_sec, 1.0)

    if start_time:
        cmd.extend(["-ss", start_time])
    if end_time:
        cmd.extend(["-to", end_time])

    cmd.extend(["-i", infile])

    filters = []
    should_scale = target_res != "Original Source"

    if should_scale:
        res = RESOLUTION_MAP.get(target_res, "3440:1440")
        filters.append(f"[0:v]scale={res}[vout]")

    if not strip_audio:
        if is_single_track:
            filters.append(f"[0:a:0]volume={sys_vol:.1f}[aout]")
        else:
            filters.append(f"[0:a:0]volume={sys_vol:.1f}[sys]")
            filters.append(f"[0:a:1]volume={mic_vol:.1f}[mic]")
            filters.append("[sys][mic]amix=inputs=2:duration=longest[aout]")

    if filters:
        cmd.extend(["-filter_complex", ";".join(filters)])

    if should_scale:
        cmd.extend(["-map", "[vout]"])
    else:
        cmd.extend(["-map", "0:v"])

    if strip_audio:
        cmd.append("-an")
    else:
        if filters:
            cmd.extend(["-map", "[aout]"])
        else:
            cmd.extend(["-map", "0:a"])

    if should_scale:
        encoder_args = ENCODER_MAP.get(
            selected_encoder,
            ["-c:v", "libx264", "-preset", "fast", "-crf", "22"],
        )
        cmd.extend(encoder_args)
    else:
        cmd.extend(["-c:v", "copy"])

    if not strip_audio:
        cmd.extend(["-c:a", "aac"])

    cmd.append(outfile)

    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

    process = subprocess.Popen(
        cmd,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        creationflags=creationflags,
    )

    time_pattern = re.compile(r"time=(\d{2}:\d{2}:\d{2}\.\d{2})")

    while True:
        if abort_event.is_set():
            process.kill()
            process.wait()
            if os.path.exists(outfile):
                try:
                    os.remove(outfile)
                except OSError:
                    pass
            raise InterruptedError("Process aborted by user.")

        line = process.stderr.readline()
        if not line and process.poll() is not None:
            break

        if line:
            match = time_pattern.search(line)
            if match and progress_callback:
                current_secs = parse_time_to_seconds(match.group(1))
                progress = min(current_secs / target_duration, 1.0)
                percentage = int(progress * 100)
                progress_callback(progress, f"Processing: {percentage}%")

    if process.returncode != 0 and not abort_event.is_set():
        raise RuntimeError(
            "FFmpeg failed to process. Check input video formatting or audio track modes."
        )

    return outfile