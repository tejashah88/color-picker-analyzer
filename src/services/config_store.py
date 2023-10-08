from collections import defaultdict

class ConfigStore:
    def __init__(self, initial = {}):
        self.store = initial
        self.callbacks = defaultdict(list)

        for (key, value) in initial.items():
            setattr(self, key, value)


    def get(self, name):
        if name not in self.store:
            raise Exception(f'Value of "{name}" does not exist in config store')
        return self.store[name]


    def set(self, name, value):
        self.store[name] = value

        for cb_func in self.callbacks.get(name, []):
            cb_func(value)


    def refresh(self, name):
        self.set(name, self.get(name))


    def listen(self, name, callback):
        self.callbacks[name].append(callback)


    def deafen(self, name):
        self.callbacks[name].clear()
