import abc
from .camera import Camera as _Camera
from .create import Create as _Create, CreateSensor as _CreateSensor
from .sensor import Sensor as _Sensor
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from typing import Callable as _Callable, Generic as _Generic, Protocol as _Protocol, TypeVar as _TypeVar, List as _List

class Controller(_ABC, metaclass=abc.ABCMeta):
    """Abstract class for controllers.
    """
    @_abstractmethod
    def get_status(self) -> bool: ...

class _Comparable(_Protocol):
    def __lt__(self, other: _T) -> bool: ...
    
_T = _TypeVar("_T", bound=_Comparable)

class ValueController(_ABC, _Generic[_T], metaclass=abc.ABCMeta):
    """Derived abstract class for value controllers including LessThan, GreaterThan, IsFalse, and IsTrue.
    """
    @_abstractmethod
    def get_status(self, current_value: _T) -> bool: ...

class LessThan(ValueController, _Generic[_T]):
    """Controller for whether the current value is less than a specified value.

    Args:
        target_value (generic T): Target value of the controller.
        
    Attributes:
        target_value (generic T): Target value of the controller.
    """
    target_value: _T
    def __init__(self, target_value: _T) -> None: ...
    def get_status(self, current_value: _T) -> bool:
        """Compare the current value to the target value.

        Args:
            current_value (generic T): Current value to be compared.

        Returns:
            bool: Whether the current value is less than the target value.
        """

class GreaterThan(ValueController, _Generic[_T]):
    """Controller for whether the current value is greater than a specified value.

    Args:
        target_value (generic T): Target value of the controller.
        
    Attributes:
        target_value (generic T): Target value of the controller.
    """
    target_value: _T
    def __init__(self, target_value: _T) -> None: ...
    def get_status(self, current_value: _T) -> bool:
        """Compare the current value to the target value.

        Args:
            current_value (generic T): Current value to be compared.

        Returns:
            bool: Whether the current value is less than the target value.
        """

class IsTrue(ValueController):
    """Controller for whether the current value is True.
    """
    def __init__(self) -> None: ...
    def get_status(self, current_value: bool) -> bool:
        """Check if the current value is True.

        Args:
            current_value (bool): Current value to be checked.

        Returns:
            bool: Whether the current value is True.
        """

class IsFalse(ValueController):
    """Controller for whether the current value is False.    
    """
    def __init__(self) -> None: ...
    def get_status(self, current_value: bool) -> bool:
        """Check if the current value is False.

        Args:
            current_value (bool): Current value to be checked.

        Returns:
            bool: Whether the current value is False.
        """

class TimeController(Controller):
    """Controller for the amount of time elapsed.

    Args:
        duration (float): Amount of time (in seconds) before time is up.
        
    Attributes:
        duration (float): Amount of time (in seconds) before time is up.
        start_time (float): Start time to be compared to when calculating the time elapsed.
    """
    duration: float
    start_time: float
    def __init__(self, duration: float) -> None: ...
    def get_status(self) -> bool:
        """Check whether or not time is up.

        Returns:
            bool: Whether or not time is up (True: time is up; False: time is not up).
        """
    def reset(self) -> None:
        """Reset the start time of the controller, allowing it to be reused.
        """

class SensorController(Controller):
    """Controller for a digital or analog sensor and a target sensor value.
    
    Args:
        sensor (Sensor): The Sensor object that represents the robot sensor.
        sensor_threshold (ValueController): A `ValueController` object to check the sensor value.
        
    Attributes:
        sensor (Sensor): The Sensor object that represents the robot sensor.
        sensor_threshold (ValueController): A `ValueController` object to check the sensor value.
    """
    sensor: _Sensor
    sensor_threshold: ValueController
    def __init__(self, sensor: _Sensor, sensor_threshold: ValueController) -> None: ...
    def get_status(self) -> bool:
        """Check whether the current sensor value exceeds the specified threshold.

        Returns:
            bool: Whether the current sensor value exceeds the specified threshold.
        """

