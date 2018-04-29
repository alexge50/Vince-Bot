
class BotInstanceManager:
    def __init__(self, bot, default_properties):
        self.bot = bot
        self.default_properties = default_properties

        self.instances = {}

    def add_instance(self, serverid):
        if self.database_lookup("servers", serverid) is None:
            self.database_update("servers", serverid, {})

        for key, value in self.default_properties.items():
            if self.database_lookup(key, serverid) is None:
                self.database_update(key, serverid, value)

        self.instances[serverid] = BotInstance(self, serverid)

    def database_lookup(self, table, id):  # looks into database's table, for the object with a certain id
        table = 'table_' + table
        return self.bot.database[table].find_one(_id=id)

    def database_update(self, table, id, data):  # updates row
        table = 'table_' + table
        data['_id'] = id
        with self.bot.database as db:
            if db[table].find_one(_id=id) is None:
                db[table].insert(data)
            else:
                db[table].update(data, ['_id'])

    def get_instance(self, serverid):
        return self.instances[serverid]


class BotInstance:
    def __init__(self, owner: BotInstanceManager, serverid):
        self.owner = owner
        self.serverid = serverid

    def get_field(self, module_name, field_name):
        data = self.owner.database_lookup(module_name, self.serverid)

        assert data is not None
        assert field_name in data

        return data[field_name]

    def update_field(self, module_name, field: tuple):
        self.owner.database_update(module_name, self.serverid, {field[0]: field[1]})
