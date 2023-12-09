import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy import signal
from collections import defaultdict

class Shape:
    def __init__(self):
        self.shape_O = np.array([[1, 1], [1, 1]])  # Square shape
        self.shape_I = np.array([[1, 1, 1, 1]])  # Straight shape
        self.shape_T = np.array([[1, 1, 1], [0, 1, 0]])  # T-shape
        self.shape_J = np.array([[0, 1], [0, 1], [1, 1]])  # J-shape
        self.shape_L = np.array([[1, 0], [1, 0], [1, 1]])  # L-shape
        self.shape_S = np.array([[0, 1, 1], [1, 1, 0]])  # S-shape
        self.shape_Z = np.array([[1, 1, 0], [0, 1, 1]])  # Z-shape
        self.shapes_array = np.array([self.shape_O, self.shape_I, self.shape_T, self.shape_J], dtype=object)
   
        self.shapeProb = {
            str(self.shape_O) : 0.4,
            str(self.shape_I) : 0.2,
            str(self.shape_T) : 0.1,
            str(self.shape_J) : 0.3,
        } 

    def valid_positions(self, shape, grid):
        """
        Finds valid positions on the grid for placing a Tetris shape.
        Returns:
            list: List of valid positions (row, col).
        """
        if grid is None:
            return []
        convolution_result = signal.convolve2d(in1=(1 - grid), in2=shape[::-1, ::-1], mode="valid")
        positions = np.where(convolution_result == np.sum(shape))
        positions_dict = defaultdict(int)
        for row, col in zip(positions[0], positions[1]):
            positions_dict[col] = row
        valid_positions = [(row, col) for col, row in positions_dict.items()]
        return valid_positions

    def print_grid_states(self, shape, grid):
        """
        Prints all valid grid states after placing the Tetris shape.
        """
        rows, cols = grid.shape
        shape_positions = np.array(list(zip(*np.nonzero(shape))))
        valid_positions = self.valid_positions(shape, grid)
        for row, col in valid_positions:
            updated_grid = grid.copy()
            for a, b in shape_positions:
                updated_grid[row + a][col + b] = 1
            print(updated_grid)
            print("\n")

    def plot_state(self, shape, grid):
        """
        Plots the current game state with the Tetris shape.
        """
        rows, cols = grid.shape
        colormap = colors.ListedColormap(['white', 'black'])  # blue -> 0 red -> 1 black -> already present.
        plt.figure(figsize=(cols, rows))
        plt.pcolor(np.fliplr(np.flip(grid)), cmap=colormap, edgecolors='black', linewidths=1)
        plt.show()
        plt.close()

    def player_move(self, shape, grid, valid_positions):
        """
        Simulates a player move by placing the Tetris shape in a valid position on the grid.
        Returns:
            numpy.ndarray: Updated game grid after the player move.
        """
        rows, cols = grid.shape
        shape_positions = np.array(list(zip(*np.nonzero(shape))))
        for row, col in valid_positions:
            updated_grid = grid.copy()
            for a, b in shape_positions:
                updated_grid[row + a][col + b] = 1
            print("\n")
        return updated_grid  # Return the updated grid position.
    






    