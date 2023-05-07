from abc import ABC, abstractmethod

class Menu(ABC):

    def __init__(self, title: str, options: list[str]) -> None:
        self._title = title
        self._options = options
        self._selected_index = 0

    def draw(self):
        for i in range(len(self._options)):
            if i == self._selected_index:
                print(f"\n\t >> {self._options[i]} <<")
            else:
                print(f"\n\t    {self._options[i]}")

        print("\n\n\tENTER - Select \t  SPACE - Exit")

    @abstractmethod
    def run(self) -> int:
        pass
