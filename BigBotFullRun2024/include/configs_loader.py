from IHSBotballKit import load_json, globalize_configs

_configs = load_json("/home/snow/Documents/IHSBotballKit/BigBotFullRun2024//include/configs.json")

# def globalize_configs(configurations):
#     for key, value in configurations.items():
#         globals()[key] = value
        
# globalize_configs(_configs, globals)
globalize_configs(_configs, globals())


# print(SWEEPER_TOPHAT_PORT)

# print(globals())
# globals().update()