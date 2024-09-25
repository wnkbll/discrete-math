import curses
from collections.abc import Callable

from src.menu import Menu, draw


def __main_menu_handler(option: str) -> Callable:
    def __wrapper(stdscr: curses.window) -> None:
        if option == "create-set":
            draw(stdscr, SET_CREATION_MENU)
            return None

        if option == "enter-formula":
            return None

    return __wrapper


def __set_creation_handler(option: str) -> Callable:
    def __wrapper(stdscr: curses.window) -> None:
        if option == "back":
            draw(stdscr, MAIN_MENU)
            return None

        stdscr.addstr(f"\n{option}")
        stdscr.refresh()

    return __wrapper


MAIN_MENU = Menu(
    "Main menu",
    {
        "1": ("Create new set", __main_menu_handler("create-set")),
        "2": ("Enter formula", __main_menu_handler("enter-formula")),
    }
)

SET_CREATION_MENU = Menu(
    "Choose type of set creation:",
    {
        "1": ("random", __set_creation_handler("random")),
        "2": ("keyboard", __set_creation_handler("keyboard")),
        "3": ("condition", __set_creation_handler("condition")),
        "4": ("go back", __set_creation_handler("back"))
    }
)
