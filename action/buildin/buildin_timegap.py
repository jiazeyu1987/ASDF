import globalconfig as g
def init_timegap():
    g.time_gap[","] = 1
    g.time_gap["."] = 3
    g.time_gap[";"] = 2
    g.time_gap["，"] = 1
    g.time_gap["；"] = 2
    g.time_gap["。"] = 3
    g.time_gap[" "] = 1
    g.time_gap["\t"] = 3
    g.time_gap["\n"] = 5
    g.time_gap[','] = 1
    g.time_gap['.'] = 3
    g.time_gap[';'] = 2
    g.time_gap['，'] = 1
    g.time_gap['；'] = 2
    g.time_gap['。'] = 3
    g.time_gap[' '] = 1
    g.time_gap['\t'] = 3
    g.time_gap['\n'] = 5