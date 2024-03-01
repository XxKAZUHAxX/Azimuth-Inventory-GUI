import tkinter as tk
import customtkinter as ctk

class DR_InPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.mainframe = self.controller.create_page(self)
        self.service = controller.service
        self.df = controller.df
        self.entries = {}
        self.dr_in_scrollframe()

    def dr_in_scrollframe(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(master=self.mainframe, fg_color='#FFF2D8', label_text='DR IN')
        self.scrollable_frame.pack(expand=True, fill='both', padx=5, pady=10)
        confirm_button = ctk.CTkButton(self.mainframe, width=100, height=40, text='Confirm', font=('Arial', 14), command=lambda: self.confirm())
        confirm_button.pack(side='top', padx=10, pady=10)
        self.dr_in_contents()

    def dr_in_contents(self):
        row, col = 0, 0
        details = ['PO Number', 'DR Number', 'Store', 'Brand', 'Buying Price', 'Model', 'Type', 'Unit Remarks',
                   'DL Price', 'Serial Number', 'IMEI 1', 'IMEI 2']
        [self.scrollable_frame.columnconfigure(i, weight=1) for i in range(4)], [self.scrollable_frame.rowconfigure(i, weight=1) for i in range(3)]
        for j in details:
            frame = ctk.CTkFrame(self.scrollable_frame, fg_color='#9DAB86', width=100, height=200)
            label = ctk.CTkLabel(frame, width=30, text=j, font=('Arial', 14), text_color='black', wraplength=200)
            self.entries[j] = ctk.CTkEntry(frame, width=400, height=50, placeholder_text=j)

            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            label.pack(expand=True, padx=10, pady=10)
            self.entries[j].pack(expand=True, padx=10, pady=10)
            col += 1
            if col % 3 == 0:
                row += 1
                col = 0

    def confirm(self): # ANG PART NA MADUGO
        for key, value in (self.entries.items()):
            print(f"Key: {key} | Value: {value.get()}")


# FOR FUTURE JADE
# - ayusin ang pagkakalagay ng mga widgets sa dr in frame
# - isiping mabuti pano tatapusin yang confirm function na yan bago ka nyan tapusin
# - iexport lahat ng entry data into pandas dataframe bago iappend sa google sheets

# - PAG-ARALAN ANG INDEX MATCHING BAKA MAKATULONG BAGO MABALIW