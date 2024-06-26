from IHSBotballKit import BotController, SensorType, SensorController, IsFalse, GreaterThan

# first instantiate the bot object
bot = BotController()

# create the motor objects
left_motor = bot.create_motor(LEFT_MOTOR_PORT)
right_motor = bot.create_motor(RIGHT_MOTOR_PORT)

# motor drive function 
from IHSBotballKit.motors_extras import create_motors_drive_function, create_motors_drive_timed_function
drive = create_motors_drive_function(bot, left_motor, right_motor)
drive_timed = create_motors_drive_timed_function(bot, left_motor, right_motor)

# drive forward at full speed for 1000ms
drive_timed(1500, 1500, 1000)

# set the motors' velocity to 1500
drive(1500, 1500)

# line follow on the left side of the tape until another a button is pressed
# first create the relevant sensor objects
line_follow_tophat = bot.create_sensor(SensorType.ANALOG, LINE_FOLLOW_TOPHAT_PORT)
button = bot.create_sensor(SensorType.DIGITAL, BUTTON_PORT)

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
