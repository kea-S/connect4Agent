from game_utils import initialize, step, get_valid_col_id, is_end, is_win, is_valid_col_id
from simulator import GameController, HumanAgent
from connect_four import ConnectFour
from localBaby import LocalBabyAgent
from evaluationFunctions import evaluate
import numpy as np

# Task 2.1: Defeat the Baby Agent

class AIAgent(object):
    """
    A class representing an agent that plays Connect Four.
    """

    """
    taken evaluation function from website with docs, piece = player
    ev
    """

    # depthh = maxDepth
    def minimax(board, depth, alpha, beta, maximizing_player, current_player):
        valid_locations = get_valid_col_id(board)
        is_terminal = is_end(board) or is_win(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                # Weight the bot winning really high
                if is_win(board):
                    print("win board")
                    print(board)
                    print("win reached by:")
                    print(maximizing_player)
                    return (None, 1000000 if not maximizing_player else -100000)
                else:
                    return (None, 0)
            else:
                return (None, evaluate(current_player, board))

        if maximizing_player:
            value = float('-inf')
            # Randomise column to start
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                nextBoard = step(board, col, current_player, False)
                new_score = AIAgent.minimax(nextBoard, depth - 1, alpha, beta, False, 3 - current_player)[1]
                if new_score > value:
                    value = new_score
                    # Make 'column' the best scoring column we can get
                    column = col
                alpha = max(alpha, value)
                if value >= beta:
                    break

            return column, value

        else:  # Minimising player
            value = float('inf')
            # Randomise column to start
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                nextBoard = step(board, column, current_player, False)
                new_score = AIAgent.minimax(nextBoard, depth - 1, alpha, beta, True, 3-current_player)[1]
                if new_score < value:
                    value = new_score
                    # Make 'column' the best scoring column we can get
                    column = col
                beta = min(beta, value)
                if value <= alpha:
                    break

            return column, value

    def __init__(self, player_id):
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

        # AIAgent.minimax_alpha_beta(state, 0, 3, float('-inf'), float('inf'), self.player_id)
        # self.minimax(state, 3, float('-inf'), float('inf'), self.player_id)
        # AIAgent.get_best_move(state, self.player_id, 3)

        move, _ = AIAgent.minimax(state, 4, float('-inf'), float('inf'), True, self.player_id)

        return move


agent1 = AIAgent(player_id=1)
agent2 = LocalBabyAgent(player_id=2)

board = ConnectFour()
game = GameController(board=board, agents=[agent1, agent2])
game.run()
