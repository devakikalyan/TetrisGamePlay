import numpy as np
from modules import shape as s
from modules import grid
from modules import sysvariables

# Pass state into expectimax and it should be able to return the best moves for all the shapes.

def base_ai(state):  # Keeps blocks as low as possible!
    if state is None:
        return -1
    if np.isin(state, [0]).all():
        return state.shape[0]  # Max height
    return np.min(np.nonzero(state)[0])


def compute_score(state):  # Computing the heuristic for each state.
    if state is None:
        return -10
    rows, cols = state.shape
    row_indices, col_indices = np.nonzero(state)
    height = {}
    total_height = 0
    if len(col_indices):
        for idx in range(len(col_indices)):
            if idx not in height:
                height[idx] = rows - row_indices[idx]
                total_height += height[idx]
    return -0.5 * total_height  # Penalize for more aggregate height! 

def random_shape_generator():
    generate_shape = s.Shape()
    probabilities = []
    for shape_key, prob_value in generate_shape.shapeProb.items():
        probabilities.append(prob_value)
    return np.random.choice(generate_shape.shapes_array, 1, p=probabilities)[0]


def generate_children(shape, state):
    row_count, col_count = state.shape
    shape_rows, shape_cols = np.nonzero(shape)
    positions = np.array(list(zip(shape_rows, shape_cols)))
    tetris_shape_obj = s.Shape()
    valid_positions = tetris_shape_obj.valid_positions(shape, state)
    children = []
    
    for row, col in valid_positions:  # Assume only valid actions are returned.
        cache = state.copy()
        for shape_row, shape_col in positions:
            cache[row + shape_row][col + shape_col] = shape[shape_row, shape_col]
        current_grid = grid.Grid(row_count, col_count)
        current_grid.grid = cache
        children.append((current_grid, shape))

    return children, len(valid_positions)


def expectimax(depth, grid, shape):
    tetris_shape_obj = s.Shape()
    if depth == 0:  # Leaf node! (inherited parent score + self score)
        grid.score += compute_score(grid.grid)
        return
    children, score = generate_children(shape=shape, state=grid.grid)
    grid.children.extend(children)
    grid.score += score
    for current_child, _ in grid.children:
        current_child.max_player = not grid.max_player  # Alternating chance and max player!
        current_child.score = grid.score  # Children inherit the parent's score.
        for current_shape in tetris_shape_obj.shapes_array:
            expectimax(depth - 1, current_child, current_shape)
            sysvariables.NODES += 1
    
    # Bottom-up.
    if grid.max_player:  # MaxPlayer
        max_score = grid.score
        for g, current_shape in grid.children:
            if g.score > max_score:
                max_score = g.score
            sysvariables.DATASET.append((g.grid, current_shape, g.score))

        grid.score += max_score
    elif not grid.max_player:  # Chance player (M + C)
        num_children = len(grid.children)
        total_score = 0
        shape_dict = {}
        if num_children:
            for g, current_shape in grid.children:
                if str(current_shape) not in shape_dict:
                    shape_dict[str(current_shape)] = g.score
                else:
                    shape_dict[str(current_shape)] = max(g.score, shape_dict[str(current_shape)])
            for key, value in shape_dict.items():
                total_score += shape_dict[key] * tetris_shape_obj.shapeProb[key]

            grid.score = total_score
        else:
            grid.score = 0

    return children


                












    




    
    

    

    