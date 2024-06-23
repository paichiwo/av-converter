import json
from os import environ, path, makedirs, startfile
from customtkinter import CTkImage
from PIL import Image
from src.resource_path import resource_path
from zipfile import ZipFile


def center_window(window, width, height):
    """Create a window in the center of the screen, using desired dimensions"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


def get_downloads_folder_path():
    """Get the path to the Downloads folder on Windows"""
    user_profile = environ['USERPROFILE']
    downloads_folder = path.join(user_profile, 'Downloads')
    return downloads_folder


def imager(file_path, x, y):
    """Create image with CTK"""
    return CTkImage(Image.open(file_path), size=(x, y))


def load_settings():
    """Load settings from JSON file"""
    file_path = path.join(environ['LOCALAPPDATA'], 'Tube-Getter', 'settings.json')

    try:
        with open(file_path, 'r') as file:
            return json.load(file).get('output_folder')

    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return get_downloads_folder_path()


def save_settings(data, file_name):
    """Save settings to JSON file"""
    file_path = path.join(environ['LOCALAPPDATA'], 'Tube-Getter')
    settings_path = path.join(file_path, file_name)

    if not path.exists(file_path):
        makedirs(file_path)

    with open(settings_path, 'w') as file:
        json.dump(data, file)


def open_downloads_folder():
    """Open target folder"""
    startfile(load_settings())


def unzip_ffmpeg():
    """Unzip ffmpeg file"""
    dir_path = path.join(environ['LOCALAPPDATA'], 'Tube-Getter')
    exe_path = path.join(dir_path, 'ffmpeg.exe')

    if not path.exists(exe_path):
        makedirs(dir_path, exist_ok=True)

    with ZipFile(resource_path('ffmpeg/ffmpeg.zip'), 'r') as zip_ref:
        zip_ref.extract('ffmpeg.exe', dir_path)
