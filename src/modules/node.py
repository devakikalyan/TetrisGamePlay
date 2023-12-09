import numpy as np

class Node:
    
    def __init__(self,r,c):
        self.grid = np.zeros((r,c)) #generate grid.
        self.score = 0


    