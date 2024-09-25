import curses

from src.scenes import MAIN_MENU
from src.menu import draw


def main(stdscr: curses.window) -> None:
    draw(stdscr, MAIN_MENU)


if __name__ == "__main__":
    curses.wrapper(main)
