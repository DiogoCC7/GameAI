from games.barca.player import BarcaPlayer
from games.barca.state import BarcaState
from games.game_simulator import GameSimulator


class BarcaSimulator(GameSimulator):

    def __init__(self, player1: BarcaPlayer, player2: BarcaPlayer, size: int = 10):
        super(BarcaSimulator, self).__init__([player1, player2])

        self.__size = size

    def init_game(self):
        return BarcaState(self.__size)

    def before_end_game(self, state: BarcaState):
        # ignored for this simulator
        pass

    def end_game(self, state: BarcaState):
        # ignored for this simulator
        pass
