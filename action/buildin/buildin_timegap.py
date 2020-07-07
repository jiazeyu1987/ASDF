import globalconfig as g
def init_timegap():
    g.time_gap[","] = 1
    g.time_gap["."] = 5
    g.time_gap[";"] = 3
    g.time_gap["，"] = 1
    g.time_gap["；"] = 3
    g.time_gap["。"] = 5
    g.time_gap[" "] = 1
    g.time_gap["\t"] = 5
    g.time_gap["\n"] = 10