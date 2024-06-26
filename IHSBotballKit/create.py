from .bot import BotController as _BotController
import threading as _threading
import enum as _enum
from typing import Callable as _Callable

class CreateSensor(_enum.Enum):
    """Enum for the build-in sensors on the Create.
    """
    LEFT_CLIFF = _enum.auto()
    LEFT_FRONT_CLIFF = _enum.auto()
    RIGHT_CLIFF = _enum.auto()
    RIGHT_FRONT_CLIFF = _enum.auto()

    FURTHEST_LEFT_DISTANCE = _enum.auto()
    MIDDLE_LEFT_DISTANCE = _enum.auto()
    FORWARD_LEFT_DISTANCE = _enum.auto()

    FURTHEST_RIGHT_DISTANCE = _enum.auto()
    MIDDLE_RIGHT_DISTANCE = _enum.auto()
    FORWARD_RIGHT_DISTANCE = _enum.auto()

    LEFT_BUMP = _enum.auto()
    RIGHT_BUMP = _enum.auto()

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
    def __init__(self, bot: _BotController, retry_attempts = 5) -> None:
        self.k = bot.k
        for _ in range(retry_attempts):
            print("attempt to connect")
            success = self.k.create_connect_once()
            if success:
                print("connected")
                return
        raise Exception("Failed to connect to Create")
        
    def drive(self, left_speed: int, right_speed: int) -> None:
        """Set the Create to drive at a certain speed.

        Args:
            left_speed (int): Speed of the left wheel, -500 to 500.
            right_speed (int): Speed of the right wheel, -500 to 500.
        """
        self.k.create_drive_direct(left_speed, right_speed)

    def drive_timed(self, left_speed: int, right_speed: int, time: int) -> None:
        """Drive the Create for a certain amount of time and then stop, while blocking proceeding synchronous operations.

        Args:
            left_speed (int): Speed of the left wheel, -500 to 500.
            right_speed (int): Speed of the right wheel, -500 to 500.
            time (int): Time in milliseconds.
        """
        self.k.create_drive_direct(left_speed, right_speed)
        self.k.msleep(time)
        self.k.create_drive_direct(0, 0)

    def drive_timed_async(self, left_speed: int, right_speed: int, time: int) -> None:
        """Drive the Create asynchronously for a certain amount of time and then stop.

        Args:
            left_speed (int): Speed of the left wheel, -500 to 500.
            right_speed (int): Speed of the right wheel, -500 to 500.
            time (int): Time in milliseconds.
        """
        _threading.Thread(target=self.drive_timed, args=(left_speed, right_speed, time)).start()

    def stop(self) -> None:
        """Stop the Create.
        """
        self.k.create_drive_direct(0, 0)

    def drive_until(self, left_speed: int, right_speed: int, continuing_condition: _Callable[..., bool]) -> None:
        """Drive the Create synchronously while a condition is true.

        Args:
            left_speed (int): Speed of the left wheel, -500 to 500.
            right_speed (int): Speed of the right wheel, -500 to 500.
            continuing_condition (_Callable[..., _Any]): A function or lambda that returns a truthy value until the Create is supposed to stop. 
        """
        self.k.create_drive_direct(left_speed, right_speed)
        while(continuing_condition()): 
            continue
        self.k.create_drive_direct(0, 0)

    def get_left_cliff(self) -> int:
        """Get the value of the left cliff sensor.

        Returns:
            int: Value of the left cliff sensor.
        """
        return self.k.get_create_lcliff_amt()
    def get_left_front_cliff(self) -> int:
        """Get the value of the left front cliff sensor.

        Returns:
            int: Value of the left front cliff sensor.
        """
        return self.k.get_create_lfcliff_amt()
    def get_right_cliff(self) -> int:
        """Get the value of the right cliff sensor.

        Returns:
            int: Value of the right cliff sensor.
        """
        return self.k.get_create_rcliff_amt()
    def get_right_front_cliff(self) -> int:
        """Get the value of the right front cliff sensor.

        Returns:
            int: Value of the right front cliff sensor.
        """
        return self.k.get_create_rfcliff_amt()
    def get_furthest_left_distance(self) -> int:
        """Get the value of the furthest left light bump sensor.

        Returns:
            int: Value of the furthest left light bump sensor.
        """
        return self.k.get_create_llightbump_amt()
    def get_middle_left_distance(self) -> int:
        """Get the value of the middle left light bump sensor.

        Returns:
            int: Value of the middle left light bump sensor.
        """
        return self.k.get_create_lflightbump_amt()
    def get_forward_left_distance(self) -> int:
        """Get the value of the forward left light bump sensor.

        Returns:
            int: Value of the forward left light bump sensor.
        """
        return self.k.get_create_lclightbump_amt()
    
    def get_furthest_right_distance(self) -> int:
        """Get the value of the furthest right light bump sensor.

        Returns:
            int: Value of the furthest right light bump sensor.
        """
        return self.k.get_create_rlightbump_amt()
    def get_middle_right_distance(self) -> int:
        """Get the value of the middle right light bump sensor.

        Returns:
            int: Value of the middle right light bump sensor.
        """
        return self.k.get_create_rclightbump_amt()
    def get_forward_right_distance(self) -> int:
        """Get the value of the forward right light bump sensor.
        
        Returns:
            int: Value of the forward right light bump sensor.
        """
        return self.k.get_create_rflightbump_amt()

    def get_left_bump(self) -> int:
        """Get whether the left bump is pressed.

        Returns:
            int: 1 - pressed; 0 - not pressed.
        """
        return self.k.get_create_lbump()
    def get_right_bump(self) -> int:
        """Get whether the right bump is pressed.

        Returns:
            int: 1 - pressed; 0 - not pressed.
        """
        return self.k.get_create_rbump()

    def get_sensor(self, sensor: int) -> int:
        """Get the value of the specified Create sensor.

        Args:
            sensor (int): Create sensor specified using the `CreateSensor` enum.

        Returns:
            int: Value of the specified Create sensor.
        """
        if sensor == CreateSensor.LEFT_CLIFF:
            return self.get_left_cliff()
        elif sensor == CreateSensor.LEFT_FRONT_CLIFF:
            return self.get_left_front_cliff()
        elif sensor == CreateSensor.RIGHT_CLIFF:
            return self.get_right_cliff()
        elif sensor == CreateSensor.RIGHT_FRONT_CLIFF:
            return self.get_right_front_cliff()

        elif sensor == CreateSensor.FURTHEST_LEFT_DISTANCE:
            return self.get_furthest_left_distance()
        elif sensor == CreateSensor.MIDDLE_LEFT_DISTANCE:
            return self.get_middle_left_distance()
        elif sensor == CreateSensor.FORWARD_LEFT_DISTANCE:
            return self.get_forward_left_distance()

        elif sensor == CreateSensor.FURTHEST_RIGHT_DISTANCE:
            return self.get_furthest_right_distance()
        elif sensor == CreateSensor.MIDDLE_RIGHT_DISTANCE:
            return self.get_middle_right_distance()
        elif sensor == CreateSensor.FORWARD_RIGHT_DISTANCE:
            return self.get_forward_right_distance()

        elif sensor == CreateSensor.LEFT_BUMP:
            return self.get_left_bump()
        elif sensor == CreateSensor.RIGHT_BUMP:
            return self.get_right_bump()

    def disconnect(self) -> None:
        """Disconnect from the Create.
        """
        self.k.create_disconnect()