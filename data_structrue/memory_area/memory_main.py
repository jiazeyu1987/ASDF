from . import *
class MemoryMain:
    def __init__(self):
        self.nodes = []


    def add_node(self,node):
        self.nodes.append(node)

    def say(self):
        for node in self.nodes:
            node.say()

mm = MemoryMain()