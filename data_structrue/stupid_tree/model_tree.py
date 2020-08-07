from . import *
from .. import *
class ModelTree:
    def __init__(self):
        self._tree = StupidTree()

    def add_model(self,chain:SimpleNodeChain):
        self._tree.add_chain(chain)

    def get_model(self,chain:SimpleNodeChain):
        self._tree.get_chain(chain)

mt = ModelTree()