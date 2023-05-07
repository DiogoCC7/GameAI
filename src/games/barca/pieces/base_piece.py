
class BasePiece():

    def __init__(self,  x: int, y: int) -> None:
        self.__x = x
        self.__y = y
        self.__is_selected = False
        self.__display_value = ''

    @property
    def is_selected(self):
        """
        Check if the piece is selected by the player
        """
        return self.__is_selected

    @property
    def display_value(self) -> str:
        """
        Tells what simbol will display on the console
        """
        return self.__display_value

    @display_value.setter
    def display_value(self, value):
        self.__display_value = value

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y

    def move(self, play_x: int, play_y: int):
        """
        Move the piece, with a given x and y
        """
        self.__x = play_x
        self.__y = play_y

    def select(self):
        """
        Select the piece
        """
        self.__is_selected = True

    def un_select(self):
        """
        Unselect the piece
        """
        self.__is_selected = False
