import numpy as np

class Grid:

    def __init__ (self, r, c):
        self.grid = np.zeros((r,c))
        self.score = 0 #Initialize score to zero!
        self.children = [] # List of all the children.
        self.max_player = True

