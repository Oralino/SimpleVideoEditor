# Application Configuration
APP_TITLE = "FFmpeg Video Editor"
APP_GEOMETRY = "1200x900"
APP_MIN_SIZE = (900, 700)

DEFAULT_SYS_VOL = 0.3
DEFAULT_MIC_VOL = 1.5

RESOLUTION_OPTIONS = [
    "Original Source",
    "3440:1440 (Ultrawide)",
    "2560:1440 (16:9 1440p)",
    "1920:1080 (1080p)",
]

RESOLUTION_MAP = {
    "3440:1440 (Ultrawide)": "3440:1440",
    "2560:1440 (16:9 1440p)": "2560:1440",
    "1920:1080 (1080p)": "1920:1080",
}

# Dependency Download Links
VLC_DOWNLOAD_URL = "https://www.videolan.org/vlc/"
FFMPEG_DOWNLOAD_URL = "https://ffmpeg.org/download.html"


# Encoder Options Mapping
# Maps UI Display Names -> FFmpeg Codec Flags & Quality Settings
ENCODER_OPTIONS = [
    "NVIDIA NVENC AV1 (av1_nvenc)",
    "NVIDIA NVENC HEVC/H.265 (hevc_nvenc)",
    "NVIDIA NVENC H.264 (h264_nvenc)",
    "AMD AMF AV1 (av1_amf)",
    "AMD AMF HEVC/H.265 (hevc_amf)",
    "AMD AMF H.264 (h264_amf)",
    "Intel QSV AV1 (av1_qsv)",
    "Intel QSV HEVC/H.265 (hevc_qsv)",
    "Intel QSV H.264 (h264_qsv)",
    "CPU Software x264 (libx264)",
    "CPU Software x265 (libx265)",
    "CPU Software SVT-AV1 (libsvtav1)",
]

ENCODER_MAP = {
    "NVIDIA NVENC AV1 (av1_nvenc)": [
        "-c:v",
        "av1_nvenc",
        "-preset",
        "p6",
        "-cq",
        "24",
        "-b:v",
        "0",
    ],
    "NVIDIA NVENC HEVC/H.265 (hevc_nvenc)": [
        "-c:v",
        "hevc_nvenc",
        "-preset",
        "p6",
        "-cq",
        "22",
        "-b:v",
        "0",
    ],
    "NVIDIA NVENC H.264 (h264_nvenc)": [
        "-c:v",
        "h264_nvenc",
        "-preset",
        "p6",
        "-cq",
        "20",
        "-b:v",
        "0",
    ],
    "AMD AMF AV1 (av1_amf)": ["-c:v", "av1_amf", "-quality", "quality"],
    "AMD AMF HEVC/H.265 (hevc_amf)": ["-c:v", "hevc_amf", "-quality", "quality"],
    "AMD AMF H.264 (h264_amf)": ["-c:v", "h264_amf", "-quality", "quality"],
    "Intel QSV AV1 (av1_qsv)": [
        "-c:v",
        "av1_qsv",
        "-preset",
        "medium",
        "-global_quality",
        "24",
    ],
    "Intel QSV HEVC/H.265 (hevc_qsv)": [
        "-c:v",
        "hevc_qsv",
        "-preset",
        "medium",
        "-global_quality",
        "22",
    ],
    "Intel QSV H.264 (h264_qsv)": [
        "-c:v",
        "h264_qsv",
        "-preset",
        "medium",
        "-global_quality",
        "20",
    ],
    "CPU Software x264 (libx264)": [
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "22",
    ],
    "CPU Software x265 (libx265)": [
        "-c:v",
        "libx265",
        "-preset",
        "fast",
        "-crf",
        "24",
    ],
    "CPU Software SVT-AV1 (libsvtav1)": [
        "-c:v",
        "libsvtav1",
        "-preset",
        "6",
        "-crf",
        "26",
    ],
}