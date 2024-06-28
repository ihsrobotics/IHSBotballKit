from __future__ import annotations as _annotation
import enum as _enum

class SensorType(_enum.Enum):
    """Enum for the two types (digital and analog) of sensors.
    """
    DIGITAL: int = _enum.auto()
    ANALOG: int = _enum.auto()

class Sensor:
    """Sensor object with core functionalities.
 
    Args:
        bot (BotController): An instance of the `BotController` object.
        sensor_type (SensorType): The type of sensor specified using the `SensorType` enum.
        port (int): Port of the sensor.
  
    Attributes:
        k (CDLL): The kipr library object.
        sensor_type (SensorType): The type of the sensor (digital or analog).
        port (int): Port of the sensor.
    """
    def __init__(self, bot: _BotController, sensor_type: SensorType, port: int) -> None:
        self.k = bot.k
        self.sensor_type: SensorType = sensor_type
        self.port: int = port
        
    def get_value(self) -> int:
        """Get the value of the sensor.

        Raises:
            ValueError: Sensor type provided in object instantiation was invalid.

        Returns:
            int: The value of the sensor.
        """
        if self.sensor_type == SensorType.ANALOG:
            return self.k.analog(self.port)
        elif self.sensor_type == SensorType.DIGITAL:
            return self.k.digital(self.port)
        else:
            raise ValueError("Invalid Create sensor.")

from .bot import BotController as _BotController