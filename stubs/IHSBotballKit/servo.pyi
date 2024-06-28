from .bot import BotController as _BotController
from ctypes import CDLL

class Servo:
    """Servo object with core functionalities.
 
    Args:
        bot (BotController): An instance of the `BotController` object.
        port (int): Port of the servo.
        default_enable (bool): Whether to immediately enable the servo upon instantiation. Defaults to True.
        
    Attributes:
        k (CDLL): The kipr library object.
        port (int): Port of the servo.
    """
    k: CDLL
    port: int
    def __init__(self, bot: _BotController, port: int, default_enable: bool = True) -> None: ...
    def enable(self) -> None:
        """Enable the servo.
        """
    def disable(self) -> None:
        """Disable the servo.
        """
    def get_enabled(self) -> bool:
        """Get if the servo is enabled.

        Returns:
            bool: True - the servo is enabled; False - the servo is not enabled.
        """
    def get_position(self) -> int:
        """Get the current position of the servo.

        Returns:
            int: The current position of the servo.
        """
    def legacy_set_position(self, position: int) -> None:
        """Set the position of the servo immediately. Blocking (`msleep` or the equivalent) is required after.

        Args:
            position (int): Position to set the servo to.
        """
    def set_position(self, target_position: int, delay: int = 0) -> None:
        """Set the position of the servo immediately or slowly. Blocking is done automatically.

        Args:
            target_position (int): Position to set the servo to.
            delay (int, optional): 0 - set the position of the servo immediately; other positive integer - set position of the servo slowly. The higher the delay the slower its movement. Defaults to 0.
        """
    def set_position_async(self, target_position: int, delay: int = 0) -> None:
        """Asynchronously set the position of the servo immediately or slowly.

        Args:
            target_position (int): Position to get the servo to.
            delay (int, optional): 0 - set the position of the servo immediately; other positive integer = set the position of the servo slowly. The higher the delay the slower its movement. Defaults to 0.
        """
