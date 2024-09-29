import curses
import random
import copy
from random import randint
from typing import Callable

from src.context import context
from src.menu import draw
from src.types import ConsoleString, Line, Option, Input, Scene


def __main_menu_handler(option: str) -> Callable:
    def __wrapper(stdscr: curses.window) -> None:
        if option == "create-set":
            return draw(stdscr, SET_NAME_INPUT_SCENE)

        if option == "action":
            pass

        if option == "list-of-sets":
            sets = context.sets
            __list_of_sets_scene = copy.deepcopy(LIST_OF_SETS_SCENE)
            __index = 0
            for index, item in enumerate(sets.items()):
                __list_of_sets_scene.console_strings.append(
                    ConsoleString(index, 0, Line(f"{item[0]} = {item[1]}")),
                )
                __index = index

            __list_of_sets_scene.console_strings.append(
                ConsoleString(__index + 2, 0, Option("Назад", "4", lambda _: draw(stdscr, MAIN_SCENE)))
            )

            return draw(stdscr, __list_of_sets_scene)

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

            length = random.randint(0, 20)
            for i in range(length):
                context.sets[string].add(randint(context.left_border, context.right_border))

            __set_created_scene = copy.deepcopy(SET_CREATED_SCENE)
            __set_created_scene.console_strings[0] = ConsoleString(
                0, 0, Line(f"Множество {string} = {context.sets[string]} успешно создано")
            )

            return draw(stdscr, __set_created_scene)

        if option == "keyboard":
            context.sets[string] = set()

        stdscr.addstr(f"\n{option}")
        stdscr.refresh()

    return __wrapper


def __set_created_handler(option: str) -> Callable:
    return __main_menu_handler(option)


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

SET_CREATED_SCENE = Scene(
    title="============ МЕНЮ ============",
    has_input=False,
    console_strings=[
        ConsoleString(0, 0, Line("placeholder")),
        ConsoleString(2, 0, Option("Создать новое множество", "1", __set_created_handler("create-set"))),
        ConsoleString(3, 0, Option("Выполнить действие с множествами", "2", __set_created_handler("action"))),
        ConsoleString(4, 0, Option("Список множеств", "3", __set_created_handler("list-of-sets"))),
    ],
)

LIST_OF_SETS_SCENE = Scene(
    title="======= СПИСОК МНОЖЕСТВ =======",
    has_input=False,
    console_strings=[

    ],
)
