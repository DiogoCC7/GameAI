from games.barca.pieces.piece import Piece


class Lion(Piece):

    def __init__(self, x: int, y: int, is_alternative: bool) -> None:
        super().__init__(x, y, is_alternative)
        self.display_value = 'L'

    def validate_adj(self, piece: Piece) -> bool:
        return self.is_alternative != piece.is_alternative and piece.display_value == 'E'

    def copy(self):
        return Lion(self.x, self.y, self.is_alternative)

    def is_valid_play(self, play_x: int, play_y: int):

        """
        Moves only diagonally
        """

        diff_x = abs(play_x - self.x)
        diff_y = abs(play_y - self.y)
        return (diff_x == diff_y)
