from RPi import GPIO
from os import environ
from PyQt5.QtWidgets import  QApplication 
from PyQt5 import QtCore

from modules.cameracontrol import Microscope_camera
from modules.microscope import Microscope
from modules.position_grid import PositionsGrid
from modules.physical_controller import encoder_read, controller_startup
import time
import os
from modules.interface.main_menu import *
from modules.microscope_param import *
from modules.parametersIO import ParametersSets, create_folder
import random
import numpy as np
#from modules.interface.control_overlay import Overlay
from modules.interface.picameraQT import MainApp
import customtkinter
import sys
import cv2

def multiscale_ecc_alignment(image1, image2, num_scales=3):
    # Create a list to store downscaled versions of the images
    image1_pyramid = [image1]
    image2_pyramid = [image2]
    
    for i in range(1, num_scales):
        image1_pyramid.append(cv2.pyrDown(image1_pyramid[i-1]))
        image2_pyramid.append(cv2.pyrDown(image2_pyramid[i-1]))
    
    # Start with the smallest scale
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    for scale in range(num_scales-1, -1, -1):
        # Resize images back to original scale
        scaled_image1 = image1_pyramid[scale]
        scaled_image2 = image2_pyramid[scale]
        
        # Run ECC algorithm at the current scale
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 1000, 1e-5)
        (cc, warp_matrix) = cv2.findTransformECC(scaled_image1, scaled_image2, warp_matrix, cv2.MOTION_TRANSLATION, criteria)
        
        # Scale the warp matrix to the next level if not at the last scale
        if scale != 0:
            warp_matrix[0, 2] *= 2
            warp_matrix[1, 2] *= 2
    
    return warp_matrix

