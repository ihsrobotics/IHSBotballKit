from abc import ABC as _ABC, abstractmethod as _abstractmethod
import time as _time
from .sensor import Sensor as _Sensor
from typing import Callable as _Callable, TypeVar as _TypeVar, Generic as _Generic, Tuple as _Tuple, List as _List
from .camera import Camera as _Camera
from .create import Create as _Create

_T = _TypeVar("_T")

class Controller(_ABC):
    """Abstract class for controllers.
    """
    @_abstractmethod
    def get_status(self):
        pass
    
class ValueController(Controller, _Generic[_T]):
    """Derived abstract class for value controllers including LessThan, GreaterThan, IsFalse, and IsTrue.
    """
    pass
    
class LessThan(ValueController):
    """Controller for whether the current value is less than a specified value.

    Args:
        target_value (generic T): Target value of the controller.
        
    Attributes:
        target_value (generic T): Target value of the controller.
    """
    def __init__(self, target_value: _T) -> None:
        super().__init__()
        self.target_value = target_value
        
    def get_status(self, current_value: _T) -> bool:
        """Compare the current value to the target value.

        Args:
            current_value (generic T): Current value to be compared.

        Returns:
            bool: Whether the current value is less than the target value.
        """
        return current_value < self.target_value
    
class GreaterThan(ValueController):
    """Controller for whether the current value is greater than a specified value.

    Args:
        target_value (generic T): Target value of the controller.
        
    Attributes:
        target_value (generic T): Target value of the controller.
    """
    def __init__(self, target_value: _T) -> None:
        super().__init__()
        self.target_value = target_value
        
    def get_status(self, current_value: _T) -> bool:
        """Compare the current value to the target value.

        Args:
            current_value (generic T): Current value to be compared.

        Returns:
            bool: Whether the current value is less than the target value.
        """
        return current_value > self.target_value
    
class IsTrue(ValueController):
    """Controller for whether the current value is True.
    """
    def __init__(self) -> None:
        super().__init__()
    
    def get_status(self, current_value: bool) -> bool:
        """Check if the current value is True.

        Args:
            current_value (bool): Current value to be checked.

        Returns:
            bool: Whether the current value is True.
        """
        return current_value
    
class IsFalse(ValueController):
    """Controller for whether the current value is False.    
    """
    def __init__(self) -> None:
        super().__init__()
    
    def get_status(self, current_value: bool) -> bool:
        """Check if the current value is False.

        Args:
            current_value (bool): Current value to be checked.

        Returns:
            bool: Whether the current value is False.
        """
        return not current_value
        

class TimeController(Controller):
    """Controller for the amount of time elapsed.

    Args:
        duration (float): Amount of time (in seconds) before time is up.
        
    Attributes:
        duration (float): Amount of time (in seconds) before time is up.
        start_time (float): Start time to be compared to when calculating the time elapsed.
    """
    def __init__(self, duration: float) -> None:
        super().__init__()
        self.duration: float = duration
        self.start_time: float = _time.time()

    def get_status(self) -> bool:
        """Check whether or not time is up.

        Returns:
            bool: Whether or not time is up (True: time is up; False: time is not up).
        """
        return _time.time() - self.start_time < self.duration

    def reset(self) -> None:
        """Reset the start time of the controller, allowing it to be reused.
        """
        self.start_time = _time.time()

class SensorController(Controller):
    """Controller for a digital or analog sensor and a target sensor value.
    
    Args:
        sensor (Sensor): The Sensor object that represents the robot sensor.
        sensor_threshold (ValueController): A `ValueController` object to check the sensor value.
        
    Attributes:
        sensor (Sensor): The Sensor object that represents the robot sensor.
        sensor_threshold (ValueController): A `ValueController` object to check the sensor value.
    """
    def __init__(self, sensor: _Sensor, sensor_threshold: ValueController) -> None:
        super().__init()
        self.sensor = sensor
        self.sensor_threshold = sensor_threshold

    def get_status(self) -> bool:
        """Check whether the current sensor value exceeds the specified threshold.

        Returns:
            bool: Whether the current sensor value exceeds the specified threshold.
        """
        return self.sensor_threshold.get_status(self.sensor.get_value())

class CreateSensorController(Controller):
    """Controller for a Create sensor and a target sensor value.

    Args:
        create (Create): An instance of the `Create` object.
        sensor (int): The specific Create sensor to use, specified using the `CreateSensor` enum.
        sensor_threshold (ValueController): A `ValueController` object to check the sensor value.
        
    Attributes:
        create (Create): An instance of the `Create` object.
        sensor (int): The specific Create sensor to use, specified using the `CreateSensor` enum.
        sensor_threshold (ValueController): A `ValueController` object to check the sensor value.
    """
    def __init__(self, create: _Create, sensor: int, sensor_threshold: ValueController) -> None:
        super().__init__()
        self.create = create
        self.sensor = sensor
        self.sensor_threshold = sensor_threshold

    def get_status(self) -> bool:
        """Check whether the current Create sensor value exceeds the specified threshold.

        Returns:
            bool: Whether the current Create sensor value exceeds the specified threshold.
        """
        return self.sensor_threshold.get_status(self.create.get_sensor(self.sensor))

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
        prev_distance (list[float]): A list of previous returned hough line distances. The five most recent values all must reach the designated target for validity and reliability.
    """
    def __init__(self, camera: _Camera, 
        hough_lines_optimization_method: _Callable[
        [_List[_Tuple[float, float, float, float, float]], int, int],
        _List[_Tuple[float, float, float, float, float]]], 
        is_target_reached: _Callable[[float], bool], 
        is_slope_valid: _Callable[[float], bool], 
        is_outlier: _Callable[[float], bool], 
        use_vertical_distance: bool = True, 
        **kwargs) -> None:
        super().__init__()
        self.camera = camera
        self.hough_lines_optimization_method = hough_lines_optimization_method
        self.is_target_reached = is_target_reached
        self.is_slope_valid = is_slope_valid
        self.is_outlier = is_outlier
        self.use_vertical_distance = use_vertical_distance
        self.kwargs = kwargs
        self.prev_distance = []

    def get_status(self) -> bool:
        x_distance, y_distance, _, _, slope = self.camera.get_live_hough_line_distance(self.hough_lines_optimization_method, **self.kwargs)
        distance = y_distance if self.use_vertical_distance else x_distance
        if self.is_outlier(distance): return True
        self.prev_distance.append(distance)

        if all([self.is_target_reached(distance) for distance in self.prev_distance[-5:]]) and len(self.prev_distance) >= 5 and self.is_slope_valid(slope):
            return False
        return True
