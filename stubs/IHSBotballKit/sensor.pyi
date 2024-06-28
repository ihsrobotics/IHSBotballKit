import enum as _enum
from .bot import BotController as _BotController
from ctypes import CDLL

class SensorType(_enum.Enum):
    """Enum for the two types (digital and analog) of sensors.
    """
    DIGITAL: int
    ANALOG: int

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
    k: CDLL
    sensor_type: SensorType
    port: int
    def __init__(self, bot: _BotController, sensor_type: SensorType, port: int) -> None: ...
    def get_value(self) -> int:
        """Get the value of the sensor.

        Raises:
            ValueError: Sensor type provided in object instantiation was invalid.

        Returns:
            int: The value of the sensor.
        """
