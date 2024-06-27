from IHSBotballKit import BotController, SensorType, SensorController, IsFalse, GreaterThan
from IHSBotballKit.motors_extras import create_motors_drive_function, create_motors_drive_timed_function, create_motors_drive_until_function
from configs import *

# first instantiate the bot object
bot = BotController()

# create the motor objects
left_motor = bot.create_motor(LEFT_MOTOR)
right_motor = bot.create_motor(RIGHT_MOTOR)

# move only the right motor for 2000ms
right_motor.move_timed(-750, 2000)

# create the functions for driving both motors 
drive = create_motors_drive_function(bot, left_motor, right_motor)
drive_timed = create_motors_drive_timed_function(bot, left_motor, right_motor)

# drive forward at full speed for 1000ms
drive_timed(1500, 1500, 1000)

# set the motors' velocity to 1500
drive(1500, 1500)

# line follow on the left side of the tape until another a button is pressed
# first create the relevant sensor objects
line_follow_tophat = bot.create_sensor(SensorType.ANALOG, LEFT_TOPHAT)
button = bot.create_sensor(SensorType.DIGITAL, FRONT_BUTTON)

# controller for whether the button digital sensor returns false
button_not_pressed = SensorController(button, IsFalse())
# controller for if the tophat is on black
line_follow_tophat_on_black = SensorController(line_follow_tophat, GreaterThan(TOPHAT_BLACK))

while button_not_pressed.get_status():
    if line_follow_tophat_on_black.get_status():
        drive(1000, 600)
    else:
        drive(600, 1000)
drive(0, 0)

# using the drive_until function with continuing condition that takes in several arguments
def continuing_condition_function(a, b, c) -> bool:
    ...
    
drive_until = create_motors_drive_until_function(bot, left_motor, right_motor)
# the arguments are passed in as an ordered tuple
# if the function has no arguments then leave the last parameter empty
drive_until(1000, 1000, continuing_condition_function, (1, 2, 3))

def another_function(a) -> bool:
    ...

# note: if only one argument is needed, it is necessary to put a comma after the value 
# to inform python that it is a tuple, not a literal inside a parenthesis
drive_until(-1500, -1500, another_function, (10,))
