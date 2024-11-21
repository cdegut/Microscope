from dataclasses import dataclass

@dataclass
class LED:
    index: int = 0 
    R: int = 0
    G: int = 0
    B: int = 0

class LEDArray:
    def __init__(self, R=0,G=0,B=0, num = 16):
        self.leds = [LED(i, R,G,B) for i in range(num)]
    def half(self,R,G,B, start: int=0):
        for led in self.leds[start:start + len(self.leds)/2]:
            led.R , led.G , led.B = R,G,B
    def quarter(self,R,G,B, start:int =0):
        for led in self.leds[start:start + int(len(self.leds)/4)]:
            led.R , led.G , led.B = R,G,B



array = LEDArray(128,52,12)
array.quarter(128,0,0)
