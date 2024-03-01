import tkinter as tk
import customtkinter as ctk


class InventoryPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.controller.create_page(self)
        self.radiobutton_var = ctk.StringVar(self, value='dmr_frame')
        self.dmr_mainframe = ctk.CTkFrame(master=self, width=1920, height=1080, fg_color='black',
                                     corner_radius=-10, border_width=1)
        self.poc_mainframe = ctk.CTkFrame(master=self, width=1920, height=1080, fg_color='black',
                                          corner_radius=-10, border_width=1)
        self.radiobutton_frame()
        self.show_frame()

    def radiobutton_frame(self):
        mainframe = ctk.CTkFrame(master=self, width=1920, height=1080, fg_color='#FFF2D8',
                                 corner_radius=-10, border_width=1)
        mainframe.place(relwidth=0.85, relheight=0.1, relx=0.15)
        self.dmr_radiobutton = ctk.CTkRadioButton(mainframe, value='dmr_frame', variable=self.radiobutton_var,
                                                  width=200, height=10, text_color='black', text='DMR',
                                                  command=self.show_frame)
        self.dmr_radiobutton.grid(row=0, column=0, padx=50, pady=20)
        self.poc_radiobutton = ctk.CTkRadioButton(mainframe, value='poc_frame', variable=self.radiobutton_var,
                                                  width=200, height=10, text_color='black', text='POC',
                                                  command=self.show_frame)
        self.poc_radiobutton.grid(row=0, column=1, padx=50, pady=20)

    def show_frame(self):
        self.dmr_mainframe.place_forget()
        self.poc_mainframe.place_forget()
        if self.radiobutton_var.get() == 'dmr_frame':
            self.dmr_frame(self.dmr_mainframe)
        elif self.radiobutton_var.get() == 'poc_frame':
            self.poc_frame(self.poc_mainframe)

    def dmr_frame(self, master):
        self.dmr_mainframe.place(relwidth=0.85, relheight=0.9, relx=0.15, rely=0.1)
        page_label = ctk.CTkLabel(master=master, text=self.radiobutton_var.get(), text_color='white')
        page_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        page_button = ctk.CTkButton(master=master, text='Print Text', command=lambda: print('DMR'))
        page_button.grid(row=0, column=0)


    def poc_frame(self, master):
        self.poc_mainframe.place(relwidth=0.85, relheight=0.9, relx=0.15, rely=0.1)
        page_label = ctk.CTkLabel(master=master, text=self.radiobutton_var.get(), text_color='white')
        page_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        page_button = ctk.CTkButton(master=master, text='Print Text', command=lambda: print('POC'))
        page_button.grid(row=0, column=0)

