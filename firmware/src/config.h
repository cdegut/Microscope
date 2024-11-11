#pragma once

#define XdirPin 9
#define XstepPin 8
#define XDiagPin 6
#define XEnPin 7
#define X_DRIVER_ADDRESS 0b10 // TMC2209 Driver address according to MS1 and MS2
#define Xfastspd 200
#define Xslowspd 400
#define XmicroStep 8
#define XSg_sensitivity_initial 70
#define XSg_autoeval_divider 2.8 
#define X_0offset 7500 // Offset from true 0

#define YdirPin 2
#define YstepPin 3
#define YDiagPin 5
#define YEnPin 4
#define Y_DRIVER_ADDRESS 0b01 // TMC2209 Driver address according to MS1 and MS2
#define Yfastspd 200
#define Yslowspd 400
#define YmicroStep 8
#define YSg_sensitivity_initial 70
#define YSg_autoeval_divider 2.5

#define FdirPin D14
#define FstepPin 15
#define FDiagPin 16
#define FEnPin D13
#define F_DRIVER_ADDRESS 0b11 // TMC2209 Driver address according to MS1 and MS2
#define Ffastspd 200
#define Fslowspd 600
#define FmicroStep 8
#define FSg_sensitivity_initial 70
#define FSg_autoeval_divider 2.8

#define Led1Pin 11
#define Led2Pin 10
#define ReadyPin 17U

#define NeoPixelPin 12
#define NeoPixelCount 16


#define R_SENSE 0.11f // Match to your driver



