from abc import ABC, abstractmethod

from games.barca.pieces.base_piece import BasePiece

from utils.text_utils import DisplayColor, printColor


class Piece(BasePiece, ABC):

    """
        Base Class of All playable pieces in the game
    """

    def __init__(self, x: int, y: int, is_alternative: bool) -> None:
        super().__init__(x, y)

        self.__is_alternative = is_alternative
        self.__is_must_play = False
        self.display_value = ''


    @property
    def is_alternative(self):
        """
        Is Alternative if the piece belongs to the Player 1, if not belongs to Player 0
        """
        return self.__is_alternative

    @property
    def is_must_play(self):
        """
        If this piece is an dangerous situation, meaning is scared of other pieces this piece is marked has 'Must Play'
        """
        return self.__is_must_play

    @is_must_play.setter
    def is_must_play(self, value: bool):
        self.__is_must_play = value

    @abstractmethod
    def is_valid_play(self, play_x: int, play_y: int):
        """
        Checks the rules of the piece, how it moves
        """
        pass

    @abstractmethod
    def validate_adj(self, pieces: BasePiece) -> bool:
        """
        Verify if has any adjancy with a piece that this piece is afraid of
        """
        pass

    def __str__(self) -> str:
        return printColor(self.display_value, display_color=DisplayColor.PURPLE) \
            if self.is_must_play else printColor(self.display_value, display_color=DisplayColor.PINK) \
            if self.is_selected else printColor(self.display_value, display_color=DisplayColor.GREEN) \
            if self.is_alternative else printColor(self.display_value, display_color=DisplayColor.RED) \
