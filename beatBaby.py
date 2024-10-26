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
    #     return 1000 * (fourCountMax - fourCountMin) +\
    #         10 * (threeCountMax - threeCountMin) +\
    #         (twoCountMax - twoCountMin)

    def evaluate(player_id, state):
        """
        Evaluates the board state and returns a score based on the player's advantage.
        Parameters:
        -----------
        state : np.ndarray
            A 2D numpy array representing the current state of the game board.
        player_id : int
            The ID of the player for whom the board is being evaluated.
        Returns:
        --------
        int
            A score representing the player's advantage on the board.
        """
        COLUMN_COUNT = 7
        ROW_COUNT = 6
        # Simple evaluation function: count the number of 3-in-a-rows and 2-in-a-rows
        score = 0
        opponent_id = 1 if player_id == 2 else 2
        # Check horizontal, vertical, and diagonal lines for potential scores
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                if state[row][col] == player_id:
                    # Check horizontal
                    if col + 3 < COLUMN_COUNT and all(state[row][c] == player_id for c in range(col, col + 4)):
                        return float('inf')  # Winning move
                    if col + 2 < COLUMN_COUNT and all(state[row][c] == player_id for c in range(col, col + 3)):
                        score += 5
                    if col + 1 < COLUMN_COUNT and all(state[row][c] == player_id for c in range(col, col + 2)):
                        score += 2
                    # Check vertical
                    if row + 3 < ROW_COUNT and all(state[r][col] == player_id for r in range(row, row + 4)):
                        return float('inf')  # Winning move
                    if row + 2 < ROW_COUNT and all(state[r][col] == player_id for r in range(row, row + 3)):
                        score += 5
                    if row + 1 < ROW_COUNT and all(state[r][col] == player_id for r in range(row, row + 2)):
                        score += 2
                    # Check diagonal /
                    if row + 3 < ROW_COUNT and col + 3 < COLUMN_COUNT and all(state[row + i][col + i] == player_id for i in range(4)):
                        return float('inf')  # Winning move
                    if row + 2 < ROW_COUNT and col + 2 < COLUMN_COUNT and all(state[row + i][col + i] == player_id for i in range(3)):
                        score += 5
                    if row + 1 < ROW_COUNT and col + 1 < COLUMN_COUNT and all(state[row + i][col + i] == player_id for i in range(2)):
                        score += 2
                    # Check diagonal \
                    if row + 3 < ROW_COUNT and col - 3 >= 0 and all(state[row + i][col - i] == player_id for i in range(4)):
                        return float('inf')  # Winning move
                    if row + 2 < ROW_COUNT and col - 2 >= 0 and all(state[row + i][col - i] == player_id for i in range(3)):
                        score += 5
                    if row + 1 < ROW_COUNT and col - 1 >= 0 and all(state[row + i][col - i] == player_id for i in range(2)):
                        score += 2
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

        return AIAgent.get_best_move(state, self.player_id, 3)


agent1 = AIAgent(player_id=1)
agent2 = LocalBabyAgent(player_id=2)

board = ConnectFour()
game = GameController(board=board, agents=[agent1, agent2])
game.run()
