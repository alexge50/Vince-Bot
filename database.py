import dataset
import threading


class Database:
    def __init__(self, config):
        if config["thread-lock"]:
            self.lock = threading.Lock()
        else:
            self.lock = FakeLock()
        self.database = dataset.connect(config["protocol"])

    def update_server_properties(self, serverid, properties):
        with self.database as db:
            self.lock.acquire()
            properties["serverid"] = serverid
            db["servers"].update(properties, ["serverid"])
            self.lock.release()

    def get_servers_table(self):
        return self.database["servers"]


class FakeLock:
    def __init__(self):
        pass

    def acquire(self):
        pass

    def release(self):
        pass
