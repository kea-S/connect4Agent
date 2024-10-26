from game_utils import initialize, step, get_valid_col_id, is_end, is_win, is_valid_col_id
from simulator import GameController, HumanAgent
from connect_four import ConnectFour
from localBaby import LocalBabyAgent
import numpy as np

# Task 2.1: Defeat the Baby Agent

class AIAgent(object):
    MOVE_NONE = -1

    """
    A class representing an agent that plays Connect Four.
    """
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

    def max_value(board, depth, max_depth, current_player, a, b):
        if depth >= max_depth:
            return (AIAgent.evaluate(current_player, board), None)

        if is_end(board):
            if is_win(board):
                return (float('inf'), None)
            else:
                return (0, None)

        v = float('-inf')

        generatedMoves = get_valid_col_id(board)
        moveChosen = np.random.choice(generatedMoves)
        # I think the problem is, if get_valid_col_id(board)
        # has no valid vols, it generates a tuple of empty arrays

        # maybe some weird shit with player id

        for move in generatedMoves:
            # ok valid question, can I use step here???
            nextBoard = step(board, move, current_player, False)
            nextScore, _ = AIAgent.min_value(nextBoard, depth + 1, max_depth, 3 - current_player, a, b)
            if nextScore > v:
                v = nextScore
                moveChosen = move
            a = max(a, v)
            if a >= b:
                break

        return v, moveChosen

    def min_value(board, depth, max_depth, current_player, a, b):
        if depth >= max_depth:
            return (AIAgent.evaluate(current_player, board), None)

        if is_end(board):
            if is_win(board):
                return (float('-inf'), None)
            else:
                return (0, None)

        v = float('inf')

        generatedMoves = get_valid_col_id(board)

        moveChosen = np.random.choice(generatedMoves)

        # maybe some weird shit with playerID

        for move in generatedMoves:
            # ok valid question, can I use step here???
            nextBoard = step(board, move, current_player, False)
            nextScore, _ = AIAgent.max_value(nextBoard, depth + 1, max_depth, 3 - current_player, a, b)
            if nextScore < v:
                v = nextScore
                moveChosen = move
            a = min(b, v)
            if v <= a:
                break

        return v, moveChosen

    # figure out how to trigger the right thing to start
    def minimax_alpha_beta(
        board,
        depth,
        max_depth,
        alpha,
        beta,
        current_player
    ):
        v, move = AIAgent.max_value(board, depth, max_depth, current_player, alpha, beta)

        return move

    def __init__(self, player_id=1):
        """Initializes the agent with the specified player ID.

        Parameters:
        -----------
        player_id : int
            The ID of the player assigned to this agent (1 or 2).
        """
        self.player_id = player_id

    def make_move(self, state):
        """
        Determines and returns the next move for the agent based on the current game state.

        Parameters:
        -----------
        state : np.ndarray
            A 2D numpy array representing the current, read-only state of the game board.
            The board contains:
            - 0 for an empty cell,
            - 1 for Player 1's piece,
            - 2 for Player 2's piece.

        Returns:
        --------
        int
            The valid action, ie. a valid column index (col_id) where this agent chooses to drop its piece.
        """
        # this is a bit iffy but I think it should be fine?
        if is_end(state):
            return

        return AIAgent.minimax_alpha_beta(state, 0, 3, float('-inf'), float('inf'), self.player_id)


agent1 = AIAgent(player_id=1)
agent2 = LocalBabyAgent(player_id=2)

board = ConnectFour()
game = GameController(board=board, agents=[agent2, agent1])
game.run()
