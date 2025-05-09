import json

class Database:
    def __init__(self, json_file, default_data: dict = {}):
        self.json_file = json_file
        try:
            with open(json_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = default_data
            self.write()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __contains__(self, key):
        return key in self.data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def write(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.data, file, indent=4)