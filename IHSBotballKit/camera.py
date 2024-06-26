import cv2 as _cv2
import numpy as _np
from uuid import uuid4 as _uuid4
from typing import Callable as _Callable, TypedDict as _TypedDict


class ColorRange:
    """A color range in the hsv color space.

    Args:
        lower (list[int, int, int]): Lower bound of the hsv color range.
        upper (list[int, int, int]): Upper bound of the hsv color range.

    Attributes:
        lower (np.ndarray): Lower bound of the hsv color range.
        upper (np.ndarray): Upper bound of the hsv color range.
    """

    def __init__(self, lower: list[int, int, int], upper: list[int, int, int]) -> None:
        self.lower: _np.ndarray = _np.array(lower, dtype="uint8")
        self.upper: _np.ndarray = _np.array(upper, dtype="uint8")

    def mask(self, image: _cv2.typing.MatLike) -> _cv2.typing.MatLike:
        """Creates a mask on an hsv image, only keeping pixels that fall within the color range.

        Args:
            image (cv2.typing.MatLike): The hsv image to create the mask on.

        Returns:
            cv2.typing.MatLike: The masked image.
        """
        return _cv2.inRange(image, self.lower, self.upper)


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

    def __init__(self, port: int, **kwargs) -> None:
        self.default_parameters: CameraParameters = {
            "canny_thresh1": 50,
            "canny_thresh2": 150,
            "aperture_size": 3,
            "hough_lines_rho_resolution": 20,
            "hough_lines_thresh": 275,
            "hough_lines_optimization_slope_exponent": 20,
            "hough_lines_optimization_distance_coefficient": 100,
            "camera_crop_top": 0,
            "camera_crop_bottom": 0,
            "camera_crop_left": 0,
            "camera_crop_right": 0,
        }

        for key, value in kwargs:
            if key in self.default_parameters:
                self.default_parameters[key] = value
            else:
                print(f"{key} is not a valid camera parameter")

        self.video = _cv2.VideoCapture(port)
        if not self.video.isOpened():
            raise Exception("cannot get video")
        print("video opened")

    def get_frame(self) -> tuple[bool, _cv2.typing.MatLike]:
        """Get the current frame of the camera.

        Returns:
            tuple[bool, cv2.typing.MatLike]: (whether a frame was retrieved, frame retrieved).
        """
        return self.video.read()

    def normalize(self, image: _cv2.typing.MatLike) -> _cv2.typing.MatLike:
        """Normalize an image.

        Args:
            image (cv2.typing.MatLike): Image to be normalized.

        Returns:
            cv2.typing.MatLike: Normalized image.
        """
        lab = _cv2.cvtColor(image, _cv2.COLOR_BGR2LAB)
        l, a, b = _cv2.split(lab)
        l_norm = _cv2.normalize(l, None, 0, 255, _cv2.NORM_MINMAX)
        lab = _cv2.merge([l_norm, a, b])
        normalized_image = _cv2.cvtColor(lab, _cv2.COLOR_LAB2BGR)
        return normalized_image

    def override_default_parameters(self, **kwargs):
        """Internal helper function to override default camera parameters.

        Args:
            **kwargs: Used to specify custom values for properties defined in `CameraParameters`.

        Returns:
            CameraProperties: Camera properties dictionary with overridden values.
        """
        camera_parameters = self.default_parameters.copy()
        if kwargs:
            for key, value in kwargs.items():
                if key in camera_parameters:
                    camera_parameters[key] = value
                else:
                    print(f"{key} is not a valid default camera parameter override")
        return camera_parameters

    def crop_frame(
        self,
        frame: _cv2.typing.MatLike,
        crop_top: int,
        crop_bottom: int,
        crop_left: int,
        crop_right: int,
    ) -> _cv2.typing.MatLike:
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
        height, width = frame.shape[:2]
        return frame[crop_top : height - crop_bottom, crop_left : width - crop_right]

    def get_hough_lines(
        self,
        image: _cv2.typing.MatLike,
        optimization_method: _Callable[
            [list[tuple[float, float, float, float, float]], int, int],
            list[tuple[float, float, float, float, float]],
        ],
        **kwargs,
    ) -> list[tuple[float, float, float, float, float]]:
        """Performs the hough line transform on an image.

        Args:
            image (cv2.typing.MatLike): Image to perform the transformation on.
            optimization_method (Callable[ [list[tuple[float, float, float, float, float]], int, int], list[tuple[float, float, float, float, float]], ]): A method that takes in a list of hough lines, the slope exponent, and the distance coefficient; and sorts them.
            **kwargs: Used to override default camera parameters defined in `CameraParameters`.

        Returns:
            list[tuple[float, float, float, float, float]]: List of tuples representing hough lines. (x0, y0, cos(theta), sin(theta), slope).
        """
        camera_parameters = self.override_default_parameters(**kwargs)

        image = self.crop_frame(
            image,
            camera_parameters["camera_crop_top"],
            camera_parameters["camera_crop_bottom"],
            camera_parameters["camera_crop_left"],
            camera_parameters["camera_crop_right"],
        )

        image = self.normalize(image)
        gray_image = _cv2.cvtColor(image, _cv2.COLOR_BGR2GRAY)
        edges = _cv2.Canny(
            gray_image,
            camera_parameters["canny_thresh1"],
            camera_parameters["canny_thresh2"],
            apertureSize=camera_parameters["aperture_size"],
        )
        lines = _cv2.HoughLines(
            edges,
            camera_parameters["hough_lines_rho_resolution"],
            _np.pi / 180,
            camera_parameters["hough_lines_thresh"],
        )
        if not hasattr(lines, "__iter__"):
            print("no lines found")
            return []
        hough_lines = []
        for r_theta in lines:
            arr = _np.array(r_theta[0], dtype=_np.float64)
            r, theta = arr
            a = _np.cos(theta)
            b = _np.sin(theta)

            # converting from polar to cartesian
            x0 = a * r
            y0 = b * r
            slope = a / -b if abs(b) != 0 else float("inf")
            hough_lines.append((x0, y0, a, b, slope))

        hough_lines = optimization_method(
            hough_lines,
            camera_parameters["hough_lines_optimization_slope_exponent"],
            camera_parameters["hough_lines_optimization_distance_coefficient"],
        )
        return hough_lines

    def draw_hough_lines(
        self,
        image: _cv2.typing.MatLike,
        optimization_method: _Callable[
            [list[tuple[float, float, float, float, float]], int, int],
            list[tuple[float, float, float, float, float]],
        ],
        **kwargs,
    ) -> _cv2.typing.MatLike:
        """Performs the hough line transform on an image and draws the resulting hough lines on it.

        Args:
            image (cv2.typing.MatLike): Image to perform the operation on.
            optimization_method (Callable[ [list[tuple[float, float, float, float, float]], int, int], list[tuple[float, float, float, float, float]], ]): A method that takes in a list of hough lines, the slope exponent, and the distance coefficient; and sorts them.
            **kwargs: Used to override default camera parameters defined in `CameraParameters`.
            
        Returns:
            cv2.typing.MatLike: Image with hough lines drawn on it.
        """
        hough_lines = self.get_hough_lines(image, optimization_method, **kwargs)
        camera_parameters = self.override_default_parameters(**kwargs)

        image = self.crop_frame(
            image,
            camera_parameters["camera_crop_top"],
            camera_parameters["camera_crop_bottom"],
            camera_parameters["camera_crop_left"],
            camera_parameters["camera_crop_right"],
        )

        if len(hough_lines) == 0:
            return image.astype(_np.uint8)
        for index, line in enumerate(hough_lines):
            x0, y0, a, b, slope = line
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            if index == 0:
                _cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                _cv2.putText(
                    image,
                    str((x0, y0)),
                    (100, 50),
                    _cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                    _cv2.LINE_AA,
                )
                _cv2.putText(
                    image,
                    str(slope),
                    (100, 100),
                    _cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    _cv2.LINE_AA,
                )
            else:
                _cv2.line(
                    image,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    2,
                )
        return image.astype(_np.uint8)

    def display_live_hough_lines(
        self,
        optimization_method: _Callable[
            [list[tuple[float, float, float, float, float]], int, int],
            list[tuple[float, float, float, float, float]],
        ],
        flipped=False,
        **kwargs,
    ) -> None:
        """Performs the hough line transform on the live camera feed and displays it on the screen. Press 'q' on the keyboard to stop the function, and 's' to save a copy of the clean frame.

        Args:
            optimization_method (Callable[ [list[tuple[float, float, float, float, float]], int, int], list[tuple[float, float, float, float, float]], ]): A method that takes in a list of hough lines, the slope exponent, and the distance coefficient; and sorts them.
            flipped (bool, optional): Whether to flip the image upside down when displayed. Defaults to False.
            **kwargs: Used to override default camera parameters defined in `CameraParameters`.

        """
        camera_parameters = self.override_default_parameters(**kwargs)
        while True:
            ret, frame = self.get_frame()
            if not ret:
                print("no frame")
                break
            frame = self.draw_hough_lines(frame, optimization_method, **kwargs)
            if flipped:
                frame = _cv2.flip(frame, 0)
                frame = _cv2.flip(frame, 1)
            _cv2.imshow("frame", frame)
            k = _cv2.waitKey(1) & 0xFF
            if k == ord("q"):
                break
            elif k == ord("s"):
                ret, frame = self.get_frame()

                frame = self.crop_frame(
                    frame,
                    camera_parameters["camera_crop_top"],
                    camera_parameters["camera_crop_bottom"],
                    camera_parameters["camera_crop_left"],
                    camera_parameters["camera_crop_right"],
                )

                new_uuid = _uuid4()
                _cv2.imwrite(f"{new_uuid}.png", frame)
                print("saved", new_uuid)

    def get_live_hough_line_distance(
        self,
        optimization_method: _Callable[
            [list[tuple[float, float, float, float, float]], int, int],
            list[tuple[float, float, float, float, float]],
        ],
        **kwargs,
    ) -> tuple[float, float, float, float, float]:
        """Performs the hough line transform on the current camera frame and returns the optimal line.

        Args:
            optimization_method (Callable[ [list[tuple[float, float, float, float, float]], int, int], list[tuple[float, float, float, float, float]], ]): A method that takes in a list of hough lines, the slope exponent, and the distance coefficient; and sorts them.
            **kwargs: Used to override default camera parameters defined in `CameraParameters`.

        Raises:
            Exception: Cannot get frame.

        Returns:
            tuple[float, float, float, float, float]: The optimal line provided by the `optimization_method`. (x0, y0, cos(theta), sin(theta), slope).
        """
        ret, frame = self.video.read()
        if not ret:
            raise Exception("cannot get frame")
        hough_lines = self.get_hough_lines(frame, optimization_method, **kwargs)
        if len(hough_lines) == 0:
            return (
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
            )
        return hough_lines[0]

    def get_color_bounding_box(
        self,
        image: _cv2.typing.MatLike,
        color_range: ColorRange,
        kernel_size: int = 5,
        iterations: int = 2,
    ) -> list[tuple[int, int, int, int]]:
        """Get bounding boxes of certain hsv color blobs in an image.

        Args:
            image (_cv2.typing.MatLike): The image to perform the function on.
            color_range (ColorRange): A `ColorRange` object.
            kernel_size (int): Size of the kernel used in `cv2.erode` and `cv2.dilute` when denoising the masked image. Defaults to 5.
            iterations (int): Iterations of `cv2.erode` and `cv2.dilute` applied when denoising the masked image. Defaults to 2.

        Returns:
            list[tuple[int, int, int, int]]: List of `cv2.typing.Rect` object consisting of the four vertices, sorted from largest to smallest.
        """

        kernel = _np.ones((kernel_size), _np.uint8)
        image = self.normalize(image)
        hsv = _cv2.cvtColor(image, _cv2.COLOR_BGR2HSV)
        mask = color_range.mask(hsv)
        mask = _cv2.erode(mask, kernel, iterations=iterations)
        mask = _cv2.dilate(mask, kernel, iterations=iterations)
        contours, _ = _cv2.findContours(
            mask, _cv2.RETR_EXTERNAL, _cv2.CHAIN_APPROX_SIMPLE
        )
        boxes = []
        for c in contours:
            boxes.append(_cv2.boundingRect(c))
        boxes = sorted(boxes, key=lambda box: (box[2] * box[3]), reverse=True)
        _cv2.typing.Rect
        return boxes

    def get_live_color_bounding_box_center(
        self,
        color_range: ColorRange,
        kernel_size: int = 5,
        iterations: int = 2,
    ) -> tuple[float, float, float, float]:
        """Get the center point and size of largest hsv blob bounding box in the current frame.

        Args:
            color_range (ColorRange): A `ColorRange` object.
            kernel_size (int, optional):  Size of the kernel used in `cv2.erode` and `cv2.dilute` when denoising the masked image. Defaults to 5.
            iterations (int, optional): Iterations of `cv2.erode` and `cv2.dilute` applied when denoising the masked image. Defaults to 2.

        Raises:
            Exception: Cannot get frame.

        Returns:
            tuple[float, float]: Center point of the largest bounding rect as well as its width and height. (x_c, y_c, w, h).
        """
        ret, frame = self.video.read()
        if not ret:
            raise Exception("cannot get frame")
        bounding_boxes = self.get_color_bounding_box(
            frame, color_range, kernel_size, iterations
        )
        if len(bounding_boxes) == 0:
            return (-1, -1)
        return (
            bounding_boxes[0][0] + bounding_boxes[0][2] / 2,
            bounding_boxes[0][1] + bounding_boxes[0][3] / 2,
            bounding_boxes[0][2],
            bounding_boxes[0][3]
        )

    def close(self) -> None:
        """Stops the camera feed, frees the video index, and destroys all OpenCV windows.
        """
        self.video.release()
        _cv2.destroyAllWindows()

    class HoughLinesOptimization:
        """A collection of basic hough line optimization/sorting methods
        """
        def sort_by_horizontal(
            hough_lines: list[tuple[float, float, float, float, float]],
            slope_exponent: int,
            distance_coefficient: int,
        ) -> list[tuple[float, float, float, float, float]]:
            """Sorts the hough lines from most horizontal to least horizontal, while taking into account the vertical position (y0) of the line's center point.

            Args:
                hough_lines (list[tuple[float, float, float, float, float]]): A list of hough line tuples to be sorted.
                slope_exponent (int): Exponent of the slope term in choosing the best hough line. Increased value increases the weight of how horizontal a line is.
                distance_coefficient (int): Coefficient of y0 value of a line in choosing the best hough line. Increased positive/negative value increases the weight of the vertical position of the line.

            Returns:
                list[tuple[float, float, float, float, float]]: Sorted list of hough line tuples. (x0, y0, cos(theta), sin(theta), slope).
            """
            return sorted(
                hough_lines,
                key=lambda line: (
                    (2 * abs(line[4]) + 1) ** slope_exponent - distance_coefficient
                ),
            )

        def sort_by_vertical(
            hough_lines: list[tuple[float, float, float, float, float]],
            slope_exponent: int,
            distance_coefficient: int,
        ) -> list[tuple[float, float, float, float, float]]:
            """Sorts the hough lines from most vertical to least vertical, while taking into account the horizontal position (x0) of the line's center point.

            Args:
                hough_lines (list[tuple[float, float, float, float, float]]): A list of hough line tuples to be sorted.
                slope_exponent (int): Exponent of the slope term in choosing the best hough line. Increased value increases the weight of how vertical a line is.
                distance_coefficient (int): Coefficient of the x0 value of a line in choosing the best hough line. Increased positive/negative value increases the weight of the horizontal position of the line.

            Returns:
                list[tuple[float, float, float, float, float]]: Sorted list of hough line tuples. (x0, y0, cos(theta), sin(theta), slope).
            """
            return sorted(
                hough_lines,
                key=lambda line: (
                    1 / (abs(line[4]) ** (1 / slope_exponent)) - distance_coefficient
                ),
            )
