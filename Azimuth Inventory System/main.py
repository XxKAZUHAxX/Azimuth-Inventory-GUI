import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from pages.HomePage import HomePage
from pages.DR_InPage2 import DR_InPage
from pages.DR_OutPage import DR_OutPage
from pages.LoginPage import LoginPage
from pages.InventoryPage10 import InventoryPage
from pages.create_api_instance import Create_Instance

from pprint import pprint

class Azimuth(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.minsize(1060, 580)
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # self.geometry("1060x580")
        self.state('zoomed')
        # self.geometry("1920x1080")
        self.title('Azimuth Inventory System')
        self.iconbitmap('images/Logo-Az-crop.ico')
        self.font = font=('Berlin Sans FB', 18)
        self.instance_start()
        self.fg_colors = {"orange": "#ED7D31", "grey": "#B0A9A7", "white":"#F6F1EE", "black":"#4F4A45"}
        self.frames = {}
        for F in (LoginPage, InventoryPage, HomePage, DR_InPage, DR_OutPage):
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

    def instance_start(self):
        self.instance = Create_Instance()
        self.service = self.instance.service
        self.df = self.instance.dr_in_n_out_df
        self.spreadsheet_id = self.instance.spreadsheet_Id
        self._all_models_dict = self.instance._all_models_dict
        self.dealers_df = self.instance.dealers_df

        self.range = self.instance.range

    def create_page(self, master):
        # Navbar
        navbar_frame = ctk.CTkFrame(master=master, width=1920, height=1080, fg_color=self.fg_colors['black'], corner_radius=-10)
        navbar_frame.place(relwidth=0.15)

        mainframe = ctk.CTkFrame(master=master, width=1920, height=1080, fg_color=self.fg_colors['grey'], corner_radius=1)
        mainframe.place(relwidth=0.85, relx=0.15, relheight=1)

        # Logo Az
        LogoAz = ctk.CTkImage(Image.open("images/Logo-Az-crop.png"), size=(100, 80))
        LabelLogo = ctk.CTkLabel(master=navbar_frame, image=LogoAz, text="")
        LabelLogo.place(relx=0.5, y=100, relwidth=0.7, anchor='center')

        # Button to raise Home (Current Page)
        home_button = ctk.CTkButton(master=navbar_frame, text="HOME", font=('Berlin Sans FB', 14), text_color="black",
                                    fg_color=self.fg_colors['orange'], command=lambda: self.show_frame('HomePage'))
        home_button.place(relx=0.5, y=200, relwidth=0.7, anchor='center')

        # Button to raise DR IN Page
        dr_in_button = ctk.CTkButton(master=navbar_frame, text="DR IN", font=('Berlin Sans FB', 14), text_color="black",
                                     fg_color=self.fg_colors['orange'], command=lambda: self.show_frame('DR_InPage'))
        dr_in_button.place(relx=0.5, y=250, relwidth=0.7, anchor='center')

        # Button to raise DR OUT Page
        dr_out_button = ctk.CTkButton(master=navbar_frame, text="DR OUT", font=('Berlin Sans FB', 14),
                                      fg_color=self.fg_colors['orange'], text_color="black", command=lambda: self.show_frame('DR_OutPage'))
        dr_out_button.place(relx=0.5, y=300, relwidth=0.7, anchor='center')

        # Button to raise Inventory Page
        inventory_button = ctk.CTkButton(master=navbar_frame, text="INVENTORY", font=('Berlin Sans FB', 14),
                                         fg_color=self.fg_colors['orange'], text_color="black", command=lambda: self.show_frame('InventoryPage'))
        inventory_button.place(relx=0.5, y=350, relwidth=0.7, anchor='center')

        # Button to logout and raise Login Page
        logout_button = ctk.CTkButton(master=navbar_frame, text="LOGOUT", font=('Berlin Sans FB', 14),
                                      fg_color=self.fg_colors['orange'], text_color="black", command=self.logout)
        logout_button.place(relx=0.5, y=400, relwidth=0.7, anchor='center')
        return mainframe


if __name__ == '__main__':
    run = Azimuth()
    run.mainloop()