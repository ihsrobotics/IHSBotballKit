import threading
from roomba_drive import *
from IHSBotballKit.auxiliary.servo import Servo

class Sweeper:
    def __init__(self, sweeper_servo: Servo):
        self.is_sweeping = False
        self.sweeper_servo = sweeper_servo
    
    def sweep_right(self):
        if self.is_sweeping: return
        self.is_sweeping = True
        self.sweeper_servo.set_position(SWEEPER_RIGHT)
        self.sweeper_servo.k.msleep(500)
        self.is_sweeping = False
    
    def sweep_left(self):
        if self.is_sweeping: return
        self.is_sweeping = True
        self.sweeper_servo.set_position(SWEEPER_LEFT)
        self.sweeper_servo.k.msleep(500)
        self.is_sweeping = False

    def sweep(self):
        if self.sweeper_servo.get_position() == SWEEPER_LEFT:
            self.sweeper_right()
            self.sweeper_left()
        elif self.sweeper_servo.get_position() == SWEEPER_RIGHT:
            self.sweep_left()
            self.sweep_right()
        else:
            self.sweep_left()

    def sweep_async(self):
        if self.is_sweeping: return
        t = threading.Thread(target = self.sweep)
        t.start()
        t.join()
        return t

    def sweep_center(self):
        self.sweeper_servo.set_position(SWEEPER_CENTER)
    
    def sweep_loop(self):
        pass
