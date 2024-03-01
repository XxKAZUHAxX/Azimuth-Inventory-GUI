import tkinter as tk
import customtkinter as ctk
from pprint import pprint
from tkinter import messagebox
from datetime import datetime
import pandas as pd

class DR_OutPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.fg_colors = controller.fg_colors
        self.mainframe = self.controller.create_page(self)
        self.service = controller.service
        self.spreadsheet_id = controller.spreadsheet_id
        self.df = controller.df
        self.entries = {}
        self.ordered_result = {}
        self.dr_out_toplevel_window = None
        self.create_frontend()

    def create_frontend(self):
        def create_searchframe():
            _searchframe_inside_scrollable = ctk.CTkFrame(_main_scrollable, fg_color=self.fg_colors['black'], width=100,
                                                          height=100)
            _searchframe_inside_scrollable.grid(row=0, column=0, padx=50, pady=10, ipadx=10, sticky='nswe')
            _searchframe_inside_scrollable.columnconfigure(0, weight=1)
            search_entry = ctk.CTkEntry(_searchframe_inside_scrollable, width=600, height=50, fg_color='#FFF2D8',
                                      text_color='black', placeholder_text='SERIAL NUMBER / PART NUMBER')
            search_entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
            _search_button = ctk.CTkButton(_searchframe_inside_scrollable, width=200, height=40, fg_color=self.fg_colors['orange'],
                                    text='SEARCH', text_color='black', command=lambda: self.search_btn_clicked(search_entry))
            _search_button.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

        def create_page_contents():
            def if_int():
                self.entry = int(self.entries[item].get())
                if self.entry.isdigit:
                    return True
                else:
                    self.entries[item].configure(border_color='#FF0000')
                    return False




            _contentframe_inside_scrollable = ctk.CTkFrame(_main_scrollable, fg_color=self.fg_colors['black'], width=100, height=500)
            _contentframe_inside_scrollable.grid(row=1, column=0, padx=50, pady=10, ipadx=10, sticky='nswe')
            [_contentframe_inside_scrollable.columnconfigure(i, weight=1) for i in range(3)]
            row, col = 0, 0

            for item in ("PO NO.", "DR OUT", "SI", "TYPE OF SALES", "CLIENT NAME", "AMOUNT",
                         "12% VAT", "TOTAL AMOUNT", "DEALER'S STATUS"):
                frame = ctk.CTkFrame(_contentframe_inside_scrollable, fg_color=self.fg_colors['black'])
                label = ctk.CTkLabel(frame, text=item, text_color='white', font=self.controller.font)
                if item == 'TYPE OF SALES':
                    self.entries[item] = ctk.CTkComboBox(frame, values=["DIRECT", "DEALER", "PROJECT"], width=400,
                                                         height=50, fg_color='#FFF2D8', text_color='black', command=None)
                elif item == 'CLIENT NAME':
                    self.entries[item] = ctk.CTkComboBox(frame, values=[""], width=400, height=50, fg_color='#FFF2D8',
                                                         text_color='black', command=None)
                    self.entries[item]._canvas.tag_bind("right_parts", "<Button-1>", lambda x: self.temp_window(self.mainframe))
                    self.entries[item]._canvas.tag_bind("dropdown_arrow", "<Button-1>", lambda x: self.temp_window(self.mainframe))
                elif item == "DEALER'S STATUS":
                    self.entries[item] = ctk.CTkComboBox(frame, values=["PAID", "UNPAID", "FREE", "RETURNED", "STOCKS",
                                                         "DEFECTIVE", "PDC"], width=400, height=50, fg_color='#FFF2D8',
                                                         text_color='black', command=None)
                else:
                    self.entries[item] = ctk.CTkEntry(frame, width=400, height=50, fg_color='#FFF2D8', text_color='black', validatecommand=if_int, validate='focusout')
                frame.grid(row=row, column=col, padx=10, pady=30, sticky='nswe')
                label.pack(expand=True, padx=10)
                self.entries[item].pack(expand=True, padx=10)
                col += 1
                if col % 3 == 0:
                    row += 1
                    col = 0

        self.mainframe.rowconfigure(0, weight=1), self.mainframe.columnconfigure(0, weight=1)
        _main_scrollable = ctk.CTkScrollableFrame(self.mainframe, fg_color=self.fg_colors['grey'], label_text='DR OUT')
        _main_scrollable.grid(row=0, column=0, sticky='nsew')
        _main_scrollable.columnconfigure(0, weight=1)
        self.entry = create_searchframe()
        create_page_contents()

    def search_btn_clicked(self, value):
        def compile():
            result = {}
            result['YR'], result['MONTH'], result['DATE'] = datetime.now().strftime('%Y'), datetime.now().strftime(
                '%B').upper(), datetime.now().strftime('%d-%h-%Y')
            ord_list = ['YR', 'MONTH', 'DATE', 'PO NO.', 'DR OUT', 'SI', 'TYPE OF SALES', 'CLIENT NAME',
                        'AMOUNT', '12% VAT', 'TOTAL AMOUNT', "DEALER'S STATUS"]
            validate_values()
            # for key, value in self.entries.items():
            #     try:
            #         entry = int(value.get())
            #         print(entry)
            #
            #     except ValueError:
            #         print("Entered value is not integer")
            #     return
            #
            #     result[key] = value.get() if key == 'PO NO.' and isinstance(value.get(), str) else print("PO NO. is not an integer")
            #     result[key] = value.get() if key == 'DR OUT' and isinstance(value.get(), str) else print("DR OUT is not an integer")
            #     result[key] = value.get() if key == 'SI' and isinstance(value.get(), str) else print("SI is not an integer")
            #     result[key] = value.get() if key == 'TYPE OF SALES.' and isinstance(value.get(), int) else print(
            #         "TYPE OF SALES is not an integer")

            self.ordered_result = {key: result[key] for key in ord_list}
            main_df = pd.DataFrame(self.ordered_result)
            update_cells(main_df.values.tolist())

        def validate_values():
            pass
            # for key, value in self.entries.items():
            #     pass

        def update_cells(df):
            worksheet_name = 'DR IN N OUT!'
            cell_range_insert = f'U{row_num}'
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                valueInputOption='USER_ENTERED',
                range=worksheet_name + cell_range_insert,
                body=dict(
                    majorDimension='ROWS',
                    values=df)
            ).execute()

        try:
            row_num = self.df.index[self.df['SERIAL NO.'] == value.get()][0] + 3
            messagebox.showinfo(title='System', message=f'Serial Number: {value.get()} | Row: {row_num}')
            compile()
        except IndexError:
            messagebox.showerror(title='System', message='Serial Number not found inside the database.')

    def temp_window(self, frame):
        def close():
            self.dr_out_toplevel_window.destroy()
            self.dr_out_toplevel_window.update()

        def select(dealer):
            self.entries["CLIENT NAME"].set(dealer)
            for key, value in dealers_df.to_dict().items():
                if dealer in value:
                    self.entries["CLIENT NAME"].delete(0, tk.END)
                    self.entries["CLIENT NAME"].insert(0, key)
                self.dr_out_toplevel_window.destroy()

        dealers_df = self.controller.dealers_df
        dealers_list = dealers_df[0].to_list()
        if self.dr_out_toplevel_window is None or not self.dr_out_toplevel_window.winfo_exists():
            row, col = 0, 0
            self.dr_out_toplevel_window = ctk.CTkToplevel(frame)
            self.dr_out_toplevel_window.title("System")
            self.dr_out_toplevel_window.geometry("1280x720")
            self.dr_out_toplevel_window.resizable(False, False)
            self.dr_out_toplevel_window.attributes('-topmost', 'true')
            ctk.CTkLabel(self.dr_out_toplevel_window, text="Choose an option from the list below").grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
            temp_scrollable_frame = ctk.CTkScrollableFrame(self.dr_out_toplevel_window, fg_color='#FFF2D8', label_text='MODELS')
            self.dr_out_toplevel_window.columnconfigure(0, weight=1), self.dr_out_toplevel_window.rowconfigure(1, weight=1)
            [temp_scrollable_frame.columnconfigure(i, weight=1) for i in range(3)]
            dealers = {}
            for i, dealer in enumerate(dealers_list):
                dealers[dealer] = ctk.CTkButton(temp_scrollable_frame, width=30, text=dealer, font=('Arial', 14),
                                                command=lambda m=dealer: select(m))
                if dealers[dealer]._text_label is not None: dealers[dealer]._text_label.configure(wraplength=200)
                dealers[dealer].grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                col += 1
                if col % 3 == 0:
                    row += 1
                    col = 0
            temp_scrollable_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
            ctk.CTkButton(self.dr_out_toplevel_window, text="Close", command=close).grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        else:
            self.dr_out_toplevel_window.focus()


