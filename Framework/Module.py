from collections import namedtuple
from Framework import util

import discord
import discord.ext.commands.context

import inspect

ModuleBuilder = namedtuple('ModuleBuilder', 'name class_name default_properties resources permissions')


def load_module_builder(json_module, directory):  # creates a ModuleBuilder
    lib_name = "{}.{}".format(directory,
                              json_module['name'],
                              json_module['lib'])
    lib_path = "{}/{}/{}.py".format(directory,
                                    json_module['name'],
                                    json_module['lib'])
    lib = util.import_lib(lib_name, lib_path)

    module_class = lib.Main

    return ModuleBuilder(json_module['name'],
                         module_class,
                         json_module['default_properties'],
                         json_module['resources'],
                         json_module['permissions'])


def make_module_builder_list(module_directory):
    json_modules = util.load_json_file(module_directory + '/modules.json')

    module_builders = []
    for module_name in json_modules:
        json_file = module_directory + '/' + module_name + '/' + module_name + '.json'
        module_builders.append(load_module_builder(util.load_json_file(json_file), module_directory))

    return module_builders


def new_instance(module_builder: ModuleBuilder, bot):
    return module_builder.class_name(bot, module_builder.name, module_builder.permissions)


class ModuleBase:
    def __init__(self, bot, module_name, permissions):
        self.bot = bot
        self.name = module_name
        self.permissions = permissions

    async def send_message(self, *args, **kwargs):
        try:
            await self.bot.send_message(*args, **kwargs)
        except discord.errors.Forbidden:
            print("Unable to send message")

    async def say(self, *args, **kwargs):
        try:
            await self.bot.say(*args, **kwargs)
        except discord.errors.Forbidden:
            print("Unable to send message")

    def get_instance(self):
        ctx = self.__extract_context()
        serverid = ctx.message.channel.server.id

        return self.bot.manager.get_instance(serverid)

    def __extract_context(self):  # extracts context, from a command call
        # the command must be exactly 2 frames up
        caller_frame = inspect.getouterframes(inspect.currentframe(), 2)[2]

        return inspect.getargvalues(caller_frame[0]).locals['ctx']
