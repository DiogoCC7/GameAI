class BarcaAction:

    def __init__(self, pos_x, pos_y, move_to_x: int, move_to_y: int):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        
        self.__move_to_x = move_to_x
        self.__move_to_y = move_to_y

    @property
    def pos_x(self):
        return self.__pos_x
    
    @pos_x.setter
    def pos_x(self, value):
        self.__pos_x = value

    @property
    def pos_y(self):
        return self.__pos_y
    
    @pos_y.setter
    def move_to_y(self, value):
        self.__pos_y = value

    @property
    def move_to_x(self):
        return self.__move_to_x
    
    @move_to_x.setter
    def move_to_x(self, value):
        self.__move_to_x = value

    @property
    def move_to_y(self):
        return self.__move_to_y
    
    @move_to_y.setter
    def move_to_y(self, value):
        self.__move_to_y = value

    
