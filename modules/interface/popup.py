from .super import Interface
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkSlider, BOTH, HORIZONTAL, N


def led_focus_zoom_buttons(self, position=400):
    Focus = CTkButton(self, width=60, text="Focus", command=lambda: Focus_popup.open(self))     
    Ledbutton = CTkButton(self, width=60, text="Light", command=lambda: Led_popup.open(self))
    ZoomButton = CTkButton(self, width=60, text="Zoom", command=lambda: Zoom_popup.open(self))
    Focus.place(x=80, y=position)
    Ledbutton.place(x=10, y=position)
    ZoomButton.place(x=150, y=position)

class Led_popup(Interface, CTkFrame): #widget to fill popup window, show an stop button and a modifiable label

    def __init__(self, Tk_root, last_window, microscope, parameters, camera):
        Interface.__init__(self, Tk_root, last_window, microscope, parameters=parameters, camera=camera)
        self.auto_exp_value = "auto"
        self.awb_value = "auto"
        self.init_window(last_window)

    ###########
    ### Generate the window content, called every time window is (re)opened 
    def init_window(self, last_window):
        self.camera.print_metadata()
        self.last_window = last_window
        
        self.Tk_root.title("Light and Exposure") 
        self.pack(fill=BOTH, expand=1)

        self.Power_label = CTkLabel(self, text = "LED power:")
        self.Led_scale = CTkSlider(self, from_=0, to=255, height=60, width=200, orientation=HORIZONTAL)
        Save =  CTkButton(self, width=80, text="Save", command=self.save_led)

        Led1 = CTkButton(self, width=80, text="LED 1", command= lambda: self.led_change(1))
        Led2 = CTkButton(self, width=80, text="LED 2", command= lambda:  self.led_change(2))
        LedOff = CTkButton(self, width=80, text="Off", command= lambda: self.microscope.set_led_state(0))

        self.AutoExp = CTkButton(self, text="AutoExp ON", command=self.auto_exp)
        self.Shutter_label = CTkLabel(self, text = "Shutter speed μs")
        self.Exp_scale = CTkSlider(self, from_=100, to=20000, height=60, width=200, number_of_steps=(20000-100)/100, orientation=HORIZONTAL)
        self.Gain_label = CTkLabel(self, text = "Analogue Gain:")
        self.Gain_scale = CTkSlider(self, from_=1.0, to=10.5, height=60, width=200, number_of_steps=(10.5-1)/0.5, orientation=HORIZONTAL)
        self.EV_label = CTkLabel(self, text = "EV:")
        self.EV_scale = CTkSlider(self, from_=-2.0, to=2, height=60, width=200, number_of_steps=8, orientation=HORIZONTAL)
        
        self.AWB_button = CTkButton(self, text="Normal mode", command=self.awb)
 
        
        Led1.place(x=20,y=20)
        Led2.place(x=120,y=20)
        LedOff.place(x=70,y=55)

        self.Power_label.place(x=10, y= 80)  
        self.Led_scale.place(relx=0.5, y=105, anchor=N)
        self.Led_scale.set(self.microscope.positions[3])

        self.AWB_button.place(relx=0.5,y=190, anchor=N)       
        self.AutoExp.place(relx=0.5,y=230, anchor=N) 

        self.exposure_panel()

        self.set_exp_and_gain()
        self.set_led()
        
        Save.place(x=110, y=490)
        self.back_button(position=(10,490))

        if self.auto_exp_value == "off":
            self.AutoExp.configure(text="AutoExp OFF")
        
        if self.awb_value == "off":
            self.AWB_button.configure(text="AWB Fluo")


    def exposure_panel(self):
            
            if self.auto_exp_value == "off":
                current_exp, current_gain = self.camera.current_exposure()
                self.EV_scale.place_forget()
                self.EV_label.place_forget()

                self.Shutter_label.place(x=10, y= 270)
                self.Exp_scale.place(relx=0.5,y=295, anchor=N)
                self.Exp_scale.set(current_exp)

                self.Gain_label.place(x=10, y= 380)  
                self.Gain_scale.place(relx=0.5,y=405, anchor=N)
                self.Gain_scale.set(current_gain)

            else:
                self.Exp_scale.place_forget()
                self.Gain_scale.place_forget()
            
                self.Shutter_label.place(x=10, y= 270)
                self.Gain_label.place(x=10, y= 290)

                self.EV_label.place(x=10, y= 330)  
                self.EV_scale.place(relx=0.5,y=350, anchor=N)
                self.EV_scale.set(self.camera.EV_value)



    def led_change(self, led):
        if led == 1:
            self.microscope.set_led_state(1)
            self.camera.awb_preset("white")
            self.AWB_button.configure(text="AWB: Normal")

        if led == 2:
            self.microscope.set_led_state(2)
            self.camera.awb_preset("Green Fluo")
            self.AWB_button.configure(text="AWB: Green Fluo")

    def auto_exp(self):
        if self.auto_exp_value == "auto":
            self.camera.auto_exp_enable(False)
            self.auto_exp_value = "off"
            self.exposure_panel()

        
        elif self.auto_exp_value == "off":
            self.camera.auto_exp_enable(True)
            self.auto_exp_value = "auto"
            self.exposure_panel()
    
    def awb(self):
        if self.awb_value == "auto":
            self.awb_value = "off"
            self.camera.awb_preset("Green Fluo")
            self.AWB_button.configure(text="Green Fluo Mode")

        elif self.awb_value == "off":
            self.awb_value = "auto"
            self.camera.awb_preset( "auto")
            self.AWB_button.configure(text="Normal mode")
   
    def save_led(self):
        self.parameters.update([("led",[self.microscope.positions[3], self.microscope.positions[4]])])

    def set_led(self): ## Read the scale and set the led at the proper power
        pwr = int(self.Led_scale.get())
        self.Power_label.configure(text=f"LED power: {pwr}")
        if pwr != self.microscope.positions[3]:
            self.microscope.positions[3] = pwr
            self.microscope.set_ledpwr(pwr)
        Interface._job1 = self.after(100, self.set_led)
    
    def set_exp_and_gain(self): ## Read the scale and set the led at the proper power
        self.camera.current_exposure_nowait()

        exp_scale = int(self.Exp_scale.get())
        self.Shutter_label.configure(text=f"Shutter speed {exp_scale}μs")

        current_exp = self.camera.exp
        if exp_scale != current_exp: 
            if self.auto_exp_value == "off":
                self.camera.set_exposure( exp_scale)
            elif self.auto_exp_value == "auto":
                if current_exp > 20000:
                    current_exp = 20000
                self.Exp_scale.set(current_exp)
        
        gain_scale = int(self.Gain_scale.get())
        self.Gain_label.configure(text=f"Analogue Gain: {gain_scale}")

        current_gain = self.camera.gain
        if gain_scale != current_gain: 
            if self.auto_exp_value == "off":
                self.camera.set_exposure(gain=gain_scale)
            elif self.auto_exp_value == "auto":
                self.Gain_scale.set(current_gain)
        
        if self.auto_exp_value == "auto":
            EV = self.EV_scale.get()
            self.EV_label.configure(text=f"EV: {EV}")
            self.camera.set_EV(EV)

        Interface._job2 = self.after(200, self.set_exp_and_gain)
         

    def set_default(self): ## Read led power from Default parameter set
        led = self.parameters.get("Default")["led"]
        self.microscope.set_ledpwr(led[0])
        self.microscope.positions[3] = led[0]
        self.microscope.set_led_state(led[1])
        self.Led_scale.set(self.microscope.positions[3])
    
    def open(self):
        self.clear_jobs()
        self.clear_frame()
        if Interface._led_popup:
            Interface._led_popup.init_window(self)
        else:
            Interface._led_popup = Led_popup(self.Tk_root, last_window=self, microscope=self.microscope, parameters=self.parameters, camera=self.camera)


