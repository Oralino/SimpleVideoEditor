import sys
import webbrowser
import customtkinter as ctk
from config import FFMPEG_DOWNLOAD_URL, VLC_DOWNLOAD_URL


class DependencyDialog(ctk.CTk):

    def __init__(self, missing_vlc: bool, missing_ffmpeg: bool):
        super().__init__()

        self.title("Missing Required Dependencies")
        self.geometry("520x360")
        self.resizable(False, False)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.missing_vlc = missing_vlc
        self.missing_ffmpeg = missing_ffmpeg

        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            self,
            text="⚠️ Missing Required Components",
            font=("Segoe UI", 18, "bold"),
            text_color="#e5c07b",
        )
        header.pack(pady=(20, 10))

        desc = ctk.CTkLabel(
            self,
            text="The application requires the following software to be installed\nand available in your system path to function correctly:",
            font=("Segoe UI", 12),
            wraplength=460,
        )
        desc.pack(pady=(0, 15))

        box = ctk.CTkFrame(self, corner_radius=10)
        box.pack(padx=20, pady=5, fill="x")

        # VLC Status & Link
        if self.missing_vlc:
            vlc_frame = ctk.CTkFrame(box, fg_color="transparent")
            vlc_frame.pack(fill="x", padx=15, pady=10)

            vlc_lbl = ctk.CTkLabel(
                vlc_frame,
                text="❌ VLC Media Player (64-bit)",
                font=("Segoe UI", 13, "bold"),
                text_color="#e06c75",
            )
            vlc_lbl.pack(side="left")

            vlc_link = ctk.CTkButton(
                vlc_frame,
                text="🌐 Download VLC",
                width=120,
                height=28,
                fg_color="#2b5b84",
                hover_color="#1d3e5a",
                command=lambda: webbrowser.open(VLC_DOWNLOAD_URL),
            )
            vlc_link.pack(side="right")

        # FFmpeg Status & Link
        if self.missing_ffmpeg:
            ffmpeg_frame = ctk.CTkFrame(box, fg_color="transparent")
            ffmpeg_frame.pack(fill="x", padx=15, pady=10)

            ffmpeg_lbl = ctk.CTkLabel(
                ffmpeg_frame,
                text="❌ FFmpeg / FFprobe",
                font=("Segoe UI", 13, "bold"),
                text_color="#e06c75",
            )
            ffmpeg_lbl.pack(side="left")

            ffmpeg_link = ctk.CTkButton(
                ffmpeg_frame,
                text="🌐 Download FFmpeg",
                width=120,
                height=28,
                fg_color="#2b5b84",
                hover_color="#1d3e5a",
                command=lambda: webbrowser.open(FFMPEG_DOWNLOAD_URL),
            )
            ffmpeg_link.pack(side="right")

        info_lbl = ctk.CTkLabel(
            self,
            text="Please install the missing tools and restart the application.",
            font=("Segoe UI", 11),
            text_color="gray",
        )
        info_lbl.pack(pady=(15, 10))

        close_btn = ctk.CTkButton(
            self,
            text="Exit Application",
            fg_color="#c94a4a",
            hover_color="#963434",
            command=self.exit_app,
        )
        close_btn.pack(pady=5)

    def exit_app(self):
        self.destroy()
        sys.exit(0)