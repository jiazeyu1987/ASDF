from .. import *
from . import *
class EntityHandler:
    def __init__(self):
        pass

    def do_exec(self,item:InnerData):
        str1 = item.get_value().get_str()

        # self.change_str1_to_tmp_node()
        # self.link_tmp_node_to_info_node()
        # self.add_info_node()

        info = InfoNode()
        entity_node = EntityNode()
        entity_node.value = str1
        info.add_entity(entity_node)
        print(str1)

eh = EntityHandler()