from IHSBotballKit import BotController

# first instantiate the bot object
bot = BotController()

arm_servo = bot.create_servo(ARM_SERVO)
claw_servo = bot.create_sensor(CLAW_SERVO)


