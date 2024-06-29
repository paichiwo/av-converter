from customtkinter import CTkScrollableFrame, CTkFrame, CTkLabel, CTkButton
from src.popup_menu import CTkPopupMenu


class ListBox(CTkScrollableFrame):
    def __init__(self, master, data=None, info_lbl=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.data = data if data is not None else []
        self.frames = []
        self.selected_frame = None
        self.info_lbl = info_lbl

        self.configure(fg_color='grey17', scrollbar_button_color='grey17', scrollbar_button_hover_color='grey17')
        self.create_frames()
        self.draw_frames()
        self.update_frame_indices()
        self.bind_scroll_events()

    def bind_scroll_events(self):
        self.bind_all('<MouseWheel>', self._on_mousewheel)

    def _on_mousewheel(self, event):
        self._parent_canvas.yview_scroll(-1 * (int(event.delta / 120) * 16), 'units')

    def create_frames(self):
        for entry in self.data:
            frame = SingleFrame(self, entry, self.on_frame_left_click, self.delete_selected_frame)
            self.frames.append(frame)
        self.update_frame_indices()

    def draw_frames(self):
        for frame in self.frames:
            frame.pack(padx=5, pady=3, fill='x')

    def delete(self):
        for frame in self.frames:
            frame.delete()
        self.frames.clear()

    def delete_frame(self, frame):
        frame_index = frame.index
        frame.delete()
        self.frames.remove(frame)
        if frame_index < len(self.data):
            del self.data[frame_index]
        self.update_frame_indices()
        self.info_lbl.configure(text=f'{self.data[frame_index].split('/')[-1]} - deleted')

    def delete_selected_frame(self):
        if self.selected_frame is not None:
            self.delete_frame(self.selected_frame)
            self.selected_frame = None
        else:
            self.info_lbl.configure(text='Nothing selected')

    def update_frame_indices(self):
        for i, frame in enumerate(self.frames):
            frame.index = i

    def on_frame_left_click(self, clicked_frame, event):
        if self.selected_frame:
            self.selected_frame.configure(fg_color='grey17')

        self.selected_frame = clicked_frame
        self.selected_frame.configure(fg_color=CTkButton(self).cget('fg_color'))


class SingleFrame(CTkFrame):
    def __init__(self, master, data=None, left_click_callback=None, delete_callback=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.data = data
        self.index = 0
        self.left_click_callback = left_click_callback
        self.delete_callback = delete_callback

        self.title_lbl = CTkLabel(master=self, text=self.data.split('/')[-1])

        self.right_click_menu = CTkPopupMenu(master=self, width=80, height=50, corner_radius=8, border_width=1)
        self.right_click_delete_btn = CTkButton(self.right_click_menu.frame, text='Delete', command=self.on_delete_click,
                                                text_color=('black', 'white'), hover_color=('grey90', 'grey25'),
                                                compound='left', anchor='w', fg_color='transparent', corner_radius=5)
        self.right_click_delete_btn.pack(expand=True, fill='x', padx=10, pady=0)

        self.draw()
        self.bind_keys()

    def draw(self):
        self.title_lbl.pack(anchor='center', side='left', padx=10)

    def bind_keys(self):
        self.bind('<Button-1>', self.on_left_click)
        self.title_lbl.bind('<Button-1>', self.on_left_click)
        self.bind('<Button-3>', self.on_right_click)
        self.title_lbl.bind('<Button-3>', self.on_right_click)

    def on_left_click(self, event):
        if self.left_click_callback:
            self.left_click_callback(self, event)

    def on_right_click(self, event):
        self.right_click_menu.popup(event)

    def on_delete_click(self):
        if self.delete_callback:
            self.delete_callback()

    def delete(self):
        self.destroy()
