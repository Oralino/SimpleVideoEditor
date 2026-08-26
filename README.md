# FFmpeg Simple Video Editor
A desktop video trimming and audio mixing utility built with Python, CustomTkinter, VLC, and FFmpeg. Features drag-and-drop support, hardware-accelerated video encoding, dual-track audio volume controls, stream passthrough, and YouTube video fetching.

---

## Features

* **VLC Media Preview:** Frame-accurate video playback and interactive timeline scrubbing.
* **Dual-Track Audio Mixing:** Adjust main system audio and mic volume multipliers separately, or blend them into a single audio stream.
* **Stream Passthrough:** Direct video stream copying (`-c:v copy`) for lightning-fast exports when keeping the original resolution.
* **Hardware Acceleration:** Support for NVIDIA NVENC, AMD AMF, Intel QSV, and CPU encoding options.
* **YouTube Support:** Fetch videos directly via URL using `yt-dlp` for local editing and clipping.
* **Export Customization:** Separate destination folder selection and automatic file naming.
* **Process Control:** Real-time encoding progress tracking with a one-click abort option that cleans up temporary files.

---

## Requirements

### Python Dependencies
* Python 3.10+
* `customtkinter`
* `tkinterdnd2`
* `python-vlc`
* `yt-dlp`

Install required packages:
pip install customtkinter tkinterdnd2 python-vlc yt-dlp



<img width="1497" height="1156" alt="image" src="https://github.com/user-attachments/assets/3723bb12-c1c4-4ed1-864e-f49a7afed4e2" />

