from game_utils import initialize, step, get_valid_col_id, is_end, is_win, is_valid_col_id
from simulator import GameController, HumanAgent
from connect_four import ConnectFour
from localBaby import LocalBabyAgent
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

    def evaluate(piece, board):
        score = 0
        COLUMN_COUNT = 7
        ROW_COUNT = 6
        WINDOW_LENGTH = 4

        # Score centre column, theoretically best first play
        centre_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        centre_count = centre_array.count(piece)
        score += centre_count * 3

        # Score horizontal positions
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                # Create a horizontal window of 4
                window = row_array[c:c + WINDOW_LENGTH]
                score += AIAgent.evaluate_window(window, piece)

        # Score vertical positions
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                # Create a vertical window of 4
                window = col_array[r:r + WINDOW_LENGTH]
                score += AIAgent.evaluate_window(window, piece)

        # Score positive diagonals
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                # Create a positive diagonal window of 4
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += AIAgent.evaluate_window(window, piece)

        # Score negative diagonals
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                # Create a negative diagonal window of 4
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += AIAgent.evaluate_window(window, piece)

        # the returning -score works in my head after thinging abt it for 3 mins
        # might be fucking weird tho
        return score

    def evaluate_window(window, piece):
        score = 0
        EMPTY = 0
        # Switch scoring based on turn

        # Prioritise a winning move
        # Minimax makes this less important
        if window.count(piece) == 4:
            score += 100
        # Make connecting 3 second priority
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        # Make connecting 2 third priority
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2
        # Minimax makes this less important

        return score

    # depthh = maxDepth
    def minimax(board, depth, alpha, beta, maximizing_player, current_player):
        valid_locations = get_valid_col_id(board)
        is_terminal = is_end(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                # Weight the bot winning really high
                if is_win(board):
                    return (None, 9999999 if maximizing_player else -9999999)
                else:  # No more valid moves
                    return (None, 0)
            else:
                return (None, AIAgent.evaluate(current_player, board))

        if maximizing_player:
            value = -9999999
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
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimising player
            value = 9999999
            # Randomise column to start
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                nextBoard = step(board, column, current_player, False)
                new_score = AIAgent.minimax(nextBoard, depth - 1, alpha, beta, False, 3-current_player)[1]
                if new_score < value:
                    value = new_score
                    # Make 'column' the best scoring column we can get
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
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

        move, _ = AIAgent.minimax(state, 3, -9999999, 9999999, True, self.player_id)

        return move


agent1 = AIAgent(player_id=1)
agent2 = LocalBabyAgent(player_id=2)

board = ConnectFour()
game = GameController(board=board, agents=[agent1, agent2])
game.run()
