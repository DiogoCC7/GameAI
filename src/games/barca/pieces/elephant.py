from games.barca.pieces.piece import Piece


class Elephant(Piece):

    def __init__(self, x: int, y: int, is_alternative: bool) -> None:
        super().__init__(x, y, is_alternative)
        self.display_value = 'E'

    def validate_adj(self, piece: Piece) -> bool:
        return self.is_alternative != piece.is_alternative and piece.display_value == 'M'

    def copy(self):
        piece = Elephant(self.x, self.y, self.is_alternative)
        piece.is_must_play = self.is_must_play
        return piece

    def is_valid_play(self, play_x: int, play_y: int):
        """
        Moves diagonally, horizontally and vertically
        """

        diff_x = abs(play_x - self.x)
        diff_y = abs(play_y - self.y)

        return (
            (diff_x > 0 and diff_y == 0) or (diff_x == 0 and diff_y > 0) or (diff_x == diff_y) or
            diff_x > 0 and diff_y == 0 or
            diff_x == 0 and diff_y > 0
        )
