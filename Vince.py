import discord
from discord.ext import commands

import json

import Modules.Main


class Vince(commands.Bot):
    def __init__(self, config_file, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.modules = {}
        self.token = None
        self.personalities = None
        self.current_personality = None
        self.name = None

        with open(config_file, "r") as f:
            json_config = json.load(f)

        with open(json_config["token_file"]) as f:
            self.token = f.read()

        with open(json_config["personalities_file"]) as f:
            self.personalities = json.load(f)

        self.current_personality = json_config["initial_personality"]
        self.name = json_config["name"]

        self.modules["MainModule"] = Modules.Main.Main(self)
        self.add_cog(self.modules["MainModule"])

    async def on_ready(self):
        print('Logged in as:\n{0} (ID: {0.id})'.format(self.user))

    def run_from_config(self):
        self.run(self.token)
