import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import json

class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.fg_colors = controller.fg_colors
        self.controller.refresh_window()
        self.controller.bind('<Return>', lambda e: self.check_credentials())
        # image for hide and unhide password
        self.show_image = ctk.CTkImage(Image.open('images/hide.png').resize((30, 20)))
        self.hide_image = ctk.CTkImage(Image.open('images/Unhide.png').resize((30, 20)))
        img1 = ctk.CTkImage(Image.open("images/bg-orange.png"), size=(1980, 1280))
        # self.l1 = ctk.CTkLabel(master=self, image=img1, text="")
        self.l1 = ctk.CTkFrame(self, fg_color=self.fg_colors['grey'])
        self.l1.pack(expand=True, fill='both')
        self.start()

    def start(self):
        # Login frame
        self.frame = ctk.CTkFrame(master=self.l1, width=520, height=480, fg_color=self.fg_colors['black'])
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        l2=ctk.CTkLabel(master=self.frame, text="Azimuth Inventory System", font=('Berlin Sans FB Demi', 24), text_color="white")
        l2.place(relx=0.23, rely=0.245)

        # LOGO Company
        LogoAz = ctk.CTkImage(Image.open("images/Logo-Az-crop.png"), size=(90,70))
        LabelLogo = ctk.CTkLabel(master=self.frame, image=LogoAz, text="")
        LabelLogo.place(relx=0.43, rely=0.09)

        # placeholder Username
        self.entry1 = ctk.CTkEntry(master=self.frame, width=320, height=45, placeholder_text="Username", corner_radius=24,
                                   fg_color=self.fg_colors['white'], placeholder_text_color="#9DAB86", border_color="#304D30", font=('Berlin Sans FB', 20), text_color="#163020")
        self.entry1.place(relx=0.2, rely=0.35)
        self.entry1.insert(0, "admin")
        self.entry1.focus()

        # placeholder Password
        self.entry2 = ctk.CTkEntry(master=self.frame, width=320, height=45, placeholder_text="Password", corner_radius=24,
                                   fg_color=self.fg_colors['white'], placeholder_text_color="#9DAB86", border_color="#304D30", font=('Berlin Sans FB', 20), text_color="#163020")
        self.entry2.configure(show="●")
        self.entry2.insert(0, "admin")
        self.entry2.place(relx=0.2, rely=0.459)

        # show button
        show_button= ctk.CTkButton(master=self.frame, image=self.show_image, command=self.show, text="", width=10, height=10, fg_color=self.fg_colors['white'], hover_color="#E08F62")
        show_button.place(x=370, y=230)

        self.button1=ctk.CTkButton(master=self.frame, width=220, height=40, text="Submit", fg_color=self.fg_colors['orange'], text_color="white",
                              font=('Berlin Sans FB Demi', 17), corner_radius=24, command=self.check_credentials, hover_color="#E08F62")
        self.button1.place(relx=0.3, rely=0.653)

    def check_credentials(self):
            email, password = self.entry1.get(), self.entry2.get()
            try:
                with open("data.json") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="No data file found.")
            else:
                for number, user in enumerate(data):
                    if data[user]["Username"] == email and data[user]["Password"] == password:
                        self.controller.unbind('<Return>')
                        self.login_successfully()
                        break
                    elif number+1 == len(data):
                        self.entry1.delete(0, len(self.entry1.get())), self.entry2.delete(0, len(self.entry2.get()))
                        messagebox.showinfo(title="Error", message=f"Incorrect Email or Password")

    def login_successfully(self):
        self.entry1.delete(0, len(self.entry1.get())), self.entry2.delete(0, len(self.entry2.get()))
        messagebox.showinfo(title='System Notification', message=f"Login Successfully")
        self.controller.show_frame('HomePage')

    def hide(self):
            show_button = ctk.CTkButton(master=self.frame, image=self.show_image, command=self.show, text="", width=10, height=10, fg_color="#DED7B1", hover_color="#E08F62")
            show_button.place(x=370, y=230)
            self.entry2.configure(show="●")

    def show(self):
        hide_button = ctk.CTkButton(master=self.frame, image=self.hide_image, command=self.hide, text="", width=10, height=10, fg_color="#DED7B1", hover_color="#E08F62")
        hide_button.place(x=370, y=230)
        self.entry2.configure(show="")