import numpy as np

# def evaluate(player, state):
#         max, min = 0, 0
#         if player == 1:
#             max, min = 1, 2
#         else:
#             max, min = 2, 1
#
#         def count_n_in_any_direction(state, player, n):
#             count = 0
#             rows, cols = state.shape
#             # Check rows
#             for row in state:
#                 for i in range(cols - n + 1):
#                     if np.all(row[i:i+n] == player):
#                         count += 1
#             # Check columns
#             for col in range(cols):
#                 for i in range(rows - n + 1):
#                     if np.all(state[i:i+n, col] == player):
#                         count += 1
#             # Check diagonals (top-left to bottom-right)
#             for r in range(rows - n + 1):
#                 for c in range(cols - n + 1):
#                     if np.all(state[r:r+n, c:c+n].diagonal() == player):
#                         count += 1
#             # Check anti-diagonals (top-right to bottom-left)
#             for r in range(rows - n + 1):
#                 for c in range(2, cols):
#                     if np.all(np.fliplr(state[r:r+n, c-n+1:c+1]).diagonal() == player):
#                         count += 1
#             return count
#
#         fourCountMax = count_n_in_any_direction(state, max, 4)
#         fourCountMin = count_n_in_any_direction(state, min, 4)
#         threeCountMax = count_n_in_any_direction(state, max, 3)
#         threeCountMin = count_n_in_any_direction(state, min, 3)
#         twoCountMax = count_n_in_any_direction(state, max, 2)
#         twoCountMin = count_n_in_any_direction(state, min, 2)
#
#         return 10 * (fourCountMax - fourCountMin) +\
#             5 * (threeCountMax - threeCountMin) +\
#             2 * (twoCountMax - twoCountMin)

def evaluate(piece, board):
    score = 0
    COLUMN_COUNT = 7
    ROW_COUNT = 6
    WINDOW_LENGTH = 4
    piece = 1

    def evaluate_window(window, piece):
        piece = 1
        score = 0
        EMPTY = 0
        # Switch scoring based on turn
        opp_piece = 3 - piece

        # Prioritise a winning move
        # Make connecting 3 second priority
        if window.count(piece) == 4:
            score = 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        # Make connecting 2 third priority
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 4:
            score = -100
        elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

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
