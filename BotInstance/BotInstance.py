"""
BotInstance - a class that describes the setting of the bot in a server, identified by serverid
"""


class BotInstance:
    def __init__(self, owner, serverid, module_instance_builders, entry=None,
                 config=None):  # inits itself using the entry
        self.owner = owner
        self.serverid = serverid
        self.modules_instances = {}

        for (module_name, (module_instance_class,
                           module_instance_default_config)) in module_instance_builders.items():  # inits the modules
            self.modules_instances[module_name] = module_instance_class(self,
                                                                        entry=entry,
                                                                        config=module_instance_default_config)

        if entry is not None:
            self.current_personality = entry["current_personality"]
        elif config is not None:
            self.current_personality = config["initial_personality"]
        else:
            raise Exception("entry and config are None")

        self.update()  # update to keep data base in sync

    def update(self):  # it update the database entry
        new_entry = dict(serverid=self.serverid, current_personality=self.current_personality)
        for (module_name, module_instance) in self.modules_instances.items():
            new_entry.update(module_instance.get_attributes())
        self.owner.database.update_server_properties(self.serverid, new_entry)

    def get_database_entry(self):
        return self.owner.database.get_server_entry(self.serverid)
