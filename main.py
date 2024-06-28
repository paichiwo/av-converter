import os.path
from threading import Thread
from tkinterdnd2 import *
from tkinter import filedialog
from customtkinter import CTk, CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, CTkProgressBar, StringVar, DoubleVar
from CTkMessagebox import CTkMessagebox
from CTkListbox import CTkListbox
from src.CTkScrollableDropdown import *
from src.config import IMG_PATHS, VERSION, OUTPUT_FORMATS
from src.helpers import center_window, imager, load_codecs_from_json
from src.ffmpeg import FFMpeg


class Converter(CTk):
    def __init__(self):
        super().__init__()

        self.iconbitmap(bitmap=IMG_PATHS['icon'])
        self.title(f'AV-Converter v{VERSION}')
        center_window(self, 640, 480)
        self.minsize(640, 480)

        self.files_to_convert = []
        self.codecs = load_codecs_from_json()

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
        self.filelist = CTkListbox(self.mid_frame, border_width=0, corner_radius=10, scrollbar_button_color='grey17',
                                   scrollbar_button_hover_color='grey17')

        # BTM FRAME
        self.dropdown_menu = CTkOptionMenu(self.btm_frame)
        self.dropdown_menu.set('.mp3')
        CTkScrollableDropdown(self.dropdown_menu, values=sorted(OUTPUT_FORMATS), frame_border_width=1)

        self.browse_btn = CTkButton(self.btm_frame, text='BROWSE', command=self.browse_btn_action)
        self.clear_btn = CTkButton(self.btm_frame, text='CLEAR', command=self.clear_btn_action)
        self.convert_btn = CTkButton(self.btm_frame, text='CONVERT', command=self.convert_btn_action)

        # PRG FRAME
        self.progress_bar = CTkProgressBar(self.prg_frame, height=2)
        self.progress_bar.set(0)

        # NFO FRAME
        self.info_lbl = CTkLabel(self.nfo_frame, text='initial test')

        # PLUS LABEL
        self.plus_lbl = CTkLabel(self.mid_frame, image=imager(IMG_PATHS['plus_large'], 64, 64), text='')

        # initialize
        self.ffmpeg = FFMpeg(self)
        self.enable_drag_and_drop()
        self.draw_gui()

    def draw_gui(self):
        self.top_frame.pack(fill='x', padx=40)
        self.top_frame.columnconfigure(0, weight=10)
        self.settings_btn.grid(row=0, column=2, sticky='e', pady=(10, 0))

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

        self.plus_lbl.place(relx=.5, rely=.5, anchor='center')

    def enable_drag_and_drop(self):
        widgets = [self.mid_frame, self.filelist, self.plus_lbl]

        for widget in widgets:
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind('<<Drop>>', self.drop_action)

    def drop_action(self, event):
        if event.data and (event.widget in (self.mid_frame, self.filelist, self.plus_lbl)):
            self.plus_lbl.destroy()
            self.get_filelist(input_array=self.filelist.tk.splitlist(event.data), output_array=self.files_to_convert)

    def get_filelist(self, input_array, output_array):
        for file in input_array:
            if file.endswith(tuple(OUTPUT_FORMATS)):
                output_array.append(file)
                self.filelist.insert('end', file.split('/')[-1])
                self.info_lbl.configure(text='')
            else:
                self.plus_lbl = CTkLabel(self.mid_frame, image=imager(IMG_PATHS['plus_large'], 64, 64), text='')
                self.plus_lbl.place(relx=.5, rely=.5, anchor='center')
                self.info_lbl.configure(text='This format is not allowed')

    def settings_btn_action(self):
        self.info_lbl.configure(text='settings button clicked')

    def browse_btn_action(self):
        files = filedialog.askopenfilenames()
        if files:
            self.plus_lbl.destroy()
            self.get_filelist(input_array=self.filelist.tk.splitlist(files), output_array=self.files_to_convert)

    def clear_btn_action(self):
        self.files_to_convert.clear()
        self.filelist.delete(0, 'end')

    def convert_btn_action(self):
        def progress_call(percentage):
            self.progress_bar.set(round(percentage/100, 3))
            if self.progress_bar.get() == 1:
                self.progress_bar.set(0)
                self.info_lbl.configure(text='Conversion complete')

        def convert():
            extension = self.dropdown_menu.get()
            for input_file in self.files_to_convert:
                name, ext = os.path.splitext(input_file)
                output_file = name + extension
                codec = self.codecs[extension]
                try:
                    self.ffmpeg.use_ffmpeg(input_file, output_file, codec, progress_call)
                except FileNotFoundError:
                    self.info_lbl.configure(text='No ffmpeg.exe found')

        Thread(target=convert).start()


if __name__ == '__main__':
    Converter().mainloop()
