"""
This module is not a top level import to prevent name confusion with Create modules.
"""

from .motor import Motor as _Motor
from .bot import BotController as _BotController
from typing import Callable as _Callable, Any as _Any
from functools import wraps as _wraps
import time as _time


def timeit(func: _Callable[[_Any], _Any]):
    """Utility decorator for printing the execution time of a function.

    Args:
        func (Callable): Function to be called and timed.
    """
    @_wraps(func)
    def timeit_wrapper(*args, **kwargs) -> _Any:
        start_time = _time.perf_counter()
        result = func(*args, **kwargs)
        end_time = _time.perf_counter()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:.4f} seconds to execute.")
        return result
    return timeit_wrapper

def create_motors_drive_timed_function(bot: _BotController, motor1: _Motor, motor2: _Motor) -> _Callable[[int, int, int], None]:
    """Create a function to drive two motors for a certain amount of time and then stop, while blocking proceeding synchronous processes.

    Args:
        bot (BotController): ready_string
        motor1 (Motor): `Motor` object of the first motor.
        motor2 (Motor): `Motor` object of the second motor.

    Returns:
        Callable[[int, int, int], None]: A function that drives the two motors for a certain amount of time and then stop, while blocking proceeding synchronous processes.
    """
    def drive_timed(motor1_velocity: int, motor2_velocity: int, time: int) -> None: 
        """Drive the motors for a certain amount of time and then stop, while blocking proceeding synchronous processes.

        Args:
            motor1_velocity (int): Velocity of motor1, -1500 to 1500.
            motor2_velocity (int): Velocity of motor2, -1500 to 1500.
            time (int): Time in milliseconds.
        """
        motor1.move(motor1_velocity)
        motor2.move(motor2_velocity)
        bot.k.msleep(time)
        motor1.stop()
        motor2.stop()
    return drive_timed

def create_motors_drive_timed_async_function(bot: _BotController, motor1: _Motor, motor2: _Motor) -> _Callable[[int, int, int], None]:
    """Create a function to drive two motors asynchronously for a certain amount of time and then stop.

    Args:
        bot (BotController): An instance of the `BotController` object.
        motor1 (Motor): `Motor` object of the first motor.
        motor2 (Motor): `Motor` object of the second motor.

    Returns:
        Callable[[int, int, int], None]: A function that drives the two motors asynchronously for a certain amount of time and then stop.
    """
    def drive_timed_async(motor1_velocity: int, motor2_velocity: int, time: int) -> None:
        """Drive the motors asynchronously for a certain amount of time and then stop.

        Args:
            motor1_velocity (int): Velocity of motor1, -1500 to 1500.
            motor2_velocity (int): Velocity of motor2, -1500 to 1500.
            time (int): Time in milliseconds.
        """
        motor1.move_timed_async(motor1_velocity, time)
        motor2.move_timed_async(motor2_velocity, time)
    return drive_timed_async

def create_motors_drive_function(bot: _BotController, motor1: _Motor, motor2: _Motor) -> _Callable[[int, int], None]:
    """Create a function to set two motors to drive at a certain velocity.

    Args:
        bot (BotController): An instance of the `BotController` object.
        left_motor (Motor): `Motor` object of the first motor.
        right_motor (Motor): `Motor` object of the second motor.

    Returns:
        Callable[[int, int], None]: A function that set the two motors to drive at a certain velocity.
    """
    def drive(motor1_velocity: int, motor2_velocity: int) -> None:
        """Set the motor to drive at a certain velocity.

        Args:
            motor1_velocity (int): Velocity of motor1, -1500 to 1500.
            motor2_velocity (int): Velocity of motor2, -1500 to 1500.
        """
        motor1.move(motor1_velocity)
        motor2.move(motor2_velocity)
    return drive

def create_motors_drive_until_function(bot: _BotController, motor1: _Motor, motor2: _Motor) -> _Callable[[int, int, _Callable[..., bool], tuple], None]:
    """Create a function to move the two motors synchronously while a condition is true, and then stops.

    Args:
        bot (_BotController): An instance of the `BotController` object.
        motor1 (_Motor): `Motor` object of the first motor.
        motor2 (_Motor): `Motor` object of the second motor.

    Returns:
        _Callable[[int, int, _Callable[..., bool], tuple], None]: _description_
    """
    def drive_until(motor1_velocity: int, motor2_velocity: int, continuing_condition: _Callable[..., bool], continuing_condition_args: tuple = ()) -> None:
        """Move the motors synchronously while a condition is true, and then stops.

        Args:
            motor1_velocity (int): Velocity of motor1, -1500 to 1500.
            motor2_velocity (int): Velocity of motor2, -1500 to 1500.
            continuing_condition (Callable[..., bool]): A function or lambda that returns a truthy value until the motors are supposed to stop.
            continuing_condition_args (Optional[tuple], optional): Argument(s) for the continuing_condition function as an ordered tuple. Defaults to ()).
        """
        motor1.move(motor1_velocity)
        motor2.move(motor2_velocity)
        while continuing_condition(*continuing_condition_args):
            continue
        motor1.stop()
        motor2.stop()
    return drive_until