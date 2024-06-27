from IHSBotballKit import load_json, inject_namespace

# this should be an absolute path as the python file might not always be ran from the local directory
config_path = "/home/pi/Documents/IME_files/my_project/include/configs.json"

configs = load_json(config_path)

# using the configs as a dictionary
print(configs["ARM_SERVO"]) # 0
print(configs["CLAW_OPEN"]) # 500


# or (not really recommended), expose the variables to the global namespace
inject_namespace(globals(), configs)

# pylance will yell at you but if everything else is right then this does actually work
print(CLAW_CLOSED) # 0
print(CREATE_BLACK) # 2000
# to use these variables in other files just do `from configs import *`

# more time consuming but pylance or other type checkers won't yell at you:
LEFT_MOTOR = configs["LEFT_MOTOR"]
RIGHT_MOTOR = configs["RIGHT_MOTOR"]

print(LEFT_MOTOR) # 2
print(RIGHT_MOTOR) # 3