import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import json


class Azimuth(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.minsize(1040, 580)
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("1040x580")
        # self.geometry("1920x1080")
        self.title('Azimuth Inventory System')
        self.iconbitmap('images/Logo-Az-crop.ico')

        self.frames = {}
        for F in (LoginPage, HomePage, DR_InPage, DR_OutPage, InventoryPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='NSEW')

        self.show_frame('LoginPage')

    def show_frame(self, page_name):
        """Show frame for a given page name."""
        frame = self.frames[page_name]
        frame.tkraise()

    def refresh_window(self):
        self.update()
        self.update_idletasks()
        print("Refresh completed.")

    def logout(self):
        response = messagebox.askyesno(title="Logout", message="Are you sure you want to logout?")
        if response:
            self.destroy()
            Azimuth()

    def create_page(self, master):
        master.configure(fg_color="#FFF2D8")

        # Navbar
        navbar_frame = ctk.CTkFrame(master=master, width=1920, height=1080, fg_color='#163020')
        navbar_frame.place(relwidth=0.15, relheight=1.0)

        # Logo Az
        LogoAz = ctk.CTkImage(Image.open("images/Logo-Az-crop.png"), size=(100, 80))
        LabelLogo = ctk.CTkLabel(master=navbar_frame, image=LogoAz, text="")
        LabelLogo.place(relx=0.5, y=100, relwidth=0.7, anchor='center')

        # Button to raise Home (Current Page)
        home_button = ctk.CTkButton(master=navbar_frame, text="Home", font=('Berlin Sans FB', 14), text_color="white",
                                    command=lambda: self.show_frame('HomePage'))
        home_button.place(relx=0.5, y=200, relwidth=0.7, anchor='center')

        # Button to raise DR IN Page
        dr_in_button = ctk.CTkButton(master=navbar_frame, text="DR IN", font=('Berlin Sans FB', 14), text_color="white",
                                     command=lambda: self.show_frame('DR_InPage'))
        dr_in_button.place(relx=0.5, y=250, relwidth=0.7, anchor='center')

        # Button to raise DR OUT Page
        dr_out_button = ctk.CTkButton(master=navbar_frame, text="DR OUT", font=('Berlin Sans FB', 14),
                                      text_color="white", command=lambda: self.show_frame('DR_OutPage'))
        dr_out_button.place(relx=0.5, y=300, relwidth=0.7, anchor='center')

        # Button to raise Inventory Page
        inventory_button = ctk.CTkButton(master=navbar_frame, text="Inventory", font=('Berlin Sans FB', 14),
                                         text_color="white", command=lambda: self.show_frame('InventoryPage'))
        inventory_button.place(relx=0.5, y=350, relwidth=0.7, anchor='center')

        # Button to logout and raise Login Page
        logout_button = ctk.CTkButton(master=navbar_frame, text="Logout", font=('Berlin Sans FB', 14),
                                      text_color="white", command=self.logout)
        logout_button.place(relx=0.5, y=400, relwidth=0.7, anchor='center')


class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.controller.refresh_window()
        self.controller.bind('<Return>', lambda e: self.check_credentials())
        # image for hide and unhide password
        self.show_image = ctk.CTkImage(Image.open('images/hide.png').resize((30, 20)))
        self.hide_image = ctk.CTkImage(Image.open('images/Unhide.png').resize((30, 20)))
        img1 = ctk.CTkImage(Image.open("images/bg-orange.png"), size=(1980, 1280))
        self.l1 = ctk.CTkLabel(master=self, image=img1, text="")
        self.l1.pack()
        self.start()

    def start(self):
        # Login frame
        self.frame = ctk.CTkFrame(master=self.l1, width=520, height=480, fg_color=('#9DAB86'))
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        l2 = ctk.CTkLabel(master=self.frame, text="Azimuth Inventory System", font=('Berlin Sans FB Demi', 24),
                          text_color="black")
        l2.place(relx=0.23, rely=0.245)

        # LOGO Company
        LogoAz = ctk.CTkImage(Image.open("images/Logo-Az-crop.png"), size=(90, 70))
        LabelLogo = ctk.CTkLabel(master=self.frame, image=LogoAz, text="")
        LabelLogo.place(relx=0.43, rely=0.09)

        # placeholder Email
        self.entry1 = ctk.CTkEntry(master=self.frame, width=320, height=45, placeholder_text="Username",
                                   corner_radius=24,
                                   fg_color="#DED7B1", placeholder_text_color="#9DAB86", border_color="#304D30",
                                   font=('Berlin Sans FB', 20), text_color="#163020")
        self.entry1.place(relx=0.2, rely=0.35)

        # placeholder Password
        self.entry2 = ctk.CTkEntry(master=self.frame, width=320, height=45, placeholder_text="Password",
                                   corner_radius=24,
                                   fg_color="#DED7B1", placeholder_text_color="#9DAB86", border_color="#304D30",
                                   font=('Berlin Sans FB', 20), text_color="#163020")
        self.entry2.configure(show="●")
        self.entry2.place(relx=0.2, rely=0.459)

        # show button
        show_button = ctk.CTkButton(master=self.frame, image=self.show_image, command=self.show, text="", width=10,
                                    height=10, fg_color="#DED7B1", hover_color="#E08F62")
        show_button.place(x=370, y=230)

        self.button1 = ctk.CTkButton(master=self.frame, width=220, height=40, text="Submit", fg_color="#304D30",
                                     text_color="#f7e0bf",
                                     font=('Berlin Sans FB Demi', 17), corner_radius=24, command=self.check_credentials,
                                     hover_color="#E08F62")
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
                elif number + 1 == len(data):
                    self.entry1.delete(0, len(self.entry1.get())), self.entry2.delete(0, len(self.entry2.get()))
                    messagebox.showinfo(title="Error", message=f"Incorrect Email or Password")

    def login_successfully(self):
        self.entry1.delete(0, len(self.entry1.get())), self.entry2.delete(0, len(self.entry2.get()))
        messagebox.showinfo(title='System Notification', message=f"Login Successfully")
        self.controller.show_frame('HomePage')

    def hide(self):
        show_button = ctk.CTkButton(master=self.frame, image=self.show_image, command=self.show, text="", width=10,
                                    height=10, fg_color="#DED7B1", hover_color="#E08F62")
        show_button.place(x=370, y=230)
        self.entry2.configure(show="●")

    def show(self):
        hide_button = ctk.CTkButton(master=self.frame, image=self.hide_image, command=self.hide, text="", width=10,
                                    height=10, fg_color="#DED7B1", hover_color="#E08F62")
        hide_button.place(x=370, y=230)
        self.entry2.configure(show="")


class HomePage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.controller.create_page(self)
        self.page_contents()

    def page_contents(self):
        self.page_label = ctk.CTkLabel(master=self, text=self.__class__.__name__, text_color='black')
        self.page_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


class DR_InPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.controller.create_page(self)
        self.page_contents()

    def page_contents(self):
        self.page_label = ctk.CTkLabel(master=self, text=self.__class__.__name__, text_color='black')
        self.page_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


class DR_OutPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.controller.create_page(self)
        self.page_contents()

    def page_contents(self):
        self.page_mainframe = ctk.CTkFrame(self)
        self.page_label = ctk.CTkLabel(master=self, text=self.__class__.__name__, text_color='black')
        self.page_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


class InventoryPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.controller.create_page(self)
        self.page_contents()

    def page_contents(self):
        self.page_label = ctk.CTkLabel(master=self, text=self.__class__.__name__, text_color='black')
        self.page_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


if __name__ == '__main__':
    run = Azimuth()
    run.mainloop()