import curses

from src.menu import draw
from src.scenes import MAIN_MENU


def init_colors() -> None:
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)


def main(stdscr: curses.window) -> None:
    init_colors()

    draw(stdscr, MAIN_MENU)


if __name__ == "__main__":
    curses.wrapper(main)
