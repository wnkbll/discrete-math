import copy
import curses
import random
from random import randint
from typing import Callable

from src.context import context
from src.menu import draw
from src.types import ConsoleString, Line, Option, Input, Scene, Condition


def get_condition(conditions: list[str]) -> Condition:
    condition = Condition(
        dividers=[]
    )

    if "xinN" in conditions:
        condition.is_in_integers = True
        condition.is_in_naturals = True

    if "xinZ" in conditions:
        condition.is_in_integers = True

    for _condition in conditions:
        if "xin(" in _condition:
            line = _condition.replace("xin(", "").replace(")", "")
            borders = line.split(";")

            if int(borders[0]) > condition.left_border:
                condition.left_border = int(borders[0])

            if int(borders[1]) < condition.right_border:
                condition.right_border = int(borders[1])

        if "x/" in _condition:
            line = _condition.replace("x/", "")
            condition.dividers.append(int(line))

        if "x>" in _condition:
            if "x>=" in _condition:
                line = _condition.replace("x>=", "")
                if int(line) > condition.left_border:
                    condition.left_border = int(line)
            else:
                line = _condition.replace("x>", "")
                if int(line) > condition.left_border:
                    condition.left_border = int(line) + 1

        if "x<" in _condition:
            if "x<=" in _condition:
                line = _condition.replace("x<=", "")
                if int(line) < condition.right_border:
                    condition.left_border = int(line)
            else:
                line = _condition.replace("x<", "")
                if int(line) < condition.right_border:
                    condition.left_border = int(line) - 1

        if "x=" in _condition:
            line = _condition.replace("x=", "")
            condition.left_border = int(line)
            condition.right_border = int(line)

    return condition


def get_set_from_condition(condition: Condition) -> set:
    set_ = set()

    for number in range(condition.left_border, condition.right_border + 1):
        if condition.is_in_integers and not isinstance(number, int):
            continue

        if condition.is_in_naturals and (not isinstance(number, int) or number < 0):
            continue

        for divider in condition.dividers:
            if number % divider != 0:
                break
        else:
            set_.add(number)

    return set_


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
                ConsoleString(__index + 2, 0, Option("Назад", "1", lambda _: draw(stdscr, MAIN_SCENE)))
            )

            return draw(stdscr, __list_of_sets_scene)

    return __wrapper


def __set_name_input_handler() -> Callable:
    def __wrapper(stdscr: curses.window, string: str) -> None:
        return draw(stdscr, SET_CREATION_SCENE, string)

    return __wrapper


def __set_creation_handler(option: str) -> Callable:
    def __wrapper(stdscr: curses.window, string: str) -> None:
        if option == "back":
            return draw(stdscr, MAIN_SCENE)

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
            context.current_set_name = string

            return draw(stdscr, SET_FROM_KEYBOARD_SCENE)

        if option == "condition":
            context.sets[string] = set()
            context.current_set_name = string

            return draw(stdscr, SET_FROM_CONDITION_SCENE)

    return __wrapper


def __set_created_handler(option: str) -> Callable:
    return __main_menu_handler(option)


def __set_from_keyboard_handler() -> Callable:
    def __wrapper(stdscr: curses.window, string: str) -> None:
        elements = string.strip().split(" ")
        try:
            for element in elements:
                context.sets[context.current_set_name].add(int(element))
        except ValueError:
            pass

        __set_created_scene = copy.deepcopy(SET_CREATED_SCENE)
        __set_created_scene.console_strings[0] = ConsoleString(
            0, 0,
            Line(f"Множество {context.current_set_name} = {context.sets[context.current_set_name]} успешно создано")
        )

        return draw(stdscr, __set_created_scene)

    return __wrapper


def __set_from_condition_handler() -> Callable:
    def __wrapper(stdscr: curses.window, string: str) -> None:
        conditions = string.strip().split(",")
        formatted_conditions = []

        for condition in conditions:
            formatted_conditions.append(condition.replace(" ", ""))

        condition_ = get_condition(formatted_conditions)

        context.sets[context.current_set_name] = get_set_from_condition(condition_)

        __set_created_scene = copy.deepcopy(SET_CREATED_SCENE)
        __set_created_scene.console_strings[0] = ConsoleString(
            0, 0,
            Line(f"Множество {context.current_set_name} = {context.sets[context.current_set_name]} успешно создано")
        )

        return draw(stdscr, __set_created_scene)

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

SET_CREATED_SCENE = Scene(
    title="============ МЕНЮ ============",
    has_input=False,
    console_strings=[
        ConsoleString(0, 0, Line("placeholder")),
        ConsoleString(4, 0, Option("Создать новое множество", "1", __set_created_handler("create-set"))),
        ConsoleString(5, 0, Option("Выполнить действие с множествами", "2", __set_created_handler("action"))),
        ConsoleString(6, 0, Option("Список множеств", "3", __set_created_handler("list-of-sets"))),
    ],
)

SET_FROM_KEYBOARD_SCENE = Scene(
    title="====== СОЗДАТЬ МНОЖЕСТВО ======",
    has_input=True,
    console_strings=[
        ConsoleString(0, 0, Line("Перечислите элементы множества через пробел")),
        ConsoleString(
            1, 0, Line(f"Элементы должны принадлежать промежутку [{context.left_border}, {context.right_border}]")
        ),
        ConsoleString(3, 0, Input("", __set_from_keyboard_handler()))
    ],
)

SET_FROM_CONDITION_SCENE = Scene(
    title="====== СОЗДАТЬ МНОЖЕСТВО ======",
    has_input=True,
    console_strings=[
        ConsoleString(0, 0, Line("Обозначения: ")),
        ConsoleString(2, 0, Line("(a;b) - диапазон")),
        ConsoleString(3, 0, Line("x     - элемент множества")),
        ConsoleString(4, 0, Line("in    - принадлежность ")),
        ConsoleString(5, 0, Line("N     - множество натуральных чисел")),
        ConsoleString(6, 0, Line("Z     - множество целых чисел")),
        ConsoleString(7, 0, Line("/     - кратно ")),
        ConsoleString(8, 0, Line(">     - больше")),
        ConsoleString(9, 0, Line(">=    - больше или равно")),
        ConsoleString(10, 0, Line("<     - меньше")),
        ConsoleString(11, 0, Line("<=    - меньше или равно")),
        ConsoleString(12, 0, Line("=     - равно")),
        ConsoleString(14, 0, Line("Условия перечислять через запятую")),
        ConsoleString(15, 0, Line("Пример: x in N, x / 10, x > 19. Результат {20, 30}")),
        ConsoleString(17, 0, Input("", __set_from_condition_handler())),
    ],
)

LIST_OF_SETS_SCENE = Scene(
    title="======= СПИСОК МНОЖЕСТВ =======",
    has_input=False,
    console_strings=[

    ],
)
