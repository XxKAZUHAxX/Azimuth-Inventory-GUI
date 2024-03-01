import tkinter as tk
import customtkinter as ctk
from Google1 import Create_Service
import pandas as pd

CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
spreadsheet_Id = '1cTvm237Krvm6Mo5G5vs7yR15_KXAM4iiKX614SKyVKs'
service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
mySpreadsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_Id, majorDimension='ROWS', range='DR IN N OUT!A2:AQ3522').execute()
columns, data = mySpreadsheet['values'][0], mySpreadsheet['values'][1:]
df = pd.DataFrame(data, columns=columns)
model_serials = []

class InventoryPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.mainframe = self.controller.create_page(self)
        self.radiobutton_var = ctk.StringVar(self, value='dmr_frame')
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
        ctk.CTkTabview.__init__(self, parent, width=1920, height=1080, fg_color='#FFF2D8', corner_radius=1, anchor='s')
        self.place(relwidth=1, relheight=1)
        self.add("Radio"), self.add("Accessories"), self.add("Others")
        self.serials = {}
        self.model = ''
        global df
        DMRs, POCs, ACCESSORIES, PARTS, OTHERS = [], [], [], [], []
        for i, model in enumerate(df['MODEL']):
            if df['TYPE'][i] == 'DMR':
                DMRs.append(model)
            elif df['TYPE'][i] == 'POC':
                POCs.append(model)
            elif df['TYPE'][i] == 'ACCESSORIES':
                ACCESSORIES.append(model)
            elif df['TYPE'][i] == 'PARTS':
                PARTS.append(model)
            elif df['TYPE'][i] == 'OTHERS':
                OTHERS.append(model)
        dmr_set, poc_set, accessories_set, parts_set, others_set = (
            sorted(set(DMRs))), sorted(set(POCs)), sorted(set(ACCESSORIES)), sorted(set(PARTS)), sorted(set(OTHERS))

        dmr_df = pd.DataFrame(dmr_set)
        poc_df = pd.DataFrame(poc_set)
        accessories_df = pd.DataFrame(accessories_set)
        parts_df = pd.DataFrame(parts_set)
        others_df = pd.DataFrame(others_set)

        DMRFrame(self, self.tab("Radio"), dmr_df), POCFrame(self, self.tab("Radio"), poc_df)
        AccessoriesFrame(self, self.tab("Accessories"), accessories_df), PartsFrame(self, self.tab("Accessories"), parts_df)
        OthersFrame(self, self.tab("Others"), others_df)


    def record(self, model):
        global model_serials
        model_serials = self.serials[model]
        self.page_controller.serialsframe_refresh()
        self.page_controller.show_pageframe("SerialsFrame")


class DMRFrame(ctk.CTkScrollableFrame):
    def __init__(self, frame_controller, parent, data):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='DMR')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row,col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(data.values.flatten()):
            frame_controller.serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='black', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14), command=lambda m=model: frame_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

class POCFrame(ctk.CTkScrollableFrame):
    def __init__(self, frame_controller, parent, data):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='POC')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row, col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(data.values.flatten()):
            frame_controller.serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='black', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14), command=lambda m=model: frame_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

class AccessoriesFrame(ctk.CTkScrollableFrame):
    def __init__(self, frame_controller, parent, data):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='Accessories')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row, col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(data.values.flatten()):
            frame_controller.serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='black', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14), command=lambda m=model: frame_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

class PartsFrame(ctk.CTkScrollableFrame):
    def __init__(self, frame_controller, parent, data):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='Parts')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row, col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(data.values.flatten()):
            frame_controller.serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='black', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14), command=lambda m=model: frame_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

class OthersFrame(ctk.CTkScrollableFrame):
    def __init__(self, frame_controller, parent, data):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='Others')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row, col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(data.values.flatten()):
            frame_controller.serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='black', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14), command=lambda m=model: frame_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

class SerialsFrame(ctk.CTkFrame):
    def __init__(self, parent, page_controller):
        self.page_controller = page_controller
        ctk.CTkFrame.__init__(self, master=parent, fg_color='#FFF2D8')
        self.place(relwidth=1, relheight=1)
        btn_count = ctk.CTkButton(self, width=30, text="Return", command=lambda:self.return_page())
        btn_count.pack()

        self.filtered_serials = list(filter(None, model_serials))
        self.num_of_none = len(model_serials) - len(self.filtered_serials)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color='#FFF2D8', label_text='Serial Numbers')
        self.scrollable_frame.pack(expand=True, fill='both', padx=10, pady=5)
        self.row, self.col = 0, 0
        [self.scrollable_frame.columnconfigure(i, weight=1) for i in range(5)], [self.scrollable_frame.rowconfigure(i, weight=1) for i in range(5)]

        self.filter_serials()
        for i, serial in enumerate(self.filtered_serials):
            frame = ctk.CTkFrame(self.scrollable_frame, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=serial, font=('Arial', 22), text_color='black', wraplength=200)
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
