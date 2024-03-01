import customtkinter as ctk
import pandas as pd
from pprint import pprint
import math

df = None
model_serials = []

class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.mainframe = self.controller.create_page(self)
        self.fg_colors = controller.fg_colors
        global df
        df = controller.df
        self._all_models_dict = controller._all_models_dict
        self.page_frames = {}
        for page_frame in (MainTabview, SerialsFrame):
            page_name = page_frame.__name__
            frame = page_frame(parent=self.mainframe, page_controller=self)
            self.page_frames[page_name] = frame
        self.show_pageframe("MainTabview")

    def show_pageframe(self, page_name):
        """Show frame for a given page name."""
        frame = self.page_frames[page_name]
        frame.tkraise()

    def serialsframe_refresh(self):
        self.page_frames['SerialsFrame'].destroy()
        self.page_frames['SerialsFrame'].__init__(parent=self.mainframe, page_controller=self)

class MainTabview(ctk.CTkTabview):
    def __init__(self, parent, page_controller):
        self.page_controller = page_controller
        ctk.CTkTabview.__init__(self, parent, width=1920, height=1080, fg_color=page_controller.fg_colors['grey'], corner_radius=1, anchor='s')
        self.place(relwidth=1, relheight=1)
        self.serials = {}
        model_keys = [key for key in page_controller._all_models_dict.keys()]
        tabs = [self.add(f"Tab {i+1}") for i in range(math.ceil(len(model_keys)/2))]
        models_df = iter([pd.DataFrame(value) for value in page_controller._all_models_dict.values()])
        models_name = iter(model_keys)
        for tab in tabs:
            try:
                CreateScrollableFrame(self, tab, next(models_df), next(models_name))
                CreateScrollableFrame(self, tab, next(models_df), next(models_name))
            except StopIteration:
                pass

    def record(self, model):
        global model_serials
        model_serials = self.serials[model]
        self.page_controller.serialsframe_refresh()
        self.page_controller.show_pageframe("SerialsFrame")

class CreateScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, frame_controller, parent, data, name):
        super().__init__(master=parent, fg_color=frame_controller.page_controller.fg_colors['grey'], label_text=name)
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row,col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for model in data.values.flatten():
            frame_controller.serials[model] = [df['SERIAL NO.'][df_row] for df_row, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color=frame_controller.page_controller.fg_colors['black'], width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='white', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14),
                                      fg_color=frame_controller.page_controller.fg_colors['orange'], command=lambda m=model: frame_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, fill='both', padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

class SerialsFrame(ctk.CTkFrame):
    def __init__(self, parent, page_controller):
        self.page_controller = page_controller
        ctk.CTkFrame.__init__(self, master=parent, fg_color=page_controller.fg_colors['grey'])
        self.place(relwidth=1, relheight=1)
        btn_count = ctk.CTkButton(self, width=30, text="Return", fg_color=page_controller.fg_colors['orange'],
                                  command=lambda:self.return_page())
        btn_count.pack()

        self.filtered_serials = list(filter(None, model_serials))
        self.num_of_none = len(model_serials) - len(self.filtered_serials)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=page_controller.fg_colors['grey'], label_text='Serial Numbers')
        self.scrollable_frame.pack(expand=True, fill='both', padx=10, pady=5)
        self.row, self.col = 0, 0
        [self.scrollable_frame.columnconfigure(i, weight=1) for i in range(5)], [self.scrollable_frame.rowconfigure(i, weight=1) for i in range(5)]

        self.filter_serials()
        for serial in self.filtered_serials:
            frame = ctk.CTkFrame(self.scrollable_frame, fg_color=page_controller.fg_colors['black'], width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=serial, font=('Arial', 22), text_color='white', wraplength=200)
            frame.grid(row=self.row, column=self.col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            self.col += 1
            if self.col % 5 == 0:
                self.row += 1
                self.col = 0

    def filter_serials(self):
        num_of_none_frame = ctk.CTkFrame(self.scrollable_frame, fg_color='#163020', width=50, height=200)
        num_of_none_label = ctk.CTkLabel(num_of_none_frame, width=30, text=f"Number of None: {self.num_of_none}", font=('Arial', 22), text_color='#FFF2D8', wraplength=200)
        num_of_none_frame.grid(row=self.row, column=self.col, padx=10, pady=10, sticky='nsew')
        num_of_none_label.pack(expand=True, padx=10, pady=10)
        self.col +=1

    def return_page(self):
        self.page_controller.show_pageframe("MainTabview")
