from __future__ import annotations as _annotation
import threading as _threading

class Motor:
    """Motor object with core functionalities.

    Args:
        bot (BotController): An instance of the `BotController` object.
        port (int): Port of the motor.

    Attributes:
        k (CDLL): The kipr library object.
        port (int): Port of the motor.
    """

    def __init__(self, bot: _BotController, port: int) -> None:
        self.k = bot.k
        self.port = port

    def move_timed(self, velocity: int, time: int) -> None:
        """Drive the motor for a certain amount of time and then stop, while blocking proceeding synchronous processes.

        Args:
            velocity (int): Velocity of the motor, -1500 to 1500.
            time (int): Time in milliseconds.
        """
        self.k.mav(self.port, velocity)
        self.k.msleep(time)
        self.k.mav(self.port, 0)

    def move_timed_async(self, velocity: int, time: int) -> None:
        """Drive the motor asynchronously for a certain amount of time and then stop.

        Args:
            velocity (int): Velocity of the motor, -1500 to 1500.
            time (int): Time in milliseconds.
        """
        _threading.Thread(target=self.move_timed, args=(velocity, time)).start()

    def move(self, velocity: int) -> None:
        """Set the motor to drive at a certain velocity.

        Args:
            velocity (int): Velocity of the motor, -1500 to 1500.
        """
        self.k.mav(self.port, velocity)

    def get_position_counter(self) -> int:
        """Get the current position counter of the motor.

        Returns:
            int: The current position counter of the motor.
        """
        return self.k.gmpc(self.port)

    def clear_position_counter(self) -> None:
        """Clear the position counter of the motor.
        """
        self.k.cmpc(self.port)

    def off(self) -> None:
        """Turn off the motor.
        """
        self.k.off(self.port)

    def stop(self) -> None:
        """Hard stop the motor's movement.
        """
        self.k.mav(self.port, 0)


from .bot import BotController as _BotController
