def fitness_1(candidate):
    if candidate.mds:
        return 2.0 / candidate.cost
    else:
        return 1.0 / candidate.cost

def fitness_2(candidate):
    if candidate.mds:
        return 1.0 / candidate.cost
    else:
        return 0.0

def fitness_3(candidate):
    if candidate.mds:
        return 100-candidate.cost
    else:
        return 300

def fitness_4(candidate):
    if candidate.cost == 0:
        return -1
    if candidate.mds:
        return 2 + 1.0/candidate.cost
    else:
        return 1.0/candidate.cost