class Focus_popup(Interface, CTkFrame):

    def __init__(self, Tk_root, last_window, microscope,  grid, parameters):
        Interface.__init__(self, Tk_root, last_window=self, microscope=microscope, grid=grid, parameters=parameters)    
        self.init_window(last_window)

    ###########
    ### Generate the window content, called every time window is (re)opened 
    def init_window(self, last_window):
        self.last_window = last_window
        
        self.Tk_root.title("Focus") 
        self.pack(fill=BOTH, expand=1)
        self.show_record_label()

        Fp100 = CTkButton(self, width=80, text="Fcs +200", command=lambda: self.microscope.move_1axis(3,200))
        Fm100 = CTkButton(self, width=80,text="Fcs -200", command=lambda: self.microscope.move_1axis(3,-200))

        Fp25 = CTkButton(self, width=80,text="Fcs +25 ", command=lambda: self.microscope.move_1axis(3,25))
        Fm25 = CTkButton(self, width=80,text="Fcs -25 ", command=lambda: self.microscope.move_1axis(3,-25))

        Fp5 = CTkButton(self, width=80,text="Fcs +5  ", command=lambda: self.microscope.move_1axis(3,5))
        Fm5 = CTkButton(self, width=80,text="Fcs -5  ", command=lambda: self.microscope.move_1axis(3,-5))

        save = CTkButton(self, width=80, fg_color='green',text="Save", command=self.save_focus)
        Reset = CTkButton(self, width=80,fg_color='red', text="Reset", command=lambda: self.microscope.move_focus(self.parameters.get()["start"][2]))
        
        ObjOn = CTkButton(self, width=80, text="ObjOn", command=lambda:  self.microscope.move_focus(self.parameters.get()["start"][2] - 600 ))
        ObjOff = CTkButton(self, width=80, text="ObjOff", command=lambda: self.microscope.move_focus(0))
        
        Fp100.place(x=10, y=200)
        Fm100.place(x=100, y=200)
        Fp25.place(x=10, y=245)
        Fm25.place(x=100, y=245)
        Fp5.place(x=10, y=290)
        Fm5.place(x=100, y=290)

        ObjOff.place(x=10, y=100)
        ObjOn.place(x=100, y=100)


        save.place(x=80,y=350)
        Reset.place(x=10, y=350)
        self.back_button()

    def save_focus(self):
        self.parameters.update_start(None , None, self.microscope.positions[2], None)
        self.grid.generate_grid()
   
    
    def open(self):
        self.clear_jobs()
        self.clear_frame()
        if Interface._focus_popup:
            Interface._focus_popup.init_window(self)
        else:
            Interface._focus_popup = Focus_popup(self.Tk_root, last_window=self, microscope=self.microscope, grid=self.grid, parameters=self.parameters)