class Accuracy_tester():
    def __init__(self, microscope: Microscope, position_grid: PositionsGrid, camera: Microscope_camera,  parameters: ParametersSets):
        self.microscope = microscope
        self.position_grid = position_grid
        self.camera = camera
        self.parameters = parameters

        self.execute_function = self.testing_loop
        self.camera.switch_mode(self.camera.full_res_config, signal_function=self.camera.qpicamera.signal_done)
        self.loop_progress = 'init'

        #Grid Recording parameters
        self.positions_list = None
        self.delay_value = None
        self.repeat_value = None
        self.done_repeat = 0
        self.index_position = 0
        self.pic_taken = False
        self.pre_pic_timer = 0
        self.grid_folder = None
        self.grid_subwells_value = None
        self.pause_timer =0
        self.is_regording = False
        self.camera_is_init = False
        self.last_image = None

        self.distance_X =  0
        self.distance_Y =  0
        self.last_X_error = None
        self.last_Y_error = None
        self.back_to_start = False

        self.start_image = None
        self.current_image = None
        self.last_image = None


        self.start = self.parameters.get()["start"]
        self.target_position = self.parameters.get()["start"]

        self.microscope.go_absolute(self.target_position)

            #reset everything
        self.is_regording = True

        self.positions_list = None
        self.done_repeat = 0
        self.pic_taken = False
        self.pre_pic_timer = 0
        self.grid_subwells_value = None
        self.pause_timer =0

        if self.microscope.led1pwr ==0:
            self.microscope.set_ledspwr(50,0)

        current_time = time.localtime()        
        date = str(current_time[0])[2:] + str(current_time[1]).zfill(2) + str(current_time[2]).zfill(2) + "_"  \
            + str(current_time[3]).zfill(2) + str(current_time[4]).zfill(2)
        data_dir = self.parameters.get()["data_dir"]      
        home = os.getenv("HOME")

        self.test_data_folder = f"{home}/{data_dir}/accuracy_test-{date}/"
        create_folder(self.test_data_folder)


        open(f"{self.test_data_folder}/data.txt", "x")

        with open(f"{self.test_data_folder}/data.txt", "a") as data_file:
            data_file.write("Repeat\tX error(first image)\tX drift(last image)\tX distance\tY error(first image)\tY drift(last image)\tY distance\n")


    def at_position(self)  -> bool:
        self.microscope.update_real_state()
        if self.microscope.XYFposition == self.target_position:
            return True
        else:
            return False
    
    def get_X_Y_error(self,array1,array2):
        image1 = cv2.cvtColor(array1, cv2.COLOR_BGR2GRAY)
        image2 = cv2.cvtColor(array2, cv2.COLOR_BGR2GRAY)

        # Align images using multiscale ECC
        warp_matrix = multiscale_ecc_alignment(image1, image2)

        # Apply the warp transformation
        aligned_image2 = cv2.warpAffine(image2, warp_matrix, (image1.shape[1], image1.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
       
        # (Optional) Align image2 using the homography matrix and display
        aligned_image2 = cv2.warpAffine(image2, warp_matrix, (image1.shape[1], image1.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        difference = cv2.absdiff(image1, aligned_image2)
        scale_factor = 0.1
        difference_resized = cv2.resize(difference, (0, 0), fx=scale_factor, fy=scale_factor)
        cv2.imwrite(f"{self.test_data_folder}/{self.done_repeat}.jpg", difference_resized)

        Y_error = warp_matrix[0, 2]
        X_error = warp_matrix[1, 2]
        return round(X_error,1), round(Y_error,1)

    def process_difference(self):
        
        X_error, Y_error = self.get_X_Y_error(self.start_image, self.current_image)
        if not self.last_X_error:
            X_drift = X_error
            Y_drift = Y_error
        else:
            X_drift =  X_error - self.last_X_error
            Y_drift = Y_error - self.last_Y_error 

        data = f"{self.done_repeat}\t{X_error}\t{X_drift}\t{self.distance_X}\t{Y_error}\t{Y_drift}\t{self.distance_Y}\n"

        
        with open(f"{self.test_data_folder}/data.txt", "a") as data_file:
            data_file.write(data)
        
        print(f"\nRepeat n {self.done_repeat}")
        print(f"Translation error in pixels X axis: {X_error:.2f} for this image, and drift {X_drift:.2f} from last image")
        print(f"Translation error in pixels Y axis: {Y_error:.2f} for this image and drift {Y_drift:.2f} from last image")

        self.last_X_error = X_error
        self.last_Y_error = Y_error




    
    def testing_loop(self):   

        if self.at_position() == False: #return if not at position
            return
     
        match self.loop_progress :

            case 'init':
                if self.pic_taken == False and self.pre_pic_timer < 100:        
                    self.pre_pic_timer += 1
                    return
                else:
                    self.camera.create_main_array()
                    self.camera.auto_exp_enable(False)

                    self.loop_progress = "save start array"
                    return
                
            case "save start array":

                if self.camera.full_image_array is not None:
                    self.start_image = self.camera.full_image_array.copy()
                    self.last_image = self.camera.full_image_array.copy()
                    self.camera.full_image_array = None
                    self.loop_progress = "main loop"
                    return
            
            case "save current array":

                if self.camera.full_image_array is not None:
                    self.current_image = self.camera.full_image_array.copy()
                    self.camera.full_image_array = None
                    self.loop_progress = "process difference"
                    self.pre_pic_timer = 0
                    return

            case "process difference":
                self.process_difference()
                self.loop_progress = "main loop"
                return
            
            case "take image":

                ### pre image delay 3s
                if self.pic_taken == False and self.pre_pic_timer < 60000:        
                    self.pre_pic_timer += 1
                    return
                
                self.camera.create_main_array()
                self.loop_progress = "save current array"
                self.pic_taken = True
                self.done_repeat +=1
                self.pre_pic_timer = 0
                return
            
            case "main loop":

                if self.back_to_start == True:
                    self.back_to_start = False

                else:
                    self.loop_progress = "take image"

if __name__ == "__main__": 

    encoder_X, encoder_Y, encoder_F = controller_startup()                
    ### Object for microscope to run
    parameters = ParametersSets()
    microscope = Microscope(addr, ready_pin, parameters)
    position_grid = PositionsGrid(microscope, parameters)
    micro_cam = Microscope_camera(microscope)
    
    #Tkinter object
    customtkinter.set_appearance_mode("dark")
    Tk_root = customtkinter.CTk()
    Tk_root.geometry("230x564+804+36")

    ### Don't display border if on the RPi display
    display = environ.get('DISPLAY')
    if display == ":0.0" or display == ":0": ## :0.0 in terminal and :0 without terminal
        Tk_root.overrideredirect(1)
        export = False
    else:
        export = True

    ## this avoid an error with CV2 and Qt, it clear all the env starting with QT_
    for k, v in environ.items():
        if k.startswith("QT_") and "cv2" in v:
            del environ[k]   
    
    Interface._main_menu = MainMenu(Tk_root, microscope=microscope, position_grid=position_grid, camera=micro_cam,  parameters=parameters)
    
    app = QApplication(sys.argv)
    preview_window = MainApp(micro_cam, microscope, export)

    #access neede to interact with preview when doing captures
    micro_cam.qpicamera = preview_window.main_widget.qpicamera2 

    # run the old Tk interace in a Qt timer
    timer = QtCore.QTimer()
    tester = Accuracy_tester(microscope=microscope, position_grid=position_grid, camera=micro_cam,  parameters=parameters)
    timer.timeout.connect(tester.execute_function)
    timer.start(10)

    sys.exit(app.exec_())

    #GPIO cleanup
    GPIO.cleanup()
