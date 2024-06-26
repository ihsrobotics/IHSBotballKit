import sys
sys.path.append("/home/snow/Documents/IHSBotballKit/BigBotFullRun2024/include")

from roomba_drive import *
from sweeper import *

import IHSBotballKit
from IHSBotballKit import CreateSensor
from IHSBotballKit.auxiliary.sensor import SensorType
import ihs_bindings
import time

def main() -> None:
    bot = IHSBotballKit.BotController()
    
    # create = IHSBotballKit.Create(bot)

    # bot.enable_all_servos()

    START_BOX_TIME = time.time()

    sweeper_servo = bot.create_servo(SWEEPER_SERVO_PORT)
    arm_servo = bot.create_servo(ARM_PORT)
    claw_servo = bot.create_servo(CLAW_PORT)
    rod_servo = bot.create_servo(ROD_SERVO_PORT)

    sweeper = Sweeper(sweeper_servo)

    sweeper_tophat = bot.create_sensor(SWEEPER_TOPHAT_PORT, SensorType.ANALOG)
    rod_tophat = bot.create_sensor(ROD_TOPHAT_PORT, SensorType.ANALOG)
    
    print(SWEEPER_TOPHAT_PORT)

    exit()

    arm_servo.set_position(ARM_STRAIGHT_UP, 3)
    ihs_bindings.encoder_turn_degrees_v2(500, -55)
    drive_to_line(create, 250, 250, CreateSensor.LEFT_CLIFF, CreateSensor.RIGHT_CLIFF)
    drive_to_line_white(create, 100, 100, CreateSensor.LEFT_CLIFF, CreateSensor.RIGHT_CLIFF)

    create.drive_timed(200, 200, 1300)

    ihs_bindings.encoder_turn_degrees_v2(100, 90)

    print("STARTING BOX TIME:", time.time() - START_BOX_TIME)

    DRAWER_TIME = time.time()
    drive_to_line(create, -250, -250, CreateSensor.LEFT_CLIFF, CreateSensor.RIGHT_CLIFF)

    arm_servo.set_position(ARM_MIDDLE_NOODLE, 3)

    sweeper.sweep()

    drive_to_line_white(create, -150, -150, CreateSensor.LEFT_CLIFF, CreateSensor.RIGHT_CLIFF)
    drive_to_line(create, -150 -150, CreateSensor.LEFT_FRONT_CLIFF, CreateSensor.RIGHT_FRONT_CLIFF)

    rod_servo.set_position(ROD_ANGLED_DRAWER)

    bot.k.msleep(300)

    claw_servo.set_position(CLAW_OPEN)

    ihs_bindings.encoder_turn_degrees_v2(500, 10)

    sensor_align_black(create, rod_tophat, ROD_TOPHAT_BLACK, 15, -15)

    right_front_on_black = IHSBotballKit.CreateSensorController(create, CreateSensor.RIGHT_FRONT_CLIFF, BLACK, ControllerType.LESS_THAN_CONTROLLER)
    create.drive_until(200, 200, lambda: right_front_on_black.get_status())
    create.drive_timed(200, 200, 500)

    arm_servo.set_position(ARM_DOWN, 2)
    claw_servo.set_position(CLAW_DRAWER, 3)

    left_front_on_black = IHSBotballKit.CreateSensorController(create, CreateSensor.LEFT_FRONT_CLIFF, BLACK, ControllerType.LESS_THAN_CONTROLLER)
    left_front_on_white = IHSBotballKit.CreateSensorController(create, CreateSensor.LEFT_FRONT_CLIFF, BLACK, ControllerType.GREATER_THAN_CONTROLLER)
    create.drive_until(-100, -100, lambda: left_front_on_black.get_status())
    create.drive_until(-100, -100, lambda: left_front_on_white.get_status())
    create.drive_timed(-100, -100, 200)

    claw_servo.set_position(CLAW_CLOSED + 250)
    bot.k.msleep(300)

    create.drive_timed(-100, -100, 150)

    claw_servo.set_position(CLAW_DRAWER_CLOSED)
    bot.k.msleep(300)

    left_on_white = IHSBotballKit.CreateSensorController(create, CreateSensor.LEFT_CLIFF, BLACK, ControllerType.GREATER_THAN_CONTROLLER)
    left_on_black = IHSBotballKit.CreateSensorController(create, CreateSensor.LEFT_CLIFF, BLACK, ControllerType.LESS_THAN_CONTROLLER)
    
    create.drive_until(250, 250, lambda: left_on_white.get_status())
    create.drive_until(250, 250, lambda: left_on_black.get_status())
    create.drive_timed(250, 250, 100)

    claw_servo.set_position(CLAW_OPEN)
    
    create.drive_timed(-250, -250, 200)

    rod_servo.set_position(ROD_SIDE)

    ihs_bindings.encoder_turn_degrees_v2(500, -30)
    
    arm_servo.set_position(ARM_STRAIGHT_UP, 3)

    drive_to_line(create, 200, 200, CreateSensor.LEFT_CLIFF, CreateSensor.RIGHT_CLIFF)
    drive_to_line_white(create, 100, 100, CreateSensor.LEFT_CLIFF, CreateSensor.RIGHT_CLIFF)

    sweeper.sweep_async()

    ihs_bindings.encoder_turn_degrees_v2(50, -80)

    sensor_align_black(create, rod_tophat, ROD_TOPHAT_BLACK, -30, 30)

    drive_to_line(create, 300, 300, CreateSensor.LEFT_CLIFF, CreateSensor.RIGHT_CLIFF)
    print("mid line align")
    drive_to_line_white(create, 100, 100, CreateSensor.LEFT_CLIFF, CreateSensor.RIGHT_CLIFF)

    arm_servo.set_position(ARM_SHELF)
    sweeper.sweep_right()

    ihs_bindings.encoder_turn_degrees_v2(500, 180)
    sweeper.sweep_left()
    ihs_bindings.encoder_turn_degrees_v2(500, -100)
    

    
    


    







if __name__ == "__main__":
    main()