from .bot import BotController as _BotController
from typing import Callable as _Callable
from ctypes import CDLL

class Motor:
    """Motor object with core functionalities.

    Args:
        bot (BotController): An instance of the `BotController` object.
        port (int): Port of the motor.

    Attributes:
        k (CDLL): The kipr library object.
        port (int): Port of the motor.
    """
    k: CDLL
    port: int
    def __init__(self, bot: _BotController, port: int) -> None: ...
    def move_timed(self, velocity: int, time: int) -> None:
        """Drive the motor for a certain amount of time and then stop, while blocking proceeding synchronous processes.

        Args:
            velocity (int): Velocity of the motor, -1500 to 1500.
            time (int): Time in milliseconds.
        """
    def move_timed_async(self, velocity: int, time: int) -> None:
        """Drive the motor asynchronously for a certain amount of time and then stop.

        Args:
            velocity (int): Velocity of the motor, -1500 to 1500.
            time (int): Time in milliseconds.
        """
    def move(self, velocity: int) -> None:
        """Set the motor to drive at a certain velocity.

        Args:
            velocity (int): Velocity of the motor, -1500 to 1500.
        """
    def move_until(self, velocity: int, continuing_condition: _Callable[..., bool], continuing_condition_args: tuple = ()) -> None:
        """Move the motor synchronously while a condition is true, and then stops.

        Args:
            velocity (int): Velocity of the motor, -1500 to 1500.
            continuing_condition (_Callable[..., bool]): A function or lambda that returns a truthy value until the motor is supposed to stop.
            continuing_condition_args (Optional[tuple], optional): Argument(s) for the continuing_condition function as an ordered tuple. Defaults to ()). 
        """
    def get_position_counter(self) -> int:
        """Get the current position counter of the motor.

        Returns:
            int: The current position counter of the motor.
        """
    def clear_position_counter(self) -> None:
        """Clear the position counter of the motor.
        """
    def off(self) -> None:
        """Turn off the motor.
        """
    def stop(self) -> None:
        """Hard stop the motor's movement.
        """
