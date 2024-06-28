import cv2 as _cv2
from typing import Callable as _Callable, Sequence as _Sequence, TypedDict as _TypedDict
import numpy as np

class ColorRange:
    """A color range in the hsv color space.

    Args:
        lower (Tuple[int, int, int]): Lower bound of the hsv color range.
        upper (Tuple[int, int, int]): Upper bound of the hsv color range.

    Attributes:
        lower (np.ndarray): Lower bound of the hsv color range.
        upper (np.ndarray): Upper bound of the hsv color range.
    """
    lower: np.ndarray
    upper: np.ndarray
    def __init__(self, lower: tuple[int, int, int], upper: tuple[int, int, int]) -> None: ...
    def mask(self, image: _cv2.typing.MatLike) -> _cv2.typing.MatLike:
        """Creates a mask on an hsv image, only keeping pixels that fall within the color range.

        Args:
            image (cv2.typing.MatLike): The hsv image to create the mask on.

        Returns:
            cv2.typing.MatLike: The masked image.
        """

class CameraParameters(_TypedDict):
    """An interface of keyword argument parameters for many Camera methods.

    Attributes:
        canny_thresh1 (float): First threshold for the hysteresis procedure. Used in `cv2.Canny` edge detection.
        canny_thresh2 (float): Second threshold for the hysteresis procedure. Used in `cv2.Canny` edge detection.
        aperture_size (int): Aperture size for the Sobel operator. Used in `cv2.Canny` edge detection.
        hough_lines_rho_resolution (float): Distance resolution of the accumulator in pixels. Used in `cv2.HoughLines`.
        hough_lines_thresh (int): Accumulator threshold parameter. Only those lines are returned that get enough votes (> threshold). Used in `cv2.HoughLines`.
        hough_lines_optimization_slope_exponent (int): Exponent of the slope term in choosing the best hough line. Increased value increases the weight of how horizontal/vertical a line is.
        hough_lines_optimization_distance_coefficient (int): Coefficient of the x0 or y0 value of a line in choosing the best hough line. Increased positive/negative value increases the weight of the horizontal/vertical position of the line.
        camera_crop_top (int): How many pixels are cropped from the top of the image before processing.
        camera_crop_bottom (int): How many pixels are cropped from the bottom of the image before processing.
        camera_crop_left (int): How many pixels are cropped from the left of the image before processing.
        camera_crop_right (int): How many pixels are cropped from the right of the image before processing.
    """
    canny_thresh1: float
    canny_thresh2: float
    aperture_size: int
    hough_lines_rho_resolution: float
    hough_lines_thresh: int
    hough_lines_optimization_slope_exponent: int
    hough_lines_optimization_distance_coefficient: int
    camera_crop_top: int
    camera_crop_bottom: int
    camera_crop_left: int
    camera_crop_right: int

