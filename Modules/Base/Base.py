"""
base class for modules
"""


class Base:
    def __init__(self, bot, resources, personality_data):
        self.bot = bot
        self.resources = resources
        self.personality_data = personality_data

        self.send_message = self.bot.send_message
        self.load_resources()

    def get_instance(self, serverid):
        return self.bot.instance_manager.get_instance(serverid)

    def load_resources(self):
        pass

    def get_module(self, bot_instance, name):
        return bot_instance.modules_instances[name]

    def get_personality_data(self, bot_instance):
        return self.personality_data[bot_instance.current_personality]


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
