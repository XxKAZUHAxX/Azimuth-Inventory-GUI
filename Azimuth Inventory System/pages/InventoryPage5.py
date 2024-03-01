import tkinter as tk
import customtkinter as ctk
import gspread

gc = gspread.service_account('secrets.json')
spreadsheet = gc.open('Dummy of 2023 INVENTORY UPDATE 2023')
inventory = spreadsheet.worksheet('DR IN N OUT')

class InventoryPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.mainframe = self.controller.create_page(self)
        self.radiobutton_var = ctk.StringVar(self, value='dmr_frame')

        # Create Tabview
        main_tabview = ctk.CTkTabview(self.mainframe, width=1920, height=1080, fg_color='#FFF2D8', corner_radius=1, anchor='s')
        main_tabview.place(relwidth=1, relheight=1)
        main_tabview.add("Radio"), main_tabview.add("Accessories")
        dmr_frame = DMRFrame(main_tabview.tab("Radio"))
        dmr_frame = POCFrame(main_tabview.tab("Radio"))
        accessories_frame = AccessoriesFrame(main_tabview.tab("Accessories"))

class DMRFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='DMR')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        global inventory
        sorted_models = sorted(set(inventory.col_values(12)))


        row,col = 0,0
        self.columnconfigure(0, weight=1), self.columnconfigure(1, weight=1)
        for i, model in enumerate(sorted_models):
            frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=50, height=200)
            label = ctk.CTkLabel(master=frame, width=30, text=model, font=('Arial',14), text_color='black', wraplength=200)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            col += 1  # Move to the next column
            if col % 2 == 0:  # Adjust the number 4 to control frames per row
                row += 1  # Start a new row
                col = 0  # Reset column

        # model_frames = {}
        # for i, model in enumerate(sorted_models):
        #     model_frames[i] = self.pack_model_frame(model)

    def pack_model_frame(self, model):
        frame = ctk.CTkFrame(self, fg_color='#9DAB86', width=100, height=100)
        label = ctk.CTkLabel(master=frame, text=model, font=('Arial',14), text_color='black', wraplength=200)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        label.pack(expand=True, padx=5, pady=10)

class POCFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='#FFF2D8', label_text='POC')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)

class AccessoriesFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='#FFF2D8')
        self.pack(expand=True, fill='both', padx=5, pady=10)