class Camera:
    """Camera with some OpenCV functionalities.

    Args:
        port (int): Camera index (usually 0).
        **kwargs: Used to specify custom values for `default_parameters`.

    Raises:
        Exception: Cannot get video.

    Attributes:
        default_parameters (CameraParameters): Dictionary that implements default parameters defined in `CameraParameters`.
        video (cv2.VideoCapture): cv2 Video object.
    """
    default_parameters: CameraParameters
    video: _cv2.VideoCapture
    def __init__(self, port: int, **kwargs) -> None: ...
    def get_frame(self) -> tuple[bool, _cv2.typing.MatLike]:
        """Get the current frame of the camera.

        Returns:
            Tuple[bool, cv2.typing.MatLike]: (whether a frame was retrieved, frame retrieved).
        """
    def normalize(self, image: _cv2.typing.MatLike) -> _cv2.typing.MatLike:
        """Normalize an image.

        Args:
            image (cv2.typing.MatLike): Image to be normalized.

        Returns:
            cv2.typing.MatLike: Normalized image.
        """
    def override_default_parameters(self, **kwargs):
        """Internal helper function to override default camera parameters.

        Args:
            **kwargs: Used to specify custom values for properties defined in `CameraParameters`.

        Returns:
            CameraProperties: Camera properties dictionary with overridden values.
        """
    def crop_frame(self, frame: _cv2.typing.MatLike, crop_top: int, crop_bottom: int, crop_left: int, crop_right: int) -> _cv2.typing.MatLike:
        """Crops an image.

        Args:
            frame (cv2.typing.MatLike): Image to be cropped.
            crop_top (int): How many pixels are cropped from the top of the image.
            crop_bottom (int): How many pixels are cropped from the bottom of the image.
            crop_left (int): How many pixels are cropped from the left of the image.
            crop_right (int): How many pixels are cropped from the right of the image,

        Returns:
            cv2.typing.MatLike: Cropped image.
        """
    def get_hough_lines(self, image: _cv2.typing.MatLike, optimization_method: _Callable[[list[tuple[float, float, float, float, float]], int, int], list[tuple[float, float, float, float, float]]], **kwargs) -> list[tuple[float, float, float, float, float]]:
        """Performs the hough line transform on an image.

        Args:
            image (cv2.typing.MatLike): Image to perform the transformation on.
            optimization_method (Callable[ [List[Tuple[float, float, float, float, float]], int, int], List[Tuple[float, float, float, float, float]], ]): A method that takes in a list of hough lines, the slope exponent, and the distance coefficient; and sorts them.
            **kwargs: Used to override default camera parameters defined in `CameraParameters`.

        Returns:
            List[Tuple[float, float, float, float, float]]: List of tuples representing hough lines. (x0, y0, cos(theta), sin(theta), slope).
        """
    def draw_hough_lines(self, image: _cv2.typing.MatLike, optimization_method: _Callable[[list[tuple[float, float, float, float, float]], int, int], list[tuple[float, float, float, float, float]]], **kwargs) -> _cv2.typing.MatLike:
        """Performs the hough line transform on an image and draws the resulting hough lines on it.

        Args:
            image (cv2.typing.MatLike): Image to perform the operation on.
            optimization_method (Callable[ [List[Tuple[float, float, float, float, float]], int, int], List[Tuple[float, float, float, float, float]], ]): A method that takes in a list of hough lines, the slope exponent, and the distance coefficient; and sorts them.
            **kwargs: Used to override default camera parameters defined in `CameraParameters`.

        Returns:
            cv2.typing.MatLike: Image with hough lines drawn on it.
        """
    def display_live_hough_lines(self, optimization_method: _Callable[[list[tuple[float, float, float, float, float]], int, int], list[tuple[float, float, float, float, float]]], flipped: bool = False, **kwargs) -> None:
        """Performs the hough line transform on the live camera feed and displays it on the screen. Press 'q' on the keyboard to stop the function, and 's' to save a copy of the clean frame.

        Args:
            optimization_method (Callable[ [List[Tuple[float, float, float, float, float]], int, int], List[Tuple[float, float, float, float, float]], ]): A method that takes in a list of hough lines, the slope exponent, and the distance coefficient; and sorts them.
            flipped (bool, optional): Whether to flip the image upside down when displayed. Defaults to False.
            **kwargs: Used to override default camera parameters defined in `CameraParameters`.

        """
    def get_live_hough_line_distance(self, optimization_method: _Callable[[list[tuple[float, float, float, float, float]], int, int], list[tuple[float, float, float, float, float]]], **kwargs) -> tuple[float, float, float, float, float]:
        """Performs the hough line transform on the current camera frame and returns the optimal line.

        Args:
            optimization_method (Callable[ [List[Tuple[float, float, float, float, float]], int, int], List[Tuple[float, float, float, float, float]], ]): A method that takes in a list of hough lines, the slope exponent, and the distance coefficient; and sorts them.
            **kwargs: Used to override default camera parameters defined in `CameraParameters`.

        Raises:
            Exception: Cannot get frame.

        Returns:
            Tuple[float, float, float, float, float]: The optimal line provided by the `optimization_method`. (x0, y0, cos(theta), sin(theta), slope).
        """
    def get_color_bounding_box(self, image: _cv2.typing.MatLike, color_range: ColorRange, kernel_size: int = 5, iterations: int = 2) -> list[_Sequence[int]]:
        """Get bounding boxes of certain hsv color blobs in an image.

        Args:
            image (_cv2.typing.MatLike): The image to perform the function on.
            color_range (ColorRange): A `ColorRange` object.
            kernel_size (int): Size of the kernel used in `cv2.erode` and `cv2.dilute` when denoising the masked image. Defaults to 5.
            iterations (int): Iterations of `cv2.erode` and `cv2.dilute` applied when denoising the masked image. Defaults to 2.

        Returns:
            List[Tuple[int, int, int, int]]: List of `cv2.typing.Rect` object consisting of the four vertices, sorted from largest to smallest.
        """
    def get_live_color_bounding_box_center(self, color_range: ColorRange, kernel_size: int = 5, iterations: int = 2) -> tuple[float, float, float, float]:
        """Get the center point and size of largest hsv blob bounding box in the current frame.

        Args:
            color_range (ColorRange): A `ColorRange` object.
            kernel_size (int, optional):  Size of the kernel used in `cv2.erode` and `cv2.dilute` when denoising the masked image. Defaults to 5.
            iterations (int, optional): Iterations of `cv2.erode` and `cv2.dilute` applied when denoising the masked image. Defaults to 2.

        Raises:
            Exception: Cannot get frame.

        Returns:
            Tuple[float, float, float, float]: Center point of the largest bounding rect as well as its width and height. (x_c, y_c, w, h).
        """
    def close(self) -> None:
        """Stops the camera feed, frees the video index, and destroys all OpenCV windows."""

class HoughLinesOptimization:
    """A collection of basic hough line optimization/sorting methods"""
    @staticmethod
    def sort_by_horizontal(hough_lines: list[tuple[float, float, float, float, float]], slope_exponent: int, distance_coefficient: int) -> list[tuple[float, float, float, float, float]]:
        """Sorts the hough lines from most horizontal to least horizontal, while taking into account the vertical position (y0) of the line's center point.

        Args:
            hough_lines (List[Tuple[float, float, float, float, float]]): A list of hough line tuple to be sorted.
            slope_exponent (int): Exponent of the slope term in choosing the best hough line. Increased value increases the weight of how horizontal a line is.
            distance_coefficient (int): Coefficient of y0 value of a line in choosing the best hough line. Increased positive/negative value increases the weight of the vertical position of the line.

        Returns:
            List[Tuple[float, float, float, float, float]]: Sorted list of hough line tuple. (x0, y0, cos(theta), sin(theta), slope).
        """
    @staticmethod
    def sort_by_vertical(hough_lines: list[tuple[float, float, float, float, float]], slope_exponent: int, distance_coefficient: int) -> list[tuple[float, float, float, float, float]]:
        """Sorts the hough lines from most vertical to least vertical, while taking into account the horizontal position (x0) of the line's center point.

        Args:
            hough_lines (List[Tuple[float, float, float, float, float]]): A list of hough line tuple to be sorted.
            slope_exponent (int): Exponent of the slope term in choosing the best hough line. Increased value increases the weight of how vertical a line is.
            distance_coefficient (int): Coefficient of the x0 value of a line in choosing the best hough line. Increased positive/negative value increases the weight of the horizontal position of the line.

        Returns:
            List[Tuple[float, float, float, float, float]]: Sorted list of hough line tuple. (x0, y0, cos(theta), sin(theta), slope).
        """
