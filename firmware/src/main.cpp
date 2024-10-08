#include "main.h"

PwmOut Led1(Led1Pin);
PwmOut Led2(Led2Pin);

Stepstick X(XstepPin, XdirPin, XEnPin); 
TMC2209Stepper X_driver(&Serial1, R_SENSE, X_DRIVER_ADDRESS);

Stepstick Y(YstepPin, YdirPin, YEnPin); 
TMC2209Stepper Y_driver(&Serial1, R_SENSE, Y_DRIVER_ADDRESS);

Stepstick Focus(FstepPin, FdirPin, FEnPin); 
TMC2209Stepper F_driver(&Serial1, R_SENSE, F_DRIVER_ADDRESS);

CRGBArray<NeoPixelCount> NeoPixel;


//Adafruit_NeoPixel strip(NeoPixelCount, NeoPixelPin,  NEO_GRB + NEO_KHZ800);

long timer;

void setup() {
  

  Serial.begin(250000);
  Serial1.begin(115200);

  pinMode(ReadyPin, OUTPUT);
  FastLED.addLeds<WS2812, NeoPixelPin, GRB>(NeoPixel, NeoPixelCount);


  neopixelSolidColour(64,0,0);
  delay(500); // avoid low crrent on RPi

  #ifdef DEBUG_HOMING
    while (!Serial) {;} //wait for serial for debugging
  #endif

  X.begin();
  X.setup_TMC(&X_driver, XmicroStep, X_current);
  X.setup_stallguard(XDiagPin, XSg_sensitivity_initial);
  X.config_coolstep();          
  X.config_speed(Xslowspd,Xfastspd);
  delay(500); // avoid low crrent on RPi

  Y.begin();
  Y.setup_TMC(&Y_driver, YmicroStep, Y_current);
  Y.setup_stallguard(YDiagPin, YSg_sensitivity_initial);
  Y.config_coolstep();          
  Y.config_speed(Yslowspd,Yfastspd);
  delay(500); // avoid low crrent on RPi

  Focus.begin();
  Focus.setup_TMC(&F_driver, FmicroStep, F_current);
  Focus.setup_stallguard(FDiagPin, FSg_sensitivity_initial);
  Focus.config_coolstep();          
  Focus.config_speed(Fslowspd,Ffastspd);
  delay(500); // avoid low crrent on RPi

  home_XYF(4000);

  timer = millis();

  X.motion_planner(1000);
  Y.motion_planner(1000);
  Focus.motion_planner(1000);
  run_loop(X,Y,Focus);
  X.override_position(0); //apply the offset

  //I2C set up
  Wire.begin(0x8); // I2C interface at adress 0x08
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  Led1.begin(40000.0f, 0.0f);
  Led2.begin(40000.0f, 0.0f);
  neopixelSolidColour(0,0,0);

}


void loop() {

    X.run();
    Y.run();
    Focus.run();

    if ( (X.get_state() == OFF) && (Y.get_state() == OFF) && (Focus.get_state() == OFF)) {
      digitalWrite(ReadyPin, HIGH);
    }
    else {
       digitalWrite(ReadyPin, LOW);
    }

    delayMicroseconds(1);
} 
