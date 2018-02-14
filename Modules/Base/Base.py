"""
base class for modules
"""

import discord.ext.commands.context
import discord.message
from discord.permissions import Permissions
from discord.user import User
from discord.channel import Channel

import inspect


class Base:
    def __init__(self, bot, resources, permissions, personality_data, global_personality_data):
        self.bot = bot
        self.name = self.__class__.__name__
        self.resources = resources
        self.permissions = permissions
        self.personality_data = personality_data
        self.global_personality_data = global_personality_data

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

    def get_personality_data(self, bot_instance, is_global=False, message_name=None):
        if is_global:
            return self.global_personality_data[bot_instance.current_personality][message_name]
        else:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)
            caller_name = caller_frame[1][3]

            return self.personality_data[bot_instance.current_personality][caller_name]

    def check_permissions(self, ctx: discord.ext.commands.context.Context):
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller_name = caller_frame[1][3]

        permissions = self.permissions[caller_name]
        user = ctx.message.author
        channel = ctx.message.channel

        return Base.check_required_permissions(user, channel, permissions)

    async def print_unmet_permissions_error(self, ctx):
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller_name = caller_frame[1][3]

        permissions = self.permissions[caller_name]
        user = ctx.message.author
        channel = ctx.message.channel

        unmet_permissions = Base.get_unmet_permissions(user, channel, permissions)

        if "alexge50" not in unmet_permissions:
            await self.send_message(channel,
                                    self.get_personality_data(self.get_instance(ctx),
                                                              is_global=True,
                                                              message_name="permissions_not_met").format(
                                        Base.list_to_string(unmet_permissions)))

    @staticmethod
    def list_to_string(l: list):
        result = "{}".format(l[0])
        l.remove(l[0])
        for x in l:
            result = result + ", " + "{}".format(x)

        return result

    @staticmethod
    def get_unmet_permissions(user: User, channel: Channel, permissions_required: list):
        user_permissions = channel.permissions_for(user)
        user_permissions_dictionary = Base.build_permissions_dictionary(user_permissions)

        unmet_permissions = []

        for permission in permissions_required:
            if permission == "alexge50":
                if user.id != "304170392375787520":
                    unmet_permissions.append(permission)
            else:
                if not user_permissions_dictionary[permission]:
                    unmet_permissions.append(permission)

        return unmet_permissions

    @staticmethod
    def check_required_permissions(user: User, channel: Channel, permissions_required: list):
        user_permissions = channel.permissions_for(user)
        user_permissions_dictionary = Base.build_permissions_dictionary(user_permissions)

        check = True

        for permission in permissions_required:
            if permission == "alexge50":
                check = check and user.id == "304170392375787520"
            else:
                check = check and user_permissions_dictionary[permission]

        return check

    def help(self):
        return "", {}

    @staticmethod
    def build_permissions_dictionary(user_permissions):
        user_permissions_dictionary = {"kick members": user_permissions.kick_members,
                                       "ban members": user_permissions.ban_members,
                                       "administrator": user_permissions.administrator,
                                       "manage channels": user_permissions.manage_channels,
                                       "manage server": user_permissions.manage_server,
                                       "read": user_permissions.read_messages,
                                       "write": user_permissions.send_messages,
                                       "manage messages": user_permissions.manage_messages,
                                       "manage nicknames": user_permissions.manage_nicknames,
                                       "manage roles": user_permissions.manage_roles}
        return user_permissions_dictionary

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
