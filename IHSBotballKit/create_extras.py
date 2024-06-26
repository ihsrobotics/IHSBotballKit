"""
This module is not a top level import to prevent name confusion with other Create and motor modules.
"""

from .create import Create as _Create
from .sensor import Sensor as _Sensor
from .controller import CreateSensorController as _CreateSensorController, LessThan as _LessThan, GreaterThan as _GreaterThan, SensorController as _SensorController, IsFalse as _IsFalse, IsTrue as _IsTrue
from typing import Callable as _Callable

def align_to_line(create: _Create, left_speed: int, right_speed: int, left_sensor: int, right_sensor: int, threshold: int) -> None:
    """Align to the front side of a tape by driving to it from white.

    Args:
        create (Create): An instance of the `Create` object.
        left_speed (int): Speed of the left wheel, -500 to 500.
        right_speed (int): Speed of the right wheel, -500 to 500.
        left_sensor (int): Left Create sensor to be used for alignment, specified using the `CreateSensor` enum.
        right_sensor (int): Right Create sensor to be used for alignment, specified using the `CreateSensor` enum.
        threshold (int): Threshold between white and tape color.
    """
    left_on_white = _CreateSensorController(create, left_sensor, _LessThan(threshold))
    right_on_white = _CreateSensorController(create, right_sensor, _LessThan(threshold))
    create.drive_until(left_speed, right_speed, lambda: left_on_white.get_status() and right_on_white.get_status())
    for _ in range(2):
        create.drive_until(left_speed, 0, lambda: left_on_white.get_status())
        create.drive_until(0, right_speed, lambda: right_on_white.get_status())
    create.stop()
    
def align_to_line_white(create: _Create, left_speed: int, right_speed: int, left_sensor: int, right_sensor: int, threshold: int) -> None:
    """Align to the back side of a tape by driving to it from black (already on the tape).

    Args:
        create (Create): An instance of the `Create` object.
        left_speed (int): Speed of the left wheel, -500 to 500.
        right_speed (int): Speed of the right wheel, -500 to 500.
        left_sensor (int): Left Create sensor to be used for alignment, specified using the `CreateSensor` enum.
        right_sensor (int): Right Create sensor to be used for alignment, specified using the `CreateSensor` enum.
        threshold (int): Threshold between white and tape color.
    """
    left_on_black = _CreateSensorController(create, left_sensor, _GreaterThan(threshold))
    right_on_black = _CreateSensorController(create, right_sensor, _GreaterThan(threshold))
    create.drive_until(left_speed, right_speed, lambda: left_on_black.get_status() and right_on_black.get_status())
    for _ in range(2):
        create.drive_until(left_speed, 0, lambda: left_on_black.get_status())
        create.drive_until(0, right_speed, lambda: right_on_black.get_status())
    create.stop()
    
def drive_until_create_sensor(create: _Create, left_speed: int, right_speed: int, sensor: int, threshold: _LessThan | _GreaterThan) -> None:
    """Drive the Create until a specified value is reached on a certain Create sensor.

    Args:
        create (Create): An instance of the `Create` object.
        left_speed (int): Speed of the left wheel, -500 to 500.
        right_speed (int): Speed of the right wheel, -500 to 500.
        sensor (int): Create sensor specified using the `CreateSensor` enum.
        threshold (LessThan | GreaterThan): A LessThan or GreaterThan object to compare a target sensor value.
    """
    sensor_controller = _CreateSensorController(create, sensor, threshold)
    create.drive_until(left_speed, right_speed, lambda: sensor_controller.get_status())
    
def drive_until_sensor(create: _Create, left_speed: int, right_speed: int, sensor: _Sensor, threshold: _LessThan | _GreaterThan | _IsFalse | _IsTrue) -> None:
    """Drive the Create until a specified value is reached on a certain analog or digital sensor.

    Args:
        create (Create): An instance of the `Create` object.
        left_speed (int): Speed of the left wheel, -500 to 500.
        right_speed (int): Speed of the right wheel, -500 to 500.
        sensor (Sensor): The Sensor object that represents the robot sensor.
        threshold (LessThan | GreaterThan | IsFalse | IsTrue): A LessThan or GreaterThan or IsFalse or IsTrue object to compare a target sensor value.
    """
    sensor_controller = _SensorController(sensor, threshold)
    create.drive_until(left_speed, right_speed, lambda: sensor_controller.get_status())

def line_follow_left_once(create: _Create, slow_speed: int, fast_speed: int, sensor_on_black_controller: _SensorController | _CreateSensorController) -> None:
    """Perform one iteration of line follow on the left side of the tape.

    Args:
        create (Create): An instance of the `Create` object.
        slow_speed (int): Speed of the slower wheel.
        fast_speed (int): Speed of the faster wheel for correction.
        sensor_on_black_controller (SensorController | CreateSensorController): A SensorController or CreateSensorController for whether the sensor is on the tape.
    """
    if sensor_on_black_controller.get_status():
        create.drive(fast_speed, slow_speed)
    else:
        create.drive(slow_speed, fast_speed)
        
