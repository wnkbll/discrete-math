import curses
from collections import namedtuple
from typing import Callable

ConsoleString = namedtuple("ConsoleString", ["position", "line"])


class Menu:
    title: str
    options: dict[str, tuple[str, Callable]]


class Scene:
    console_strings: list[ConsoleString]


def draw_header(stdscr: curses.window) -> None:
    stdscr.addstr("Лабораторная работа #1 | Теория множеств: основные операции\n")
    stdscr.addstr("Source code: https://github.com/wnkbll/set-wrapper\n")


def draw(stdscr: curses.window, menu: Menu = None) -> None:
    stdscr.clear()

    draw_header(stdscr)

    if menu is not None:
        stdscr.addstr(f"\n{menu.title}", curses.color_pair(1))

        for index, option in enumerate(menu.options.items()):
            key = option[0]
            description = option[1][0]
            stdscr.addstr(5 + index, 0, f"[{key}] - {description}")

    stdscr.addstr("\n\n[0] - Выход")

    while True:
        key_input = stdscr.getkey()

        if key_input == "0":
            curses.endwin()
            return None

        if menu is not None:
            if key_input in menu.options.keys():
                menu.options[key_input][1](stdscr)
                return None
