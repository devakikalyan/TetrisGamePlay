import sys
sys.path.append("..")
from modules import expectimax
from modules import shape
from modules import grid

def baseline_ai(tetris):
    s = shape.Shape()
    score = 0
    is_playable = True
    initial_arg = tuple((0, 0))
    while is_playable:
        current_shape = expectimax.random_shape_generator()
        print(f"Incoming shape:\n {current_shape}")
        input("Press Enter to continue...")
        moves = []  # Reset moves
        children, _ = expectimax.generate_children(shape=current_shape, state=tetris.grid)
        if children is None or not len(children):
            is_playable = False
            break
        
        best_move = (0, float('-inf'))
        for grid in children:
            current_score = expectimax.base_ai(grid[0].grid)
            if current_score > best_move[1]:
                best_move = (grid[0].grid, current_score)
        
        tetris.grid = best_move[0]
        print(f"Grid state:\n {tetris.grid}")
        score += 1
    print(f"Baseline AI final score: {score}")
    return score


if __name__ == "__main__":
    print("Enter Row and Col size with spaces ex. 6 6")
    rows, cols = map(int, input().split())
    tetris = grid.Grid(rows, cols)  # Set grid size.
   
    valid = [float('inf')]
    print(tetris.grid)

    print(baseline_ai(tetris))




    
    
    
        
        
        
        
        
        
    
    

