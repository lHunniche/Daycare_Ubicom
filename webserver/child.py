import json

class Child:
    def __init__(self, name, id, status, photo=None):
        self.name = name
        self.id = id
        self.status = status
        self.photo = photo
        self.history = []

    def __str__(self):
        return json.dumps(self.__dict__)
