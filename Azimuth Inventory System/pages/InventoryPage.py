import tkinter as tk
import customtkinter as ctk


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
        super().__init__(master=parent, fg_color='#FFF2D8')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)
        values = ["value 1", "value 2", "value 3", "value 4", "value 5", "value 6"]
        for i, value in enumerate(values):
            checkbox = ctk.CTkCheckBox(self, text=value, text_color='black')
            checkbox.pack(padx=50, pady=50)

class POCFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='#FFF2D8')
        self.pack(expand=True, side='left', fill='both', padx=5, pady=10)

class AccessoriesFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='#FFF2D8')
        self.pack(expand=True, fill='both', padx=5, pady=10)