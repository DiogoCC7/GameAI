from games.barca.pieces.base_piece import BasePiece
from games.barca.pieces.piece import Piece
from utils.text_utils import DisplayColor, printColor

class Goal(BasePiece):

    """
        Class that represents the Objective that each piece has to acquire
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)

        self.display_value = 'O'
        self.__available = False
        self.__content = None

    """
        Get the piece inside the goal

        Returns:
            Piece: if goal has a piece
            int: -1 whether the goal hasn't a piece
    """
    @property
    def is_must_play(self):
        if self.has_piece():
            return self.content.is_must_play
        
        return False

    @is_must_play.setter
    def is_must_play(self, value):
        if self.has_piece():
            self.content.is_must_play = value

    @property
    def content(self) -> Piece | int:
        return self.__content if self.has_piece() else -1

    @content.setter
    def content(self, value):
        self.__content = value

    def move(self, play_x: int, play_y: int):
        if self.has_piece():
            self.content.move(play_x, play_y)
            # self.clear_piece()

    def has_piece(self) -> bool:
        return self.__content is not None
    
    def validate_adj(self, piece: Piece) -> bool:
        if self.has_piece():
            return self.content.validate_adj(piece)
        
        return False

    def clear_piece(self):
        self.content = None

    def set_available(self):
        if not self.has_piece():
            self.__available = True
        
    def copy(self):
        goal = Goal(self.x, self.y)
        goal.content = self.__content

        return goal
    
    def is_valid_play(self, play_x: int, play_y: int):
        """
        Checks the rules of the piece, how it moves
        """
        if self.has_piece():
            self.content.is_valid_play(play_x, play_y)

        return False

    def __str__(self) -> str:
        
        if self.__available:
            self.__available = False
            return printColor(self.display_value, DisplayColor.YELLOW)
        
        if self.is_selected:
            return printColor(self.content, DisplayColor.PINK)
        
        if self.has_piece():
            return printColor(str(self.content), DisplayColor.BLUE)
        
        return printColor(self.display_value, DisplayColor.BLUE)

