import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from Google1 import Create_Service
import pandas as pd

CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
spreadsheet_Id = '1cTvm237Krvm6Mo5G5vs7yR15_KXAM4iiKX614SKyVKs'
service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
mySpreadsheet = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_Id,
    majorDimension='ROWS',
    range='DR IN N OUT!A2:AQ3522'
).execute()
columns, data = mySpreadsheet['values'][0], mySpreadsheet['values'][1:]
df = pd.DataFrame(data, columns=columns)

class InventoryPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.mainframe = self.controller.create_page(self)
        self.radiobutton_var = ctk.StringVar(self, value='dmr_frame')
        self.serials = {}

        # Create Tabview
        main_tabview = ctk.CTkTabview(self.mainframe, width=1920, height=1080, fg_color='#FFF2D8', corner_radius=1, anchor='s')
        main_tabview.place(relwidth=1, relheight=1)
        main_tabview.add("Radio"), main_tabview.add("Accessories"), main_tabview.add("Others")
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
        dmr_set = sorted(set(DMRs))
        poc_set = sorted(set(POCs))
        accessories_set = sorted(set(ACCESSORIES))
        parts_set = sorted(set(PARTS))
        others_set = sorted(set(OTHERS))

        dmr_df = pd.DataFrame(dmr_set)
        poc_df = pd.DataFrame(poc_set)
        accessories_df = pd.DataFrame(accessories_set)
        parts_df = pd.DataFrame(parts_set)
        others_df = pd.DataFrame(others_set)

        DMRFrame(self, main_tabview.tab("Radio"), dmr_df), POCFrame(self, main_tabview.tab("Radio"), poc_df)
        AccessoriesFrame(self, main_tabview.tab("Accessories"), accessories_df), PartsFrame(self, main_tabview.tab("Accessories"), parts_df)
        OthersFrame(self, main_tabview.tab("Others"), others_df)

    def count(self, serials, model):
        messagebox.showinfo(title='Serial Number(s)', message=serials[model])

    def record(self, model):
        print(model)
        model_serials = ('\t').join(self.serials[model])
        messagebox.showinfo(title='Serial Number(s)', message=model_serials)
        # self.count(model_serials, model)

class DMRFrame(ctk.CTkScrollableFrame):
    def __init__(self, page_controller, parent, data):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='DMR')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row,col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(data.values.flatten()):
            page_controller.serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='black', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14),command=lambda m=model: page_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

class POCFrame(ctk.CTkScrollableFrame):
    def __init__(self, page_controller, parent, data):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='POC')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row, col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(data.values.flatten()):
            page_controller.serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='black', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14), command=lambda m=model: page_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

class AccessoriesFrame(ctk.CTkScrollableFrame):
    def __init__(self, page_controller, parent, data):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='Accessories')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row, col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(data.values.flatten()):
            page_controller.serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='black', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14), command=lambda m=model: page_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

class PartsFrame(ctk.CTkScrollableFrame):
    def __init__(self, page_controller, parent, data):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='Parts')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row, col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(data.values.flatten()):
            page_controller.serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='black', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14), command=lambda m=model: page_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0

class OthersFrame(ctk.CTkScrollableFrame):
    def __init__(self, page_controller, parent, data):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='Others')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        row, col = 0, 0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(data.values.flatten()):
            page_controller.serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(frame, width=30, text=model, font=('Arial', 14), text_color='black', wraplength=200)
            btn_count = ctk.CTkButton(frame, width=30, text=str(len(df[df['MODEL'] == model])), font=('Arial', 14), command=lambda m=model: page_controller.record(m))
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            btn_count.pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 2 == 0:
                row += 1
                col = 0
