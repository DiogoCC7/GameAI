import math
import random
from games.barca.pieces.base_piece import BasePiece
from games.barca.pieces.piece import Piece
from games.barca.player import BarcaPlayer
from games.barca.result import BarcaResult
from games.barca.state import BarcaState

class MinimaxPlayer(BarcaPlayer):

    def __init__(self, name):
        super().__init__(name)
        self.__opponent = 0 if self.get_current_pos() == 1 else 1

    def get_opponent(self):
        return self.__opponent

    def get_action(self, state: BarcaState):
        action = self.minimax(state, 11)

        if not action:
            raise Exception("No valid play")

        print(f'Action: {state.get_grid()[action.move_to_x][action.move_to_y]} Piece {state.get_piece(action.pos_x, action.pos_y)} | My Piece ')

        action.final = True
        return action

    def __must_score(self, state: BarcaState) -> int:
        # get all the pieces of the current player
        minimax_pieces = state.get_player_pieces(self.get_current_pos())

        # get all the pieces that are afraid of opponent's pieces
        must_play_pieces = [piece for piece in minimax_pieces if piece.is_must_play]

        # assign a higher score if there are more must-play pieces
        score = len(must_play_pieces) * 20

        return score
    
    def euclidean_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def __goal_score(self, state: BarcaState, pos_x, pos_y) -> int:
        # # count the number of pieces that are not in the opponent's goal
        # # num_pieces_not_in_goal = sum( 1 for goal in state.get_goals() if goal.has_piece() and state.check_piece_player(goal.content, self.get_current_pos()))

        # num_minimax_goal = state.get_player_goals(self.get_current_pos())

        # # if there are no pieces outside the opponent's goal, the must-score objective has been achieved
        # if num_minimax_goal == 3:
        #     return 100

        # # if there are pieces outside the opponent's goal, return the number of pieces that need to be scored
        # num_pieces_to_be_taken = sum(1 for goal in state.get_goals() if not goal.has_piece() or goal.has_piece() and state.check_piece_player(goal.content, self.get_opponent()))

        # return 20 * num_pieces_to_be_taken

        agent_goals = state.get_player_goals(self.get_current_pos())

        # Get the opponent's goals
        opponent_goals = state.get_player_goals(self.get_opponent())

        # Calculate the difference between the number of agent goals and opponent goals
        goal_difference = len(agent_goals) - len(opponent_goals)

        # If the agent has achieved all its goals, it wins
        if len(agent_goals) == 3:
            return float('inf')

        # If the agent has no goals left, it loses
        if len(agent_goals) == 0:
            return float('-inf')

        # Calculate the distance to the closest agent goal
        min_agent_goal_distance = float('inf')
        for goal in agent_goals:
            distance = self.euclidean_distance(pos_x, pos_y, goal.x, goal.y)
            if distance < min_agent_goal_distance:
                min_agent_goal_distance = distance

        # Calculate the distance to the closest opponent goal
        min_opponent_goal_distance = float('inf')
        for goal in opponent_goals:
            distance = self.euclidean_distance(pos_x, pos_y, goal.x, goal.y)
            if distance < min_opponent_goal_distance:
                min_opponent_goal_distance = distance

        # Calculate the outcome based on the goal difference and the distance to the goals
        outcome = (1000 * goal_difference) - (10 * min_agent_goal_distance) + (5 * min_opponent_goal_distance)

        return outcome

        # Achive 3
        minimax_goals = state.get_player_goals(self.get_current_pos())

        if len(minimax_goals) > 2:
            return 100000
        
        opponent_goals = state.get_player_goals(self.get_opponent())

        print(f"Minimax: {len(minimax_goals)} | Opponent {len(opponent_goals)}")

        if len(minimax_goals) >= 2:
            outcome = 100000
        elif len(opponent_goals) >= 2:
            outcome = -100000
        else:
            outcome = (1000 * len(minimax_goals)) - (2000 * len(opponent_goals))

        print(f"Outcome: {outcome}")
        
        return outcome

        # For each goal gives 1000 points
        outcome = ( 1000 * (len(minimax_goals) + 1) ) + ( - 2000 * (len(opponent_goals) + 1) )


        return outcome

    def __fear_score(self, state: BarcaState) -> int:

        opponent_pieces: list[Piece] = state.get_player_pieces(self.get_opponent())
        minimax_pieces: list[Piece] = state.get_player_pieces(self.get_current_pos())

        # Pieces that the opponent has fear of death
        opponent_fear_pieces = [opponent_piece for mini in minimax_pieces for opponent_piece in opponent_pieces if opponent_piece.validate_adj(mini)]

        num_fear_pieces = len(opponent_fear_pieces)

        # Decrease score based on how many fear pieces the opponent has
        if num_fear_pieces == 0:
            return 0
        elif num_fear_pieces == 1:
            return -10
        elif num_fear_pieces == 2:
            return -20
        elif num_fear_pieces == 3:
            return -30
        else:
            return -40


    def __define_objective_weights(self, state: BarcaState) -> dict[str, float]:

        weights = {
            # 'must_score': .5, 
            'goal_score': .8, 
            # 'fear_score': .2
        }

        return weights

    def minimax(
            self,
            state: BarcaState,
            depth: int,
            alpha: int = -math.inf,
            beta: int = math.inf,
            is_initial_node: bool = True):

        # define the objective weights based on the state and the agent's preferences
        objective_weights = self.__define_objective_weights(state)

        my_pieces = state.get_player_pieces(self.get_current_pos())
        closest_piece = min(my_pieces, key=lambda p: min(self.euclidean_distance(p.x, p.y, g.x, g.y) for g in state.get_player_pieces(self.get_opponent())))

        # calculate the score for each objective based on the current state
        scores = {
            # 'must_score': self.__must_score(state) * objective_weights['must_score'],
            'goal_score': self.__goal_score(state, closest_piece.x, closest_piece.y) * objective_weights['goal_score'],
            # 'fear_score': self.__fear_score(state) * objective_weights['fear_score']
        }

        # calculate the total score by summing the weighted scores for each objective
        total_score = sum(scores.values())

        # first we check if we are in a terminal node (victory, draw or loose)
        if state.is_finished():
            return {
                BarcaResult.WIN: 40,
                BarcaResult.LOOSE: -40,
                BarcaResult.DRAW: 0
            }[state.get_result(self.get_current_pos())]

        # if we reached the maximum depth, we will return the total score
        if depth == 0:
            return total_score
        
        # if we are the acting player
        if self.get_current_pos() == state.get_acting_player():
            best_score = -math.inf
            best_action = None
            # value = -math.inf
            # selected_action = None

            for action in state.get_possible_actions(closest_piece.x, closest_piece.y):
                next_state = state.sim_play(action)

                value = self.minimax(next_state, depth - 1, alpha,
                                beta, False)

                if value > best_score:
                    best_score = value
                    best_action = action

                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            return best_action if is_initial_node else best_score

        # if it is the opponent's turn
        else:
            worst_score = math.inf
            for piece in state.get_player_pieces(self.get_opponent()):
                for action in state.get_possible_actions(piece.x, piece.y):
                    next_state = state.sim_play(action)
                    value = self.minimax(state.sim_play(action), depth - 1, alpha, beta, False)
                    
                    if value < worst_score:
                        worst_score = value
                        
                    beta = min(beta, value)
                    if beta <= alpha:
                        break

            return worst_score

    
    def event_action(self, pos: int, action, new_state: BarcaState):
        # ignore
        pass

    def event_end_game(self, final_state: BarcaState):
        # ignore
        pass
