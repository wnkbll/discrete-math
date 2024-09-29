import curses
from typing import Any

from src.types import Scene, Option, Input


def draw_header(stdscr: curses.window) -> None:
    stdscr.addstr("Лабораторная работа #1 | Теория множеств: основные операции\n")
    stdscr.addstr("Source code: https://github.com/wnkbll/set-wrapper\n")


def __draw_scene_with_input(stdscr: curses.window, scene: Scene) -> None:
    curses.echo()

    for console_string in scene.console_strings:
        line = console_string.line
        text = line.text
        if isinstance(line, Option):
            key = line.keybind
            stdscr.addstr(5 + console_string.y, console_string.x, f"[{key}] - {text}")
        else:
            stdscr.addstr(5 + console_string.y, console_string.x, f"{text}")

    string = stdscr.getstr().decode()

    curses.noecho()

    for console_string in scene.console_strings:
        if isinstance(console_string.line, Input):
            return console_string.line.event(stdscr, string)


def draw(stdscr: curses.window, scene: Scene, *args, **kwargs) -> Any | None:
    stdscr.clear()
    draw_header(stdscr)

    stdscr.addstr(f"\n{scene.title}", curses.color_pair(1))

    if scene.has_input:
        return __draw_scene_with_input(stdscr, scene)

    for console_string in scene.console_strings:
        line = console_string.line
        text = line.text
        if isinstance(line, Option):
            key = line.keybind
            stdscr.addstr(5 + console_string.y, console_string.x, f"[{key}] - {text}")
        else:
            stdscr.addstr(5 + console_string.y, console_string.x, f"{text}")

    stdscr.addstr("\n\n[0] - Выход")

    while True:
        key_input = stdscr.getkey()

        if key_input == "0":
            curses.endwin()
            return None

        for console_string in scene.console_strings:
            line = console_string.line
            if isinstance(line, Option):
                if key_input == line.keybind:
                    return line.event(stdscr, *args)
