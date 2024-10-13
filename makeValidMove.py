from game_utils import initialize, step, get_valid_col_id, is_end
from simulator import GameController, HumanAgent
from connect_four import ConnectFour


## Task 1.1 Make a valid move

class AIAgent(object):
    """
    A class representing an agent that plays Connect Four.
    """
    def __init__(self, player_id=1):
        """Initializes the agent with the specified player ID.

        Parameters:
        -----------
        player_id : int
            The ID of the player assigned to this agent (1 or 2).
        """
        pass
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
        if is_end(state):
            return

        validMoves = get_valid_col_id(state)
        return validMoves[0]


def test_task_1_1():
    from utils import check_step, actions_to_board
    
    # Test case 1
    res1 = check_step(ConnectFour(), 1, AIAgent)
    assert(res1 == "Pass")
    
    # Test case 2
    res2 = check_step(actions_to_board([0, 0, 0, 0, 0, 0]), 1, AIAgent)
    assert(res2 == "Pass")
    
    # Test case 3
    res2 = check_step(actions_to_board([4, 3, 4, 5, 5, 1, 4, 4, 5, 5]), 1, AIAgent)
    assert(res2 == "Pass")

test_task_1_1()
