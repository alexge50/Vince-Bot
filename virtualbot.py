import database
import modules

# I call an instance a collection of properties, that are tied to a certain server
# BotInstance - which hold the properties of the bot instance
# BotInstanceManager - the manager for instances


class BotInstance:  # this holds the properties, as well as properties for each module
    def __init__(self, serverid, module_instance_build_helper,  entry=None, config=None): # inits itself using the entry
        self.serverid = serverid
        self.modules_instances = {}
        for (module_name, module_settings) in module_instance_build_helper.item(): # inits the modules
            self.modules_instances["module_name"] = module_settings["class"](self,
                                                                             entry=entry,
                                                                             config=module_settings["default_config"])

        if entry is not None:
            self.current_personality = entry["current_personality"]
        elif config is not None:
            self.current_personality = config["initial_personality"]
        else:
            raise Exception("entry and config are None")


class BotInstanceManager:
    def __init__(self, database_config, modules_config, server_config):
        self.modules_config = modules_config
        self.server_config = server_config
        self.module_instance_build_helpers = modules.build_module_instance_list(modules_config)

        self.servers_table = {}
        self.database = database.Database(database_config)

    def new_instance(self, serverid):  # checks to see if the server was already registered, if not add it
        if serverid is not self.servers_table:
            server_entry = self.database.get_server_entry(serverid)
            if server_entry  is not None: # init from entry
                self.servers_table[server_entry["serverid"]] = BotInstance(server_entry["serverid"],
                                                                           self.module_instance_build_helpers,
                                                                           entry=server_entry)
            else:
                self.servers_table[server_entry["serverid"]] = BotInstance(server_entry["serverid"],
                                                                           self.module_instance_build_helpers,
                                                                           config=self.server_config)

