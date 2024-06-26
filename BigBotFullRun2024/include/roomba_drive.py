from configs_loader import *

from IHSBotballKit import Sensor, Create, CreateSensor, CreateSensorController, ControllerType, SensorController, TimeController
from typing import Callable, Any

def drive_to_line(create: Create, left_speed: int, right_speed: int, left_sensor: CreateSensor = CreateSensor.LEFT_FRONT_CLIFF, right_sensor: CreateSensor = CreateSensor.RIGHT_FRONT_CLIFF) -> None:
    left_on_white = CreateSensorController(create, left_sensor, BLACK, ControllerType.GREATER_THAN_CONTROLLER)
    right_on_white = CreateSensorController(create, right_sensor, BLACK, ControllerType.GREATER_THAN_CONTROLLER)
    create.drive_until(left_speed, right_speed, lambda: left_on_white.get_status() and right_on_white.get_status())
    for i in range(2):
        create.drive_until(left_speed, 0, lambda: left_on_white.get_status())
        create.drive_until(0, right_speed, lambda: right_on_white.get_status())
    create.stop()

def drive_to_line_white(create: Create, left_speed: int, right_speed: int, left_sensor: CreateSensor, right_sensor: CreateSensor) -> None:
    left_on_black = CreateSensorController(create, left_sensor, BLACK, ControllerType.LESS_THAN_CONTROLLER)
    right_on_black = CreateSensorController(create, right_sensor, BLACK, ControllerType.LESS_THAN_CONTROLLER)
    create.drive_until(left_speed, right_speed, lambda: left_on_black.get_status() and right_on_black.get_status())
    for i in range(2):
        create.drive_until(left_speed, 0, lambda: left_on_black.get_status())
        create.drive_until(0, right_speed, lambda: right_on_black.get_status())
    create.stop()

# must must greater than controller for black
def line_follow_left(create: Create, sensor_on_black: SensorController, slow_speed: int, fast_speed: int) -> None:
    if sensor_on_black.get_status():
        create.drive(fast_speed, slow_speed)
    else: 
        create.drive(slow_speed, fast_speed)

# must use greater than controller for black
def line_follow_right(create: Create, sensor_on_black: SensorController, slow_speed: int, fast_speed: int) -> None:
    if sensor_on_black.get_status():
        create.drive(slow_speed, fast_speed)
    else: 
        create.drive(slow_speed, fast_speed)

def line_follow_sensor(create: Create, sensor: Sensor, continue_condition: Callable[..., bool], slow_speed: int = -100, fast_speed: int = -125) -> None:
    sensor_on_black = SensorController(sensor, SWEEPER_BLACK, ControllerType.GREATER_THAN_CONTROLLER)
    while continue_condition():
        line_follow_left(create, sensor_on_black, slow_speed, fast_speed)
    create.stop()

def line_follow_time(create: Create, sensor: Sensor, duration: int, slow_speed: int = -100, fast_speed: int = -125) -> None:
    time_controller = TimeController(duration)
    line_follow_sensor(create, sensor, time_controller.get_status, slow_speed, fast_speed)

def sensor_align_white(create: Create, sensor: Sensor, sensor_thresh: int, left_speed: int, right_speed: int) -> None:
    # true for greater than white
    sensor_on_black = SensorController(sensor, sensor_thresh, ControllerType.GREATER_THAN_CONTROLLER)
    create.drive_until(left_speed, right_speed, sensor_on_black.get_status)

def sensor_align_black(create: Create, sensor: Sensor, sensor_thresh: int, left_speed: int, right_speed: int) -> None:
    # true for less than black
    sensor_on_white = SensorController(sensor, sensor_thresh, ControllerType.LESS_THAN_CONTROLLER)
    create.drive_until(left_speed, right_speed, sensor_on_white.get_status)
