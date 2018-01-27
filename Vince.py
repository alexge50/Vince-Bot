import json

from discord.ext import commands

from BotInstance.BotInstance import BotInstance
from BotInstance.BotInstanceManager import BotInstanceManager


def make_module_builders(module_config, modules_directory):
    lib = "{}.{}.{}".format(modules_directory,
                            module_config["lib"],
                            module_config["lib"])

    exec("import {}".format(lib))

    module_builder = eval("{}.{}".format(lib,
                                         module_config["class"]))

    module_instance_builder = (eval("{}.{}".format(lib,
                                                   module_config["instance_class"])),
                               module_config["default_instance_config"])

    return module_builder, module_instance_builder


class Vince(commands.Bot):
    def __init__(self, config_file, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.modules = []
        self.token = None
        self.personalities_data = {}
        self.active_personalities = None
        self.name = None
        self.event_listeners = {}

        for event_name in event_names:
            self.event_listeners[event_name] = []

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

            for event_name in module_config[module_name]["listens_to"]:
                self.event_listeners[event_name].append(eval("module.{}".format(event_name)))

            self.modules.append(module)
            self.add_cog(module)

        self.instance_manager = BotInstanceManager(json_config["database"],
                                                   module_instance_builders,
                                                   json_config["default_server_config"])

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
            self.instance_manager.new_instance(server.id)

    async def on_server_join(self, server):
        print("Bot was invited to {}".format(server.name))
        self.instance_manager.new_instance(server.id)

    async def call_listeners_on_event(self, event_name, **kwargs):
        print(self.event_listeners[event_name])
        for listener in self.event_listeners[event_name]:
            print("calling listener")
            print(kwargs)
            #await listener(**kwargs)

    async def on_message(self, message):
        await self.call_listeners_on_event("on_message", message=message)
        await self.process_commands(message)

    async def on_message_deleted(self, message):
        await self.call_listeners_on_event("on_message_deleted", message=message)

    async def on_message_edit(self, before, after):
        await self.call_listeners_on_event("on_message_edit", before=before, after=after)

    async def on_reaction_add(self, reaction, user):
        await self.call_listeners_on_event("on_reaction_add", reaction=reaction, user=user)

    async def on_reaction_remove(self, reaction, user):
        await self.call_listeners_on_event("on_reaction_remove", reaction=reaction, user=user)

    async def on_reaction_clear(self, message, reactions):
        await self.call_listeners_on_event("on_reaction_clear", message=message, reactions=reactions)

    async def on_channel_delete(self, channel):
        await self.call_listeners_on_event("on_channel_delete", channel=channel)

    async def on_channel_create(self, channel):
        await self.call_listeners_on_event("on_channel_create", channel=channel)

    async def on_channel_update(self, before, after):
        await self.call_listeners_on_event("on_channel_update", before=before, after=after)

    async def on_member_join(self, member):
        await self.call_listeners_on_event("on_member_join", member=member)

    async def on_member_remove(self, member):
        await self.call_listeners_on_event("on_member_remove", member=member)

    async def on_member_update(self, before, after):
        await self.call_listeners_on_event("on_member_update", before=before, after=after)

    async def on_server_update(self, before, after):
        await self.call_listeners_on_event("on_server_update", before=before, after=after)

    async def on_server_role_create(self, role):
        await self.call_listeners_on_event("on_server_role_create", role=role)

    async def on_server_role_delete(self, role):
        await self.call_listeners_on_event("on_server_role_delete", role=role)

    async def on_server_role_update(self, before, after):
        await self.call_listeners_on_event("on_server_role_update", before=before, after=after)

    def run_from_config(self):
        self.run(self.token)


event_names = ["on_message",
               "on_message_deleted",
               "on_message_edit",
               "on_reaction_add",
               "on_reaction_remove",
               "on_reaction_clear",
               "on_channel_delete",
               "on_channel_create",
               "on_channel_update",
               "on_member_join",
               "on_member_remove",
               "on_member_update",
               "on_server_update",
               "on_server_role_create",
               "on_server_role_delete",
               "on_server_role_update"]
