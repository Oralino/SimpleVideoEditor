import sys
from ui.app import FFmpegStudioApp
from ui.dependency_dialog import DependencyDialog
from utils import check_ffmpeg_installed, check_vlc_installed

if __name__ == "__main__":
    vlc_ok = check_vlc_installed()
    ffmpeg_ok = check_ffmpeg_installed()

    if not vlc_ok or not ffmpeg_ok:
        # Show dependency prompt dialog if components are missing
        dialog = DependencyDialog(
            missing_vlc=not vlc_ok, missing_ffmpeg=not ffmpeg_ok
        )
        dialog.mainloop()
        sys.exit(0)

    # Launch main application if all dependencies pass
    app = FFmpegStudioApp()
    app.mainloop()