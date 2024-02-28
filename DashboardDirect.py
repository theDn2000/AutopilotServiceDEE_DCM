import customtkinter as ctk
import os
import sys
import time
import threading

# Import the Dron class
from Dron import Dron
# Create a Dron object
dron = Dron(ID=1)

# Night mode
ctk.set_appearance_mode("dark")



# Create App class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x400")
        self.title("Dashboard Direct")
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
        self.connect_button = ctk.CTkButton(self.main_frame, text="Connect", command=self.on_button_connect_click, fg_color="#3117ea", hover_color="#190b95")
        self.connect_button.grid(row=3, column=1, padx=10, pady=0, sticky="we", ipady=10)



        # LABELS

        

        # TEXTBOXES
        # Create the info_textbox (read-only)
        self.info_textbox = ctk.CTkTextbox(self.main_frame, width=280, height=310)
        self.info_textbox.grid(row=0, column=1, padx=0, pady=3, rowspan=3)
        self.info_textbox.insert("1.0", "Welcome to DashboardDirect.\nThis tool allows you to interact with the\nautopilot functions directly without using any\nbroker.\n\nPlease, click the 'Connect' button to start.")
        # Add a version number to the textbox
        self.info_textbox.insert("end", "\n\nPATCH NOTES:\n\n- Version: 0.1.0: Initial release\n\n- Version: 0.1.1: Connect and telemetry info      added.\n\n- Version: 0.1.2: Control and pad buttons added.")

        self.info_textbox.configure(state="disabled")

        # Create the info_textbox2 (read-only)
        self.info_textbox2 = ctk.CTkTextbox(self.main_frame, width=280, height=380)
        self.info_textbox2.grid(row=0, column=0, padx=0, pady=0, rowspan=4)
        self.info_textbox2.insert("1.0", "Space reserved for the logo or image.")
        self.info_textbox2.configure(state="disabled")








    # FUNCTIONS (FRONTEND)
    def on_button_connect_click(self):

        # Make the button invisible and substitute it with a label
        self.connect_button.grid_forget()
        self.connect_label = ctk.CTkLabel(self.main_frame, text="Connecting...")
        self.connect_label.grid(row=3, column=1, padx=10, pady=0, sticky="we", ipady=10)


        # Connect to the autopilot 1000ms later
        self.after(1000, self.connect)

    def set_main_page(self):
        # Create the main page view

        # Create the main_textbox (for pages of the main view)
        self.main_textbox = ctk.CTkTextbox(self.main_frame, width=300, height=380)
        self.main_textbox.grid(row=0, column=0, padx=10, pady=0, rowspan=4)
        self.main_textbox.insert("1.0", "Space reserved for the pages of the main view.")
        self.main_textbox.configure(state="disabled")



        # Create the main_frame_telemetry (for telemetry info)
        self.frame_telemetry = ctk.CTkFrame(self.main_frame, width=300, height=80)
        self.frame_telemetry.grid(row=0, column=1, padx=10, pady=9, rowspan=1, sticky="we")
        # Color the frame
        self.frame_telemetry.configure(fg_color="#1f1f1f")
        # frame_telemetry can't be resized
        self.frame_telemetry.grid_propagate(False)

        # Separate the frame_telemetry into 2 vertical sections
        self.frame_telemetry.columnconfigure(0, weight=1)
        self.frame_telemetry.columnconfigure(1, weight=1)

        # Separate the frame_telemetry into 3 horizontal section
        self.frame_telemetry.rowconfigure(0, weight=1)
        self.frame_telemetry.rowconfigure(1, weight=1)
        self.frame_telemetry.rowconfigure(2, weight=1)

        # Create the labels for the telemetry info, 6 parameters (lat, lon, alt, heading, groundSpeed, battery) inide every frame
        self.label_telemetry_lat = ctk.CTkLabel(self.frame_telemetry, text="Latitude: ", font=("TkDefaultFont", 11))
        self.label_telemetry_lat.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.label_telemetry_lat_value = ctk.CTkLabel(self.frame_telemetry, text="0.0", font=("TkDefaultFont", 11, "bold"))
        self.label_telemetry_lat_value.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.label_telemetry_lon = ctk.CTkLabel(self.frame_telemetry, text="Longitude: ", font=("TkDefaultFont", 11))
        self.label_telemetry_lon.grid(row=1, column=0, padx=5, pady=0, sticky="w")
        self.label_telemetry_lon_value = ctk.CTkLabel(self.frame_telemetry, text="0.0", font=("TkDefaultFont", 11, "bold"))
        self.label_telemetry_lon_value.grid(row=1, column=0, padx=5, pady=0, sticky="e")

        self.label_telemetry_alt = ctk.CTkLabel(self.frame_telemetry, text="Altitude: ",font=("TkDefaultFont", 11))
        self.label_telemetry_alt.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.label_telemetry_alt_value = ctk.CTkLabel(self.frame_telemetry, text="0.0", font=("TkDefaultFont", 11, "bold"))
        self.label_telemetry_alt_value.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.label_telemetry_hea = ctk.CTkLabel(self.frame_telemetry, text="Heading: ", font=("TkDefaultFont", 11))
        self.label_telemetry_hea.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.label_telemetry_hea_value = ctk.CTkLabel(self.frame_telemetry, text="0.0", font=("TkDefaultFont", 11, "bold"))
        self.label_telemetry_hea_value.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.label_telemetry_gs = ctk.CTkLabel(self.frame_telemetry, text="Ground Speed: ", font=("TkDefaultFont", 11))
        self.label_telemetry_gs.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.label_telemetry_gs_value = ctk.CTkLabel(self.frame_telemetry, text="0.0", font=("TkDefaultFont", 11, "bold"))
        self.label_telemetry_gs_value.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        self.label_telemetry_bat = ctk.CTkLabel(self.frame_telemetry, text="Battery: ", font=("TkDefaultFont", 11))
        self.label_telemetry_bat.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.label_telemetry_bat_value = ctk.CTkLabel(self.frame_telemetry, text="0.0", font=("TkDefaultFont", 11, "bold"))
        self.label_telemetry_bat_value.grid(row=2, column=1, padx=5, pady=5, sticky="e")



        # Create the main_frame_control_buttons (for control buttons)
        self.main_frame_control_buttons = ctk.CTkFrame(self.main_frame, width=300, height=200)
        self.main_frame_control_buttons.grid(row=2, column=1, padx=10, pady=10, rowspan=2)
        # Color the frame
        self.main_frame_control_buttons.configure(fg_color="#1f1f1f")
        # frame_telemetry can't be resized
        self.main_frame_control_buttons.grid_propagate(False)

        # Separate the frame_telemetry into 3 vertical sections
        self.main_frame_control_buttons.columnconfigure(0, weight=1)
        self.main_frame_control_buttons.columnconfigure(1, weight=1)
        self.main_frame_control_buttons.columnconfigure(2, weight=1)

        # Create the control buttons
        self.control_button_take_off = ctk.CTkButton(self.main_frame_control_buttons, text="Arm", command=self.arm, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_take_off.grid(row=0, column=0, padx=5, pady=5, sticky="we", ipady=10)

        self.control_button_land = ctk.CTkButton(self.main_frame_control_buttons, text="Take Off", command=self.take_off, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_land.grid(row=0, column=1, padx=5, pady=5, sticky="we", ipady=10)

        self.control_button_goto = ctk.CTkButton(self.main_frame_control_buttons, text="RTL", command=self.rtl, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_goto.grid(row=0, column=2, padx=5, pady=5, sticky="we", ipady=10)



        # Create the main_frame_control_pad (for control pad)
        self.main_frame_control_pad = ctk.CTkFrame(self.main_frame, width=300, height=100)
        self.main_frame_control_pad.grid(row=1, column=1, padx=10, pady=10, rowspan=1)
        # Color the frame
        self.main_frame_control_pad.configure(fg_color="#1f1f1f")
        # frame_telemetry can't be resized
        self.main_frame_control_pad.grid_propagate(False)

        # Separate the frame_telemetry into 3 vertical sections
        self.main_frame_control_pad.columnconfigure(0, weight=1)
        self.main_frame_control_pad.columnconfigure(1, weight=1)
        self.main_frame_control_pad.columnconfigure(2, weight=1)

        # Separate the frame_telemetry into 3 horizontal section
        self.main_frame_control_pad.rowconfigure(0, weight=1)
        self.main_frame_control_pad.rowconfigure(1, weight=1)
        self.main_frame_control_pad.rowconfigure(2, weight=1)


        # Create the control pad buttons
        self.control_pad_button_nw = ctk.CTkButton(self.main_frame_control_pad, text="NW", command=lambda : self.go("NorthWest"), fg_color="#3117ea", hover_color="#190b95")
        self.control_pad_button_nw.grid(row=0, column=0, padx=5, pady=5, sticky="we", ipady=10)

        self.control_pad_button_n = ctk.CTkButton(self.main_frame_control_pad, text="N", command=lambda : self.go("North"), fg_color="#3117ea", hover_color="#190b95")
        self.control_pad_button_n.grid(row=0, column=1, padx=5, pady=5, sticky="we", ipady=10)

        self.control_pad_button_ne = ctk.CTkButton(self.main_frame_control_pad, text="NE", command=lambda : self.go("NorthEast"), fg_color="#3117ea", hover_color="#190b95")
        self.control_pad_button_ne.grid(row=0, column=2, padx=5, pady=5, sticky="we", ipady=10)

        self.control_pad_button_w = ctk.CTkButton(self.main_frame_control_pad, text="W", command=lambda : self.go("West"), fg_color="#3117ea", hover_color="#190b95")
        self.control_pad_button_w.grid(row=1, column=0, padx=5, pady=5, sticky="we", ipady=10)

        self.control_pad_button_stop = ctk.CTkButton(self.main_frame_control_pad, text="STOP", command=lambda : self.go("Stop"), fg_color="#3117ea", hover_color="#190b95")
        self.control_pad_button_stop.grid(row=1, column=1, padx=5, pady=5, sticky="we", ipady=10)

        self.control_pad_button_e = ctk.CTkButton(self.main_frame_control_pad, text="E", command=lambda : self.go("East"), fg_color="#3117ea", hover_color="#190b95")
        self.control_pad_button_e.grid(row=1, column=2, padx=5, pady=5, sticky="we", ipady=10)

        self.control_pad_button_sw = ctk.CTkButton(self.main_frame_control_pad, text="SW", command=lambda : self.go("SouthWest"), fg_color="#3117ea", hover_color="#190b95")
        self.control_pad_button_sw.grid(row=2, column=0, padx=5, pady=5, sticky="we", ipady=10)

        self.control_pad_button_s = ctk.CTkButton(self.main_frame_control_pad, text="S", command=lambda : self.go("South"), fg_color="#3117ea", hover_color="#190b95")
        self.control_pad_button_s.grid(row=2, column=1, padx=5, pady=5, sticky="we", ipady=10)

        self.control_pad_button_se = ctk.CTkButton(self.main_frame_control_pad, text="SE", command=lambda : self.go("SouthEast"), fg_color="#3117ea", hover_color="#190b95")
        self.control_pad_button_se.grid(row=2, column=2, padx=5, pady=5, sticky="we", ipady=10)



    # FUNCTIONS (BACKEND)
        
    # Connect
    def connect(self):

        # Connect to the autopilot
        dron.connect_v0("DashboardDirect", "simulation", None, None, None)

        if dron.state == "connected":
            # Delete every element and start the main page view
            self.connect_label.grid_forget()
            self.info_textbox.grid_forget()
            self.info_textbox2.grid_forget()

            # Create the main page view
            self.set_main_page()

            # Start the telemetry info
            dron.send_telemetry_info_trigger(None, None, None, self.telemetry)

        else:
            # Make the label invisible and show the button again
            self.connect_label.grid_forget()
            self.connect_button.grid(row=3, column=1, padx=10, pady=0, sticky="we", ipady=10)
            # Show an error message in the textbox, in red
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("1.0", "end")
            self.info_textbox.insert("1.0", "Error: Couldn't connect to the autopilot. Please, try again.")
            self.info_textbox.configure(state="disabled")
            # The message should be in red
            self.info_textbox.configure(text_color="red")

    def telemetry(self, telemetry_info):
        # Callback function to update the telemetry info in the main page view
        self.label_telemetry_lat_value.configure(text=telemetry_info['lat'])
        self.label_telemetry_lon_value.configure(text=telemetry_info['lon'])
        self.label_telemetry_alt_value.configure(text=telemetry_info['altitude'])
        self.label_telemetry_hea_value.configure(text=telemetry_info['heading'])
        self.label_telemetry_gs_value.configure(text=telemetry_info['groundSpeed'])
        self.label_telemetry_bat_value.configure(text=telemetry_info['battery'])

    def arm(self):
        # Arm the drone
        dron.arm_MAVLINK()

    def take_off(self):
        # Take off
        if dron.state == "armed" or "onHearth":
            t = threading.Thread(target=dron.takeOff_MAVLINK, args=[5, True])
            t.start()
            print("Vehicle taking off.")
        else:
            print("The vehicle is not armed.")

        # Wait until the vehicle reaches the target altitude
        t2 = threading.Thread(target=self.wait_take_off)
        t2.start()

    def go(self, direction):
        # Go to a direction
        if dron.state == "flying":
            dron.go_order(direction)
        else:
            print("The vehicle is not flying.")

    def rtl(self):
        # Return to launch
        if dron.state == "flying":
            dron.returning_trigger()

    def wait_take_off(self):
        # Wait until the vehicle reaches the target altitude
        while dron.state != "flying":
            if dron.state == "flying":
                break
            else:
                # Wait 0.5 seconds
                time.sleep(0.5)
        dron.flying_trigger()
        print("Vehicle reached target altitude.")






















# Run the app
app = App()
app.mainloop()