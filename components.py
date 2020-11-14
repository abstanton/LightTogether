import RPi.GPIO as gpio
import time


class LED:
    def __init__(self, pin):
        self.pin = pin
        self.on = 0
        
        gpio.setup(self.pin, gpio.OUT)
        gpio.output(self.pin, self.on)

    def switch(self, value=-1):
        if value < 0:
            self.on = not self.on
        elif value in [0, 1]:
            self.on = value
        gpio.output(self.pin, self.on)
                
        
class Stepper:
    def __init__(self, pins, wait=0.001):
        self.pins = pins
        self.wait = wait
        
        for pin in self.pins:
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin, 0)

        self.halfstep_positive_seq = [[1, 0, 0, 0],
                                      [1, 1, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 1, 1, 0],
                                      [0, 0, 1, 0],
                                      [0, 0, 1, 1],
                                      [0, 0, 0, 1],
                                      [1, 0, 0, 1]]

        self.halfstep_negative_seq = [[0, 0, 0, 1],
                                      [0, 0, 1, 1],
                                      [0, 0, 1, 0],
                                      [0, 1, 1, 0],
                                      [0, 1, 0, 0],
                                      [1, 1, 0, 0],
                                      [1, 0, 0, 0],
                                      [1, 0, 0, 1]]


    def right(self, steps):
        for i in range(steps):
            for halfstep in range(len(self.halfstep_positive_seq)):
                for pin in range(len(self.pins)):
                    gpio.output(self.pins[pin], self.halfstep_positive_seq[halfstep][pin % 4])
                time.sleep(self.wait)
            
            
    def left(self, steps):
        for i in range(steps):
            for halfstep in range(len(self.halfstep_negative_seq)):
                for pin in range(len(self.pins)):
                    gpio.output(self.pins[pin], self.halfstep_negative_seq[halfstep][pin % 4])
                time.sleep(self.wait)


class Button:
    def __init__(self, pin):
        self.pressed = False
        self.pin = pin
        gpio.setup(self.pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        
    def isPressed(self):
        return gpio.input(self.pin) == gpio.HIGH

    def getNext(self):
        while(True):
            pressedCurr = self.isPressed()
            if self.pressed == pressedCurr:
                continue
            else:
                self.pressed = pressedCurr
                return self.pressed
