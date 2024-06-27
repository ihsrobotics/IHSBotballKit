from IHSBotballKit import Camera, CameraHoughLinesController, ColorRange, HoughLinesOptimization

camera = Camera(0, camera_crop_bottom = 200, canny_thresh1 = 100, canny_thresh2 = 250)

# example application of hough lines: getting the distance of a pipe in front of the robot
# as the robot gets closer to the pipe, the hough line will be lower on the horizon
# this corresponds to a higher y-coordinate value
is_target_reached = lambda distance: distance > 200
# we don't want a vertical line to be accidentally counted
is_slope_valid = lambda slope: slope < 1
# for example, anything beyond 270 would be unreasonable and came from something else because by the time the value reaches 240 the robot would have already crashed into the pipe
is_outlier = lambda distance: distance > 270
hough_lines_controller = CameraHoughLinesController(camera, HoughLinesOptimization.sort_by_vertical, is_target_reached, is_slope_valid, is_outlier, True, canny_thresh1 = 150)

while hough_lines_controller.get_status():
    # perform actions while the controller's target has not been reached
    pass

# example application of color bounding box: driving up to a blue cube using its relative position
# create the hsv color profile of the cube
blue = ColorRange([95, 45, 0], [130, 255, 160])
x_c, y_c, width, height = camera.get_live_color_bounding_box_center(blue)
while width * height < 200:
    x_c, y_c, width, height = camera.get_live_color_bounding_box_center(blue)
    # correct for whether the cube is to the left or to the right (300 is just an example value)
    if x_c < 300:
        pass
    else:
        pass

camera.close()