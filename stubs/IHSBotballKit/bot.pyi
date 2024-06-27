from .motor import Motor as _Motor
from .sensor import Sensor as _Sensor, SensorType as _SensorType
from .servo import Servo as _Servo
from ctypes import CDLL

class BotController:
    """Bot object that contains the kipr library and wrappers for basic components.
    
    Args:
        libkipr_path (str | None, optional): Path of the libkipr shared object. Defaults to /usr/local/lib/libkipr.so.

    Attributes:
        k (CDLL): The kipr library object.
    """
    k: CDLL
    def __init__(self, libkipr_path: str | None = None) -> None: ...
    def wait_for_light(self, light_port: int, reset_file_path: str) -> None:
        """Wait for light using the light sensor at the start of the round.

        Args:
            light_port (int): Port number of the light sensor.
            reset_file_path (str): File path of the 'reset' program. Leave as empty string if not applicable.
        """
    def shut_down_in(self, seconds: float) -> None:
        """Terminate the program and stop robot in set amount of time.

        Args:
            seconds (float): Amount of time in seconds.
        """
    def enable_all_servos(self) -> None:
        """Enables all servo ports.
        """
    def disable_all_servos(self) -> None:
        """Disables all servo ports.
        """
    def stop_all_motors(self) -> None:
        """Stops all motors.
        """
    def create_servo(self, port: int, default_enable: bool = True) -> _Servo:
        """A wrapper for the Servo class.

        Args:
            port (int): Port of the servo.
            default_enable (bool, optional): Whether to immediately enable the servo upon instantiation. Defaults to True.

        Returns:
            Servo: A Servo object.
        """
    def create_motor(self, port: int) -> _Motor:
        """A wrapper for the Motor class.

        Args:
            port (int): Port of the motor.

        Returns:
            Motor: A Motor object.
        """
    def create_sensor(self, sensor_type: _SensorType, port: int) -> _Sensor:
        """A wrapper for the Sensor class.

        Args:
            sensor_type (SensorType): Type of the sensor (ANALOG or DIGITAL) using the `SensorType` enum from the sensor module.
            port (int): Port of the sensor.

        Returns:
            Sensor: A Sensor object.
        """
