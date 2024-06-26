from __future__ import annotations as _annotations
from ctypes import CDLL as _CDLL
import time as _time
import os as _os
import signal as _signal
import threading as _threading

class BotController:
    """Bot object that contains the kipr library and wrappers for basic components.
    
    Args:
        libkipr_path (str | None, optional): Path of the libkipr shared object. Defaults to /usr/local/lib/libkipr.so.

    Attributes:
        k (CDLL): The kipr library object.
    """
    def __init__(self, libkipr_path: str | None = None) -> None:
        path = libkipr_path if libkipr_path is not None else "/usr/local/lib/libkipr.so"
        self.k: _CDLL = _CDLL(path)

    def wait_for_light(self, light_port: int, reset_file_path: str) -> None:
        """Wait for light using the light sensor at the start of the round.

        Args:
            light_port (int): Port number of the light sensor.
            reset_file_path (str): File path of the 'reset' program. Leave as empty string if not applicable.
        """
        _IHSRunner(self, light_port, reset_file_path)

    def shut_down_in(self, seconds: float) -> None:
        """Terminate the program and stop robot in set amount of time.

        Args:
            seconds (float): Amount of time in seconds.
        """
        def terminate():
            _time.sleep(seconds)
            _os.kill(_os.getpid(), _signal.SIGTERM)
        terminator_thread = _threading.Thread(target=terminate)
        terminator_thread.daemon = True
        terminator_thread.start()

    def enable_all_servos(self) -> None:
        """Enables all servo ports.
        """
        self.k.enable_servos()

    def disable_all_servos(self) -> None:
        """Disables all servo ports.
        """
        self.k.disable_servos()

    def stop_all_motors(self) -> None:
        """Stops all motors.
        """
        self.k.ao()

    def create_servo(self, port: int, default_enable: bool = True) -> _Servo:
        """A wrapper for the Servo class.

        Args:
            port (int): Port of the servo.
            default_enable (bool, optional): Whether to immediately enable the servo upon instantiation. Defaults to True.

        Returns:
            Servo: A Servo object.
        """
        return _Servo(self, port, default_enable)

    def create_motor(self, port: int) -> _Motor:
        """A wrapper for the Motor class.

        Args:
            port (int): Port of the motor.

        Returns:
            Motor: A Motor object.
        """
        return _Motor(self, port)

    def create_sensor(self, sensor_type: int, port: int) -> _Sensor:
        """A wrapper for the Sensor class.

        Args:
            sensor_type (int): Type of the sensor (ANALOG or DIGITAL) using the `SensorType` enum from the sensor module.
            port (int): Port of the sensor.

        Returns:
            Sensor: A Sensor object.
        """
        return _Sensor(self, sensor_type, port)
        

from .motor import Motor as _Motor
from .sensor import Sensor as _Sensor, SensorType as _SensorType
from .servo import Servo as _Servo
from .runner import IHSRunner as _IHSRunner
