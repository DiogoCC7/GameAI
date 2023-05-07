from utils.menu.menu import Menu

import msvcrt
import os


class WindowsMenu(Menu):

    ENTER_KEY = 13
    SPACE_KEY = 32
    ARROW_UP_KEY = 72
    ARROW_DOWN_KEY = 80

    def __init__(self, title: str, options: list[str]) -> None:
        super().__init__(title, options)

    def run(self) -> int:

        key = 0

        while key != self.ENTER_KEY:
            os.system("cls" if os.name == "nt" else "clear")
            print(f"\n\t< < {self._title} > >\n")

            self.draw()

            key = ord(msvcrt.getch())

            if key == self.ARROW_UP_KEY:
                self._selected_index -= 1
                if self._selected_index < 0:
                    self._selected_index = len(self._options) - 1
            elif key == self.ARROW_DOWN_KEY:
                self._selected_index += 1
                if self._selected_index > len(self._options) - 1:
                    self._selected_index = 0
            elif key == self.SPACE_KEY:
                return -1

        return self._selected_index
