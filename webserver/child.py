import json
from flask import jsonify

class Child:
    def __init__(self, name, id, status):
        self.name = name
        self.id = id
        self.status = status
        self.last_change = ""
        self.history = []

    def __str__(self):
        return str(self.__dict__)

