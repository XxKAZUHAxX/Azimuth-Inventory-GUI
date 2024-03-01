import tkinter as tk
import customtkinter as ctk

class HomePage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.fg_colors = controller.fg_colors
        self.controller.create_page(self)
        self.page_contents()
    def page_contents(self):
        page_mainframe = ctk.CTkFrame(master=self, width=1920, height=1080, fg_color=self.fg_colors['grey'], corner_radius=-10, border_width=1)
        page_mainframe.place(relwidth=0.85, relheight=1, relx=0.15)

        self.page_label = ctk.CTkLabel(master=page_mainframe, text=self.__class__.__name__, text_color='grey')
        self.page_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)