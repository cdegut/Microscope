#Software Endstop (need to be =< to hardware set endstop)
software_endstops = True
Xmaxrange = 65000
Ymaxrange = 100000
Fmaxrange = 27000

#Software Endstop that are active if focus is > safe_Fcs = avoid collision
#Set so that extended Focus axis can't collide with plate holder.
dynamic_endstops = True
soft_Xmax = 63000
soft_Xmin = 10000
soft_Ymax = 90000
soft_Ymin = 1550
safe_Fcs = 10000

#number of retry possible for motor command sent, 10 by default (normal error error rate should not exceed 2 in a row)
retry = 10
#number of retry possible for read position, 10 by default (normal error error rate should not exceed 2 in a row)
read_retry = 10

# I²C bus address, need to match the arduino adress specified in the arduino firmware:  "Wire.begin(addr);"
addr = 0x8 
ready_pin = 4

# physical controler parameters
Y_controler_steps = 10
X_controler_steps = 10
F_controler_steps = 1
sw_step_multiplier = 20

