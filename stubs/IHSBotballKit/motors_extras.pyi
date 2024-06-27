from .bot import BotController as _BotController
from .motor import Motor as _Motor
from typing import Any as _Any, Callable as _Callable

def timeit(func: _Callable[[_Any], _Any]):
    """Utility decorator for printing the execution time of a function.

    Args:
        func (Callable): Function to be called and timed.
    """
def create_motors_drive_timed_function(bot: _BotController, motor1: _Motor, motor2: _Motor) -> _Callable[[int, int, int], None]:
    """Create a function to drive two motors for a certain amount of time and then stop, while blocking proceeding synchronous processes.

    Args:
        bot (BotController): ready_string
        motor1 (Motor): `Motor` object of the first motor.
        motor2 (Motor): `Motor` object of the second motor.

    Returns:
        Callable[[int, int, int], None]: A function that drives the two motors for a certain amount of time and then stop, while blocking proceeding synchronous processes.
    """
def create_motors_drive_timed_async_function(bot: _BotController, motor1: _Motor, motor2: _Motor) -> _Callable[[int, int, int], None]:
    """Create a function to drive two motors asynchronously for a certain amount of time and then stop.

    Args:
        bot (BotController): An instance of the `BotController` object.
        motor1 (Motor): `Motor` object of the first motor.
        motor2 (Motor): `Motor` object of the second motor.

    Returns:
        Callable[[int, int, int], None]: A function that drives the two motors asynchronously for a certain amount of time and then stop.
    """
def create_motors_drive_function(bot: _BotController, motor1: _Motor, motor2: _Motor) -> _Callable[[int, int], None]:
    """Create a function to set two motors to drive at a certain velocity.

    Args:
        bot (BotController): An instance of the `BotController` object.
        left_motor (Motor): `Motor` object of the first motor.
        right_motor (Motor): `Motor` object of the second motor.

    Returns:
        Callable[[int, int], None]: A function that set the two motors to drive at a certain velocity.
    """
def create_motors_drive_until_function(bot: _BotController, motor1: _Motor, motor2: _Motor) -> _Callable[[int, int, _Callable[..., bool], tuple], None]:
    """Create a function to move the two motors synchronously while a condition is true, and then stops.

    Args:
        bot (_BotController): An instance of the `BotController` object.
        motor1 (_Motor): `Motor` object of the first motor.
        motor2 (_Motor): `Motor` object of the second motor.

    Returns:
        _Callable[[int, int, _Callable[..., bool], tuple], None]: _description_
    """
