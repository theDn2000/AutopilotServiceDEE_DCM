from customtkinter import *

app = CTk()
app.geometry("500x400")


btn = CTkButton(master=app, text="Click me", command=lambda: print("Button clicked"))

btn.place(relx=0.5, rely=0.5, anchor="center")


app.mainloop()