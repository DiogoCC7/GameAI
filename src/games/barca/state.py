import itertools
from typing import Optional

from games.barca.action import BarcaAction
from games.barca.pieces.base_piece import BasePiece
from games.barca.pieces.mouse import Mouse
from games.barca.pieces.lion import Lion
from games.barca.pieces.elephant import Elephant
from games.barca.pieces.goal import Goal
from games.barca.pieces.piece import Piece
from games.barca.result import BarcaResult
from games.state import State
from utils.text_utils import DisplayColor, intToChac, printColor


class BarcaState(State):
    EMPTY_CELL = -1
    POSSIBLE_CELL_PLAY = -2

    def __init__(self, size: int = 10):
        super().__init__()

        if size != 10:
            raise Exception("The board of Barca game must be 10x10")
        
        """
        the dimensions of the board
        """
        self.__size = size

        """
        the grid
        """
        self.__grid = [[
            BarcaState.EMPTY_CELL for _i in range(self.__size)
        ] for _j in range(self.__size)]

        """
        counts the number of turns in the current game
        """
        self.__turns_count = 1
        """
        the index of the current acting player
        """
        self.__acting_player = 0
        """
        determine if a winner was found already 
        """
        self.__has_winner = False

        self.__display_initial_pieces()

    def __goals(self) -> list[Goal]:
        """
        Define all the goals
        """
        return [
            Goal(3, 3),
            Goal(3, 6),
            Goal(6, 3),
            Goal(6, 6),
        ]

    def __red_pieces(self) -> list[Piece]:
        """
        Defines the red pieces
        """
        return [
            Lion(1, 3, True),
            Lion(1, 6, True),

            Mouse(1, 4, True),
            Mouse(1, 5, True),

            Elephant(0, 4, True),
            Elephant(0, 5, True)
        ]

    def __green_pieces(self) -> list[Piece]:
        """
        Defines the green pieces
        """
        return [
            Lion(8, 3, False),
            Lion(8, 6, False),

            Mouse(8, 4, False),
            Mouse(8, 5, False),

            Elephant(9, 4, False),
            Elephant(9, 5, False)
        ]
    
    def __display_initial_pieces(self):
        self.__convert_piece_to_board(self.__goals())
        self.__convert_piece_to_board(self.__red_pieces())
        self.__convert_piece_to_board(self.__green_pieces())

    def __convert_piece_to_board(self, array: list[BasePiece]):
        for piece in array:
            self.__grid[piece.x][piece.y] = piece

    def __get_all_playable_pieces(self):
        red = []
        green = []
        goals = []

        for i, row in enumerate(self.__grid):
            for j, _ in enumerate(row):

                piece = self.get_piece(i,j)

                if isinstance(piece, Piece) and piece.is_alternative:
                    if isinstance(piece, Goal) and piece.has_piece() and piece.piece.is_alternative:
                        red.append(piece.content)
                    else:
                        red.append(piece)

                elif isinstance(piece, Piece) and not piece.is_alternative:
                    if isinstance(piece, Goal) and piece.has_piece() and not piece.piece.is_alternative:
                        green.append(piece.content)
                    else:
                        green.append(piece)

                if isinstance(piece, Goal):
                    goals.append(piece)

        return red, green, goals

    def get_goals(self) -> list[Goal]:
        _, _, goals = self.__get_all_playable_pieces()
        return goals

    def get_player_pieces(self, acting_player: int) -> list[Piece]:
        red, green, _ = self.__get_all_playable_pieces()

        return {
            1: red,
            0: green
        }[acting_player]

    def get_player_goals(self, player: int):
        return [goal for goal in self.get_goals() if goal.has_piece() and self.check_piece_player(goal.content, player)]

    def __check_winner(self):
        return len(self.get_player_goals(self.__acting_player)) == 3

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2
    
    def __verify_fear_pieces(self) -> list[list[Piece]]:

        """
        Verify in board what are the pieces that are with fear
        """

        # Array of an Array of each piece that is afraid of each player, 0, 1
        lista = [[], []]

        for i, row in enumerate(self.__grid):
            for j, _ in enumerate(row):

                current_piece: Piece = self.get_piece(i, j)

                if not isinstance(current_piece, BasePiece):
                    continue

                current_piece.is_must_play = False

                if isinstance(current_piece, Goal):
                    if current_piece.has_piece():
                        current_piece = current_piece.content
                    else:
                        continue

                for adj_piece in self.get_adjacent_pieces(current_piece.x, current_piece.y):
                    if current_piece.validate_adj(adj_piece):
                        current_piece.is_must_play = True
                        lista[1 if current_piece.is_alternative else 0].append(current_piece)

        return lista

    def __get_must_play_pieces(self):

        must_play_pieces = [[], []]

        pieces = self.__verify_fear_pieces()[self.get_acting_player()]
        
        for piece in pieces:
            if len(self.get_possible_actions(piece.x, piece.y)) > 0:
                must_play_pieces[1 if piece.is_alternative else 0].append(piece)

        return must_play_pieces
    
    def get_my_must_play_pieces(self) -> int:
        print(self.__get_must_play_pieces()[self.__acting_player])
        return len(self.__get_must_play_pieces()[self.__acting_player])
    
    def play_must_play_piece(self, piece: BasePiece) -> bool:
        
        if piece is BarcaState.EMPTY_CELL:
            return False

        if isinstance(piece, Goal) and piece.has_piece():
            piece = piece.content

        # If this piece does not have possible actions then let play the game
        if len(self.get_possible_actions(piece.x, piece.y)) == 0:
            return True

        if not piece in self.__get_must_play_pieces()[self.__acting_player]:
            return False
        
        piece.is_must_play = False

        return True
    
    def get_adjacent_pieces(self, x: int, y: int) -> list[Piece]:

        # Adjacent pieces
        adj_pieces = []

        combinations = list(itertools.product([-1, 0, 1], repeat=2))
        combinations = [c for c in combinations if c != (0, 0)]

        for c in combinations:

            # Verifies if is possible to play in this cell
            ex_x = x + c[0]
            ex_y = y + c[1]

            if ex_x > self.__size - 1 \
                    or ex_y > self.__size - 1 \
                    or ex_x < 1 \
                    or ex_y < 1:
                continue

            piece = self.__grid[ex_x][ex_y]

            if isinstance(piece, Piece):
                adj_pieces.append(piece)
            elif isinstance(piece, Goal) and piece.has_piece():
                adj_pieces.append(piece.content)

        return adj_pieces
    
    def check_piece_player(self, piece: Piece, player: int):
        
        if not isinstance(piece, BasePiece):
            return False

        if isinstance(piece, Goal):
            piece = piece.content

        if piece.is_alternative and player == 1:
            return True

        if not piece.is_alternative and player == 0:
            return True

        return False
    
    def __dont_jump_piece(self, x_start, y_start, x_end, y_end):

        # combinations
        diff_row = 1 if x_end > x_start else -1 if x_end < x_start else 0
        diff_col = 1 if y_end > y_start else -1 if y_end < y_start else 0

        for i in range(1, max(abs(x_end - x_start), abs(y_end - y_start))):
            row = x_start + i * diff_row
            col = y_start + i * diff_col
            if row < 0 or row >= len(self.__grid) or col < 0 or col >= len(self.__grid[0]):
                return False

            check_piece = self.get_piece(row, col)

            if isinstance(check_piece, Goal) and check_piece.has_piece():
                return False

            if isinstance(check_piece, Piece):
                return False

        return True

    def validate_action(self, action: BarcaAction) -> bool:
        move_to_x = action.move_to_x
        move_to_y = action.move_to_y

        base_piece = self.get_piece(action.pos_x, action.pos_y)

        if base_piece is BarcaState.EMPTY_CELL:
            return False

        if isinstance(base_piece, Goal) and not base_piece.has_piece():
            return False

        base_piece = base_piece.content if isinstance(base_piece, Goal) else base_piece

        # valid move_to_x
        if move_to_x < 0 or move_to_x >= self.__size:
            return False

        # valid move_to_yumn
        if move_to_y < 0 or move_to_y >= self.__size:
            return False

        # Verifies the adjency of fear pieces        
        if len([ adj for adj in self.get_adjacent_pieces(action.move_to_x, action.move_to_y) if base_piece.validate_adj(adj) ]) > 0:
            return False
        
        # Verifies if is trying to play on top of a piece
        if isinstance(self.get_piece(action.move_to_x, move_to_y), Piece) or isinstance(self.get_piece(action.move_to_x, move_to_y), Goal) and self.get_piece(action.move_to_x, move_to_y).has_piece():
            return False

        # Verifies if player is trying to move opponents piece
        if not self.check_piece_player(base_piece, self.__acting_player):
            return False
        
        return base_piece.is_valid_play(move_to_x, move_to_y) \
            and self.__dont_jump_piece(action.pos_x, action.pos_y, action.move_to_x, action.move_to_y)

    def update(self, action: BarcaAction):

        # move piece
        self.__move_piece(action)

        for i, row in enumerate(self.__grid):
            for j, _ in enumerate(row):
                if isinstance(self.__grid[i][j], BasePiece):
                    print(f"{self.__grid[i][j]} | {intToChac(self.__grid[i][j].x + 1)} | {self.__grid[i][j].y + 1}")

        # determine if there is a winner
        self.__has_winner = self.__check_winner()

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def __move_piece(self, action: BarcaAction):

        # Goal to Normal
        if isinstance(self.get_piece(action.pos_x, action.pos_y), Goal):
            
            # Goal to Goal
            if isinstance(self.get_piece(action.move_to_x, action.move_to_y), Goal):
                before_goal_piece: Goal = self.get_piece(action.pos_x, action.pos_y)
                move_goal_piece: Goal = self.get_piece(action.move_to_x, action.move_to_y)

                move_goal_piece.content = before_goal_piece.content.copy()
                move_goal_piece.content.move(action.move_to_x, action.move_to_y)
                before_goal_piece.clear_piece()
                return

            goal_piece: BasePiece = self.get_piece(action.pos_x, action.pos_y)
            self.set_piece(action.move_to_x, action.move_to_y, goal_piece.content.copy())

            goal_piece.content.move(action.move_to_x, action.move_to_y)
            goal_piece.clear_piece()
            return

        # Move to Goal
        if isinstance(self.get_piece(action.move_to_x, action.move_to_y), Goal):
            
            before_piece: BasePiece = self.get_piece(action.pos_x, action.pos_y)
            goal_piece: Goal = self.get_piece(action.move_to_x, action.move_to_y)
            goal_piece.content = before_piece.copy()
            goal_piece.content.move(action.move_to_x, action.move_to_y)

            # Sets last location to -1
            self.set_piece(action.pos_x, action.pos_y, BarcaState.EMPTY_CELL)
            return
        
        # Sets Moves the New Piece
        before_piece: BasePiece = self.get_piece(action.pos_x, action.pos_y)
        new_piece: BasePiece = before_piece.copy()
        new_piece.move(action.move_to_x, action.move_to_y)
        self.set_piece(action.move_to_x, action.move_to_y, new_piece)

        # Sets last location to -1
        self.set_piece(action.pos_x, action.pos_y, BarcaState.EMPTY_CELL)
        return


    # Display Cell Content
    def __display_cell(self, row, col):

        cell = self.__grid[row][col]

        if isinstance(cell, BasePiece):
            print(str(cell), end="")
        else:
            print({
                BarcaState.EMPTY_CELL: ' ',
                BarcaState.POSSIBLE_CELL_PLAY: printColor(
                    '+', DisplayColor.YELLOW)
            }[cell], end="")

    # print Board Index
    def __display_numbers(self):
        print('  ', end="")
        for col in range(0, self.__size):
            if col < 10:
                print(' ', end="")
            print(f'{col + 1}', end="")
        print("")

    def __display_separator(self):
        print("  ", end="")
        for _ in range(0, self.__size):
            print("--", end="")
        print("-")

    # Print Board
    def display(self):
        self.__display_numbers()
        self.__display_separator()

        for row in range(0, self.__size):
            print(f"{chr((row + 1) - 1 + ord('A'))} "'|', end="")
            for col in range(0, self.__size):
                self.__display_cell(row, col)
                print('|', end="")
            print("")
            self.__display_separator()

        print("")

    def is_finished(self) -> bool:
        return self.__has_winner

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = BarcaState(self.__size)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner

        for row in range(0, self.__size):
            for col in range(0, self.__size):

                current_piece = self.get_piece(row, col)

                if isinstance(current_piece, BasePiece):
                    cloned_state.set_piece(row, col, current_piece.copy())
                else:
                    cloned_state.set_piece(row, col, current_piece)
                
        return cloned_state

    def get_result(self, pos) -> Optional[BarcaResult]:
        if self.__has_winner:
            return BarcaResult.LOOSE if pos == self.__acting_player else BarcaResult.WIN
        if self.__is_full():
            return BarcaResult.DRAW
        return None

    def get_piece(self, x: int, y: int) -> BasePiece:
        return self.__grid[x][y]

    def set_piece(self, x: int, y: int, value: int|BasePiece):
        self.__grid[x][y] = value
    
    def get_num_rows(self):
        return self.__size

    def get_num_cols(self):
        return self.__size

    def before_results(self):
        pass

    def get_possible_actions(self, pos_x: int, pos_y: int):
        return list(filter(
            lambda action: self.validate_action(action),
            map(
                lambda position: BarcaAction(pos_x, pos_y, position[0], position[1]),
                itertools.product(range(0, self.__size),
                                  range(0, self.__size)))
            ))

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
