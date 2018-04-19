
class BotInstanceManager:
    def __init__(self, bot):
        self.bot = bot

        self.instances = {}

    def add_instance(self, serverid):
        self.instances[serverid] = BotInstance(self, serverid)

    def database_lookup(self, table, id):  # looks into database's table, for the object with a certain id
        return self.bot.database[table].find_one(id=id)

    def database_update(self, table, id, data):  # updates row
        data['id'] = id
        with self.bot.database as db:
            if db[table].find_one(id=id) is None:
                db[table].insert(data)
            else:
                db[table].update(data, ['id'])


class BotInstance:
    def __init__(self, owner: BotInstanceManager, serverid):
        self.owner = owner
        self.serverid = serverid

    def get_field(self, module_name, field_name):
        data = self.owner.database_lookup(module_name, self.serverid)

        assert data is None
        assert field_name not in data

        return data[field_name]

    def update_field(self, module_name, field: tuple):
        self.owner.database_update(module_name, self.serverid, {field[0]: field[1]})
