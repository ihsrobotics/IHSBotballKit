from IHSBotballKit import BotController, Create, CreateSensor, LessThan, GreaterThan, SensorType, TimeController
from IHSBotballKit.create_extras import drive_until_create_sensor, drive_until_sensor, line_follow_right_using_create_sensor_until
from configs import *

# first instantiate the bot object and the create object
bot = BotController()
create = Create(bot)

# simple drive
create.drive_timed(500, 500, 1000)
create.stop()

# drive until the left front cliff is on black
drive_until_create_sensor(create, 300, 300, CreateSensor.LEFT_FRONT_CLIFF, LessThan(CREATE_BLACK))
# the drive until function has stop built in

# drive until an analog sensor is
# first create the sensor object for the analog sensor
tophat_sensor = bot.create_sensor(SensorType.ANALOG, RIGHT_TOPHAT)
drive_until_sensor(create, 300, 300, tophat_sensor, GreaterThan(TOPHAT_BLACK))

# line follow for 10 seconds using the front right cliff sensor
ten_seconds_controller = TimeController(10)
line_follow_right_using_create_sensor_until(create, 150, 300, CreateSensor.RIGHT_FRONT_CLIFF, CREATE_BLACK, ten_seconds_controller.get_status)
create.stop()

create.disconnect()