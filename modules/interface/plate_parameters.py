from tinker import Frame, Button, BOTH, Label, StringVar, OptionMenu
from .super import Interface
from .freemove import FreeMovementInterface


class Plate_parameters(Interface,Frame):
    def __init__(self, Tk_root, microscope, grid, parameters):
        Interface.__init__(self, Tk_root, microscope=microscope, grid=grid, parameters=parameters)
        self._param_config = None
        self.init_window()

    
    def open(self):
        self.clear_jobs()
        self.clear_frame()
        if Interface._plate_parameters:
            Interface._plate_parameters.init_window()
        else:
            pass
            Interface._plate_parameters = Plate_parameters(self.Tk_root, self.microscope, self.grid, self.parameters)

    ###########
    ### Generate the window content, called every time window is (re)opened 
    def init_window(self):
 
        self.Tk_root.title("Grid") 
        self.pack(fill=BOTH, expand=1)

        self.Xsteps = self.parameters.get()["Xsteps"]
        self.Ysteps = self.parameters.get()["Ysteps"]
        self.subwells_spacing = self.parameters.get()["subwells_spacing"]

        self.parameter_menu(20,10)
        self.lines_columns_subwels(10,90)
        self.XYstep_config_buttons(10,220)
        self.back_to_main_button()   

    def XYstep_config_buttons(self, x_p=20, y_p=220):

        TopLabel = Label(self, text="Grid distances:")
        XstepsLabel = Label(self, text="X steps:\n" + str(self.Xsteps))
        YstepsLabel = Label(self, text="Y steps:\n" + str(self.Ysteps))
        Configure_XY =  Button(self, text="Configure X and Y step", command=self.set_steps)

        TopLabel.place(x=x_p, y=y_p)
        XstepsLabel.place(x=x_p+20, y=y_p+20)
        YstepsLabel.place(x=x_p+90, y=y_p+20)
        Configure_XY.place(x=x_p, y=y_p+60)

        A1X = self.parameters.get()["start"][0]
        A1Y = self.parameters.get()["start"][1]
        A1Label = Label(self, text=f"A1 position X: {A1X} Y: {A1Y}")
        A1position =  Button(self, text="Change A1 position", command=self.set_A1_position)
        A1Label.place(x=x_p, y=y_p+110)
        A1position.place(x=x_p, y=y_p+130)
    
    
    
    def lines_columns_subwels(self, x_p=10, y_p=10):
        
        self.lines = StringVar()
        self.columns = StringVar()
        self.subwells = StringVar()

        self.lines.set(self.parameters.get()["lines"])
        self.columns.set(self.parameters.get()["columns"])
        self.subwells.set(self.parameters.get()["subwells"])

        TopLabel = Label(self, text="Grid characteristics:")
        LinesLabel = Label(self, text="Lines:")
        LinesMenu = OptionMenu(self, self.lines, *[4,8,16])
        ColumnsLabel = Label(self, text="Columns:")
        ColumnsMenu = OptionMenu(self, self.columns, *[6,12,24])
        SubWellsLabel = Label(self, text="Subwells:")
        SubWellsMenu = OptionMenu(self, self.subwells, *[1,2,3,4])

        Save = Button(self, text="Save grid", command=self.save_grid_param)
        
        w=3
        LinesMenu.config(width=w)
        ColumnsMenu.config(width=w)
        SubWellsMenu.config(width=w)

        TopLabel.place(x=x_p, y=y_p)
        y_p = y_p +20
        LinesLabel.place(x=x_p+5, y=y_p)
        LinesMenu.place(x=x_p, y=y_p+20)
        ColumnsLabel.place(x=x_p+70, y=y_p)
        ColumnsMenu.place(x=x_p+70, y=y_p+20)
        SubWellsLabel.place(x=x_p+140, y=y_p)
        SubWellsMenu.place(x=x_p+140, y=y_p+20)
        Save.place(x=x_p, y=y_p+60)

    def parameter_menu(self, x_p, y_p):
        self.parameters_selector = StringVar()
        self.parameters_selector.set(self.parameters.selected)
        parameters_set_list = self.parameters.list_all()

        ParametersSet = OptionMenu(self, self.parameters_selector, *parameters_set_list,  command=self.parameter_set_changed)
        ParametersSet.config(width=15)
        ParametersSet_label =  Label(self, text="Parameters set:")
        ParametersSet_label.place(x=x_p, y=y_p)
        ParametersSet.place(x=x_p, y=y_p+20)
    
    def parameter_set_changed(self, new_param):
        self.parameters.select(new_param)
        endstops_dict = self.parameters.get()["dyn_endstops"] ## Load the specific dynamic endstops
        self.microscope.set_dynamic_endsotop(endstops_dict)
        self.init_window()


    def save_grid_param(self):
        self.parameters.update([ 
        ("lines", int(self.lines.get())), 
        ("columns", int(self.columns.get())),
        ("subwells", int(self.subwells.get())) ])
        self.grid.generate_grid()
    
    def set_steps(self):
        self.clear_frame()
        if self._param_config:
            self._param_config.init_window(step=True)
        else:
            pass
            self._param_config = ParametersConfig(self.Tk_root, self.microscope, self.grid, self.Xsteps, self.Ysteps, self.parameters)
            self._param_config.init_window(step=True)
    
    def set_A1_position(self):
        self.clear_frame()
        if self._param_config:
            self._param_config.init_window(A1=True)
        else:
            pass
            self._param_config = ParametersConfig(self.Tk_root, self.microscope, self.grid, self.Xsteps, self.Ysteps, self.parameters)
            self._param_config.init_window(A1=True)

    def set_dyn_endstop_position(self):
        self.clear_frame()
        if self._param_config:
            self._param_config.init_window(dyn=True)
        else:
            pass
            self._param_config = ParametersConfig(self.Tk_root, self.microscope, self.grid, self.Xsteps, self.Ysteps, self.parameters)
            self._param_config.init_window(dyn=True)        

