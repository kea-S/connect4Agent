from game_utils import initialize, step, get_valid_col_id, is_end, is_win, is_valid_col_id
import math
import random

# Task 2.1: Defeat the Baby Agent

class AIAgent(object):
    """
    A class representing an agent that plays Connect Four.
    """

    """
    taken evaluation function from website with docs, piece = player
    ev
    """

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

        # load constants
        PLAYER_ID = self.player_id
        OPP_PIECE = 3 - self.player_id
        COLUMN_COUNT = 7
        ROW_COUNT = 6
        WINDOW_LENGTH = 4
        EMPTY = 0

        def winning_move(board, player):
            # Check horizontal locations for win
            for c in range(COLUMN_COUNT-3):
                for r in range(ROW_COUNT):
                    if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                        return True

            # Check vertical locations for win
            for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT-3):
                    if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                        return True

            # Check positively sloped diaganols
            for c in range(COLUMN_COUNT-3):
                for r in range(ROW_COUNT-3):
                    if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                        return True

            # Check negatively sloped diaganols
            for c in range(COLUMN_COUNT-3):
                for r in range(3, ROW_COUNT):
                    if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                        return True

        def evaluate(board):
            score = 0

            def evaluate_window(window):
                score = 0
                # Switch scoring based on turn

                # Prioritise a winning move
                # Make connecting 3 second priority
                if window.count(PLAYER_ID) == 4:
                    score += 100
                elif window.count(PLAYER_ID) == 3 and window.count(EMPTY) == 1:
                    score += 5
                # Make connecting 2 third priority
                elif window.count(PLAYER_ID) == 2 and window.count(EMPTY) == 2:
                    score += 2

                if window.count(OPP_PIECE) == 3 and window.count(EMPTY) == 1:
                    score -= 4

                return score

            # Score centre column, theoretically best first few plays
            centre_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
            centre_count = centre_array.count(PLAYER_ID)
            score += centre_count * 3

            # Score horizontal positions
            for r in range(ROW_COUNT):
                row_array = [int(i) for i in list(board[r, :])]
                for c in range(COLUMN_COUNT - 3):
                    # Create a horizontal window of 4
                    window = row_array[c:c + WINDOW_LENGTH]
                    score += evaluate_window(window)

            # Score vertical positions
            for c in range(COLUMN_COUNT):
                col_array = [int(i) for i in list(board[:, c])]
                for r in range(ROW_COUNT - 3):
                    # Create a vertical window of 4
                    window = col_array[r:r + WINDOW_LENGTH]
                    score += evaluate_window(window)

            # Score positive diagonals
            for r in range(ROW_COUNT - 3):
                for c in range(COLUMN_COUNT - 3):
                    # Create a positive diagonal window of 4
                    window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                    score += evaluate_window(window)

            # Score negative diagonals
            for r in range(ROW_COUNT - 3):
                for c in range(COLUMN_COUNT - 3):
                    # Create a negative diagonal window of 4
                    window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                    score += evaluate_window(window)

            # the returning -score works in my head after thinging abt it for 3 mins
            # might be fucking weird tho

            # ok its not switching pieces correctly

            return score

        # depthh = maxDepth
        def minimax(board, depth, alpha, beta, maximizing_player, current_player):
            valid_locations = get_valid_col_id(board)
            is_terminal = is_end(board) or is_win(board)
            if depth == 0 or is_terminal:
                if is_terminal:
                    if winning_move(board, PLAYER_ID):
                        return (None, 100000000000000)
                    elif winning_move(board, OPP_PIECE):
                        return (None, -100000000000000)
                    else:
                        return (None, 0)

                return (None, evaluate(board))

            if maximizing_player:
                value = -math.inf
                # Randomise column to start
                column = random.choice(valid_locations)
                for col in valid_locations:
                    nextBoard = step(board, col, current_player, False)
                    new_score = minimax(nextBoard, depth - 1, alpha, beta, False, 3 - current_player)[1]
                    if new_score > value:
                        value = new_score
                        # Make 'column' the best scoring column we can get
                        column = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break

                return column, value

            else:  # Minimising player
                value = math.inf
                # Randomise column to start
                column = random.choice(valid_locations)
                for col in valid_locations:
                    nextBoard = step(board, column, current_player, False)
                    new_score = minimax(nextBoard, depth - 1, alpha, beta, True, 3 - current_player)[1]
                    if new_score < value:
                        value = new_score
                        # Make 'column' the best scoring column we can get
                        column = col
                    beta = min(beta, value)
                    if beta <= alpha:
                        break

                return column, value

        move, _ = minimax(state, 3, -math.inf, math.inf, True, PLAYER_ID)

        return move