def line_follow_right_once(create: _Create, slow_speed: int, fast_speed: int, sensor_on_black_controller: _SensorController | _CreateSensorController) -> None:
    """Perform one iteration of line follow on the right side of the tape.

    Args:
        create (Create): An instance of the `Create` object.
        slow_speed (int): Speed of the slower wheel.
        fast_speed (int): Speed of the faster wheel for correction.
        sensor_on_black_controller (SensorController | CreateSensorController): A SensorController or CreateSensorController for whether the sensor is on the tape.
    """
    if sensor_on_black_controller.get_status():
        create.drive(slow_speed, fast_speed)
    else:
        create.drive(fast_speed, slow_speed)
        
def line_follow_left_using_create_sensor_until(create: _Create, slow_speed: int, fast_speed: int, sensor: int, threshold: int, continuing_condition: _Callable[..., bool]) -> None:
    """Line follow on the left side of the tape using a specified Create sensor while a condition is true.

    Args:
        create (Create): An instance of the `Create` object.
        slow_speed (int): Speed of the slower wheel.
        fast_speed (int): Speed of the faster wheel for correction.
        sensor (int): The specific Create sensor to use, specified using the `CreateSensor` enum.
        threshold (int): Threshold between white and tape color.
        continuing_condition (_Callable[..., bool]): A function or lambda that returns a truthy value until the line follow is supposed to stop.
    """
    sensor_on_black_controller = _CreateSensorController(create, sensor, _GreaterThan(threshold))
    while continuing_condition():
        line_follow_left_once(create, slow_speed, fast_speed, sensor_on_black_controller)
    create.stop()
    
def line_follow_left_using_sensor_until(create: _Create, slow_speed: int, fast_speed: int, sensor: _Sensor, threshold: int, continuing_condition: _Callable[..., bool]) -> None:
    """Line follow on the left side of the tape using a specified Create sensor while a condition is true.

    Args:
        create (Create): An instance of the `Create` object.
        slow_speed (int): Speed of the slower wheel.
        fast_speed (int): Speed of the faster wheel for correction.
        sensor (Sensor): The Sensor object that represents the robot sensor used for line follow.
        threshold (int): Threshold between white and tape color.
        continuing_condition (_Callable[..., bool]): A function or lambda that returns a truthy value until the line follow is supposed to stop.
    """
    sensor_on_black_controller = _SensorController(sensor, _LessThan(threshold))
    while continuing_condition():
        line_follow_left_once(create, slow_speed, fast_speed, sensor_on_black_controller)
    create.stop()
        
def line_follow_right_using_create_sensor_until(create: _Create, slow_speed: int, fast_speed: int, sensor: int, threshold: int, continuing_condition: _Callable[..., bool]) -> None:
    """Line follow on the right side of the tape using a specified Create sensor while a condition is true.

    Args:
        create (Create): An instance of the `Create` object.
        slow_speed (int): Speed of the slower wheel.
        fast_speed (int): Speed of the faster wheel for correction.
        sensor (int): The specific Create sensor to use, specified using the `CreateSensor` enum.
        threshold (int): Threshold between white and tape color.
        continuing_condition (_Callable[..., bool]): A function or lambda that returns a truthy value until the line follow is supposed to stop.
    """
    sensor_on_black_controller = _CreateSensorController(create, sensor, _GreaterThan(threshold))
    while continuing_condition():
        line_follow_right_once(create, slow_speed, fast_speed, sensor_on_black_controller)
    create.stop()
    
def line_follow_right_using_sensor_until(create: _Create, slow_speed: int, fast_speed: int, sensor: _Sensor, threshold: int, continuing_condition: _Callable[..., bool]) -> None:
    """Line follow on the right side of the tape using a specified Create sensor while a condition is true.

    Args:
        create (Create): An instance of the `Create` object.
        slow_speed (int): Speed of the slower wheel.
        fast_speed (int): Speed of the faster wheel for correction.
        sensor (Sensor): The Sensor object that represents the robot sensor used for line follow.
        threshold (int): Threshold between white and tape color.
        continuing_condition (_Callable[..., bool]): A function or lambda that returns a truthy value until the line follow is supposed to stop.
    """
    sensor_on_black_controller = _SensorController(sensor, _LessThan(threshold))
    while continuing_condition():
        line_follow_right_once(create, slow_speed, fast_speed, sensor_on_black_controller)
    create.stop()    
