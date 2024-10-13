from game_utils import initialize, step, get_valid_col_id, is_end
from simulator import GameController, HumanAgent
from connect_four import ConnectFour
from localBaby import LocalBabyAgent
import numpy as np

def evaluate(player, state):
        max, min = 0, 0
        if player == 1:
            max, min = 1, 2
        else:
            max, min = 2, 1

        def count_n_in_any_direction(state, player, n):
            count = 0
            rows, cols = state.shape
            # Check rows
            for row in state:
                for i in range(cols - n + 1):
                    if np.all(row[i:i+n] == player):
                        count += 1
            # Check columns
            for col in range(cols):
                for i in range(rows - n + 1):
                    if np.all(state[i:i+n, col] == player):
                        count += 1
            # Check diagonals (top-left to bottom-right)
            for r in range(rows - n + 1):
                for c in range(cols - n + 1):
                    if np.all(state[r:r+n, c:c+n].diagonal() == player):
                        count += 1
            # Check anti-diagonals (top-right to bottom-left)
            for r in range(rows - n + 1):
                for c in range(2, cols):
                    if np.all(np.fliplr(state[r:r+n, c-n+1:c+1]).diagonal() == player):
                        count += 1
            return count

        fourCountMax = count_n_in_any_direction(state, max, 4)
        fourCountMin = count_n_in_any_direction(state, min, 4)
        threeCountMax = count_n_in_any_direction(state, max, 3)
        threeCountMin = count_n_in_any_direction(state, min, 3)
        twoCountMax = count_n_in_any_direction(state, max, 2)
        twoCountMin = count_n_in_any_direction(state, min, 2)

        return 1000 * (fourCountMax - fourCountMin) +\
            10 * (threeCountMax - threeCountMin) +\
            (twoCountMax - twoCountMin)

board = initialize()
step(board, col_id=2, player_id=1, in_place=True)
step(board, col_id=2, player_id=1, in_place=True)
step(board, col_id=2, player_id=1, in_place=True)
step(board, col_id=2, player_id=1, in_place=True)
step(board, col_id=3, player_id=2, in_place=True)
step(board, col_id=3, player_id=2, in_place=True)
step(board, col_id=3, player_id=2, in_place=True)
step(board, col_id=4, player_id=2, in_place=True)
print(board)
print(evaluate(2, board))
