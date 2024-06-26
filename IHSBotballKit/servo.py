from __future__ import annotations as _annotation

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
    def __init__(self, bot: _BotController, port: int, default_enable: bool = True) -> None:
        self.k = bot.k
        self.port = port
        if default_enable:
            self.enable()
    
    def enable(self) -> None:
        """Enable the servo.
        """
        self.k.enable_servo(self.port)

    def disable(self) -> None:
        """Disable the servo.
        """
        self.k.disable_servo(self.port)

    def get_enabled(self) -> bool:
        """Get if the servo is enabled.

        Returns:
            bool: True - the servo is enabled; False - the servo is not enabled.
        """
        return self.k.get_servo_enabled(self.port)

    def get_position(self) -> int:
        """Get the current position of the servo.

        Returns:
            int: The current position of the servo.
        """
        return self.k.get_servo_position(self.port)

    def legacy_set_position(self, position: int) -> None:
        """Set the position of the servo immediately. Blocking (`msleep` or the equivalent) is required after.

        Args:
            position (int): Position to set the servo to.
        """
        self.k.set_servo_position(self.port, position)

    def set_position(self, target_position: int, delay: int = 0) -> None:
        """Set the position of the servo immediately or slowly. Blocking is done automatically.

        Args:
            target_position (int): Position to set the servo to.
            delay (int, optional): 0 - set the position of the servo immediately; other positive integer - set position of the servo slowly. The higher the delay the slower its movement. Defaults to 0.
        """
        position = self.get_position()
        if target_position == position: 
            return
        elif delay == 0:
            self.k.set_servo_position(self.port, position)
            self.k.msleep(150)
            return
        while self.get_position() < target_position and self.get_position() + 5 < 2048:
            position = self.get_position() + 5
            self.k.set_servo_position(self.port, position)
            self.k.msleep(delay)
        while self.get_position() > target_position and self.get_position() - 5 > 0:
            position = self.get_position() - 5
            self.k.set_servo_position(self.port, position)
            self.k.msleep(delay)
        self.k.set_servo_position(self.port, target_position)
        self.k.msleep(50)
  
from .bot import BotController as _BotController