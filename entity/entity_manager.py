from . import *
class EntityManager:
    def __init__(self):
        self.list = []

    def create_entity(self):
        et = Entity()
        self.list.append(et)

em = EntityManager()