import customtkinter as ctk

root = ctk.CTk()

# placeholder = ctk.CTkComboBox(root, values=[""], width=400, height=50, fg_color='#FFF2D8', text_color='black')
# placeholder.pack(expand=False, fill='both', padx=50, pady=50)
top_level = ctk.CTkToplevel(root)
# placeholder.
# button = ctk.CTkButton(root, text="Sample Button Sample Button Sample Button")
# button.pack(padx=50, pady=50)
# print(button._text_label.configure(wraplength=200))
frame = ctk.CTkScrollableFrame(top_level, fg_color='#9DAB86', width=100, height=200)
frame.pack(expand=True, fill='both', padx=50, pady=50)
row, col = 0, 0
[frame.columnconfigure(i, weight=1) for i in range(3)]
for i in ("Button 1"*5, "Button 2"*5, "Button 3"*5, "Button 4"*5, "Button 5"*5, "Button 6"*5, "Button 7"*5, "Button 8"*5, "Button 9"*5):
    model_btn = ctk.CTkButton(frame, width=30, text=i, font=('Arial', 14))
    print(model_btn._text_label.__class__)
    model_btn._text_label.configure(wraplength=200)
    model_btn.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
    col+=1
    if col % 3 == 0:
        row += 1
        col = 0





root.mainloop()