from discord.ext import commands
import discord

from Framework import util, Module
from Framework.BotInstance import *
from Framework.Permission import *


import dataset


class Vince(commands.Bot):
    def __init__(self, config_file, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.token = None
        self.database = None
        self.manager = None
        self.module_builders = None
        self.modules = {}

        config = util.load_json_file(config_file)
        self.token = util.load_file(config['token_file'])  # token
        self.database = dataset.connect(config['database'])  # database
        self.module_builders = Module.make_module_builder_list(config['modules_directory'])  # module builders

        # create instances of modules
        default_properties = {}
        naked_permission_required = {}
        for module_builder in self.module_builders:
            self.modules[module_builder.name] = Module.new_instance(module_builder, self)
            self.add_cog(self.modules[module_builder.name])

            default_properties[module_builder.name] = module_builder.default_properties \
                if module_builder.default_properties != "" \
                else {}

            naked_permission_required.update(module_builder.permissions)

        self.manager = BotInstanceManager(self, default_properties)
        self.permissions_manager = PermissionManager(self, naked_permission_required, None)

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        print('Logged in as:\n{0} (ID: {0.id})'.format(self.user))

        for server in self.servers:
            self.manager.add_instance(server.id)

    async def on_server_join(self, server):
        print("Bot was invited to {}".format(server.name))
        self.manager.add_instance(server.id)

    async def on_message(self, message):
        await self.process_commands(message)

    async def on_error(self, event, *args, **kwargs):
        pass
