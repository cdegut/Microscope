#Software Endstop (need to be =< to hardware set endstop)
software_endstops = True
Xmaxrange = 70000
Ymaxrange = 93000
Fmaxrange = 30000

overshoot_X = -16
undershoot_X = -4
overshoot_Y = -100
undershoot_Y = +40

#fluorescent gain value
awbR_fluo = 1
awbB_fluo = 0.35
awbR_white = 3
awbB_white = 0.8

#number of retry possible for motor command sent, 10 by default (normal error error rate should not exceed 2 in a row)
retry = 10
#number of retry possible for read position, 10 by default (normal error error rate should not exceed 2 in a row)
read_retry = 10



# I²C bus address, need to match the arduino address specified in the arduino firmware:  "Wire.begin(addr);"
addr = 0x8 
ready_pin = 4

Y_controller_short = 10
X_controller_short = 10
F_controller_short = 1

Y_controller_long = 100
X_controller_long = 100
F_controller_long = 10

Y_controller_pinA = 19
Y_controller_pinB = 16
Y_controller_Switch = 13
X_controller_pinA = 26
X_controller_pinB = 20
X_controller_Switch = 21
F_controller_pinA = 6
F_controller_pinB = 12
F_controller_Switch = 5


#Preview window size
preview_resolution = (800, 600)