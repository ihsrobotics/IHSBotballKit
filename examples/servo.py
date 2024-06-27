from IHSBotballKit import BotController, Create
from configs import *

# first instantiate the bot object
bot = BotController()
create = Create(bot)

# create the relevant servo objects
arm_servo = bot.create_servo(ARM_SERVO)
claw_servo = bot.create_servo(CLAW_SERVO)

# move the claw servo immediately
claw_servo.set_position(CLAW_OPEN)

# move the arm servo slowly
arm_servo.set_position(ARM_STRAIGHT, 3)

# move the claw servo very slowly
claw_servo.set_position(CLAW_CLOSED, 10)

# move the arm servo while doing something else
arm_servo.set_position_async(ARM_UP, 5)
create.drive_timed(150, 150, 3000)


create.disconnect()