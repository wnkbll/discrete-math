import curses

from src.menu import draw
from src.scenes import MAIN_SCENE


def main(stdscr: curses.window) -> None:
    draw(stdscr, MAIN_SCENE)


if __name__ == "__main__":
    curses.wrapper(main)
