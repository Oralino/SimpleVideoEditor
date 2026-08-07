import os
from tkinter import filedialog
import customtkinter as ctk
from config import (
    DEFAULT_MIC_VOL,
    DEFAULT_SYS_VOL,
    ENCODER_OPTIONS,
    RESOLUTION_OPTIONS,
)


class RightPanel(ctk.CTkFrame):

    def __init__(self, parent, process_callback, abort_callback):
        super().__init__(parent, corner_radius=15)
        self.process_callback = process_callback
        self.abort_callback = abort_callback
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(
            self, text="Audio Mixing & Levels", font=("Segoe UI", 15, "bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.single_track_switch = ctk.CTkSwitch(
            self,
            text="Single Audio Track Mode (No Split Mic)",
            command=self.toggle_track_mode,
        )
        self.single_track_switch.pack(anchor="w", padx=15, pady=(5, 10))

        self.sys_label = ctk.CTkLabel(
            self, text=f"Main Volume Multiplier: {DEFAULT_SYS_VOL}"
        )
        self.sys_label.pack(anchor="w", padx=15)
        self.sys_slider = ctk.CTkSlider(
            self,
            from_=0.0,
            to=2.0,
            number_of_steps=20,
            command=self.update_sys_label,
        )
        self.sys_slider.set(DEFAULT_SYS_VOL)
        self.sys_slider.pack(fill="x", padx=15, pady=(0, 10))

        self.mic_label = ctk.CTkLabel(
            self, text=f"Mic Volume Multiplier: {DEFAULT_MIC_VOL}"
        )
        self.mic_label.pack(anchor="w", padx=15)
        self.mic_slider = ctk.CTkSlider(
            self,
            from_=0.0,
            to=3.0,
            number_of_steps=30,
            command=self.update_mic_label,
        )
        self.mic_slider.set(DEFAULT_MIC_VOL)
        self.mic_slider.pack(fill="x", padx=15, pady=(0, 10))

        self.strip_audio_switch = ctk.CTkSwitch(
            self, text="Strip Audio Completely (Mute Video)"
        )
        self.strip_audio_switch.pack(anchor="w", padx=15, pady=5)

        ctk.CTkLabel(
            self,
            text="Resolution & Video Encoder",
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor="w", padx=15, pady=(15, 5))

        ctk.CTkLabel(self, text="Target Resolution:").pack(anchor="w", padx=15)
        self.res_option = ctk.CTkOptionMenu(self, values=RESOLUTION_OPTIONS)
        self.res_option.set("Original Source")
        self.res_option.pack(fill="x", padx=15, pady=(2, 10))

        self.encoder_label = ctk.CTkLabel(self, text="Video Encoder Codec:")
        self.encoder_label.pack(anchor="w", padx=15)

        self.encoder_option = ctk.CTkOptionMenu(self, values=ENCODER_OPTIONS)
        self.encoder_option.set("NVIDIA NVENC AV1 (av1_nvenc)")
        self.encoder_option.pack(fill="x", padx=15, pady=(2, 10))

        ctk.CTkLabel(
            self, text="Export Settings", font=("Segoe UI", 15, "bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))

        ctk.CTkLabel(self, text="Output Path:").pack(anchor="w", padx=15)

        folder_box = ctk.CTkFrame(self, fg_color="transparent")
        folder_box.pack(fill="x", padx=15, pady=(2, 8))
        folder_box.grid_columnconfigure(0, weight=1)

        self.output_dir_entry = ctk.CTkEntry(
            folder_box, placeholder_text="Select destination folder..."
        )
        self.output_dir_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.browse_folder_btn = ctk.CTkButton(
            folder_box,
            text="📁 Browse",
            width=80,
            command=self.browse_folder_location,
        )
        self.browse_folder_btn.grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(self, text="File Name (No extension needed):").pack(
            anchor="w", padx=15
        )

        self.file_name_entry = ctk.CTkEntry(
            self, placeholder_text="e.g. Clip 1"
        )
        self.file_name_entry.pack(fill="x", padx=15, pady=(2, 10))

        self.progress_label = ctk.CTkLabel(
            self, text="Ready", font=("Segoe UI", 12)
        )
        self.progress_label.pack(anchor="w", padx=15, pady=(10, 2))

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0.0)
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 10))

        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(fill="x", padx=15, pady=(10, 15))
        btn_box.grid_columnconfigure(0, weight=3)
        btn_box.grid_columnconfigure(1, weight=1)

        self.process_btn = ctk.CTkButton(
            btn_box,
            text="🚀 Process Video",
            font=("Segoe UI", 14, "bold"),
            height=45,
            fg_color="#2fa572",
            hover_color="#1e7e54",
            command=self.process_callback,
        )
        self.process_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.abort_btn = ctk.CTkButton(
            btn_box,
            text="🛑 Abort",
            font=("Segoe UI", 14, "bold"),
            height=45,
            fg_color="#c94a4a",
            hover_color="#963434",
            state="disabled",
            command=self.abort_callback,
        )
        self.abort_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    def browse_folder_location(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.output_dir_entry.delete(0, "end")
            self.output_dir_entry.insert(0, selected_folder)

    def set_defaults_from_input(self, input_filepath: str):
        folder_path, base_filename = os.path.split(input_filepath)
        raw_name, _ = os.path.splitext(base_filename)

        self.output_dir_entry.delete(0, "end")
        self.output_dir_entry.insert(0, folder_path)

        self.file_name_entry.delete(0, "end")
        self.file_name_entry.insert(0, f"{raw_name}_processed")

    def toggle_track_mode(self):
        if self.single_track_switch.get():
            self.mic_slider.configure(state="disabled")
            self.mic_label.configure(text_color="gray")
            self.sys_label.configure(
                text=f"Single Track Volume Multiplier: {self.sys_slider.get():.1f}"
            )
        else:
            self.mic_slider.configure(state="normal")
            self.mic_label.configure(text_color="white")
            self.sys_label.configure(
                text=f"System Volume Multiplier: {self.sys_slider.get():.1f}"
            )

    def update_sys_label(self, val):
        prefix = (
            "Single Track"
            if self.single_track_switch.get()
            else "System Volume"
        )
        self.sys_label.configure(text=f"{prefix} Multiplier: {val:.1f}")

    def update_mic_label(self, val):
        self.mic_label.configure(text=f"Mic Volume Multiplier: {val:.1f}")

    def update_progress(self, value: float, text: str):
        self.progress_bar.set(value)
        self.progress_label.configure(text=text)

    def set_processing_state(self, is_processing: bool):
        if is_processing:
            self.process_btn.configure(state="disabled")
            self.abort_btn.configure(state="normal")
        else:
            self.process_btn.configure(state="normal")
            self.abort_btn.configure(state="disabled")