class InnerData:
    OUTER_SEE = 0
    INNER_SEE = 0
    OUTER_LISTEN = 1
    INNER_LISTEN = 1
    FAST_TREE = 2
    def __init__(self,source,value):
        self.value = value
        self.source = source