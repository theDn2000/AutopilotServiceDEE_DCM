import customtkinter as ctk

# Night mode
ctk.set_appearance_mode("dark")

# Create App class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x400")
        self.title("Autopilot Direct")
        self.resizable(False, False)



        # MAIN FRAME
        # Create the main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Separate the main_frame into two vertical sections
        column0 = self.main_frame.columnconfigure(0, weight=1)
        column1 = self.main_frame.columnconfigure(1, weight=1)

        # Separate the main_frame into 4 horizontal sections
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.rowconfigure(3, weight=1)


        # BUTTONS
        # Create the connect_button
        self.connect_button = ctk.CTkButton(self.main_frame, text="Connect", command=self.connect, fg_color="#3117ea", hover_color="#190b95")
        self.connect_button.grid(row=3, column=1, padx=10, pady=0, sticky="we", ipady=10)



        # LABELS
        # Create the info_label
        #self.info_label = ctk.CTkLabel(self.main_frame, text="Welcome to AutopilotDirect. This tool allows you to interact with the autopilot functions directly without using the broker. Please, click the 'Connect' button to start.")
        #self.info_label.grid(row=0, column=1, padx=0, pady=0)

        

        # TEXTBOXES
        # Create the info_textbox (read-only)
        self.info_textbox = ctk.CTkTextbox(self.main_frame, width=280, height=310)
        self.info_textbox.grid(row=0, column=1, padx=0, pady=3, rowspan=3)
        self.info_textbox.insert("1.0", "Welcome to AutopilotDirect.\nThis tool allows you to interact with the\nautopilot functions directly without using any\nbroker.\n\nPlease, click the 'Connect' button to start.")
        # Add a version number to the textbox
        self.info_textbox.insert("end", "\n\nPATCH NOTES:\n\n- Version: 0.1.0: Initial release")

        self.info_textbox.configure(state="disabled")

        # Create the info_textbox2 (read-only)
        self.info_textbox2 = ctk.CTkTextbox(self.main_frame, width=280, height=380)
        self.info_textbox2.grid(row=0, column=0, padx=0, pady=0, rowspan=4)
        self.info_textbox2.insert("1.0", "Space reserved for the logo or image.")
        self.info_textbox2.configure(state="disabled")


    def connect(self):
        print("Button clicked")

# Run the app
app = App()
app.mainloop()