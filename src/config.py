from src.resource_path import resource_path

VERSION = '1.2.0'

IMG_PATHS = {
    'icon': resource_path('images/audio-video_converter_icon_512x512.ico'),
    'icon_png': resource_path('images/audio-video_converter_icon_64x64.png'),
    'settings': resource_path('images/settings_icon.png'),
    'filepath': resource_path('images/filepath.png'),
    'folder': resource_path('images/folder_icon.png'),
    'plus': resource_path('images/plus_16x16.png'),
    'plus_large': resource_path('images/plus.png'),
    'github': resource_path('images/github_icon_32x32.png')
}

OUTPUT_FORMATS = [
    '.webm',
    '.mpg',
    '.mp2',
    '.mpeg',
    '.mpe',
    '.mpv',
    '.ogg',
    '.mp4',
    '.m4p',
    '.m4v',
    '.avi',
    '.wmv',
    '.mov',
    '.qt',
    '.flv',
    '.swf',
    '.mp3',
    '.flac',
    '.wav',
    '.aac',
    '.aiff',
    '.m4a',
    '.mkv'
]

D = 'disabled'
N = 'normal'


GITHUB_URL = "https://github.com/paichiwo/"

SETTINGS_HEADER = f"""
AV - CONVERTER v{VERSION}
Paichiwo
2023
"""

SETTINGS_MSG = """
This is simple to use audio-video converter application written in Python.
FFmpeg comes with the app, no need to have it installed.

Convert audio files such as MP3, WAV, AAC, FLAC, etc. between audio formats.
Convert video files such as MP4, AVI, MKV, MOV, etc. to other video or audio.
"""
