"""
base class for modules
"""

import discord.ext.commands.context
import discord.message


class Base:
    def __init__(self, bot, resources, personality_data):
        self.bot = bot
        self.name = self.__class__.__name__
        self.resources = resources
        self.personality_data = personality_data

        self.load_resources()

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

    def get_instance(self, *args):
        serverid = None
        if type(args[0]) is discord.ext.commands.context.Context:
            serverid = self.get_id_from_context(args[0])
        elif type(args[0]) is discord.Message:
            serverid = self.get_id_from_message(args[0])
        elif type(args[0]) == str:
            serverid = args[0]

        return self.bot.instance_manager.get_instance(serverid)

    def load_resources(self):
        pass

    def get_personality_data(self, bot_instance):
        return self.personality_data[bot_instance.current_personality]

    def help(self):
        return "", {}

    @staticmethod
    def get_module(bot_instance, name):
        return bot_instance.modules_instances[name]

    @staticmethod
    def get_id_from_context(ctx):
        return ctx.message.channel.server.id

    @staticmethod
    def get_id_from_message(message):
            return message.channel.server.id


class BaseInstance:
    def __init__(self, bot_instance, entry=None, config=None):
        self.bot_instance = bot_instance
        self.name = self.__class__.__name__

        if entry is not None and self.name in entry:  # check if the module is registered in database entry
            self.init(entry)
        elif config is not None:
            self.init(config)
        else:
            raise Exception("Cannot configure {}, entry and config are None".format(self.name))

    def init(self, config):
        pass

    def get_attributes(self):
        attr = {self.name: ""}
        attr.update(self.convert_to_dictionary())
        return attr

    def convert_to_dictionary(self):
        return dict()
