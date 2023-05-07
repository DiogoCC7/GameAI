from games.barca.pieces.base_piece import BasePiece
from games.barca.pieces.goal import Goal
from games.barca.player import BarcaPlayer
from games.barca.action import BarcaAction
from games.barca.state import BarcaState
from utils.text_utils import DisplayColor, characterToInt, printColor, printInfo, printMust, printWarning


class HumanPlayer(BarcaPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: BarcaState):
        
        # Check if the player has must play pieces
        human_must_play = state.get_my_must_play_pieces()
        state.display()

        while True:

            try:
                
                # Initial Text
                move_piece_text = f"Player {self.get_current_pos()}, choose a row and column to move your piece (Example: A1): "

                # Get X, Y from Player
                play_piece = input({
                    1: printColor(move_piece_text, DisplayColor.GREEN),
                    0: printColor(move_piece_text, DisplayColor.RED)
                }[state.get_acting_player()])

                # Select a position
                if len(play_piece) < 2:
                    raise Exception(printInfo("Please provid a valid position"))

                # Select a valid second column
                if len(play_piece[:1]) > 2 and len(play_piece[:1]) < 3:
                    raise Exception(printInfo("Please Provid a valid position"))

                # Get the board piece
                piece: BasePiece = state.get_piece(characterToInt(play_piece[0]), int(play_piece[1:]) - 1)

                # Must Select a valid piece
                if isinstance(piece, BasePiece) is False:
                    raise Exception(printWarning('Please, select a valid piece!'))
                
                # Cannot select an opponent piece
                if not state.check_piece_player(piece, self.get_current_pos()):
                    raise Exception(printWarning("You cannot select an opponent piece!"))
                
                # Verify Must Play Piece
                if human_must_play > 0:
                    
                    # Check if played must play piece
                    if not state.play_must_play_piece(piece):
                        raise Exception(printMust("You must play a purple piece!"))

                # Display all possible position for the choosen piece
                self.__display_all_possible_position_to_play(state, piece.x, piece.y)
                
                # Select the piece
                piece.select()
                state.display()
                piece.un_select()

                # Move to
                play_to = input(
                    printInfo(f'Move Piece to (Example: A1) [To Exit Play (ENTER)]:')
                )
 
                if len(play_to) == 0:
                    raise Exception()

                return BarcaAction(
                    characterToInt(play_piece[0]),
                    int(play_piece[1:]) - 1,
                    characterToInt(play_to[0]),
                    int(play_to[1:]) - 1
                )

            except Exception as e:
                print(e)
    
     # Tries to display all possible actions of a specific piece
    def __display_all_possible_position_to_play(self, state: BarcaState, pos_x: int, pos_y: int):
        for action in state.get_possible_actions(pos_x, pos_y):
            cell = state.get_piece(action.move_to_x, action.move_to_y)

            # Set the goal to be a possible action
            if isinstance(cell, Goal):
                cell.set_available()
            else:
                state.set_piece(action.move_to_x, action.move_to_y, BarcaState.POSSIBLE_CELL_PLAY)

    def event_action(self, pos: int, action, new_state: BarcaState):
        # ignore
        pass

    def event_end_game(self, final_state: BarcaState):
        # ignore
        pass
