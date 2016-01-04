import os

def get_negation_cue():
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, "negation_cue.txt")

    with open(filename,"r") as negation_cue:
        return negation_cue.read().split()
