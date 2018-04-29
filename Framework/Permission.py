import discord
from Framework.BotInstance import BotInstance

from discord.permissions import Permissions

# dictionary of all available permissions from discord, as string
permissions = {"kick members": Permissions.kick_members,
               "ban members": Permissions.ban_members,
               "administrator": Permissions.administrator,
               "manage channels": Permissions.manage_channels,
               "manage server": Permissions.manage_server,
               "read": Permissions.read_messages,
               "write": Permissions.send_messages,
               "manage messages": Permissions.manage_messages,
               "manage nicknames": Permissions.manage_nicknames,
               "manage roles": Permissions.manage_roles}


# naked permission = permission that a user posses.
# role permission = permission to access a function, accorded by a role that a user has
class PermissionManager:
    def __init__(self, bot, naked_permissions_required, command_list):
        self.manager = bot.manager
        self.naked_permissions_required = {}
        for key, val in naked_permissions_required.items():
            self.naked_permissions_required[key] = [permissions[x] for x in val]
        self.command_list = command_list

        template_row = {}
        for x in command_list:
            template_row[x] = None

        self.manager.database_update('roles_permissions', 0,
                                     template_row)  # for checking whether a role is able to invoke a command
        self.manager.database_update('commands_availability', 0,
                                     template_row)  # a list of disabled/enabled modules. by default, everything is enabled

    async def check(self, serverid, ):
        pass

    def allow_role_command(self, roleid, command_name):
        self.manager.database_update('roles_permissions', roleid, {command_name: True})

    def disallow_role_command(self, roleid, command_name):
        self.manager.database_update('roles_permissions', roleid, {command_name: False})

    def allow_role_module(self, roleid, module_name):
        for x in self.get_commands_from_module(module_name):
            self.allow_role_command(roleid, x)

    def disallow_role_module(self, roleid, module_name):
        for x in self.get_commands_from_module(module_name):
            self.disallow_role_command(roleid, x)

    def enable_command(self, serverid, command_name):
        self.manager.database_update('commands_availability', serverid, {command_name: True})

    def disable_command(self, serverid, command_name):
        self.manager.database_update('commands_availability', serverid, {command_name: False})

    def enable_module(self, serverid, module_name):
        for x in self.get_commands_from_module(module_name):
            self.enable_command(serverid, x)

    def disable_module(self, serverid, module_name):
        for x in self.get_commands_from_module(module_name):
            self.disable_command(serverid, x)

    def get_commands_from_module(self, module_name):
        l = []

        for x in self.command_list:
            if x.split('.')[0] == module_name:
                l.append(x)

        return l
