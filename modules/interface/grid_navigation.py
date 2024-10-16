from customtkinter import CTkFrame, CTkButton, CTkLabel, BOTH, CTkOptionMenu, N
from .super import Interface
from .popup import led_focus_zoom_buttons
from .plate_parameters import Plate_parameters, ParametersConfig

plate_name = "Plate" ##is a place holder to later add a plate type selector, maybe

class MainGridInterface(Interface, CTkFrame): #main GUI window
    
    def __init__(self, Tk_root, microscope, position_grid, camera, parameters):
        Interface.__init__(self, Tk_root, microscope=microscope, position_grid=position_grid, camera=camera, parameters=parameters)
        self._param_config = None

        self.init_window()
        self.start_position = self.parameters.get()["start"]
    
    ######Function called to open this window, generate an new object the first time, 
    ###### then recall the init_window function of the same object
    def open(self):
        self.clear_jobs()
        self.clear_frame()
        if Interface._grid_main:
            Interface._grid_main.init_window()
        else:
            Interface._grid_main = MainGridInterface(self.Tk_root, self.microscope, self.position_grid, self.camera, self.parameters)

    ###########
    ### Generate the window content, called every time window is (re)opened 
    def init_window(self):
              
        #Title of the root  
        self.Tk_root.title("Control Panel")
        self.pack(fill=BOTH, expand=1)

        ##Generic buttons
        self.back_to_main_button()
        led_focus_zoom_buttons(self)

        ##Navigation pads as function
        self.grid_position_pad((20,20))
        self.grid_navigation_pad((20,160))
        self.coordinate_place()

        # creating buttons instances          
        self.snap_button()
        Adjust_A1 = CTkButton(self, width=80, text="Adjust A1 position", command=self.adjust_A1)
        Adjust_A1.place(x=10, y=300)

        # placing the elements

    def adjust_A1(self):
        self.clear_jobs()
        self.clear_frame()
        if self._param_config:
            self._param_config.init_window()
        else:
            pass
            self._param_config = ParametersConfig(self.Tk_root, self, self.microscope, self.position_grid, self.parameters, self.camera)
            self._param_config.A1_mode = True
            self._param_config.init_window()

    def grid_position_pad(self, pad_position):
        w = 65
        h = 30
        A1 = CTkButton(self, width=w, fg_color='Green', text="A1", command=lambda: self.position_grid.go("A1"))
        A12 = CTkButton(self, width=w, text="A12", command=lambda: self.position_grid.go("A12"))
        H1 = CTkButton(self, width=w, text="H1", command=lambda: self.position_grid.go("H1"))
        H12 = CTkButton(self, width=w, text="H12", command=lambda: self.position_grid.go("H12"))
        D6 = CTkButton(self, width=w, text="D6", command=lambda: self.position_grid.go("D6"))
        ### Pad as relative position to pad_position       
        A1.place(x=pad_position[0], y=pad_position[1])
        A12.place(x=pad_position[0]+w*2, y=pad_position[1])
        D6.place(x=pad_position[0]+w, y=pad_position[1]+h)
        H1.place(x=pad_position[0], y=pad_position[1]+h*2)
        H12.place(x=pad_position[0]+w*2, y=pad_position[1]+h*2)

    
    def grid_navigation_pad(self, pad_position):
        w = 65
        h = 40
        NextC = CTkButton(self, text="Col +",  width=w, command=lambda: self.position_grid.go_next_well("column", 1))
        NextL = CTkButton(self, text="Line +", width=w, command=lambda:self.position_grid.go_next_well("line", 1))
        PrevC = CTkButton(self, text="Col -",  width=w, command=lambda: self.position_grid.go_next_well("column", -1))
        PrevL = CTkButton(self, text="Line -", width=w, command=lambda:self.position_grid.go_next_well("line", -1))
        SubW = CTkButton(self, text="Sub", width=w, command=lambda:self.position_grid.switch_subwell())
        self.well_info = CTkLabel(self, text="## - #", font=("arial", 15))

        PrevL.place(x=pad_position[0]+w, y=pad_position[1])
        PrevC.place(x=pad_position[0], y=pad_position[1]+h)
        NextC.place(x=pad_position[0]+w*2, y=pad_position[1]+h)
        NextL.place(x=pad_position[0]+w, y=pad_position[1]+h*2)
        self.well_info.place(x=pad_position[0]+w+w/2, y=pad_position[1]+h, anchor=N)
        SubW.place(x=pad_position[0]+w*2, y=pad_position[1]+h*2)


    def go_start(self):
        start_position = self.parameters.get()["start"]
        led = self.parameters.get()["led"]
        self.microscope.go_absolute(start_position) #this function return only after arduin is ready
        self.microscope.set_ledpwr(led[0])
        self.microscope.set_led_state(led[1])


#main loop
if __name__ == "__main__": 
    from modules.cameracontrol import Microscope_camera
    from modules.microscope import Microscope
    from modules.position_grid import PositionsGrid
    from modules.physical_controller import encoder_read, controller_startup
    from modules.interface.main_menu import *
    from modules.microscope_param import *
    from modules.parametersIO import ParametersSets, create_folder
    import customtkinter
    ### Object for microscope to run

    #Tkinter object
    parameters = ParametersSets()
    microscope = Microscope(addr, ready_pin, parameters)
    position_grid = PositionsGrid(microscope, parameters)
    micro_cam = None

    #Tkinter object
    customtkinter.set_appearance_mode("dark")
    Tk_root = customtkinter.CTk()
    Tk_root.geometry("230x560+800+35")   
    
    ### Don't display border if on the RPi display
    Interface._grid_main = MainGridInterface(Tk_root, microscope=microscope, position_grid=position_grid, camera=None, parameters=parameters)

    Tk_root.mainloop()
