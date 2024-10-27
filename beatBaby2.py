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
    # def evaluate(player, state):
    #     max, min = 0, 0
    #     if player == 1:
    #         max, min = 1, 2
    #     else:
    #         max, min = 2, 1
    #
    #     def count_n_in_any_direction(state, player, n):
    #         count = 0
    #         rows, cols = state.shape
    #         # Check rows
    #         for row in state:
    #             for i in range(cols - n + 1):
    #                 if np.all(row[i:i+n] == player):
    #                     count += 1
    #         # Check columns
    #         for col in range(cols):
    #             for i in range(rows - n + 1):
    #                 if np.all(state[i:i+n, col] == player):
    #                     count += 1
    #         # Check diagonals (top-left to bottom-right)
    #         for r in range(rows - n + 1):
    #             for c in range(cols - n + 1):
    #                 if np.all(state[r:r+n, c:c+n].diagonal() == player):
    #                     count += 1
    #         # Check anti-diagonals (top-right to bottom-left)
    #         for r in range(rows - n + 1):
    #             for c in range(2, cols):
    #                 if np.all(np.fliplr(state[r:r+n, c-n+1:c+1]).diagonal() == player):
    #                     count += 1
    #         return count
    #
    #     fourCountMax = count_n_in_any_direction(state, max, 4)
    #     fourCountMin = count_n_in_any_direction(state, min, 4)
    #     threeCountMax = count_n_in_any_direction(state, max, 3)
    #     threeCountMin = count_n_in_any_direction(state, min, 3)
    #     twoCountMax = count_n_in_any_direction(state, max, 2)
    #     twoCountMin = count_n_in_any_direction(state, min, 2)
    #
    #     return 100 * (fourCountMax - fourCountMin) +\
    #         5 * (threeCountMax - threeCountMin) +\
    #         2 * (twoCountMax - twoCountMin)

    """
    taken evaluation function from website with docs, piece = player
    ev
    """

    def evaluate(self, piece, board):
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
        return score if self.player_id == piece else -score

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

    # def max_value(board, depth, max_depth, current_player, a, b):
    #     if depth >= max_depth:
    #         return (AIAgent.evaluate(current_player, board), None)
    #
    #     if is_end(board):
    #         if is_win(board):
    #             return (float('inf'), None)
    #
    #     v = float('-inf')
    #
    #     generatedMoves = get_valid_col_id(board)
    #     moveChosen = np.random.choice(generatedMoves)
    #     # I think the problem is, if get_valid_col_id(board)
    #     # has no valid vols, it generates a tuple of empty arrays
    #
    #     # maybe some weird shit with player id
    #
    #     for move in generatedMoves:
    #         # ok valid question, can I use step here???
    #         nextBoard = step(board, move, current_player, False)
    #         nextScore, _ = AIAgent.min_value(nextBoard, depth + 1, max_depth, 3 - current_player, a, b)
    #         if nextScore > v:
    #             v = nextScore
    #             moveChosen = move
    #         a = max(a, v)
    #         if a >= b:
    #             break
    #
    #     return v, moveChosen
    #
    # def min_value(board, depth, max_depth, current_player, a, b):
    #     if depth >= max_depth:
    #         return (AIAgent.evaluate(current_player, board), None)
    #
    #     if is_end(board):
    #         if is_win(board):
    #             return (float('-inf'), None)
    #
    #     v = float('inf')
    #
    #     generatedMoves = get_valid_col_id(board)
    #
    #     moveChosen = np.random.choice(generatedMoves)
    #
    #     # maybe some weird shit with playerID
    #
    #     for move in generatedMoves:
    #         # ok valid question, can I use step here???
    #         nextBoard = step(board, move, current_player, False)
    #         nextScore, _ = AIAgent.max_value(nextBoard, depth + 1, max_depth, 3 - current_player, a, b)
    #         if nextScore < v:
    #             v = nextScore
    #             moveChosen = move
    #         a = min(b, v)
    #         if v <= a:
    #             break
    #
    #     return v, moveChosen
    #
    # # figure out how to trigger the right thing to start
    # def minimax_alpha_beta(
    #     board,
    #     depth,
    #     max_depth,
    #     alpha,
    #     beta,
    #     current_player
    # ):
    #     v, move = AIAgent.max_value(board, depth, max_depth, current_player, alpha, beta)
    #
    #     return move

    # depthh = maxDepth
    # def minimax(self, board, depth, alpha, beta, current_player):
    #     valid_locations = get_valid_col_id(board)
    #     print("im using stolen minimax!")
    #
    #     is_terminal = is_end(board)
    #     if depth == 0 or is_terminal:
    #         if is_terminal:
    #             # Weight the bot winning really high
    #             if is_win(board):
    #                 if current_player == self.player_id:
    #                     return (None, 9999999)
    #                 else:
    #                     return (None, -9999999)
    #             else:  # No more valid moves
    #                 return (None, 0)
    #         # Return the bot's score
    #         else:
    #             return (None, AIAgent.evaluate(self.player_id, board))
    #
    #     print(current_player)
    #     print(self.player_id)
    #     if current_player == self.player_id:  # maximizing player (bot)
    #         value = -9999999
    #         # Randomise column to start
    #         column = np.random.choice(valid_locations)
    #         for col in valid_locations:
    #             nextBoard = step(board, col, current_player, False)
    #             new_score = self.minimax(nextBoard, depth - 1, alpha, beta, 3-current_player)[1]
    #             if new_score > value:
    #                 value = new_score
    #                 # Make 'column' the best scoring column we can get
    #                 column = col
    #             alpha = max(alpha, value)
    #             if alpha >= beta:
    #                 break
    #         return column, value
    #
    #     else:  # Minimising player
    #         value = 9999999
    #         # Randomise column to start
    #         column = np.random.choice(valid_locations)
    #         for col in valid_locations:
    #             nextBoard = step(board, column, current_player, False)
    #             new_score = self.minimax(nextBoard, depth - 1, alpha, beta, 3-current_player)[1]
    #             if new_score < value:
    #                 value = new_score
    #                 # Make 'column' the best scoring column we can get
    #                 column = col
    #             beta = min(beta, value)
    #             if alpha >= beta:
    #                 break
    #         return column, value

    def minimax(state, depth, alpha, beta, maximizing_player, player_id):
        """
        Minimax algorithm with alpha-beta pruning to find the best move.
        Parameters:
        -----------
        state : np.ndarray
            The current game board, represented as a 2D numpy array.
        depth : int
            The current depth in the game tree.
        alpha : float
            The best value that the maximizer currently can guarantee at that level or above.
        beta : float
            The best value that the minimizer currently can guarantee at that level or above.
        maximizing_player : bool
            True if the current move is for the maximizing player, False otherwise.
        player_id : int
            The ID of the player making the move (1 for Player 1, 2 for Player 2).
        Returns:
        --------
        tuple
            A tuple containing the best score and the best column index for the move.
        """
        valid_columns = get_valid_col_id(state)
        is_terminal = is_end(state)
        if depth == 0 or is_terminal:
            if is_terminal:
                if is_win(state):
                    return (float('inf') if maximizing_player else float('-inf'), None)
                else:  # Game is over, no more valid moves
                    return (0, None)
            else:  # Depth is zero
                return (AIAgent.evaluate(player_id, state), None)
        if maximizing_player:
            value = float('-inf')
            # could it be some weird shit with random choice?
            best_col = np.random.choice(valid_columns)
            for col in valid_columns:
                new_state = step(state, col, player_id, in_place=False)
                new_score, _ = AIAgent.minimax(new_state, depth - 1, alpha, beta, False, player_id)
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Alpha-beta pruning
            return value, best_col
        else:  # Minimizing player
            value = float('inf')
            # could it be some weird shit with random choice?
            best_col = np.random.choice(valid_columns)
            opponent_id = 1 if player_id == 2 else 2
            for col in valid_columns:
                new_state = step(state, col, opponent_id, in_place=False)
                new_score, _ = AIAgent.minimax(new_state, depth - 1, alpha, beta, True, player_id)
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha-beta pruning
            return value, best_col

    def get_best_move(state, player_id, depth):
        """
        Determines the best move for the given player using the minimax algorithm.
        Parameters:
        -----------
        state : np.ndarray
            The current game board, represented as a 2D numpy array.
        player_id : int
            The ID of the player making the move (1 for Player 1, 2 for Player 2).
        depth : int, optional
            The maximum depth to search in the game tree (default is MAX_DEPTH).
        Returns:
        --------
        int
            The column index of the best move for the player.
        """
        _, best_col = AIAgent.minimax(state, depth, float('-inf'), float('inf'), True, player_id)
        return best_col


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

        return AIAgent.get_best_move(state, self.player_id, 3)


agent1 = AIAgent(player_id=1)
agent2 = LocalBabyAgent(player_id=2)

board = ConnectFour()
game = GameController(board=board, agents=[agent1, agent2])
game.run()
