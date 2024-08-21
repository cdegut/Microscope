from RPi import GPIO
from os import environ

from modules.cameracontrol import Microscope_camera
from modules.microscope import Microscope
from modules.position_grid import PositionsGrid
from modules.physical_controller import encoder_read, controller_startup
from modules.interface.main_menu import *
from modules.microscope_param import *
from modules.parametersIO import ParametersSets, create_folder
import customtkinter
import tkinter as Tk
import PIL


#main loop
if __name__ == "__main__": 


    encoder_X, encoder_Y, encoder_F = controller_startup()                
    ### Object for microscope to run
    parameters = ParametersSets()
    microscope = Microscope(addr, ready_pin, parameters)
    grid = PositionsGrid(microscope, parameters)
    micro_cam = Microscope_camera()

    #Tkinter object
    customtkinter.set_appearance_mode("dark")
    Tk_root = customtkinter.CTk()
    Tk_root.geometry("230x560+800+35")

    #touch control
    Tk_control = Tk.Tk()

    Tk_control.geometry("200x200+0+35")
    Tk_control.attributes('-alpha',1.0)
    Tk_control.wm_attributes("-topmost", True)
    #Tk_control.wm_attributes("-disabled", True)
    Tk_control.wait_visibility(Tk_control)
    Tk_control.wm_attributes("-alpha", 0)

    ### Don't display border if on the RPi display
    display = environ.get('DISPLAY')
    if display == ":0.0" or display == ":0": ## :0.0 in terminal and :0 without terminal
        Tk_root.overrideredirect(1) ### not working with remote display !!
        Tk_control.overrideredirect(1)

    Interface._main_menu = MainMenu(Tk_root, microscope=microscope, grid=grid, camera=micro_cam,  parameters=parameters)



    if display == ":0.0" or display == ":0": ## :0.0 in terminal and :0 without terminal
        micro_cam.initialise()   
    else:
        micro_cam.initialise(QT=True)

    
    if microscope.positions[4] == 1:
        micro_cam.awb_preset("white")
    if microscope.positions[4] == 2:
        micro_cam.awb_preset("Green Fluo")

    #Interface._main_menu.display_image_as_label()

    ## Microscope controller main loop
    while not Interface._exit:

        ##Read physical interface
        encoder_read(microscope, encoder_X,1,X_controller_short, X_controller_long)
        encoder_read(microscope, encoder_Y,2,Y_controller_short, Y_controller_long)
        encoder_read(microscope, encoder_F,3,F_controller_short, F_controller_long)

        #Tkinter mainloop
        Tk_root.update_idletasks()
        Tk_root.update()
        Tk_control.update()

    Tk_root.destroy()

    #GPIO cleanup
    GPIO.cleanup()
