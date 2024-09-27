import curses
import random
from random import randint
from typing import Callable

from src.context import context
from src.menu import ConsoleString, Option, Input, Scene, draw


def __main_menu_handler(option: str) -> Callable:
    def __wrapper(stdscr: curses.window) -> None:
        if option == "create-set":
            draw(stdscr, SET_NAME_INPUT_SCENE)
            return None

        if option == "action":
            pass

        if option == "list-of-sets":
            pass

    return __wrapper


def __set_name_input_handler() -> Callable:
    def __wrapper(stdscr: curses.window, string: str) -> None:
        draw(stdscr, SET_CREATION_SCENE, string)

    return __wrapper


def __set_creation_handler(option: str) -> Callable:
    def __wrapper(stdscr: curses.window, string: str) -> None:
        if option == "back":
            draw(stdscr, MAIN_SCENE)
            return None

        if option == "random":
            context.sets[string] = set()

            length = random.randint(0, 61)
            for i in range(length):
                context.sets[string].add(randint(-30, 30))

            return None

        if option == "keyboard":
            context.sets[string] = set()

        stdscr.addstr(f"\n{option}")
        stdscr.refresh()

    return __wrapper


MAIN_SCENE = Scene(
    title="============ МЕНЮ ============",
    has_input=False,
    console_strings=[
        ConsoleString(0, 0, Option("Создать новое множество", "1", __main_menu_handler("create-set"))),
        ConsoleString(1, 0, Option("Выполнить действие с множествами", "2", __main_menu_handler("action"))),
        ConsoleString(2, 0, Option("Список множеств", "3", __main_menu_handler("list-of-sets"))),
    ],
)

SET_NAME_INPUT_SCENE = Scene(
    title="====== СОЗДАТЬ МНОЖЕСТВО ======",
    has_input=True,
    console_strings=[
        ConsoleString(0, 0, Input("Укажите имя множества: ", __set_name_input_handler()))
    ],
)

SET_CREATION_SCENE = Scene(
    title="====== СОЗДАТЬ МНОЖЕСТВО ======",
    has_input=False,
    console_strings=[
        ConsoleString(0, 0, Option("Случайно", "1", __set_creation_handler("random"))),
        ConsoleString(1, 0, Option("По условию", "2", __set_creation_handler("condition"))),
        ConsoleString(2, 0, Option("Перечислением", "3", __set_creation_handler("keyboard"))),
        ConsoleString(3, 0, Option("Назад", "4", __set_creation_handler("back"))),
    ],
)
