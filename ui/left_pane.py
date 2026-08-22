import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import yt_dlp
import vlc
from utils import format_time, get_video_duration


class LeftPanel(ctk.CTkFrame):

    def __init__(self, parent, on_file_loaded_callback):
        super().__init__(parent, corner_radius=15)
        self.on_file_loaded = on_file_loaded_callback

        self.input_file = ""
        self.video_duration = 0.0
        self.is_seeking = False

        self.vlc_instance = vlc.Instance("--no-xlib", "--quiet")
        self.vlc_player = self.vlc_instance.media_player_new()

        self.build_ui()
        self.start_time_tracker()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.file_btn = ctk.CTkButton(
            self,
            text="📁 Browse Video File",
            command=self.browse_file,
            font=("Segoe UI", 13, "bold"),
            height=35,
        )
        self.file_btn.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")

        self.file_label = ctk.CTkLabel(
            self,
            text="Drag and drop a video file anywhere, or click Browse",
            text_color="gray",
            wraplength=450,
        )
        self.file_label.grid(row=1, column=0, padx=15, pady=(0, 10))

        # YouTube URL input controls
        yt_box = ctk.CTkFrame(self, fg_color="transparent")
        yt_box.grid(row=2, column=0, padx=15, pady=(0, 10), sticky="ew")
        yt_box.grid_columnconfigure(0, weight=1)

        self.yt_entry = ctk.CTkEntry(
            yt_box, placeholder_text="Paste YouTube URL here..."
        )
        self.yt_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.yt_btn = ctk.CTkButton(
            yt_box,
            text="⬇ Fetch",
            width=80,
            command=self.start_youtube_download,
        )
        self.yt_btn.grid(row=0, column=1)

        self.video_panel = tk.Frame(self, bg="black")
        self.video_panel.grid(row=3, column=0, padx=15, pady=5, sticky="nsew")

        self.drop_hint = tk.Label(
            self.video_panel,
            text="📥 Drag & Drop Video File Here",
            fg="#777777",
            bg="black",
            font=("Segoe UI", 14, "bold"),
        )
        self.drop_hint.place(relx=0.5, rely=0.5, anchor="center")

        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.grid(row=4, column=0, padx=15, pady=5, sticky="ew")
        controls.grid_columnconfigure(0, weight=1)

        self.play_btn = ctk.CTkButton(
            controls,
            text="▶ Play",
            command=self.toggle_play,
            state="disabled",
            fg_color="#1f6aa5",
            width=120,
        )
        self.play_btn.pack(pady=5)

        self.scrub_slider = ctk.CTkSlider(
            controls,
            from_=0,
            to=100,
            command=self.on_scrub_move,
            state="disabled",
        )
        self.scrub_slider.pack(fill="x", pady=(5, 0))
        self.scrub_slider.bind("<ButtonRelease-1>", self.on_scrub_release)

        self.time_readout = ctk.CTkLabel(
            controls, text="00:00:00 / 00:00:00", font=("Consolas", 12)
        )
        self.time_readout.pack(pady=2)

        clip_box = ctk.CTkFrame(self, fg_color="transparent")
        clip_box.grid(row=5, column=0, padx=15, pady=(5, 15), sticky="ew")
        clip_box.grid_columnconfigure((0, 1), weight=1)

        self.set_start_btn = ctk.CTkButton(
            clip_box,
            text="✂ Set Start Time",
            command=self.set_start_time,
            state="disabled",
        )
        self.set_start_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.set_end_btn = ctk.CTkButton(
            clip_box,
            text="✂ Set End Time",
            command=self.set_end_time,
            state="disabled",
        )
        self.set_end_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.start_entry = ctk.CTkEntry(
            clip_box, placeholder_text="Start: 00:00:00"
        )
        self.start_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.end_entry = ctk.CTkEntry(
            clip_box, placeholder_text="End: 00:00:00"
        )
        self.end_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def start_youtube_download(self):
        url = self.yt_entry.get().strip()
        if not url:
            return

        self.yt_btn.configure(state="disabled", text="Fetching...")
        self.yt_entry.configure(state="disabled")

        threading.Thread(
            target=self.process_youtube_download, args=(url,), daemon=True
        ).start()

    def process_youtube_download(self, url: str):
        # Creates a directory and downloads the best quality mp4 format
        download_dir = os.path.join(os.getcwd(), "youtube_downloads")
        os.makedirs(download_dir, exist_ok=True)

        def progress_hook(d):
            # Updates the button text with the download percentage
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', '0%').strip()
                self.after(
                    0, lambda p=percent: self.yt_btn.configure(text=f"{p}")
                )

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(download_dir, '%(title)s [%(id)s].%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [progress_hook],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            self.after(0, lambda f=filename: self.on_download_complete(f))
        except Exception as e:
            self.after(
                0,
                lambda err=str(e): messagebox.showerror("Download Error", err),
            )
            self.after(0, self.reset_youtube_ui)

    def on_download_complete(self, filepath: str):
        self.reset_youtube_ui()
        self.load_video(filepath)

    def reset_youtube_ui(self):
        self.yt_btn.configure(state="normal", text="⬇ Fetch")
        self.yt_entry.configure(state="normal")
        self.yt_entry.delete(0, 'end')

    def browse_file(self):
        filepath = tk.filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4 *.mkv *.mov")]
        )
        if filepath:
            self.load_video(filepath)

    def load_video(self, filepath: str):
        self.input_file = filepath
        self.file_label.configure(
            text=os.path.basename(filepath), text_color="white"
        )
        self.drop_hint.place_forget()

        media = self.vlc_instance.media_new(filepath)
        self.vlc_player.set_media(media)

        handle = self.video_panel.winfo_id()
        if os.name == "nt":
            self.vlc_player.set_hwnd(handle)
        else:
            self.vlc_player.set_xwindow(handle)

        self.vlc_player.play()
        time.sleep(0.1)
        self.vlc_player.pause()

        self.video_duration = get_video_duration(filepath)
        self.scrub_slider.configure(
            state="normal", from_=0, to=self.video_duration
        )
        self.scrub_slider.set(0)

        self.play_btn.configure(state="normal", text="▶ Play")
        self.set_start_btn.configure(state="normal")
        self.set_end_btn.configure(state="normal")

        if self.on_file_loaded:
            self.on_file_loaded(filepath)

    def toggle_play(self):
        if not self.input_file:
            return
        if self.vlc_player.is_playing():
            self.vlc_player.pause()
            self.play_btn.configure(text="▶ Play")
        else:
            self.vlc_player.play()
            self.play_btn.configure(text="⏸ Pause")

    def pause_video(self):
        if self.vlc_player.is_playing():
            self.vlc_player.pause()
            self.play_btn.configure(text="▶ Play")

    def on_scrub_move(self, val):
        self.is_seeking = True
        self.time_readout.configure(
            text=f"{format_time(float(val))} / {format_time(self.video_duration)}"
        )

    def on_scrub_release(self, event):
        if self.video_duration > 0:
            target_ms = int(self.scrub_slider.get() * 1000)
            self.vlc_player.set_time(target_ms)
        self.is_seeking = False

    def start_time_tracker(self):
        if self.vlc_player.is_playing() and not self.is_seeking:
            current_ms = self.vlc_player.get_time()
            if current_ms > 0:
                sec = current_ms / 1000.0
                self.scrub_slider.set(sec)
                self.time_readout.configure(
                    text=f"{format_time(sec)} / {format_time(self.video_duration)}"
                )
        self.after(250, self.start_time_tracker)

    def set_start_time(self):
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, format_time(self.scrub_slider.get()))

    def set_end_time(self):
        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, format_time(self.scrub_slider.get()))