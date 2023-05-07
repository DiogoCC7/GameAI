from games.barca.pieces.piece import Piece


class Mouse(Piece):

    """
        Class that represents the piece Mouse
    """

    def __init__(self, x, y, is_alternative: bool) -> None:
        super().__init__(x, y, is_alternative)
        self.display_value = 'M'

    def validate_adj(self, piece: Piece) -> bool:
        return self.is_alternative != piece.is_alternative and piece.display_value == 'L'

    def copy(self):
        return Mouse(self.x, self.y, self.is_alternative)

    def is_valid_play(self, play_x: int, play_y: int):
        """
        Moves only horizontally or vertically
        """

        diff_x = abs(play_x - self.x)
        diff_y = abs(play_y - self.y)
        return (diff_x > 0 and diff_y == 0) or (diff_x == 0 and diff_y > 0)
