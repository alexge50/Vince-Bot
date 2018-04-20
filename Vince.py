from discord.ext import commands
import discord

from Framework import util, Module
from Framework.BotInstance import *

import dataset


class Vince(commands.Bot):
    def __init__(self, config_file, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.token = None
        self.database = None
        self.manager = BotInstanceManager(self)
        self.module_builders = None
        self.modules = {}

        config = util.load_json_file(config_file)
        self.token = util.load_file(config['token_file'])  # token
        self.database = dataset.connect(config['database'])  # database
        self.module_builders = Module.make_module_builder_list(config['modules_directory'])  # module builders

        # create instances of modules
        for module_builder in self.module_builders:
            self.modules[module_builder.name] = Module.new_instance(module_builder, self)
            self.add_cog(self.modules[module_builder.name])

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
