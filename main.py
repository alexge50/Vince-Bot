import Vince

#Vince.init("config.json")
#Vince.run()
bot = Vince.Vince("config.json", command_prefix="v$")
bot.run_from_config()