class Zoom_popup(Interface, CTkFrame): #widget to fill popup window, show an stop button and a modifiable label

    def __init__(self, Tk_root, last_window, microscope, parameters, camera):
        Interface.__init__(self, Tk_root, last_window, microscope, parameters=parameters, camera=camera)
        self.init_window(last_window)

    ###########
    ### Generate the window content, called every time window is (re)opened 
    def init_window(self, last_window):
        self.last_window = last_window 
        self.Tk_root.title("Zoom") 
        self.pack(fill=BOTH, expand=1)
        self.show_record_label()

        if not Interface._video_timer: ## Deactivate zoom button if filming
            zoom_buttons = [(" 1x", 1),("1.5x", 0.75),(" 2x", 0.5),(" 4x", 0.25),(" 8x", 0.125)]
            y_p = 60
            Zoom_1 = CTkButton(self, text=zoom_buttons[0][0], width=80, height=40, command=lambda: self.camera.change_zoom(zoom_buttons[0][1]))
            Zoom_1.place(relx=0.5, y=30, anchor=N)
            Zoom_2 = CTkButton(self, text=zoom_buttons[1][0], width=80, height=40, command=lambda: self.camera.change_zoom(zoom_buttons[1][1]))
            Zoom_2.place(relx=0.5, y=30+y_p, anchor=N)
            Zoom_3 = CTkButton(self, text=zoom_buttons[2][0], width=80, height=40, command=lambda: self.camera.change_zoom(zoom_buttons[2][1]))
            Zoom_3.place(relx=0.5, y=30+y_p*2, anchor=N)
            Zoom_4 = CTkButton(self, text=zoom_buttons[3][0], width=80, height=40, command=lambda: self.camera.change_zoom(zoom_buttons[3][1]))
            Zoom_4.place(relx=0.5, y=30+y_p*3, anchor=N)
            Zoom_5 = CTkButton(self, text=zoom_buttons[4][0], width=80, height=40, command=lambda: self.camera.change_zoom(zoom_buttons[4][1]))
            Zoom_5.place(relx=0.5, y=30+y_p*4, anchor=N)

        else:
            warning = CTkLabel(self, text="Can't change zoom \n whilerecording video")
            warning.place(x=10, y=30)

        self.back_button()
        self.snap_button()

    
    def open(self):
        self.clear_jobs()
        self.clear_frame()
        if Interface._zoom_popup:
            Interface._zoom_popup.init_window(self)
        else:
            Interface._zoom_popup = Zoom_popup(self.Tk_root, last_window=self, microscope=self.microscope, parameters=self.parameters, camera=self.camera)

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
    grid = PositionsGrid(microscope, parameters)
    micro_cam = Microscope_camera()
    micro_cam.initialise(QT=True)

    #Tkinter object
    customtkinter.set_appearance_mode("dark")
    Tk_root = customtkinter.CTk()
    Tk_root.geometry("230x560+800+35")   
    
    ### Don't display border if on the RPi display
    Interface._freemove_main = FreeMovementInterface(Tk_root, microscope=microscope, grid=grid, camera=micro_cam, parameters=parameters)


    Tk_root.mainloop()