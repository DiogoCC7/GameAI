import os


class DisplayColor:
    PINK = '\033[95m'
    GREEN = '\033[91m'
    RED = '\033[32m'
    BLUE = '\033[34m'
    YELLOW = '\033[93m'
    PURPLE = '\033[35m'

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def characterToInt(string: str):
    return ord(string.upper()) - ord('A') + 1 - 1


def intToChac(number: int):
    return chr(number + ord('A') - 1)


def printColor(text: str, display_color: DisplayColor):
    return display_color + str(text) + '\033[0m'

def printInfo(text: str):
    return printColor(text, DisplayColor.YELLOW)

def printWarning(text: str):
    return printColor(text, DisplayColor.BLUE)

def printMust(text: str):
    return printColor(text, DisplayColor.PURPLE)

__all__ = [characterToInt, intToChac, printColor, printInfo, printWarning, printMust,clear_screen]
