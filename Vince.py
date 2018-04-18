import traceback

import json

from discord.ext import commands
import discord



class Vince(commands.Bot):
    def __init__(self, config_file, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.token = None

        with open(config_file, "r") as f:
            config = json.load(f)

        # token
        with open(config["token_file"], "r") as f:
            self.token = f.read()

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        print('Logged in as:\n{0} (ID: {0.id})'.format(self.user))

    async def on_server_join(self, server):
        print("Bot was invited to {}".format(server.name))

    async def on_message(self, message):
        await self.process_commands(message)

    async def on_error(self, event, *args, **kwargs):
        pass
