import os
import threading
from subprocess import PIPE, CompletedProcess, Popen
from tkinterdnd2 import *
from tkinter import filedialog
from customtkinter import CTk, CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, CTkProgressBar, StringVar, DoubleVar
from CTkMessagebox import ctkmessagebox
from CTkListbox import CTkListbox
from src.CTkScrollableDropdown import *
from src.config import IMG_PATHS, VERSION, OUTPUT_FORMATS
from src.helpers import center_window, imager


class Converter(CTk):
    def __init__(self):
        super().__init__()

        self.iconbitmap(bitmap=IMG_PATHS['icon'])
        self.title(f'AV-Converter v{VERSION}')
        center_window(self, 640, 480)
        self.minsize(640, 480)

        # GUI
        self.top_frame = CTkFrame(self, fg_color='transparent')
        self.mid_frame = CTkFrame(self, corner_radius=30)
        self.btm_frame = CTkFrame(self, fg_color='transparent')
        self.prg_frame = CTkFrame(self)
        self.nfo_frame = CTkFrame(self, corner_radius=0)

        # TOP FRAME
        self.settings_btn = CTkButton(self.top_frame, image=imager(IMG_PATHS['settings'], 20, 20),
                                      text='', width=40, fg_color='transparent', command=self.settings_btn_action)
        # MID FRAME
        self.filelist = CTkListbox(self.mid_frame, border_width=0, corner_radius=10, scrollbar_button_color='grey17')

        # BTM FRAME
        self.dropdown_menu = CTkOptionMenu(self.btm_frame)
        self.dropdown_menu.set('.mp3')
        CTkScrollableDropdown(self.dropdown_menu, values=sorted(OUTPUT_FORMATS), frame_border_width=1)

        self.browse_btn = CTkButton(self.btm_frame, text='BROWSE')
        self.clear_btn = CTkButton(self.btm_frame, text='CLEAR')
        self.convert_btn = CTkButton(self.btm_frame, text='CONVERT')

        # PRG FRAME
        self.progress_bar = CTkProgressBar(self.prg_frame, height=2)
        self.progress_bar.set(0)

        # NFO FRAME
        self.info_lbl = CTkLabel(self.nfo_frame, text='initial test')

        self.draw_gui()

    def draw_gui(self):
        self.top_frame.pack(fill='x', padx=40)
        self.top_frame.columnconfigure(0, weight=10)
        self.settings_btn.grid(row=0, column=2, sticky='e', padx=(0, 10), pady=(10, 0))

        self.mid_frame.pack(fill='both', expand=True, padx=40, pady=10)
        self.mid_frame.columnconfigure(0, weight=1)
        self.filelist.pack(fill='both', expand=True, padx=10, pady=10)

        self.btm_frame.pack(fill='x', padx=40, pady=(0, 20))
        self.btm_frame.rowconfigure(0, weight=10)
        self.btm_frame.rowconfigure(1, weight=10)
        self.btm_frame.rowconfigure(2, weight=10)
        self.btm_frame.columnconfigure(0, weight=10)
        self.btm_frame.columnconfigure(1, weight=10)
        self.btm_frame.columnconfigure(2, weight=10)
        self.dropdown_menu.grid(row=0, column=1, pady=(10, 20))
        self.browse_btn.grid(row=1, column=0, sticky='w')
        self.clear_btn.grid(row=1, column=1)
        self.convert_btn.grid(row=1, column=2, sticky='e')

        self.prg_frame.pack(fill='x')
        self.progress_bar.pack(fill='x')

        self.nfo_frame.pack(fill='x')
        self.info_lbl.pack(fill='x', padx=10, side='left')

    def settings_btn_action(self):
        print('settings button clicked')



if __name__ == '__main__':
    Converter().mainloop()