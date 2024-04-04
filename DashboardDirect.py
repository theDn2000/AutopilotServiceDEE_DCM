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
        self.title("Dashboard Direct")
        self.resizable(False, False)

        # CLASS VARIABLES
        self.mission_waypoints = []
        self.geofence_points = []


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
        self.info_textbox.insert("end", "\n\nPATCH NOTES:\n\n- Version: 0.1.0: Initial release\n\n- Version: 0.1.1: Connect and telemetry info      added.\n\n- Version: 0.1.2: Control and pad buttons added.")

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
            self.dron = Dron(int(self.id_input.get()))
            
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


        # Insert tabview
        self.main_tabview = ctk.CTkTabview(self.main_frame)
        self.main_tabview.grid(row=5, column=0, padx=10, pady=10, rowspan=3, columnspan=6, sticky="nswe")
        # Create the tabs
        self.main_tabview.add("Parameters")
        self.main_tabview.add("Mission")
        self.main_tabview.add("Geofence")

        # Parameters tab
        # Add a table to see the parameters using treeview
        ####
        # Add a TEST button to get all the parameters
        #self.get_parameters_button = ctk.CTkButton(self.main_tabview.tab("Parameters"), text="Get parameters", command=self.get_all_parameters, fg_color="#3117ea", hover_color="#190b95")
        #self.get_parameters_button.grid(row=0, column=0, padx=10, pady=10, sticky="we", ipady=10)
        
        # Create a frame for the table
        #self.table_frame = ctk.CTkFrame(self.main_tabview.tab("Parameters"), width=265, height=80)
        #self.table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="we")

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
        self.main_frame_control_buttons = ctk.CTkFrame(self.main_frame)
        self.main_frame_control_buttons.grid(row=2, column=6, padx=10, pady=10, rowspan=7, columnspan=2, sticky="nswe")
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
        
        self.main_frame_control_pad = ctk.CTkFrame(self.main_frame)
        self.main_frame_control_pad.grid(row=1, column=6, padx=10, pady=10, rowspan=1, columnspan=2, sticky="nswe")
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




    # FUNCTIONS (BACKEND)
        
    # Connect
    def connect(self):

        # Depending if real time or simulation mode is selected, the connection string will be different
        mode_selector = self.mode_selector.get()
        mode_selector = "simulation" # This variable will change depending on the user's selection when connecting

        if mode_selector == "simulation":
            print('Simulation mode selected')
            if self.dron.ID == 1:
                connection_string = "tcp:127.0.0.1:5763"
            if self.dron.ID == 2:
                connection_string = "tcp:127.0.0.1:5773"
            else:
                connection_string = "tcp:127.0.0.1:5763" # Default connection string
        
        else:
            print ('Real mode selected')
            # connection_string = "/dev/ttyS0"
            connection_string = "com7"
            # connection_string = "udp:127.0.0.1:14550"

        # Connect to the autopilot
        self.dron.connect("DashboardDirect", "simulation", None, None, None, connection_string, True)

        if self.dron.state == "connected":
            # Delete every element and start the main page view
            self.connect_label.grid_forget()
            self.info_textbox.grid_forget()
            self.info_textbox2.grid_forget()

            # Create the main page view
            self.set_main_page()

            # Start the telemetry info
            self.dron.send_telemetry_info_trigger(None, None, None, self.telemetry)

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
        self.dron.arm(False)

    def take_off(self):

        self.dron.take_off(10, False)
        # Take off
        #if dron.state == "armed" or "onHearth":
        #    t = threading.Thread(target=dron.takeOff_MAVLINK, args=[5, True])
        #    t.start()
        #    print("Vehicle taking off.")
        #else:
        #    print("The vehicle is not armed.")

        # Wait until the vehicle reaches the target altitude
        #t2 = threading.Thread(target=self.wait_take_off)
        #t2.start()

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
            parameter_value = self.dron.get_parameter_MAVLINK(parameter_id)
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
                self.dron.modify_parameter_MAVLINK(parameter_id, parameter_value)
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




 










# Run the app
app = App()
app.mainloop()