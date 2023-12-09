from modules import grid
from ai_types import baseline_ai,expecti_ai,train_nn_ai

problem_sizes = [(4, 4), (5, 5), (6, 6), (7, 7), (8, 8)]

print("Select a problem size:")
for index, size in enumerate(problem_sizes):
    print(f"num: {index} size: {size}")

selected_index = int(input("Enter the number corresponding to your choice: "))
selected_size = problem_sizes[selected_index]
print(f"Your selected problem size: {selected_size}")

print("Select the player type:")
print("1. Baseline AI  2. Expectimax (Heuristic)  3. NN ")

type = int(input("Enter the number corresponding to your choice: "))
tetris = grid.Grid(selected_size[0], selected_size[1])
print(f"Initial grid state:\n {tetris.grid}")

if type == 1:
    baseline_ai.baseline_ai(tetris)
elif type == 2:
    expecti_ai.expectiAI(tetris)
elif type == 3:
    print("If choosing NN, the problem size is fixed to 5 x 5")
    train_nn_ai.run()
else:
    print("Invalid choice. Please choose a valid player type.")