class ParametersConfig(Interface, Frame):

    def __init__(self, Tk_root, microscope, grid, Xsteps, Ysteps, parameters):
        Interface.__init__(self, Tk_root, microscope=microscope, grid=grid, parameters=parameters)               
        self.Tk_window = Tk_root
        self.Xold_steps = Xsteps
        self.Yold_steps = Ysteps

   #Creation of init_window
    def init_window(self, A1=False, step=False, dyn=False):

        self.Tk_window.title("Steps") 
        self.pack(fill=BOTH, expand=1)
        self.show_record_label()
        self.start = self.parameters.get()["start"]   
            
        FreeMovementInterface.XYsliders(self,l=200)

        Cancel =  Button(self, text="Back", command=self.close_xy)
        Cancel.place(x=10,y=530)

        if step:
            self.grid_go_pad((100,320))
            self.save_XY_buttons(menus_position= (20,380))
        if A1:
            self.save_A1_button()
    
    def grid_go_pad(self, pad_position):
        A1 = Button(self, width=3, heigh=2, text="A1", command=lambda: self.grid.go("A1"))        
        B2 = Button(self, width=3, heigh=2, text="B2", command=lambda: self.go_and_change_divisor("B2", (1,1)))
        H1 = Button(self, width=3, heigh=2, text="H1", command=lambda: self.go_and_change_divisor("H1", (7,1)))
        A12 = Button(self, width=3, heigh=2, text="A12", command=lambda: self.go_and_change_divisor("A12", (1,11)))
        H12 = Button(self, width=3, heigh=2, text="H12", command=lambda: self.go_and_change_divisor("H12", (7,11)))

        A1.place(x=pad_position[0]-90, y=pad_position[1]-50)
        A12.place(x=pad_position[0]+70, y=pad_position[1]-50)
        H1.place(x=pad_position[0]-90, y=pad_position[1])
        H12.place(x=pad_position[0]+70, y=pad_position[1])
        B2.place(x=pad_position[0]-10, y=pad_position[1]-25)
    
    def go_and_change_divisor(self, position, div):      
        self.grid.go(position)
        self.divisorX.set(div[0])
        self.divisorY.set(div[1])
       
    ### Panel only for setting up X Y steps
    def save_XY_buttons(self, menus_position):
        self.divisorX = StringVar()
        self.divisorY = StringVar()
        self.divisorX.set(7)
        self.divisorY.set(11)
 
        DivisorXLabel = Label(self, text="Divisor X")
        DivisorXMenu = OptionMenu(self,  self.divisorX, *["      1   ","      2   ","      5   ","      7    "])
        DivisorXMenu.config(width=4)
        DivisorYLabel = Label(self, text="Divisor Y")
        DivisorYMenu = OptionMenu(self,  self.divisorY, *["      1   ","      2   ","      5   ","      11   "])
        DivisorYMenu.config(width=4)
        
        self.XSteps_label = Label(self, text="test")
        self.YSteps_label = Label(self, text="test")
        SaveX =  Button(self, text="Save X ", command=lambda:  self.save_measure(x=True))
        SaveY =  Button(self, text="Save Y", command=lambda: self.save_measure(y=True))

        DivisorXLabel.place(x=menus_position[0], y=menus_position[1])
        DivisorXMenu.place(x=menus_position[0], y=menus_position[1]+20)
        DivisorYLabel.place(x=menus_position[0]+125, y=menus_position[1])
        DivisorYMenu.place(x=menus_position[0]+125, y=menus_position[1]+20)       
        self.XSteps_label.place(x=menus_position[0], y=menus_position[1]+60)
        self.YSteps_label.place(x=menus_position[0]+125, y=menus_position[1]+60)
        SaveX.place(x=menus_position[0], y=menus_position[1]+100)
        SaveY.place(x=menus_position[0]+125, y=menus_position[1]+100)
        
        self.label_update()

    ### Panel only for setting up A1 position
    def save_A1_button(self, x_p=10, y_p=410):
        SaveA1 = Button(self, text="Save A1 center", command=self.save_A1)
        SaveA1.place(x=10,y=410)

    def save_A1(self):
        start = self.parameters.get()["start"]
        start[0] = self.microscope.positions[0]
        start[1] = self.microscope.positions[1]
        self.parameters.update([("start", start)])
        self.start = start
        self.grid.generate_grid()

    def measure(self):  
        self.Xsteps = abs(int( (self.microscope.positions[0] - self.start[0]) / int(self.divisorX.get())))
        self.Ysteps = abs(int( (self.microscope.positions[1] - self.start[1]) / int(self.divisorY.get())))
    
    def label_update(self):
        self.measure()
        self.XSteps_label.configure(text="Current X: " + str(self.Xold_steps)+ "\nNew:     " + str(self.Xsteps))
        self.YSteps_label.configure(text="Y: " + str(self.Yold_steps)+ "\n   " + str(self.Ysteps))
        Interface._job1 = self.after(500, self.label_update)
    
    def save_measure(self, x=False, y=False ):
        self.measure()
        if x:
            self.parameters.update([("X steps", self.Xsteps)])
        if y:
            self.parameters.update([("Y steps", self.Ysteps)])
        self.grid.generate_grid()
        self.close()
    
    def close_xy(self):
        self.clear_jobs()
        self.clear_frame()
        Interface._plate_parameters.init_window()

#main loop for testing only
if __name__ == "__main__": 
    from ..microscope import Microscope
    from ..position_grid import PositionsGrid
    from ..microscope_param import *
    from tinker import Tk

    ### Object for microscope to run
    microscope = Microscope(addr, ready_pin)
    grid = PositionsGrid(microscope)

    #Tkinter object
    Tk_root = Tk()
    Tk_root.geometry("230x560+800+35")   
    
    ### Don't display border if on the RPi display
    Interface._plate_parameters = Plate_parameters(Tk_root, last_window=None, microscope=microscope, grid=grid)

    Tk_root.mainloop()