class CreateSensorController(Controller):
    """Controller for a Create sensor and a target sensor value.

    Args:
        create (Create): An instance of the `Create` object.
        sensor (CreateSensor): The specific Create sensor to use, specified using the `CreateSensor` enum.
        sensor_threshold (ValueController): A `ValueController` object to check the sensor value.
        
    Attributes:
        create (Create): An instance of the `Create` object.
        sensor (CreateSensor): The specific Create sensor to use, specified using the `CreateSensor` enum.
        sensor_threshold (ValueController): A `ValueController` object to check the sensor value.
    """
    create: _Create
    sensor: _CreateSensor
    sensor_threshold: ValueController
    def __init__(self, create: _Create, sensor: _CreateSensor, sensor_threshold: ValueController) -> None: ...
    def get_status(self) -> bool:
        """Check whether the current Create sensor value exceeds the specified threshold.

        Returns:
            bool: Whether the current Create sensor value exceeds the specified threshold.
        """

class CameraHoughLinesController(Controller):
    """A controller for the approximate distance a robot is from a wall or pipe or tape line or any other straight obstacle using the best hough line found in the camera frame.

    Args:
        camera (Camera): An instance of the `Camera` object.
        hough_lines_optimization_method (Callable[ [List[Tuple[float, float, float, float, float]], int, int], List[Tuple[float, float, float, float, float]], ]): A method that takes in a list of hough lines, the slope exponent, and the distance coefficient; and sorts them. See the `HoughLinesOptimization` class for simple static methods.
        is_target_reached (Callable[[float], bool]): A function or lambda that takes in a hough line distance and returns whether it has reached the target.
        is_slope_valid (Callable[[float], bool]): A function or lambda that takes in a slope value and returns whether it is acceptable. This helps eliminate unexpected outliers that otherwise meet all requirements.
        is_outlier (Callable[[float], bool]): A function or lambda that takes in a hough line distance and returns whether it is a valid distance. This is used to eliminate passing values that are obviously unrealistic.
        use_vertical_distance (bool, optional): Whether to use the vertical distance (usually for horizon) or horizontal distance (usually for relative angle). Defaults to True (vertical distance).
        **kwargs: Used to override default camera parameters defined in `CameraParameters`.
        
    Attributes:
        camera (Camera): An instance of the `Camera` object.
        hough_lines_optimization_method (Callable[ [List[Tuple[float, float, float, float, float]], int, int], List[Tuple[float, float, float, float, float]], ]): A method that takes in a list of hough lines, the slope exponent, and the distance coefficient; and sorts them.
        is_target_reached (Callable[[float], bool]): A function or lambda that takes in a hough line distance and returns whether it has reached the target.
        is_slope_valid (Callable[[float], bool]): A function or lambda that takes in a slope value and returns whether it is acceptable. This helps eliminate unexpected outliers that otherwise meet all requirements.
        is_outlier (Callable[[float], bool]): A function or lambda that takes in a hough line distance and returns whether it is a valid distance. This is used to eliminate passing values that are obviously unrealistic.
        use_vertical_distance (bool, optional): Whether to use the vertical distance (usually for horizon) or horizontal distance (usually for relative angle). Defaults to True (vertical distance).
        kwargs (dict[str, int | float]): Used to override default camera parameters defined in `CameraParameters`.
        prev_distance (List[float]): A list of previous returned hough line distances. The five most recent values all must reach the designated target for validity and reliability.
    """
    camera: _Camera
    hough_lines_optimization_method: _Callable[[list[tuple[float, float, float, float, float]], int, int], list[tuple[float, float, float, float, float]]]
    is_target_reached: _Callable[[float], bool]
    is_slope_valid: _Callable[[float], bool]
    is_outlier: _Callable[[float], bool]
    use_vertical_distance: bool
    kwargs: dict[str, int | float]
    prev_distance: _List[float]
    def __init__(self, camera: _Camera, hough_lines_optimization_method: _Callable[[list[tuple[float, float, float, float, float]], int, int], list[tuple[float, float, float, float, float]]], is_target_reached: _Callable[[float], bool], is_slope_valid: _Callable[[float], bool], is_outlier: _Callable[[float], bool], use_vertical_distance: bool = True, **kwargs) -> None: ...
    def get_status(self) -> bool: ...
