import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import pandas as pd
from datetime import datetime
from pages.create_api_instance import Create_Instance
from pprint import pprint

class DR_InPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.fg_colors = controller.fg_colors
        self.mainframe = self.controller.create_page(self)
        self.service = controller.service
        self.df = controller.df
        self.spreadsheet_id = controller.spreadsheet_id
        self.range = controller.range
        self.entries = {}
        self.str_vars = {}
        self.ordered_result = {}
        self.toplevel_window = None
        self._all_models_dict = controller._all_models_dict
        self._dr_in_scrollframe()

    def _dr_in_scrollframe(self):
        [self.mainframe.columnconfigure(i, weight=1) for i in range(2)], self.mainframe.rowconfigure(0, weight=1)
        self._scrollable_frame = ctk.CTkScrollableFrame(master=self.mainframe, fg_color=self.fg_colors['grey'], label_text='DR IN')
        self._scrollable_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        _submit_button = ctk.CTkButton(self.mainframe, width=100, height=40, text='Submit', font=('Arial', 14),
                                       fg_color=self.fg_colors['orange'], text_color='black', command=lambda: self._submit())
        _submit_button.grid(row=1, column=0, padx=50, pady=10, sticky='nsew')
        _check_button = ctk.CTkButton(self.mainframe, width=100, height=40, text='Check', font=('Arial', 14),
                                      fg_color=self.fg_colors['orange'], text_color='black')
        _check_button.grid(row=1, column=1, padx=50, pady=10, sticky='nsew')
        self._dr_in_contents()

    def _dr_in_contents(self):
        row, col = 0, 0
        details = ['PO NUMBER', 'DR NUMBER', 'STORE', 'BRAND', 'BUYING PRICE', 'MODEL', 'TYPE', 'UNIT REMARKS',
                   'DL PRICE', 'SERIAL NUMBER', 'IMEI 1', 'IMEI 2']
        data = ('12345', '54321', 'Azimuth', 'Kirisun', '5000', 'DP-405', '', '10', '50000')
        to_be_inserted = iter(data)
        main_frame_inside_scrollable = ctk.CTkFrame(self._scrollable_frame, fg_color=self.fg_colors['black'], width=100, height=200)
        main_frame_inside_scrollable.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10, sticky='nsew')
        [self._scrollable_frame.columnconfigure(i, weight=1) for i in range(3)], [self._scrollable_frame.rowconfigure(i, weight=1) for i in range(2)]
        [main_frame_inside_scrollable.columnconfigure(i, weight=1) for i in range(4)]
        for i, j in enumerate(details[:9]):
            self.str_vars[j] = ctk.StringVar()
            self.str_vars[j].set(next(to_be_inserted))
            frame = ctk.CTkFrame(main_frame_inside_scrollable, fg_color=self.fg_colors['black'], width=100, height=200)
            label = ctk.CTkLabel(frame, width=30, text=j, font=self.controller.font, text_color='white', wraplength=200)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10)
            if i+1 == 6:
                self.entries[j] = ctk.CTkComboBox(frame, values=[""], width=400, height=50, fg_color='#FFF2D8', text_color='black',
                                                  command=None)
                self.entries[j].pack(expand=True, padx=10)
                self.entries[j]._canvas.tag_bind("right_parts", "<Button-1>", lambda x: self.temp_window(self.mainframe))
                self.entries[j]._canvas.tag_bind("dropdown_arrow", "<Button-1>", lambda x: self.temp_window(self.mainframe))
            else:
                self.entries[j] = ctk.CTkEntry(frame, width=400, height=50, placeholder_text=j, fg_color='#FFF2D8', text_color='black', textvariable=self.str_vars[j])
                self.entries[j].pack(expand=True, padx=10)
            col += 1
            if col % 3 == 0:
                row += 1
                col = 0
        row, col = 1, 0
        for i, j in enumerate(details[9:]):
            frame = ctk.CTkFrame(self._scrollable_frame, fg_color=self.fg_colors['black'], width=100, height=100)
            label = ctk.CTkLabel(frame, width=30, text=j, font=self.controller.font, text_color='white', wraplength=200)
            self.entries[j] = ctk.CTkTextbox(frame, width=400, height=260, fg_color='#FFF2D8', text_color='black')
            frame.grid(row=row, column=i, padx=10, pady=10, ipady=10, sticky='nsew')
            label.pack(expand=True, padx=10)
            self.entries[j].pack(expand=True, padx=10, pady=10)

    def temp_window(self, frame):
        def close():
            self.toplevel_window.destroy()
            self.toplevel_window.update()

        def select(model):
            self.entries["MODEL"].set(model)
            for key, value in self._all_models_dict.items():
                if model in value:
                    self.entries["TYPE"].delete(0, tk.END)
                    self.entries["TYPE"].insert(0, key)
                self.toplevel_window.destroy()

        models_list = sum(self._all_models_dict.values(), [])
        sorted_models = sorted(set(models_list))
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            row, col = 0, 0
            self.toplevel_window = ctk.CTkToplevel(frame)
            self.toplevel_window.title("System")
            self.toplevel_window.geometry("1280x720")
            self.toplevel_window.resizable(False, False)
            self.toplevel_window.attributes('-topmost', 'true')
            label = ctk.CTkLabel(self.toplevel_window, text="Choose an option from the list below").grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
            temp_scrollable_frame = ctk.CTkScrollableFrame(self.toplevel_window, fg_color='#FFF2D8', label_text='MODELS')
            self.toplevel_window.columnconfigure(0, weight=1), self.toplevel_window.rowconfigure(1, weight=1)
            [temp_scrollable_frame.columnconfigure(i, weight=1) for i in range(3)]
            models = {}
            for i, model in enumerate(sorted_models):
                models[model] = ctk.CTkButton(temp_scrollable_frame, width=30, text=model, font=('Arial', 14), command=lambda m=model: select(m))
                if models[model]._text_label is not None: models[model]._text_label.configure(wraplength=200)
                models[model].grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                col += 1
                if col % 3 == 0:
                    row += 1
                    col = 0
            temp_scrollable_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
            ctk.CTkButton(self.toplevel_window, text="Close", command=close).grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        else:
            self.toplevel_window.focus()


    def _submit(self): # ANG PART NA MADUGO "LORD HELP :(((("
        result = {}
        ord_list = ['YR', 'MONTH', 'PO NUMBER', 'DR DATE', 'DR NUMBER', 'STORE', 'BRAND', 'SERIAL NUMBER', 'IMEI 1',
                    'IMEI 2', 'BUYING PRICE', 'MODEL', 'TYPE', 'UNIT REMARKS', 'DL PRICE']
        result['YR'], result['MONTH'], result['DR DATE'] = datetime.now().strftime('%Y'), datetime.now().strftime('%B').upper(), datetime.now().strftime('%d-%h-%Y')

        for key, value in (self.entries.items()):
            class_name = value.__class__
            if 'CTkEntry' in str(class_name):
                result[key] = value.get()
            elif 'CTkTextbox' in str(class_name):
                result[key] = value.get(0.0, 'end')
            elif 'CTkComboBox' in str(class_name):
                result[key] = value.get()
        self.ordered_result = {key: result[key] for key in ord_list}
        self.controller.instance = Create_Instance()
        self.controller.df = self.controller.instance.dr_in_n_out_df
        if self.ordered_result['TYPE'].upper() not in self._all_models_dict.keys():
            messagebox.showerror(title="System", message="ERROR:\nEntered type is not included in type list.")
            return None
        elif self.ordered_result['TYPE'] == 'DMR':
            print("Type: DMR")
            self.ordered_result.pop('TYPE')
            pprint(self.ordered_result)
            # self._dmr_option()
        elif self.ordered_result['TYPE'] == 'POC':
            print("Type: POC")
            self.ordered_result.pop('TYPE')
            pprint(self.ordered_result)
            # self._poc_option()
        else:
            print("Type: OTHERS")
            self.ordered_result.pop('TYPE')
            pprint(self.ordered_result)
            # self._other_option()
        # print(f"After: {self.controller.df}")
    def _dmr_option(self):
        serials, imei1, imei2 = self.ordered_result['SERIAL NUMBER'].split(), self.ordered_result['IMEI 1'].split(), \
            self.ordered_result['IMEI 2'].split()
        if len(imei1)+len(imei2) == 0:
            response = messagebox.askyesno(title="System", message="Are you sure you want to proceed?")
            if response:
                main_df = pd.DataFrame(self.ordered_result, index=[0])
                _placeholder_df = main_df.copy()
                for i in range(max(len(serials), len(imei1), len(imei2))):
                    _placeholder_df[['SERIAL NUMBER']] = [serials[i]]
                    main_df.loc[i] = _placeholder_df.loc[0]
                self.append_row(main_df.values.tolist())
        else:
            messagebox.showerror(title="System", message="ERROR:\nDMR's don't have IMEIs. Please review the details.")
    def _poc_option(self):
        serials, imei1, imei2 = self.ordered_result['SERIAL NUMBER'].split(), self.ordered_result['IMEI 1'].split(), \
        self.ordered_result['IMEI 2'].split()
        if (len(serials) == len(imei1) == len(imei2)) or (len(imei2) == 0 and len(serials) == len(imei1)):
            response = messagebox.askyesno(title="System", message="Are you sure you want to proceed?")
            if response:
                main_df = pd.DataFrame(self.ordered_result, index=[0])
                _placeholder_df = main_df.copy()
                for i in range(max(len(serials), len(imei1), len(imei2))):
                    if len(imei2) != 0:
                        _placeholder_df[['SERIAL NUMBER', 'IMEI 1', 'IMEI 2']] = [serials[i], imei1[i], imei2[i]]
                    else:
                        _placeholder_df[['SERIAL NUMBER', 'IMEI 1']] = [serials[i], imei1[i]]
                    main_df.loc[i] = _placeholder_df.loc[0]
                self.append_row(main_df.values.tolist())
        else:
            messagebox.showerror(title="System", message="ERROR:\nThe input field(s) is/are incomplete.")

    def _other_option(self):
        serials, imei1, imei2 = self.ordered_result['SERIAL NUMBER'].split(), self.ordered_result['IMEI 1'].split(),\
            self.ordered_result['IMEI 2'].split()
        response = messagebox.askyesno(title="System", message="Are you sure you want to proceed?")
        if response:
            main_df = pd.DataFrame(self.ordered_result, index=[0])
            _placeholder_df = main_df.copy()
            for i in range(max(len(serials), len(imei1), len(imei2))):
                try:
                    if len(serials) != 0: _placeholder_df[['SERIAL NUMBER']] = [serials[i]]
                    if len(imei1) != 0: _placeholder_df[['IMEI 1']] = [imei1[i]]
                    if len(imei2) != 0: _placeholder_df[['IMEI 2']] = [imei2[i]]
                except ValueError:
                    print("There is a value problem")
                    pass
                main_df.loc[i] = _placeholder_df.loc[0]
            self.append_row(main_df.values.tolist())


    def append_row(self, df):
        """Appends one or more cell(s)"""
        cell_range_insert = f'A{self.locate_lastrow()}'
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            valueInputOption='RAW',
            range='DR IN N OUT!' + cell_range_insert,
            body=dict(
                majorDimension='ROWS',
                values=df)
        ).execute()

    def locate_lastrow(self):
        """Locates the last row of a given column"""
        last_row = 2
        response = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            majorDimension='ROWS',
            range='DR IN N OUT!A2:A'
        ).execute()
        last_row += len(response['values']) - 1
        return last_row
