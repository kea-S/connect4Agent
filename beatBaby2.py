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

    def winning_move(board, piece):
        # Check horizontal locations for win
        COLUMN_COUNT = 7
        ROW_COUNT = 6

        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

    def evaluate(self, board):
        score = 0
        COLUMN_COUNT = 7
        ROW_COUNT = 6
        WINDOW_LENGTH = 4
        piece = self.player_id
        opp_piece = 3 - piece

        def evaluate_window(window, piece):
            score = 0
            EMPTY = 0
            # Switch scoring based on turn
            opp_piece = 3 - piece

            # Prioritise a winning move
            # Make connecting 3 second priority
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 5
            # Make connecting 2 third priority
            elif window.count(piece) == 2 and window.count(EMPTY) == 2:
                score += 2

            if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
                score -= 4

            return score

        # Score centre column, theoretically best first few plays
        centre_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        centre_count = centre_array.count(piece)
        score += centre_count * 3

        # Score horizontal positions
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                # Create a horizontal window of 4
                window = row_array[c:c + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score vertical positions
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                # Create a vertical window of 4
                window = col_array[r:r + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score positive diagonals
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                # Create a positive diagonal window of 4
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        # Score negative diagonals
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                # Create a negative diagonal window of 4
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        # the returning -score works in my head after thinging abt it for 3 mins
        # might be fucking weird tho

        # ok its not switching pieces correctly

        return score

    # depthh = maxDepth
    def minimax(self, board, depth, alpha, beta, maximizing_player, current_player):
        valid_locations = get_valid_col_id(board)
        is_terminal = is_end(board) or is_win(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if AIAgent.winning_move(board, self.player_id):
                    return (None, 100000000000000)
                elif AIAgent.winning_move(board, 3 - self.player_id):
                    return (None, -10000000000000)
                else:
                    return (None, 0)

            return (None, self.evaluate(board))

        if maximizing_player:
            value = float('-inf')
            # Randomise column to start
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                nextBoard = step(board, col, current_player, False)
                new_score = self.minimax(nextBoard, depth - 1, alpha, beta, False, 3 - current_player)[1]
                if new_score > value:
                    value = new_score
                    # Make 'column' the best scoring column we can get
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return column, value

        else:  # Minimising player
            value = float('inf')
            # Randomise column to start
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                nextBoard = step(board, column, current_player, False)
                new_score = self.minimax(nextBoard, depth - 1, alpha, beta, True, 3 - current_player)[1]
                if new_score < value:
                    value = new_score
                    # Make 'column' the best scoring column we can get
                    column = col
                beta = min(beta, value)
                if beta <= alpha:
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

        move, _ = self.minimax(state, 2, float('-inf'), float('inf'), True, self.player_id)

        return move


agent1 = AIAgent(player_id=1)
agent2 = LocalBabyAgent(player_id=2)

board = ConnectFour()
game = GameController(board=board, agents=[agent1, agent2])
game.run()
