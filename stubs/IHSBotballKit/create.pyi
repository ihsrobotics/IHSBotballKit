import enum as _enum
from .bot import BotController as _BotController
from typing import Callable as _Callable
from ctypes import CDLL

class CreateSensor(_enum.Enum):
    """Enum for the build-in sensors on the Create.
    """
    LEFT_CLIFF: int
    LEFT_FRONT_CLIFF: int
    RIGHT_CLIFF: int
    RIGHT_FRONT_CLIFF: int
    FURTHEST_LEFT_DISTANCE: int
    MIDDLE_LEFT_DISTANCE: int
    FORWARD_LEFT_DISTANCE: int
    FURTHEST_RIGHT_DISTANCE: int
    MIDDLE_RIGHT_DISTANCE: int
    FORWARD_RIGHT_DISTANCE: int
    LEFT_BUMP: int
    RIGHT_BUMP: int

class Create:
    """Create object with core functionalities.
    
    Args:
        bot (BotController): An instance of the `BotController` object.
        retry_attempts (int): How many attempts to connect to the Create before throwing an exception.
        
    Raises:
        Exception: Failed to connect to Create.
        
    Attributes:
        k (CDLL): The kipr library object.    
    """
    k: CDLL
    def __init__(self, bot: _BotController, retry_attempts: int = 5) -> None: ...
    def drive(self, left_speed: int, right_speed: int) -> None:
        """Set the Create to drive at a certain speed.

        Args:
            left_speed (int): Speed of the left wheel, -500 to 500.
            right_speed (int): Speed of the right wheel, -500 to 500.
        """
    def drive_timed(self, left_speed: int, right_speed: int, time: int) -> None:
        """Drive the Create for a certain amount of time and then stop, while blocking proceeding synchronous operations.

        Args:
            left_speed (int): Speed of the left wheel, -500 to 500.
            right_speed (int): Speed of the right wheel, -500 to 500.
            time (int): Time in milliseconds.
        """
    def drive_timed_async(self, left_speed: int, right_speed: int, time: int) -> None:
        """Drive the Create asynchronously for a certain amount of time and then stop.

        Args:
            left_speed (int): Speed of the left wheel, -500 to 500.
            right_speed (int): Speed of the right wheel, -500 to 500.
            time (int): Time in milliseconds.
        """
    def stop(self) -> None:
        """Stop the Create.
        """
    def drive_until(self, left_speed: int, right_speed: int, continuing_condition: _Callable[..., bool], continuing_condition_args: tuple = ()) -> None:
        """Drive the Create synchronously while a condition is true, and then stops.

        Args:
            left_speed (int): Speed of the left wheel, -500 to 500.
            right_speed (int): Speed of the right wheel, -500 to 500.
            continuing_condition (_Callable[..., _Any]): A function or lambda that returns a truthy value until the Create is supposed to stop. 
            continuing_condition_args (Optional[tuple], optional): Argument(s) for the continuing_condition function as an ordered tuple. Defaults to ()).
        """
    def get_left_cliff(self) -> int:
        """Get the value of the left cliff sensor.

        Returns:
            int: Value of the left cliff sensor.
        """
    def get_left_front_cliff(self) -> int:
        """Get the value of the left front cliff sensor.

        Returns:
            int: Value of the left front cliff sensor.
        """
    def get_right_cliff(self) -> int:
        """Get the value of the right cliff sensor.

        Returns:
            int: Value of the right cliff sensor.
        """
    def get_right_front_cliff(self) -> int:
        """Get the value of the right front cliff sensor.

        Returns:
            int: Value of the right front cliff sensor.
        """
    def get_furthest_left_distance(self) -> int:
        """Get the value of the furthest left light bump sensor.

        Returns:
            int: Value of the furthest left light bump sensor.
        """
    def get_middle_left_distance(self) -> int:
        """Get the value of the middle left light bump sensor.

        Returns:
            int: Value of the middle left light bump sensor.
        """
    def get_forward_left_distance(self) -> int:
        """Get the value of the forward left light bump sensor.

        Returns:
            int: Value of the forward left light bump sensor.
        """
    def get_furthest_right_distance(self) -> int:
        """Get the value of the furthest right light bump sensor.

        Returns:
            int: Value of the furthest right light bump sensor.
        """
    def get_middle_right_distance(self) -> int:
        """Get the value of the middle right light bump sensor.

        Returns:
            int: Value of the middle right light bump sensor.
        """
    def get_forward_right_distance(self) -> int:
        """Get the value of the forward right light bump sensor.
        
        Returns:
            int: Value of the forward right light bump sensor.
        """
    def get_left_bump(self) -> int:
        """Get whether the left bump is pressed.

        Returns:
            int: 1 - pressed; 0 - not pressed.
        """
    def get_right_bump(self) -> int:
        """Get whether the right bump is pressed.

        Returns:
            int: 1 - pressed; 0 - not pressed.
        """
    def get_sensor(self, sensor: CreateSensor) -> int:
        """Get the value of the specified Create sensor.

        Args:
            sensor (CreateSensor): Create sensor specified using the `CreateSensor` enum.

        Raises:
            ValueError: Invalid Create sensor type provided.

        Returns:
            int: Value of the specified Create sensor.
        """
    def disconnect(self) -> None:
        """Disconnect from the Create.
        """
