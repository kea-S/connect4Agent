from game_utils import initialize, step, get_valid_col_id, is_end
from simulator import GameController, HumanAgent
from connect_four import ConnectFour


class LocalBabyAgent(object):
    def __init__(self, player_id):
        pass

    def make_move(self, state):
        if is_end(state):
            return

        validMoves = get_valid_col_id(state)
        return validMoves[0]
