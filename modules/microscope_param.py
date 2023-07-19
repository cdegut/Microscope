#Software Endstop (need to be =< to hardware set endstop)
software_endstops = True
Xmaxrange = 65000
Ymaxrange = 100000
Fmaxrange = 22000

#number of retry possible for motor command sent, 10 by default (normal error error rate should not exceed 2 in a row)
retry = 10
#number of retry possible for read position, 10 by default (normal error error rate should not exceed 2 in a row)
read_retry = 10

# I²C bus address, need to match the arduino adress specified in the arduino firmware:  "Wire.begin(addr);"
addr = 0x8 
ready_pin = 4

# physical controler parameters max value is 128
Y_controler_short = 10
X_controler_short = 10
F_controler_short = 1

Y_controler_long = 100
X_controler_long = 100
F_controler_long = 10
