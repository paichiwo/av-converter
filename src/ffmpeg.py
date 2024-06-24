from re import search
from threading import Thread
from os import path, environ, makedirs
from CTkMessagebox import CTkMessagebox
from zipfile import ZipFile
from subprocess import PIPE, Popen, CREATE_NO_WINDOW
from src.resource_path import resource_path


class FFMpeg:
    def __init__(self, main_window):
        self.dir_path = path.join(environ['LOCALAPPDATA'], 'AV-Converter')
        self.exe_path = path.join(self.dir_path, 'ffmpeg.exe')
        self.error_window = None
        self.main_window = main_window

        self.unzip_ffmpeg()

    def popup_window(self):
        self.error_window = CTkMessagebox(title='ERROR', message='ffmpeg.zip not found, Quitting...',
                                          icon='warning', option_1='OK')

        response = self.error_window.get()
        if response == 'OK' and self.main_window:
            self.main_window.after(100, self.main_window.destroy)

    def unzip_ffmpeg(self):
        """Unzip ffmpeg file"""
        try:
            if not path.exists(self.exe_path):
                makedirs(self.dir_path, exist_ok=True)

            with ZipFile(resource_path('./ffmpeg/ffmpeg.zip'), 'r') as zip_ref:
                zip_ref.extract('ffmpeg.exe', self.dir_path)
        except FileNotFoundError:
            self.popup_window()

    def use_ffmpeg(self, input_file_path, output_file_path, video_codec, progress_callback=None):
        """Use ffmpeg for conversion"""
        ffmpeg_command = [self.exe_path, '-i', input_file_path, '-c:v', video_codec, '-y', output_file_path]

        process = Popen(args=ffmpeg_command, stdout=PIPE, stderr=PIPE, stdin=PIPE,
                        creationflags=CREATE_NO_WINDOW, universal_newlines=True)

        duration = self.extract_duration(process.stderr)
        self.track_progress(process.stderr, duration, progress_callback)

        progress_thread = Thread(target=self.track_progress, args=(process.stderr, duration, progress_callback))
        progress_thread.start()

    @staticmethod
    def extract_duration(ffmpeg_output):
        """Extract duration information from ffmpeg output"""
        for line in ffmpeg_output:
            if 'Duration: ' in line:
                match = search(r'Duration:\s+(\d{2}):(\d{2}):(\d{2}).\d+', line)
                if match:
                    hours, minutes, seconds = map(int, match.groups())
                    return hours * 3600 + minutes * 60 + seconds

    @staticmethod
    def track_progress(ffmpeg_output, duration, progress_callback):
        """Extract time progress information from ffmpeg output and call the progress_callback"""
        for line in ffmpeg_output:
            if 'time=' in line and duration:
                match = search(r'time=\s*(\d{2}):(\d{2}):(\d{2}).\d+', line)
                if match:
                    hours, minutes, seconds = map(int, match.groups())
                    current_time = hours * 3600 + minutes * 60 + seconds
                    progress = (current_time / duration) * 100
                    progress_callback(progress)
