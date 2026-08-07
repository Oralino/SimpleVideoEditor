import threading
from tkinter import messagebox
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

from config import APP_GEOMETRY, APP_MIN_SIZE, APP_TITLE
from ffmpeg_engine import process_video
from ui.left_pane import LeftPanel
from ui.right_pane import RightPanel


class ModernTkinterDnD(ctk.CTk, TkinterDnD.DnDWrapper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


class FFmpegStudioApp(ModernTkinterDnD):

    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.minsize(*APP_MIN_SIZE)
        self.resizable(True, True)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.abort_event = threading.Event()

        self.build_ui()
        self.setup_dnd()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.left_panel = LeftPanel(
            self, on_file_loaded_callback=self.on_file_loaded
        )
        self.left_panel.grid(
            row=0, column=0, padx=(15, 7), pady=15, sticky="nsew"
        )

        self.right_panel = RightPanel(
            self,
            process_callback=self.start_processing_thread,
            abort_callback=self.abort_processing,
        )
        self.right_panel.grid(
            row=0, column=1, padx=(7, 15), pady=15, sticky="nsew"
        )

    def setup_dnd(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.on_file_drop)

    def on_file_drop(self, event):
        raw_path = event.data.strip()
        if raw_path.startswith("{") and raw_path.endswith("}"):
            raw_path = raw_path[1:-1]

        if raw_path.lower().endswith((".mp4", ".mkv", ".mov", ".avi", ".webm")):
            self.left_panel.load_video(raw_path)
        else:
            messagebox.showerror(
                "Invalid File", "Please drop a valid video file."
            )

    def on_file_loaded(self, filepath):
        self.right_panel.set_defaults_from_input(filepath)

    def abort_processing(self):
        self.abort_event.set()

    def start_processing_thread(self):
        if not self.left_panel.input_file:
            messagebox.showerror("Error", "Please load a video file first!")
            return

        self.abort_event.clear()
        self.right_panel.set_processing_state(is_processing=True)
        self.left_panel.pause_video()

        threading.Thread(
            target=self.run_processing_task, daemon=True
        ).start()

    def run_processing_task(self):
        try:
            outfile = process_video(
                infile=self.left_panel.input_file,
                output_dir=self.right_panel.output_dir_entry.get().strip(),
                file_name=self.right_panel.file_name_entry.get().strip(),
                start_time=self.left_panel.start_entry.get().strip(),
                end_time=self.left_panel.end_entry.get().strip(),
                sys_vol=self.right_panel.sys_slider.get(),
                mic_vol=self.right_panel.mic_slider.get(),
                is_single_track=self.right_panel.single_track_switch.get(),
                strip_audio=self.right_panel.strip_audio_switch.get(),
                target_res=self.right_panel.res_option.get(),
                selected_encoder=self.right_panel.encoder_option.get(),
                video_duration=self.left_panel.video_duration,
                abort_event=self.abort_event,
                progress_callback=lambda val, txt: self.after(
                    0, self.right_panel.update_progress, val, txt
                ),
            )

            self.after(
                0,
                self.right_panel.update_progress,
                1.0,
                "Processing Complete!",
            )
            self.after(
                0,
                messagebox.showinfo,
                "Success!",
                f"Video processed successfully!\nSaved to: {outfile}",
            )

        except InterruptedError:
            self.after(
                0,
                self.right_panel.update_progress,
                0.0,
                "Process Aborted & Cleaned Up",
            )
            self.after(
                0,
                messagebox.showwarning,
                "Aborted",
                "Processing was cancelled. Partial file removed.",
            )

        except Exception as e:
            self.after(
                0, self.right_panel.update_progress, 0.0, "Processing Failed"
            )
            self.after(0, messagebox.showerror, "Error", str(e))

        finally:
            self.after(
                0, lambda: self.right_panel.set_processing_state(is_processing=False)
            )