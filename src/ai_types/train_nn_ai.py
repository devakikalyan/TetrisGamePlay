import sys
sys.path.append("..")
from modules import expectimax
from modules import shape
from modules import sysvariables
from modules import grid
import torch as tr

DATASET = []

def expecti_AI(tetris, depth):
    SCORE = 0
    playable = True
    
    s = shape.Shape()  # Initialize shape object.
    while(playable):
        actual_shape = expectimax.random_shape_generator()
        moves = []  # reset moves
        moves = expectimax.expectimax(depth, tetris, actual_shape)
        if not len(moves):
            break
        chosen_move, _ = zip(*moves)
        chosen_move = chosen_move[0]
        for move, _ in moves:
            if move.score > chosen_move.score:
                chosen_move = move
            DATASET.append((move.grid, move.score))
        tetris = chosen_move
        SCORE += 1
    return SCORE

def nn_AI(tetris, net):
    s = shape.Shape()
    SCORE = 0
    playable = True
    arg_big = tuple((0, 0))
    while(playable):
        actual_shape = expectimax.random_shape_generator()
        print(f"Incoming shape:\n {actual_shape}")
        input("Press Enter to continue...")
        moves = [] # Reset moves
        children, _ = expectimax.generate_children(shape=actual_shape, state=tetris.grid)
        if children is None or not len(children):
            playable = False
            break

        best = (0, float('+inf'))
        for grid in children:
            curr_input = tr.Tensor(grid[0].grid)
            curr_input = curr_input.reshape(1, 25)
            print(type(curr_input))
            score = net(curr_input)
            if score < best[1]:
                best = (grid[0].grid, score)
        tetris.grid = best[0]
        print(f"Grid state:\n {tetris.grid}")
        SCORE += 1
    print(f"Neural Network AI final score: {SCORE}")
    return SCORE


def run():
    print("--------- Neural Network --- 5 x 5 grid ---- All shapes have same probabilities --- depth = 2 --------------")
    score_keeper = 0
    TOTAL = 2000
    expectiAI_scores = []
    expectiAI_nodes = []
    for i in range(TOTAL):
        sysvariables.NODES = 0  # Reset node counter
        if (i % 200) == 0:
            print(f'Percent complete: {i / TOTAL * 100}')
        tetris = grid.Grid(5, 5)
        curr = expecti_AI(tetris=tetris, depth=1)
        expectiAI_scores.append(curr)
        expectiAI_nodes.append(sysvariables.NODES)
        score_keeper += curr

    print(f'Data points collected: {len(DATASET)}')

    import torch as tr
    dataset_state = []
    dataset_utilities = []
    for a, c in DATASET:
        dataset_state.append(tr.Tensor(a))
        dataset_utilities.append(-1 * c)

    SIZE = int(len(DATASET) * 0.8)
    print(f'size of training dataset: {SIZE}')
    print(f'size of testing dataset: {len(DATASET) - SIZE}')

    training_examples = []
    testing_examples = []
    training_examples.append(dataset_state[:SIZE])
    testing_examples.append(dataset_state[SIZE:])

    training_examples.append(dataset_utilities[:SIZE])
    testing_examples.append(dataset_utilities[SIZE:])

    class LinNet(tr.nn.Module):
        def __init__(self, size, hid_features):
            super(LinNet, self).__init__()
            self.to_hidden = tr.nn.Linear(5 * size, hid_features)
            self.to_midlayer = tr.nn.Linear(hid_features, 1)
            self.to_output = tr.nn.Linear(hid_features, 1)

        def forward(self, x):
            h = tr.sigmoid(self.to_hidden(x.reshape(x.shape[0], -1)))
            h1 = tr.relu(h)
            y = tr.relu(self.to_output(h1))
            return y

        def __del__(self):
            print("Destructor")

    def batch_error(net, batch):
        states, utilities = batch
        u = utilities.reshape(-1, 1).float()
        y = net(states)
        e = tr.sum((y - u)**2) / utilities.shape[0]
        return e

    # whether to loop over individual training examples or batch them
    batched = True

    # Make the network and optimizer
    net = LinNet(size=5, hid_features=5)
    optimizer = tr.optim.SGD(net.parameters(), lr=0.0019)

    # Convert the states and their minimax utilities to tensors
    states, utilities = training_examples
    training_batch = tr.stack(states), tr.tensor(utilities)

    states, utilities = testing_examples
    testing_batch = tr.stack(states), tr.tensor(utilities)

    # Run the gradient descent iterations
    curves = [], []
    print("Training!")
    for epoch in range(10000):
        # zero out the gradients for the next backward pass
        optimizer.zero_grad()

        # batch version (fast)
        if batched:
            e = batch_error(net, training_batch)
            e.backward()
            training_error = e.item()

            with tr.no_grad():
                e = batch_error(net, testing_batch)
                testing_error = e.item()

        # take the next optimization step
        optimizer.step()

        # print/save training progress
        if epoch % 1000 == 0:
            print("%d: %f, %f" % (epoch, training_error, testing_error))

    print("Neural network ready!")

    tetris = grid.Grid(5, 5)
    nn_AI(tetris, net)







        



    