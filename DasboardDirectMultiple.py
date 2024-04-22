import customtkinter as ctk
import tkinter as ttk
import tkintermapview as tkmap
import os
import sys
import time
import threading
import json

# Import the Dron class
from Dron import Dron


# Night mode
ctk.set_appearance_mode("dark")



# Create App class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create the app
        self.geometry("900x600")
        self.title("Dashboard Direct Multiple")
        self.resizable(False, False)

        # CLASS VARIABLES
        self.mission_waypoints = []
        self.mission_markers = []

        self.geofence_points = []
        self.geofence_markers = []
        self.geofence_enabled = False
        
        # Drone selector
        self.drone_selector_id = 1

        # Drone selected
        self.dron = None

        # Drones
        self.drones = []

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
        self.info_textbox.insert("1.0", "Welcome to DashboardDirect Multiple.\nThis version of Dashboard Direct allows you to control several\ndrones simultaneously (10 maximum).\n\nPlease, click the 'Connect' button to start.")
        # Add a version number to the textbox
        self.info_textbox.insert("end", "\n\nPATCH NOTES:\n\n- Version: 0.1.0: Initial release [16/04/24].")

        self.info_textbox.configure(state="disabled")

        # Create the info_textbox2 (read-only)
        self.info_textbox2 = ctk.CTkTextbox(self.main_frame)
        self.info_textbox2.grid(row=0, column=0, padx=10, pady=10, rowspan=8, columnspan=6, sticky="nswe")
        self.info_textbox2.insert("1.0", "Space reserved for the logo or image.")
        self.info_textbox2.configure(state="disabled")

        # Create a option selector for the number of drones (1 to 10)
        self.id_drone_number = ctk.CTkOptionMenu(self.main_frame, values=["Select swarm size...", "2","3", "4", "5","6", "7", "8","9", "10" ], width=130)
        self.id_drone_number.grid(row=6, column=6, padx=10, pady=0, ipady=0, columnspan=1, sticky="we")

        # Create a option selector for the mode (real or simulation)
        self.mode_selector = ctk.CTkOptionMenu(self.main_frame, values=["Simulation", "Real"], width=130)
        self.mode_selector.grid(row=6, column=7, padx=10, pady=0, ipady=0, columnspan=1, sticky="we")







    # FUNCTIONS (FRONTEND)
    def on_button_connect_click(self):
        # If the swarm size is not selected, show an error message
        if self.id_drone_number.get() == "Select swarm size...":
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("1.0", "end")
            self.info_textbox.insert("1.0", "Error: Please, select the swarm size.")
            self.info_textbox.configure(state="disabled")
            self.info_textbox.configure(text_color="red")
            return
        else:
            # Create the drones (1 to 10 depending on the selection) [i is the ID of the drone]
            for i in range(1, int(self.id_drone_number.get()) + 1):
                self.drones.append(Dron(i))

            # Before finishing, select the first drone as the selected drone
            self.dron = self.drones[0]
            print("Drone selected: " + str(self.dron))
            
            # Make the button invisible and substitute it with a label
            self.connect_button.grid_forget()
            self.id_drone_number.grid_forget()
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
        self.map_widget.grid(row=0, column=0, padx=10, pady=10, rowspan=8, columnspan=6, sticky="nswe")
        # Change the map style to satellite
        x = -35.3633515
        y = 149.1652412
        z = 15
        self.map_widget.set_tile_server("https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", max_zoom=22)
        self.map_widget.set_position(x, y)
        #self.map_widget.place(relx=0.5, rely=0.5, anchor="center")
        # Add a right click menu to add mission waypoints
        #self.map_widget.add_right_click_menu_command(label="Add Mission Waypoint", command=self.add_mission_waypoint_event, pass_coords=True) (commented for DashboardDirectMultiple)
        # Add a right click menu to add geofence points
        #self.map_widget.add_right_click_menu_command(label="Add Geofence Point", command=self.add_geofence_point_event, pass_coords=True) (commented for DashboardDirectMultiple)
                    
        # Start the print drones on map thread
        t2 = threading.Thread(target=self.print_drones_on_map)
        t2.start()

        # Create the main_frame_telemetry (for telemetry info)
        self.frame_telemetry = ctk.CTkFrame(self.main_frame, height=60)
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

        # Create the labels for the telemetry info, 4 parameters (alt, heading, groundSpeed, battery)

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
        


        # Create a 1 row frame to select the drone that is being controlled
        self.frame_drone_selector = ctk.CTkFrame(self.main_frame, height=25)
        self.frame_drone_selector.grid(row=1, column=6, padx=10, pady=10, rowspan=1, columnspan=2, sticky="we")
        # Color the frame
        self.frame_drone_selector.configure(fg_color="#1f1f1f")
        # frame_telemetry can't be resized
        self.frame_drone_selector.grid_propagate(False)

        # Separate the frame_telemetry into 3 vertical sections
        self.frame_drone_selector.columnconfigure(0, weight=1)
        self.frame_drone_selector.columnconfigure(1, weight=1)
        self.frame_drone_selector.columnconfigure(2, weight=1)

        # Create the drone selector (1 button left, 1 label center, 1 button right)
        self.drone_selector_left = ctk.CTkButton(self.frame_drone_selector, text="<", fg_color="#3117ea", hover_color="#190b95", command=self.select_previous_drone, height=15, width=15)
        self.drone_selector_left.grid(row=0, column=0, padx=2, pady=2, sticky="w")

        self.drone_selector_label = ctk.CTkLabel(self.frame_drone_selector, text="Drone ID: 1", font=("TkDefaultFont", 10), height=15)
        self.drone_selector_label.grid(row=0, column=1, padx=0, pady=2, sticky="we")

        self.drone_selector_right = ctk.CTkButton(self.frame_drone_selector, text=">", fg_color="#3117ea", hover_color="#190b95", command=self.select_next_drone, height=15, width=15)
        self.drone_selector_right.grid(row=0, column=2, padx=2, pady=2, sticky="e")


        
        # Create the main_frame_control_buttons (for control buttons)
        self.main_frame_control_buttons = ctk.CTkFrame(self.main_frame)
        self.main_frame_control_buttons.grid(row=3, column=6, padx=10, pady=10, rowspan=7, columnspan=2, sticky="swe")
        # Color the frame
        self.main_frame_control_buttons.configure(fg_color="#1f1f1f")
        # frame_telemetry can't be resized
        self.main_frame_control_buttons.grid_propagate(False)

        # Separate the frame_telemetry into 3 vertical sections
        self.main_frame_control_buttons.columnconfigure(0, weight=1)
        self.main_frame_control_buttons.columnconfigure(1, weight=1)
        self.main_frame_control_buttons.columnconfigure(2, weight=1)

        # Create the control buttons
        
        self.control_button_arm = ctk.CTkButton(self.main_frame_control_buttons, text="Arm", command=self.arm, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_arm.grid(row=0, column=0, padx=5, pady=5, sticky="we", ipady=10)

        self.control_button_take_off = ctk.CTkButton(self.main_frame_control_buttons, text="Take Off", command=self.take_off, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_take_off.grid(row=0, column=1, padx=5, pady=5, sticky="we", ipady=10)

        self.control_button_RTL = ctk.CTkButton(self.main_frame_control_buttons, text="RTL", command=self.rtl, fg_color="#3117ea", hover_color="#190b95")
        self.control_button_RTL.grid(row=0, column=2, padx=5, pady=5, sticky="we", ipady=10)
        


        # Create the main_frame_control_pad (for control pad)
        
        self.main_frame_control_pad = ctk.CTkFrame(self.main_frame)
        self.main_frame_control_pad.grid(row=2, column=6, padx=10, pady=10, rowspan=1, columnspan=2, sticky="nswe")
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
        
        
    def create_table(self): # Incomplete
        columns = ("ID", "Value")
        self.table = ttk.Treeview(self.main_tabview.tab("Parameters"), columns=columns, show="headings")
        self.table.heading("ID", text="ID")
        self.table.heading("Value", text="Value")
        self.table.grid(row=1, column=0, padx=10, pady=10, sticky="we", columnspan=2)

    # UPDATE CONTROL BUTTONS
    def update_control_buttons(self):
        while True:
            # print("Drone ID: " + str(self.drone_selector_id) + " - State: " + self.dron.state)
            # Update the control buttons depending on the state of the drone (for the selected drone)
            if self.dron.state == "connected":
                # Change the color of the arm button to blue
                self.control_button_arm.configure(fg_color="#3117ea", hover_color="#190b95", state="normal")
                # The other buttons are disabled
                self.control_button_take_off.configure(fg_color="#3117ea", hover_color="#190b95", state="disabled")
                self.control_button_RTL.configure(fg_color="#3117ea", hover_color="#190b95", state="disabled")
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

    # PRINT DRONES ON THE MAP
    def print_drones_on_map(self):
        # Print the drones on the map
        # Create a list of markers for the drones, with the same length as the number of drones
        drones_markers = [None] * len(self.drones)
        first_time = True
        while True:
            for dron in self.drones:
                # Obtain the position of the drone
                marker_lat, marker_lon, marker_alt = dron.get_position()
                dron.get_position()

                # Delete the previous marker
                print (str(len(drones_markers)))
                if first_time == False:
                    drones_markers[dron.ID - 1].delete()

                # Create a marker for every drone
                print("Drone " + str(dron.ID) + " - Lat: " + str(marker_lat) + " - Lon: " + str(marker_lon))
                marker = self.map_widget.set_marker(marker_lat, marker_lon, text="Drone " + str(dron.ID), marker_color_circle="red", marker_color_outside="black", text_color="red")
                
                # Add the marker to the list
                drones_markers[dron.ID - 1] = marker
            
            # Wait 1 second (crash prevention)
            time.sleep(0.1)
            first_time = False

    # FUNCTIONS (BACKEND)
        
    # Connect
    def connect(self):
        # The connection ports are the following [10 possible drones]:
        self.ports = [5763, 5773, 5783, 5793, 5803, 5813, 5823, 5833, 5843, 5853]

        # Depending if real time or simulation mode is selected, the connection string will be different
        mode_selector = str(self.mode_selector.get())

        if mode_selector == "Simulation":
            print('Simulation mode selected')
            # Connect every drone to the autopilot
            for dron in self.drones:
                dron.connect("DashboardDirect", "simulation", None, None, None, "tcp:127.0.0.1:" + str(self.ports[dron.ID - 1]), True)
                # Wait 1 second and check if the drone is connected
                time.sleep(1)
                if dron.state == "connected":
                    print("Drone " + str(dron.ID) + " connected.")
                else:
                    print("Error: Drone " + str(dron.ID) + " couldn't connect.")
        else:
            # A HACER
            print ('Real mode selected')
            # connection_string = "/dev/ttyS0"
            connection_string = "com7"
            # connection_string = "udp:127.0.0.1:14550"

        # Check that every drone is connected
        verification = True
        for dron in self.drones:
            if dron.state !="connected":
                verification = False
                break
        if verification:
            # Delete every element and start the main page view
            self.connect_label.grid_forget()
            self.info_textbox.grid_forget()
            self.info_textbox2.grid_forget()

            # Create the main page view
            self.set_main_page()

            # Start the update control buttons thread
            t = threading.Thread(target=self.update_control_buttons)
            t.start()

            # Start the telemetry info for every drone
            for dron in self.drones:
                dron.send_telemetry_info_trigger(None, None, None, self.telemetry)

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

    def telemetry(self, telemetry_info, drone_id):
        # Callback function to update the telemetry info in the main page view
        # Check if the drone ID is the same as the selected drone
        if drone_id == self.drone_selector_id:
            # Update the telemetry info
            #self.label_telemetry_lat_value.configure(text=telemetry_info['lat'])
            #self.label_telemetry_lon_value.configure(text=telemetry_info['lon'])
            self.label_telemetry_alt_value.configure(text=telemetry_info['altitude'])
            self.label_telemetry_hea_value.configure(text=telemetry_info['heading'])
            self.label_telemetry_gs_value.configure(text=telemetry_info['groundSpeed'])
            self.label_telemetry_bat_value.configure(text=telemetry_info['battery'])

    def arm(self):
        # Change the arm button color to orange
        self.control_button_arm.configure(fg_color="orange", hover_color="darkorange")
        # Arm the drone
        self.dron.arm(False)

    def take_off(self):
        # Change the take off button color to orange
        self.control_button_take_off.configure(fg_color="orange", hover_color="darkorange")
        # Take off the drone
        self.dron.take_off(10, False)

    def go(self, direction):
        # Go to a direction
        if self.dron.state == "flying":
            self.dron.go_order(direction)
        else:
            print("The vehicle is not flying.")

    def rtl(self):
        # Return to launch
        if self.dron.state == "flying":
            self.dron.return_to_launch(False)

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
            parameter_value = self.dron.get_parameter(parameter_id, True)
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
                self.dron.modify_parameter(parameter_id, parameter_value, True)
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


    # DRONE SELECTOR:

    def select_previous_drone(self):
        # Select the previous drone
        if self.drone_selector_id > 1:
            self.drone_selector_id -= 1
            self.drone_selector_label.configure(text="Drone ID: " + str(self.drone_selector_id))
            self.dron = self.drones[self.drone_selector_id - 1]
        else:
            self.drone_selector_id = len(self.drones)
            self.drone_selector_label.configure(text="Drone ID: " + str(self.drone_selector_id))
            self.dron = self.drones[self.drone_selector_id - 1]

    def select_next_drone(self):
        # Select the next drone
        if self.drone_selector_id < len(self.drones):
            self.drone_selector_id += 1
            self.drone_selector_label.configure(text="Drone ID: " + str(self.drone_selector_id))
            self.dron = self.drones[self.drone_selector_id - 1]
        else:
            self.drone_selector_id = 1
            self.drone_selector_label.configure(text="Drone ID: " + str(self.drone_selector_id))
            self.dron = self.drones[self.drone_selector_id - 1]
 










# Run the app
app = App()
app.mainloop()