from . import *
import globalconfig as g
class StupidTree:
    def __init__(self):
        self.root = StupidNode("擱")

    def add_value(self,str1):
        current_node = self.root
        for char in str1:
            new_node = current_node.add_node(char)
            current_node = new_node
        uni = current_node.add_node(str1)
        uni.unique = True



    def say(self):
        self.root.say()