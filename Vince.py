import traceback

import json

from discord.ext import commands
import discord

from BotInstance.BotInstance import BotInstance
from BotInstance.BotInstanceManager import BotInstanceManager


def make_module_builders(module_config, modules_directory):
    lib = "{}.{}.{}".format(modules_directory,
                            module_config["lib"],
                            module_config["lib"])

    exec("import {}".format(lib))

    module_builder = eval("{}.{}".format(lib,
                                         module_config["class"]))

    module_config["default_instance_config"].update({module_config["instance_class"]: ""})
    module_instance_builder = (eval("{}.{}".format(lib,
                                                   module_config["instance_class"])),
                               module_config["default_instance_config"]
                               )

    return module_builder, module_instance_builder


class Vince(commands.Bot):
    def __init__(self, config_file, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.modules = []
        self.token = None
        self.personalities_data = {}
        self.active_personalities = None
        self.name = None

        with open(config_file, "r") as f:
            json_config = json.load(f)

        with open(json_config["token_file"]) as f:
            self.token = f.read()

        self.name = json_config["name"]

        self.active_personalities = json_config["personalities"]["active_personalities"]
        for personality_name in self.active_personalities:
            self.personalities_data[personality_name] = {}

        module_instance_builders = {}

        for module_name in json_config["modules"]["active_modules"]:
            module_directory = json_config["modules"]["modules_directory"] + "/" + module_name + "/"
            module_config_file = module_directory + module_name + ".json"

            with open(module_config_file) as f:
                module_config = json.load(f)

            (module_builder, module_instance_builder) = make_module_builders(module_config[module_name],
                                                                             json_config["modules"]["modules_directory"]
                                                                             )
            module_personalities_data = self.load_personality(module_directory, module_name)
            module = module_builder(self,
                                    module_config[module_name]["resource"],
                                    module_personalities_data)

            module_instance_builders[module_name] = module_instance_builder

            self.modules.append(module)
            self.add_cog(module)

        self.instance_manager = BotInstanceManager(json_config["database"],
                                                   module_instance_builders,
                                                   json_config["default_server_config"])

        self.remove_command("help")
        self.add_command(self.help)

    def load_personality(self, module_directory, module_name):
        module_personalities_data = {}
        for personality_name in self.active_personalities:
            with open(module_directory + "personalities/" + personality_name + ".json") as f:
                personality_data = json.load(f)
            module_personalities_data[personality_name] = personality_data[module_name]
            self.personalities_data[personality_name][module_name] = personality_data[module_name]

        return module_personalities_data

    async def on_ready(self):
        print('Logged in as:\n{0} (ID: {0.id})'.format(self.user))

        for server in self.servers:
            print("server: {}, {}".format(server.name, server.id))
            self.instance_manager.new_instance(server.id)

    async def on_server_join(self, server):
        print("Bot was invited to {}".format(server.name))
        self.instance_manager.new_instance(server.id)

    async def on_message(self, message):
        await self.process_commands(message)

    async def on_error(self, event, *args, **kwargs):
        print("here")
        # await self.send_message(self.get_channel('407261193745465348'), "```\n{}```".format(traceback.format_exc()))

    @commands.command(pass_context=True, no_pm=True)
    async def help(self, ctx):
        message = ""
        message += "```cpp\n\"{}'s commands list\"```\n".format(self.name)
        for module in self.modules:
            (module_info, command_info) = module.help()
            module_name = module.name
            message += "**{}**: {}\n".format(module_name, module_info)

            message += "```\n"
            for(command_name, command_description) in command_info.items():
                message += "{} - {}\n".format(command_name, command_description)
            message += "```\n"

        await self.send_message(ctx.message.channel, message)

    def run_from_config(self):
        self.run(self.token)
