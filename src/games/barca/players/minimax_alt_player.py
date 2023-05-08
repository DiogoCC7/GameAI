import math
import time

from games.barca.player import BarcaPlayer
from games.barca.result import BarcaResult
from games.barca.state import BarcaState
from games.state import State


class MinimaxBarcaPlayerOther(BarcaPlayer):

    def __init__(self, name):
        super().__init__(name)

    '''
    This heuristic will simply count the maximum number of consecutive pieces that the player has
    It's not a great heuristic as it doesn't take into consideration a defensive approach
    '''

    def __heuristic(self, state: BarcaState):

        heuristic_result = 0
            
        # tem algum peça no golo, meu
        player_in_goals = len(state.get_player_goals(self.get_current_pos()))
            
        # Caso cheque aos três = 60
        if player_in_goals > 0:
            heuristic_result = player_in_goals * 20

        # Caso os golos estejam completos
        for piece in state.get_player_not_in_goal():
            for goal_piece in state.get_goals():
                if goal_piece.has_piece() and piece.is_valid_play(goal_piece.x, goal_piece.y) and piece.validate_adj(goal_piece.content) and state.dont_jump_piece(piece.x, piece.y, goal_piece.x, goal_piece.y):
                    heuristic_result += 2

        for piece in state.get_player_not_in_goal():
            for goal in state.get_goals():
                if piece.is_valid_play(goal.x, goal.y) and not goal.has_piece() and state.dont_jump_piece(piece.x, piece.y, goal_piece.x, goal_piece.y):
                    heuristic_result += 10

        if self.get_current_pos() != state.get_acting_player():
            heuristic_result = heuristic_result * -1

        return heuristic_result

    """Implementation of minimax search (recursive, with alpha/beta pruning) :param state: the state for which the 
    search should be made :param depth: maximum depth of the search :param alpha: to optimize the search :param beta: 
    to optimize the search :param is_initial_node: if true, the function will return the action with max ev, 
    otherwise it return the max ev (ev = expected value) """

    def minimax(self,
                state: BarcaState,
                depth: int,
                alpha: int = -math.inf,
                beta: int = math.inf,
                is_initial_node: bool = True):
        
        # first we check if we are in a terminal node (victory, draw or loose)
        if state.is_finished():
            return {
                BarcaResult.WIN: 60,
                BarcaResult.LOOSE: -60,
                BarcaResult.DRAW: 0
            }[state.get_result(self.get_current_pos())]

        # if we reached the maximum depth, we will return the value of the heuristic
        if depth == 0:
            return self.__heuristic(state)

        # if we are the acting player
        if self.get_current_pos() == state.get_acting_player():
            # very small integer
            value = -math.inf
            selected_action = None

            for action in state.get_all_possible_actions():
                pre_value = value
                value = max(
                    value,
                    self.minimax(state.sim_play(action), depth - 1, alpha,
                                 beta, False))
                if value > pre_value:
                    # input("move")
                    selected_action = action
                if value > beta:
                    break
                alpha = max(alpha, value)

            return selected_action if is_initial_node else value

        # if it is the opponent's turn
        else:
            value = math.inf
            for action in state.get_all_possible_actions():
                value = min(
                    value,
                    self.minimax(state.sim_play(action), depth - 1, alpha,
                                 beta, False))
                if value < alpha:
                    break
                beta = min(beta, value)
            return value

    def get_action(self, state: BarcaState):
        
        # time.sleep(1)
        state.display()
        state.get_my_must_play_pieces()

        return self.minimax(state, 2)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
