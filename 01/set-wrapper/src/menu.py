import curses
from typing import Any

from src.types import Scene, Option, Input


def is_in_max_size(stdscr: curses.window, scene: Scene) -> bool:
    y, _ = stdscr.getmaxyx()

    for console_string in scene.console_strings:
        if 5 + console_string.y > y:
            return False

    return True


def resize_window(stdscr: curses.window, scene: Scene) -> None:
    y_values = []

    for console_string in scene.console_strings:
        y_values.append(console_string.y)

    max_y = max(y_values)

    _, x = stdscr.getmaxyx()
    curses.resize_term(max_y + 15, x)


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


def draw(stdscr: curses.window, scene: Scene, *args) -> Any | None:
    if not is_in_max_size(stdscr, scene):
        stdscr.clear()
        resize_window(stdscr, scene)
        stdscr.refresh()

    stdscr.clear()
    draw_header(stdscr)

    stdscr.addstr(f"\n{scene.title}")

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
