import curses
from typing import Callable


class Menu:
    def __init__(self, title: str, options: dict[str, tuple[str, Callable]]) -> None:
        self.title = title
        self.options = options


def draw(stdscr: curses.window, menu: Menu = None) -> None:
    stdscr.clear()

    stdscr.addstr("set wrapper learning project\n")
    stdscr.addstr("https://github.com/wnkbll/set-wrapper\n")

    if menu is not None:
        for index, option in enumerate(menu.options.items()):
            key = option[0]
            description = option[1][0]
            stdscr.addstr(3 + index, 0, f"[{key}] - {description}")

    stdscr.addstr("\n\n[0] - to exit")

    key_input = stdscr.getkey()

    if key_input == "0":
        curses.endwin()
        return None

    if menu is not None:
        if key_input in menu.options.keys():
            menu.options[key_input][1](stdscr)
