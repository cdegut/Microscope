# microcontrol
Software for the microscope
Works on raspberypi os bulseye

# Raspbery pi config in /boot/config.txt
```
# activate I2C interface
dtparam=i2c_arm=on
# Clock stretching by slowing down to 10KHz
dtparam=i2c_arm_baudrate=10000
gpu_mem=256
```

# Package needed

pip install smbus2

# Misc
Strongly suggest to increase the size of the Swap file