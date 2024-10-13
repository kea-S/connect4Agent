from game_utils import initialize, step, get_valid_col_id

c4_board = initialize()

step(c4_board, col_id=2, player_id=2, in_place=True)
step(c4_board, col_id=2, player_id=1, in_place=True)
step(c4_board, col_id=2, player_id=2, in_place=True)
step(c4_board, col_id=2, player_id=1, in_place=True)
step(c4_board, col_id=2, player_id=2, in_place=True)
step(c4_board, col_id=2, player_id=1, in_place=True)
print(c4_board)

print(get_valid_col_id(c4_board))
