import database
from BotInstance.BotInstance import BotInstance
"""
BotInstanceManager - manages the 'BotInstance's 
"""


class BotInstanceManager:
    def __init__(self, database_config, module_instance_builders, default_server_config):
        self.module_instance_builders = module_instance_builders
        self.default_server_config = default_server_config

        self.servers_table = {}
        self.database = database.Database(database_config)

    def get_instance(self, serverid):
        if serverid in self.servers_table:
            return self.servers_table[serverid]
        else:
            raise Exception("server wasn't registered before")

    def new_instance(self, serverid):  # checks to see if the server was already registered, if not add it
        if serverid not in self.servers_table:
            server_entry = self.database.get_server_entry(serverid)
            if server_entry is not None:  # init from entry
                self.servers_table[server_entry["serverid"]] = BotInstance(self,
                                                                           server_entry["serverid"],
                                                                           self.module_instance_builders,
                                                                           entry=server_entry)
            else:
                self.servers_table[serverid] = BotInstance(self,
                                                           serverid,
                                                           self.module_instance_builders,
                                                           config=self.default_server_config)
                self.servers_table[serverid].update()
