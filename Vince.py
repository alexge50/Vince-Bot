import discord
from discord.ext import commands
import json

import modules
import virtualbot


class Vince(commands.Bot):
    def __init__(self, config_file, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.modules = []
        self.token = None
        self.personalities = None
        self.name = None

        with open(config_file, "r") as f:
            json_config = json.load(f)

        with open(json_config["token_file"]) as f:
            self.token = f.read()

        with open(json_config["personalities_file"]) as f:
            self.personalities = json.load(f)

        with open(json_config["modules_config_file"]) as f:
            modules_config = json.load(f)

        self.name = json_config["name"]

        modules_constructors = modules.build_modules_list(json_config["modules_config_file"])
        self.instance_manager = virtualbot.BotInstanceManager(json_config["database"], modules_config, json_config)

        for (x, y) in modules_constructors.items():
            module = y(self, modules_config[x]["resource"], None)
            self.modules.append(module)
            self.add_cog(module)

    async def on_ready(self):
        print('Logged in as:\n{0} (ID: {0.id})'.format(self.user))

        for server in self.servers:
            self.instance_manager.new_instance(server.id)

    async def on_server_join(self, server):
        print("Bot was invited to {}".format(server.name))
        self.self.instance_manager.new_instance(server.id)

    def run_from_config(self):
        self.run(self.token)
