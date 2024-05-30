import customtkinter as ctk
import tkinter as ttk
import tkintermapview as tkmap
import os
import sys
import time
import threading
import json
import base64
import io
from PIL import Image, ImageTk

# Import the Dron class
from Dron import Dron

# Import the Camera class
from Camera import Camera

# Night mode
ctk.set_appearance_mode("dark")



# Create App class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create the app
        self.geometry("900x600")
        self.title("Dashboard Direct")
        self.resizable(False, False)

        # CLASS VARIABLES
        self.mission_waypoints = []
        self.mission_markers = []

        self.geofence_points = []
        self.geofence_markers = []
        self.geofence_enabled = False

        # Dron marker variable
        self.dron_marker = None

        # Load images
        current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.plane_circle_1_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "drone_circle.png")).resize((35, 35)))

        # Go to point
        self.go_to_point_coords = None


        # MAIN FRAME
        # Create the main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Separate the main_frame into 8 vertical sections
        self.column0 = self.main_frame.columnconfigure(0, weight=1)
        self.column1 = self.main_frame.columnconfigure(1, weight=1)
        self.column2 = self.main_frame.columnconfigure(2, weight=1)
        self.column3 = self.main_frame.columnconfigure(3, weight=1)
        self.column4 = self.main_frame.columnconfigure(4, weight=1)
        self.column5 = self.main_frame.columnconfigure(5, weight=1)
        self.column6 = self.main_frame.columnconfigure(6, weight=1)
        self.column7 = self.main_frame.columnconfigure(7, weight=1)



        # Separate the main_frame into 8 horizontal sections
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        self.main_frame.rowconfigure(4, weight=1)
        self.main_frame.rowconfigure(5, weight=1)
        self.main_frame.rowconfigure(6, weight=1)
        self.main_frame.rowconfigure(7, weight=1)



        # BUTTONS
        # Create the connect_button
        self.connect_button = ctk.CTkButton(self.main_frame, text="Connect", command=self.on_button_connect_click, fg_color="#3117ea", hover_color="#190b95")
        self.connect_button.grid(row=7, column=6, padx=10, pady=10, sticky="nswe", ipady=0, columnspan=2)

        # TEXTBOXES
        # Create the info_textbox (read-only)
        self.info_textbox = ctk.CTkTextbox(self.main_frame)
        self.info_textbox.grid(row=0, column=6, padx=10, pady=10, rowspan=6, columnspan=2, sticky="nswe")
        self.info_textbox.insert("1.0", "Welcome to DashboardDirect.\nThis tool allows you to interact with the\nautopilot functions directly without using any\nbroker.\n\nPlease, click the 'Connect' button to start.")
        # Add a version number to the textbox
        self.info_textbox.insert("end", "\n\nPATCH NOTES:\n\n- Version: 0.1.0: Initial release\n\n- Version: 0.1.1: Connect and telemetry info added.\n\n- Version: 0.1.2: Control and pad buttons added.")

        self.info_textbox.configure(state="disabled")

        # Create the info_textbox2 (read-only)
        self.info_textbox2 = ctk.CTkTextbox(self.main_frame)
        self.info_textbox2.grid(row=0, column=0, padx=10, pady=10, rowspan=8, columnspan=6, sticky="nswe")
        self.info_textbox2.insert("1.0", "Space reserved for the logo or image.")
        self.info_textbox2.configure(state="disabled")

        # Create the ID input textbox with a shadow text inside
        self.id_input = ctk.CTkEntry(self.main_frame, border_color="#3117ea", text_color="gray", width=130, placeholder_text="type drone ID...")
        self.id_input.grid(row=6, column=6, padx=10, pady=0, ipady=0, columnspan=1, sticky="we")

        # Create a option selector for the mode (real or simulation)
        self.mode_selector = ctk.CTkOptionMenu(self.main_frame, values=["Simulation", "Real"], width=130)
        self.mode_selector.grid(row=6, column=7, padx=10, pady=0, ipady=0, columnspan=1, sticky="we")







    # FUNCTIONS (FRONTEND)
    def on_button_connect_click(self):
        # If it is not a integer, show an error message in the textbox, in red
        if not self.id_input.get().isdigit():
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("1.0", "end")
            self.info_textbox.insert("1.0", "Error: The ID must be a number.")
            self.info_textbox.configure(state="disabled")
            self.info_textbox.configure(text_color="red")
            return
        else:
            # Create the Dron object
            self.dron = Dron(int(self.id_input.get()))

            # Create Camera object
            self.camera = Camera(int(self.id_input.get()))
            
            # Make the button invisible and substitute it with a label
            self.connect_button.grid_forget()
            self.id_input.grid_forget()
            self.mode_selector.grid_forget()
            self.connect_label = ctk.CTkLabel(self.main_frame, text="Connecting...")
            self.connect_label.grid(row=7, column=6, padx=10, pady=0, sticky="nswe", columnspan=2)


            # Connect to the autopilot 1000ms later
            self.after(1000, self.connect)

    def set_main_page(self):
        # Create the main page view

        # Create the main_frame with tabs for the functionalities of the dashboard

        # Add a map to the main frame
        self.map_widget = tkmap.TkinterMapView(self.main_frame)
        self.map_widget.grid(row=0, column=0, padx=10, pady=10, rowspan=5, columnspan=6, sticky="nswe")
        # Change the map style to satellite
        x = -35.3633515
        y = 149.1652412
        z = 15
        self.map_widget.set_tile_server("https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", max_zoom=22)
        self.map_widget.set_position(x, y)
        #self.map_widget.place(relx=0.5, rely=0.5, anchor="center")
        # Add a right click menu to add mission waypoints
        self.map_widget.add_right_click_menu_command(label="Add Mission Waypoint", command=self.add_mission_waypoint_event, pass_coords=True)
        # Add a right click menu to add geofence points
        self.map_widget.add_right_click_menu_command(label="Add Geofence Point", command=self.add_geofence_point_event, pass_coords=True)
        # Add a right click menu to add a GO TO point
        self.map_widget.add_right_click_menu_command(label="Go to", command=self.go_to_point_event, pass_coords=True)


        # Insert tabview
        self.main_tabview = ctk.CTkTabview(self.main_frame)
        self.main_tabview.grid(row=5, column=0, padx=10, pady=10, rowspan=3, columnspan=6, sticky="nswe")
        # Create the tabs
        self.main_tabview.add("Parameters")
        self.main_tabview.add("Mission")
        self.main_tabview.add("Geofence")

        # Parameters tab

        # Create a frame for get a parameter, with grey background
        self.get_parameter_frame = ctk.CTkFrame(self.main_tabview.tab("Parameters"), height=80, width=265)
        self.get_parameter_frame.grid(row=0, column=0, padx=10, pady=5, sticky="we")
        self.get_parameter_frame.configure(fg_color="#1f1f1f")
        # Separate the frame into 4 vertical sections
        self.get_parameter_frame.columnconfigure(0, weight=1)
        self.get_parameter_frame.columnconfigure(1, weight=1)
        self.get_parameter_frame.columnconfigure(2, weight=1)
        self.get_parameter_frame.columnconfigure(3, weight=1)
        # Separate the frame into 2 horizontal section
        self.get_parameter_frame.rowconfigure(0, weight=1)
        self.get_parameter_frame.rowconfigure(1, weight=1)
        
        # Add a button to get the value of a parameter
        self.get_parameter_button = ctk.CTkButton(self.get_parameter_frame, text="Get parameter", command=self.get_parameter, fg_color="#3117ea", hover_color="#190b95", width=40)
        self.get_parameter_button.grid(row=0, column=1, padx=10, pady=5)
        # Add a entry to write the parameter ID
        self.parameter_id_input = ctk.CTkEntry(self.get_parameter_frame, border_color="#3117ea", text_color="gray", width=130, placeholder_text="type parameter ID...")
        self.parameter_id_input.grid(row=0, column=0, padx=10, pady=5)
        # Add a label to show the value of the parameter
        self.parameter_value_label = ctk.CTkLabel(self.get_parameter_frame, text="Value: ", font=("TkDefaultFont", 11))
        self.parameter_value_label.grid(row=3, column=0, padx=10, pady=5, sticky="w", columnspan=2)
        

        # Create a frame for set a parameter, with grey background
        
        self.set_parameter_frame2 = ctk.CTkFrame(self.main_tabview.tab("Parameters"), width=265, height=80)
        self.set_parameter_frame2.grid(row=1, column=0, padx=10, pady=5, sticky="we", columnspan=2)
        self.set_parameter_frame2.configure(fg_color="#1f1f1f")
        # Separate the frame into 2 vertical sections
        self.set_parameter_frame2.columnconfigure(0, weight=1)
        self.set_parameter_frame2.columnconfigure(1, weight=1)
        # Separate the frame into 2 horizontal section
        self.set_parameter_frame2.rowconfigure(0, weight=1)
        self.set_parameter_frame2.rowconfigure(1, weight=1)

        # Add a button to set the value of a parameter
        self.set_parameter_button = ctk.CTkButton(self.set_parameter_frame2, text="Set parameter", command=self.set_parameter, fg_color="#3117ea", hover_color="#190b95", width=40)
        self.set_parameter_button.grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky="we")
        # Add a entry to write the parameter ID
        self.parameter_id_input_set = ctk.CTkEntry(self.set_parameter_frame2, border_color="#3117ea", text_color="gray", placeholder_text="type ID...", width=120)
        self.parameter_id_input_set.grid(row=0, column=0, padx=10, pady=5)
        # Add a entry to write the parameter value
        self.parameter_value_input = ctk.CTkEntry(self.set_parameter_frame2, border_color="#3117ea", text_color="gray", placeholder_text="type value...", width=100)
        self.parameter_value_input.grid(row=0, column=1, padx=10, pady=5)
        


        # Mission tab
        # Separate the tab into 2 horizontal sections
        self.main_tabview.tab("Mission").rowconfigure(0, weight=1)
        self.main_tabview.tab("Mission").rowconfigure(1, weight=1)

        # Separate the tab into 4 vertical sections
        self.main_tabview.tab("Mission").columnconfigure(0, weight=1)
        self.main_tabview.tab("Mission").columnconfigure(1, weight=1)
        self.main_tabview.tab("Mission").columnconfigure(2, weight=1)
        self.main_tabview.tab("Mission").columnconfigure(3, weight=1)
        
        # Add a button to upload the flight plan
        self.upload_flight_plan_button = ctk.CTkButton(self.main_tabview.tab("Mission"), text="Upload Flight Plan", command=self.upload_flight_plan, fg_color="#3117ea", hover_color="#190b95")
        self.upload_flight_plan_button.grid(row=0, column=0, padx=10, pady=10, sticky="we", ipady=10)

        # Add a button to execute the flight plan
        self.execute_flight_plan_button = ctk.CTkButton(self.main_tabview.tab("Mission"), text="Execute Flight Plan", command=self.execute_flight_plan, fg_color="#3117ea", hover_color="#190b95")
        self.execute_flight_plan_button.grid(row=0, column=1, padx=10, pady=10, sticky="we", ipady=10)



        # Geofence tab
        # Separate the tab into 2 horizontal sections
        self.main_tabview.tab("Geofence").rowconfigure(0, weight=1)
        self.main_tabview.tab("Geofence").rowconfigure(1, weight=1)

        # Separate the tab into 3 vertical sections
        self.main_tabview.tab("Geofence").columnconfigure(0, weight=1)
        self.main_tabview.tab("Geofence").columnconfigure(1, weight=1)
        self.main_tabview.tab("Geofence").columnconfigure(2, weight=1)

        # Add a button to Enable the geofence
        self.enable_geofence_button = ctk.CTkButton(self.main_tabview.tab("Geofence"), text="Enable Geofence", command=self.enable_disable_geofence, fg_color="#3117ea", hover_color="#190b95")
        self.enable_geofence_button.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        # Add a button to upload the geofence
        self.upload_geofence_button = ctk.CTkButton(self.main_tabview.tab("Geofence"), text="Upload Fence", command=self.upload_geofence, fg_color="#3117ea", hover_color="#190b95")
        self.upload_geofence_button.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        # Add a selector to choose the geofence action
        self.geofence_action_selector = ctk.CTkOptionMenu(self.main_tabview.tab("Geofence"), values=["RTL", "Report", "Brake"], width=130, command=self.set_geofence_action)
        self.geofence_action_selector.grid(row=0, column=2, padx=10, pady=10, sticky="we")

        # Add a button to clear the geofence and map
        self.clear_geofence_button = ctk.CTkButton(self.main_tabview.tab("Geofence"), text="Clear Geofence Points", command=self.clear_geofence, fg_color="#3117ea", hover_color="#190b95")
        self.clear_geofence_button.grid(row=1, column=0, padx=10, pady=10, sticky="we", columnspan=3)


        # Create the main_frame_telemetry (for telemetry info)
        self.frame_telemetry = ctk.CTkFrame(self.main_frame, height=80)
        self.frame_telemetry.grid(row=0, column=6, padx=10, pady=10, rowspan=1, columnspan=2, sticky="we")
        # Color the frame
        self.frame_telemetry.configure(fg_color="#1f1f1f")
        # frame_telemetry can't be resized
        self.frame_telemetry.grid_propagate(False)

        # Separate the frame_telemetry into 2 vertical sections
        self.frame_telemetry.columnconfigure(0, weight=1)
        self.frame_telemetry.columnconfigure(1, weight=1)

        # Separate the frame_telemetry into 2 horizontal section
        self.frame_telemetry.rowconfigure(0, weight=1)
        self.frame_telemetry.rowconfigure(1, weight=1)

        # Create the labels for the telemetry info, 6 parameters (lat, lon, alt, heading, groundSpeed, battery) inide every frame

        self.label_telemetry_alt = ctk.CTkLabel(self.frame_telemetry, text="Altitude: ",font=("TkDefaultFont", 11))
        self.label_telemetry_alt.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.label_telemetry_alt_value = ctk.CTkLabel(self.frame_telemetry, text="0.0", font=("TkDefaultFont", 11, "bold"))
        self.label_telemetry_alt_value.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.label_telemetry_hea = ctk.CTkLabel(self.frame_telemetry, text="Heading: ", font=("TkDefaultFont", 11))
        self.label_telemetry_hea.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.label_telemetry_hea_value = ctk.CTkLabel(self.frame_telemetry, text="0.0", font=("TkDefaultFont", 11, "bold"))
        self.label_telemetry_hea_value.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.label_telemetry_gs = ctk.CTkLabel(self.frame_telemetry, text="Ground Speed: ", font=("TkDefaultFont", 11))
        self.label_telemetry_gs.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.label_telemetry_gs_value = ctk.CTkLabel(self.frame_telemetry, text="0.0", font=("TkDefaultFont", 11, "bold"))
        self.label_telemetry_gs_value.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.label_telemetry_bat = ctk.CTkLabel(self.frame_telemetry, text="Battery: ", font=("TkDefaultFont", 11))
        self.label_telemetry_bat.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.label_telemetry_bat_value = ctk.CTkLabel(self.frame_telemetry, text="0.0", font=("TkDefaultFont", 11, "bold"))
        self.label_telemetry_bat_value.grid(row=1, column=1, padx=5, pady=5, sticky="e")


        # Create a frame for the video stream

        self.frame_stream = ctk.CTkFrame(self.main_frame, height=250)
        self.frame_stream.grid(row=1, column=6, padx=10, pady=10, rowspan=3, columnspan=2, sticky="we")
        # Color the frame
        self.frame_stream.configure(fg_color="#1f1f1f")
        # frame_telemetry can't be resized
        self.frame_stream.grid_propagate(False)

        # Create label for photo (no text, just the photo)
        self.label_photo = ctk.CTkLabel(self.frame_stream, text="", font=("TkDefaultFont", 11))
        self.label_photo.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Create the main_frame_control_pad (for control pad)
        
        self.main_frame_control_pad = ctk.CTkFrame(self.main_frame)
        self.main_frame_control_pad.grid(row=4, column=6, padx=10, pady=10, rowspan=1, columnspan=2, sticky="nswe")
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
        


        # Create the main_frame_control_buttons (for control buttons)
        self.main_frame_control_buttons = ctk.CTkFrame(self.main_frame, height=120)
        self.main_frame_control_buttons.grid(row=5, column=6, padx=10, pady=10, rowspan=1, columnspan=2, sticky="we")
        # Color the frame
        self.main_frame_control_buttons.configure(fg_color="#1f1f1f")
        # frame_telemetry can't be resized
        self.main_frame_control_buttons.grid_propagate(False)

        # Separate the frame_telemetry into 3 vertical sections
        self.main_frame_control_buttons.columnconfigure(0, weight=1)
        self.main_frame_control_buttons.columnconfigure(1, weight=1)
        self.main_frame_control_buttons.columnconfigure(2, weight=1)

        # Separate the frame_telemetry into 2 horizontal section
        self.main_frame_control_buttons.rowconfigure(0, weight=1)
        self.main_frame_control_buttons.rowconfigure(1, weight=1)
        self.main_frame_control_buttons.rowconfigure(2, weight=1)

        # Create the control buttons
        
        self.control_button_arm = ctk.CTkButton(self.main_frame_control_buttons, text="Arm", command=self.arm, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_arm.grid(row=0, column=0, padx=5, pady=5, sticky="we", ipady=10)

        self.control_button_take_off = ctk.CTkButton(self.main_frame_control_buttons, text="Take Off", command=self.take_off, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_take_off.grid(row=0, column=1, padx=5, pady=5, sticky="we", ipady=10)

        self.control_button_RTL = ctk.CTkButton(self.main_frame_control_buttons, text="RTL", command=self.rtl, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_RTL.grid(row=0, column=2, padx=5, pady=5, sticky="we", ipady=10)
        
        self.control_button_goto = ctk.CTkButton(self.main_frame_control_buttons, text="Goto", fg_color="#3117ea", hover_color="#190b95")
        self.control_button_goto.grid(row=1, column=2, padx=5, pady=5, sticky="we", ipady=10)

        self.control_button_picture = ctk.CTkButton(self.main_frame_control_buttons, text="Take Picture", command=self.take_picture, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_picture.grid(row=1, column=0, padx=5, pady=5, sticky="we", ipady=10)

        self.control_button_take_off_all = ctk.CTkButton(self.main_frame_control_buttons, text="Start Stream", command=self.start_stream, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_take_off_all.grid(row=1, column=1, padx=5, pady=5, sticky="we", ipady=10)

        # Create the disconnect button (Red)

        self.info_textbox_drones = ctk.CTkButton(self.main_frame, height=60 , text="Disconnect", command=self.disconnect, fg_color="red", hover_color="darkred")
        self.info_textbox_drones.grid(row=6, column=6, padx=10, pady=10, rowspan=1, columnspan=2, sticky="nswe")
        




    # UPDATE CONTROL BUTTONS
    def update_control_buttons(self):
        while True:
            if self.dron.state == "connected":
                # Change the colors of the buttons to blue and enable the arm button
                self.control_button_arm.configure(fg_color="#3117ea", hover_color="#190b95", state="normal")
                self.control_button_take_off.configure(fg_color="#3117ea", hover_color="#190b95")
                self.control_button_RTL.configure(fg_color="#3117ea", hover_color="#190b95")
                # The other buttons are disabled
                self.control_button_take_off.configure(state="disabled")
                self.control_button_RTL.configure(state="disabled")
            if self.dron.state == "armed":
                # Change the color of the arm button to green
                self.control_button_arm.configure(fg_color="green", hover_color="darkgreen")
                # The take off button is enabled and the RTL button is disabled
                self.control_button_take_off.configure(fg_color="#3117ea", hover_color="#190b95", state="normal")
                self.control_button_RTL.configure(fg_color="#3117ea", hover_color="#190b95", state="disabled")
            if self.dron.state == "takingOff":
                # Change the color of the take off button to orange
                self.control_button_take_off.configure(fg_color="orange", hover_color="darkorange")
                # The arm button is disabled and the RTL button is disabled
                self.control_button_arm.configure(fg_color="green", hover_color="darkgreen", state="disabled")
                self.control_button_RTL.configure(fg_color="#3117ea", hover_color="#190b95", state="disabled")
            if self.dron.state == "flying":
                # Change the color of the take off button to green
                self.control_button_take_off.configure(fg_color="green", hover_color="darkgreen", state="disabled")
                # The arm button is disabled and the RTL button is enabled
                self.control_button_arm.configure(fg_color="green", hover_color="darkgreen", state="disabled")
                self.control_button_RTL.configure(fg_color="#3117ea", hover_color="#190b95", state="normal")
            if self.dron.state == "returningHome":
                # Change the color of the RTL button to orange
                self.control_button_RTL.configure(fg_color="orange", hover_color="darkorange")
                # The arm button is disabled and the take off button is disabled
                self.control_button_arm.configure(fg_color="green", hover_color="darkgreen", state="disabled")
                self.control_button_take_off.configure(fg_color="green", hover_color="darkgreen", state="disabled")
            if self.dron.state == "onHearth":
                # Reset the colors of the buttons
                self.control_button_arm.configure(fg_color="#3117ea", hover_color="#190b95", state="normal")
                self.control_button_take_off.configure(fg_color="#3117ea", hover_color="#190b95", state="disabled")
                self.control_button_RTL.configure(fg_color="#3117ea", hover_color="#190b95", state="disabled")
            time.sleep(0.5)



    # FUNCTIONS (BACKEND)
        
    # Connect
    def connect(self):

        # Depending if real time or simulation mode is selected, the connection string will be different
        mode_selector = self.mode_selector.get()
        # mode_selector = "simulation" # This variable will change depending on the user's selection when connecting

        if mode_selector == "simulation":
            print('Simulation mode selected')
            if self.dron.ID == 1:
                connection_string = "tcp:127.0.0.1:5763"
            if self.dron.ID == 2:
                connection_string = "tcp:127.0.0.1:5773"
            else:
                connection_string = "tcp:127.0.0.1:5763" # Default connection string
        
        else: # A MODIFICAR
            print ('Real mode selected')
            # connection_string = "/dev/ttyS0"
            connection_string = "com5"
            # connection_string = "udp:127.0.0.1:14550"

        # Connect to the autopilot
        self.dron.connect_trigger(connection_string, True)

        if self.dron.state == "connected":
            # Delete every element and start the main page view
            self.connect_label.grid_forget()
            self.info_textbox.grid_forget()
            self.info_textbox2.grid_forget()

            # Create the main page view
            self.set_main_page()

            # Start the update control buttons thread
            t = threading.Thread(target=self.update_control_buttons)
            t.start()

            # Start the telemetry info
            self.dron.send_telemetry_info_trigger(self.telemetry)

        else:
            # Make the label invisible and show the button again
            self.connect_label.grid_forget()
            self.connect_button.grid(row=3, column=1, padx=10, pady=0, sticky="we", ipady=10)
            # Show an error message in the textbox, in red
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("1.0", "end")
            self.info_textbox.insert("1.0", "Error: Couldn't connect to the autopilot. Please, reset the application and try again.")
            self.info_textbox.configure(state="disabled")
            # The message should be in red
            self.info_textbox.configure(text_color="red")

    # Disconnect
    def disconnect(self):
        # Disconnect every drone
        self.dron.disconnect()

        # Restart the application
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def telemetry(self, telemetry_info, drone_id):
        # Callback function to update the telemetry info in the main page view
        #self.label_telemetry_lat_value.configure(text=telemetry_info['lat'])
        #self.label_telemetry_lon_value.configure(text=telemetry_info['lon'])
        self.label_telemetry_alt_value.configure(text=telemetry_info['altitude'])
        self.label_telemetry_hea_value.configure(text=telemetry_info['heading'])
        self.label_telemetry_gs_value.configure(text=telemetry_info['groundSpeed'])
        self.label_telemetry_bat_value.configure(text=telemetry_info['battery'])

        # Check if a marker for the drone has been created previously
        if self.dron_marker is not None:
            # Delete the marker
            self.dron_marker.delete()

        # Create a marker for the drone
        marker = self.map_widget.set_marker(telemetry_info['lat'], telemetry_info['lon'], text="Drone ", icon=self.plane_circle_1_image, marker_color_circle="green", marker_color_outside="black", text_color="black")
        # Update the marker
        self.dron_marker = marker

    def arm(self):
        # Change the arm button color to orange
        self.control_button_arm.configure(fg_color="orange", hover_color="darkorange")
        # Arm the drone
        self.dron.arm_trigger(False)

    def take_off(self):
        # Change the take off button color to orange
        self.control_button_take_off.configure(fg_color="orange", hover_color="darkorange")

        self.dron.take_off_trigger(10, False)


    def go(self, direction):
        # Go to a direction
        if self.dron.state == "flying":
            self.dron.go_order(direction)
        else:
            print("The vehicle is not flying.")

    def rtl(self):
        # Return to launch
        if self.dron.state == "flying":
            self.dron.return_to_launch_trigger(False)

    def wait_take_off(self):
        # Wait until the vehicle reaches the target altitude
        while self.dron.state != "flying":
            if self.dron.state == "flying":
                break
            else:
                # Wait 0.5 seconds
                time.sleep(0.5)
        self.dron.flying_trigger()
        print("Vehicle reached target altitude.")

    def get_all_parameters(self):
        # Get all parameters
        parameters_id, parameters_value = self.dron.get_all_parameters(True)
        print("Button pressed. Getting all parameters...")
        print(parameters_id) # Ver como mostrarlo en la interfaz

    def get_parameter(self):
        # Get a parameter and show it in the label
        parameter_id = self.parameter_id_input.get()
        if parameter_id != "":
            parameter_value = self.dron.get_parameter_trigger(parameter_id, True)
            self.parameter_value_label.configure(text="Value: " + str(parameter_value))
        else:
            self.parameter_value_label.configure(text="Value: ")

    def set_parameter(self):
        # Set a parameter
        parameter_id = self.parameter_id_input_set.get()
        parameter_value = float(self.parameter_value_input.get())
        if parameter_id != "" and parameter_value != "":
            # Try to set the parameter, if it is not possible, show an error message
            try:
                self.dron.modify_parameter_trigger(parameter_id, parameter_value, True)
                print("Parameter set.")
            except:
                print("Error setting the parameter.")

    # FLIGHT PLAN:

    def upload_flight_plan(self):
        # Upload the flight plan
        print("Uploading flight plan...")
        # Create a JSON string with the mission waypoints, with the following format:
        '''
        {
        "coordinates": [
            {"lat": 47.6205, "lon": -122.3493, "alt": 100},  // Coordinate 1
            {"lat": 47.6153, "lon": -122.3448, "alt": 150},  // Coordinate 2
            {"lat": 47.6102, "lon": -122.3425, "alt": 200}   // Coordinate 3
        ]
        }
        '''
        waypoints = {"coordinates": self.mission_waypoints}
        waypoints_json = json.dumps(waypoints)
        print(waypoints_json)
        
        self.dron.uploadFlightPlan(waypoints_json)

    def execute_flight_plan(self):
        # Execute the flight plan
        print("Executing flight plan...")
        self.dron.executeFlightPlan()

    # GEOFENCE:

    def enable_disable_geofence(self):
        # Check if the geofence is enabled or disabled
        if self.geofence_enabled:
            # Disable the geofence
            print("Disabling geofence...")
            self.dron.disable_geofence() # Disable the geofence
            self.geofence_enabled = False

            # Make the button blue and change the text to "Enable Geofence"
            self.enable_geofence_button.configure(text="Enable Geofence", fg_color="#3117ea", hover_color="#190b95")
        else:
            # Enable the geofence
            print("Enabling geofence...")

            self.dron.enable_geofence() # Enable the geofence
            self.geofence_enabled = True

            # Make the button red and change the text to "Disable Geofence"
            self.enable_geofence_button.configure(text="Disable Geofence", fg_color="red", hover_color="darkred")

    def upload_geofence(self):
        if len(self.geofence_points) < 3:
            print("Error: You need at least 3 points to create a geofence.")

        else:
            # Add the first point to the end of the list to close the geofence
            self.geofence_points.append(self.geofence_points[0])
            # Add the first point to the first position of the list, as the reference point
            self.geofence_points.insert(0, self.geofence_points[0])
            # Convert the list of points to a list of tuples
            fencelist = [(point["lat"], point["lon"]) for point in self.geofence_points]

            print(fencelist)

            # Call the function to upload the geofence
            print("Uploading geofence...")
            self.dron.set_fence_geofence(fencelist)
        
    def set_geofence_action(self, action):
        # Set the geofence action
        print("Geofence action set to:", action)
        if action == "RTL":
            action_id = 1
        elif action == "Report":
            action_id = 2
        elif action == "Brake":
            action_id = 3
        else:
            action_id = 1
        self.dron.action_geofence(action_id)
    
    def clear_geofence(self):
        # Clear the geofence
        print("Clearing geofence...")
        # Delete every element from the geofence points list
        self.geofence_points = []
        # Delete every element from the geofence markers list
        for marker in self.geofence_markers:
            marker.delete()
        # Delete every element from the geofence markers list
        self.geofence_markers = []

    # MAP:

    def add_mission_waypoint_event(self, coords):
        # Add altitude to the coords (6 meters)
        coords = (coords[0], coords[1], 6)
        print("Add Mission Waypoint:", coords)
        # Add the waypoint to the mission waypoints list with altitude 6
        entry = {"lat": coords[0], "lon": coords[1], "alt": 6}
        self.mission_waypoints.append(entry)
        new_marker = self.map_widget.set_marker(coords[0], coords[1], text=str(len(self.mission_waypoints)), marker_color_circle="red", marker_color_outside="black", text_color="red")
    
    def add_geofence_point_event(self, coords):
        print("Add Geofence Point:", coords)
        # Add the point to the geofence points list
        entry = {"lat": coords[0], "lon": coords[1]}
        self.geofence_points.append(entry)
        new_marker = self.map_widget.set_marker(coords[0], coords[1], text=str(len(self.geofence_points)), marker_color_circle="blue", marker_color_outside="black", text_color="blue")
        # Add the new marker to the list
        self.geofence_markers.append(new_marker)


    def go_to_point_event(self, coords):
        print("Go to:", coords)
        # Go to a point
        self.dron.goto_trigger(coords[0], coords[1], 10, False)
 
 # CAMERA:

    def take_picture(self):
        # Take a picture
        print("Taking picture...")
        jpg_as_text = self.camera.take_picture()

        # Process the frame
        self.process_frame(jpg_as_text)


    def start_stream(self):
        # Start the video stream
        print("Starting stream...")
        self.camera.start_video_stream(self.process_frame)


    def process_frame(self, jpg_as_text):
        
        # Convert to bytes
        image_bytes = base64.b64decode(jpg_as_text)

        # Create image PIL with the bytes
        image_pil = Image.open(io.BytesIO(image_bytes))
        # Resize the image
        image_pil = image_pil.resize((280, 135), Image.ANTIALIAS)

        # Convert to custom tkinter image
        image_tk = ImageTk.PhotoImage(image_pil)

        # Show the image in the image label
        self.label_photo.configure(image=image_tk)






# Run the app
app = App()
app.mainloop()