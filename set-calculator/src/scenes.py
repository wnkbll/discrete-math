import copy
import random
from typing import Callable

from src.context import context
from src.menu import draw
from src.set_wrapper import SetWrapper
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
        if "xin[" in _condition:
            line = _condition.replace("xin[", "").replace("]", "")
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


def __home_button_handler() -> Callable:
    def __wrapper() -> None:
        draw(MAIN_SCENE)

    return __wrapper


def __main_menu_handler(option: str) -> Callable:
    def __wrapper() -> None:
        if option == "create-set":
            return draw(SET_NAME_INPUT_SCENE)

        if option == "action":
            sets = context.sets
            __action_scene = copy.deepcopy(ACTION_SCENE)

            __action_scene.console_strings.append(
                ConsoleString(Line("Существующие множества:")),
            )

            for index, item in enumerate(sets.items()):
                __action_scene.console_strings.append(
                    ConsoleString(Line(f"{item[0]} = {item[1]}")),
                )

            __action_scene.console_strings.append(
                ConsoleString(Line(""))
            )
            __action_scene.console_strings.append(
                ConsoleString(Line(">> - принадлежность"))
            )
            __action_scene.console_strings.append(
                ConsoleString(Line("*  - пересечение"))
            )
            __action_scene.console_strings.append(
                ConsoleString(Line("+  - объединение"))
            )
            __action_scene.console_strings.append(
                ConsoleString(Line("-  - разность"))
            )
            __action_scene.console_strings.append(
                ConsoleString(Line("~  - дополнение до универсума"))
            )
            __action_scene.console_strings.append(
                ConsoleString(Line("^  - симметрическая разность"))
            )
            __action_scene.console_strings.append(
                ConsoleString(Input("", __action_handler()))
            )

            return draw(__action_scene)

        if option == "list-of-sets":
            sets = context.sets
            __list_of_sets_scene = copy.deepcopy(LIST_OF_SETS_SCENE)
            for index, item in enumerate(sets.items()):
                __list_of_sets_scene.console_strings.append(
                    ConsoleString(Line(f"{item[0]} = {item[1]}")),
                )

            __list_of_sets_scene.console_strings.append(
                ConsoleString(Line(""))
            )

            __list_of_sets_scene.console_strings.append(
                ConsoleString(Option("Назад", "1", __home_button_handler()))
            )

            return draw(__list_of_sets_scene)

    return __wrapper


def __set_name_input_handler() -> Callable:
    def __wrapper(string: str) -> None:
        return draw(SET_CREATION_SCENE, string)

    return __wrapper


def __set_creation_handler(option: str) -> Callable:
    def __wrapper(string: str) -> None:
        if option == "back":
            return draw(MAIN_SCENE)

        if option == "random":
            context.sets[string] = SetWrapper(set())

            length = random.randint(0, 20)
            for i in range(length):
                context.sets[string].add(random.randint(context.left_border, context.right_border))

            __set_created_scene = copy.deepcopy(SET_CREATED_SCENE)
            __set_created_scene.console_strings = [
                ConsoleString(Line(f"Множество {string} = {context.sets[string]} успешно создано")),
                ConsoleString(Line("")),
                ConsoleString(Option("Создать новое множество", "1", __set_created_handler("create-set"))),
                ConsoleString(Option("Выполнить действие с множествами", "2", __set_created_handler("action"))),
                ConsoleString(Option("Список множеств", "3", __set_created_handler("list-of-sets"))),
            ]

            return draw(__set_created_scene)

        if option == "keyboard":
            context.sets[string] = SetWrapper(set())
            context.current_set_name = string

            return draw(SET_FROM_KEYBOARD_SCENE)

        if option == "condition":
            context.sets[string] = SetWrapper(set())
            context.current_set_name = string

            return draw(SET_FROM_CONDITION_SCENE)

    return __wrapper


def __set_created_handler(option: str) -> Callable:
    return __main_menu_handler(option)


def __set_from_keyboard_handler() -> Callable:
    def __wrapper(string: str) -> None:
        elements = string.strip().split(" ")
        try:
            for element in elements:
                context.sets[context.current_set_name].add(int(element))
        except ValueError:
            pass

        __set_created_scene = copy.deepcopy(SET_CREATED_SCENE)
        __set_created_scene.console_strings = [
            ConsoleString(Line(
                f"Множество {context.current_set_name} = {context.sets[context.current_set_name]} успешно создано")),
            ConsoleString(Line("")),
            ConsoleString(Option("Создать новое множество", "1", __set_created_handler("create-set"))),
            ConsoleString(Option("Выполнить действие с множествами", "2", __set_created_handler("action"))),
            ConsoleString(Option("Список множеств", "3", __set_created_handler("list-of-sets"))),
        ]

        return draw(__set_created_scene)

    return __wrapper


def __set_from_condition_handler() -> Callable:
    def __wrapper(string: str) -> None:
        conditions = string.strip().split(",")
        formatted_conditions = []

        for condition in conditions:
            formatted_conditions.append(condition.replace(" ", ""))

        condition_ = get_condition(formatted_conditions)

        context.sets[context.current_set_name] = get_set_from_condition(condition_)

        __set_created_scene = copy.deepcopy(SET_CREATED_SCENE)
        __set_created_scene.console_strings = [
            ConsoleString(Line(
                f"Множество {context.current_set_name} = {context.sets[context.current_set_name]} успешно создано")),
            ConsoleString(Line("")),
            ConsoleString(Option("Создать новое множество", "1", __set_created_handler("create-set"))),
            ConsoleString(Option("Выполнить действие с множествами", "2", __set_created_handler("action"))),
            ConsoleString(Option("Список множеств", "3", __set_created_handler("list-of-sets"))),
        ]

        return draw(__set_created_scene)

    return __wrapper


def __action_handler() -> Callable:
    def __wrapper(string: str) -> None:
        for key in context.sets.keys():
            if key in string:
                string = string.replace(key, f"context.sets['{key}']")

        result = eval(string)

        if isinstance(result, bool):
            __action_done_scene = copy.deepcopy(ACTION_DONE_SCENE)
            __action_done_scene.console_strings = [
                ConsoleString(Line(f"Результат: {result}")),
                ConsoleString(Line("")),
                ConsoleString(Option("Создать новое множество", "1", __action_done_handler("create-set"))),
                ConsoleString(Option("Выполнить действие с множествами", "2", __action_done_handler("action"))),
                ConsoleString(Option("Список множеств", "3", __action_done_handler("list-of-sets"))),
            ]

            return draw(__action_done_scene)

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for letter in alphabet:
            if letter not in context.sets.keys():
                context.sets[letter] = result
                context.current_set_name = letter
                break

        __action_done_scene = copy.deepcopy(ACTION_DONE_SCENE)
        __action_done_scene.console_strings = [
            ConsoleString(Line(f"Результат: {context.current_set_name} = {context.sets[context.current_set_name]}")),
            ConsoleString(Line("")),
            ConsoleString(Option("Создать новое множество", "1", __action_done_handler("create-set"))),
            ConsoleString(Option("Выполнить действие с множествами", "2", __action_done_handler("action"))),
            ConsoleString(Option("Список множеств", "3", __action_done_handler("list-of-sets"))),
        ]

        return draw(__action_done_scene)

    return __wrapper


def __action_done_handler(option: str) -> Callable:
    return __main_menu_handler(option)


MAIN_SCENE = Scene(
    title="============ МЕНЮ ============",
    has_input=False,
    console_strings=[
        ConsoleString(Option("Создать новое множество", "1", __main_menu_handler("create-set"))),
        ConsoleString(Option("Выполнить действие с множествами", "2", __main_menu_handler("action"))),
        ConsoleString(Option("Список множеств", "3", __main_menu_handler("list-of-sets"))),
    ],
)

SET_NAME_INPUT_SCENE = Scene(
    title="====== СОЗДАТЬ МНОЖЕСТВО ======",
    has_input=True,
    console_strings=[
        ConsoleString(Input("Укажите имя множества: ", __set_name_input_handler()))
    ],
)

SET_CREATION_SCENE = Scene(
    title="====== СОЗДАТЬ МНОЖЕСТВО ======",
    has_input=False,
    console_strings=[
        ConsoleString(Option("Случайно", "1", __set_creation_handler("random"))),
        ConsoleString(Option("По условию", "2", __set_creation_handler("condition"))),
        ConsoleString(Option("Перечислением", "3", __set_creation_handler("keyboard"))),
        ConsoleString(Option("Назад", "4", __set_creation_handler("back"))),
    ],
)

SET_CREATED_SCENE = Scene(
    title="============ МЕНЮ ============",
    has_input=False,
    console_strings=[

    ],
)

SET_FROM_KEYBOARD_SCENE = Scene(
    title="====== СОЗДАТЬ МНОЖЕСТВО ======",
    has_input=True,
    console_strings=[
        ConsoleString(Line("Перечислите элементы множества через пробел")),
        ConsoleString(
            Line(f"Элементы должны принадлежать промежутку [{context.left_border}, {context.right_border}]")
        ),
        ConsoleString(Input("", __set_from_keyboard_handler()))
    ],
)

SET_FROM_CONDITION_SCENE = Scene(
    title="====== СОЗДАТЬ МНОЖЕСТВО ======",
    has_input=True,
    console_strings=[
        ConsoleString(Line("Обозначения: ")),
        ConsoleString(Line("[a;b] - диапазон")),
        ConsoleString(Line("x     - элемент множества")),
        ConsoleString(Line("in    - принадлежность ")),
        ConsoleString(Line("N     - множество натуральных чисел")),
        ConsoleString(Line("Z     - множество целых чисел")),
        ConsoleString(Line("/     - кратно ")),
        ConsoleString(Line(">     - больше")),
        ConsoleString(Line(">=    - больше или равно")),
        ConsoleString(Line("<     - меньше")),
        ConsoleString(Line("<=    - меньше или равно")),
        ConsoleString(Line("=     - равно")),
        ConsoleString(Line("Условия перечислять через запятую")),
        ConsoleString(Line("Пример: x in N, x / 10, x > 19. Результат {20, 30}")),
        ConsoleString(Input("", __set_from_condition_handler())),
    ],
)

ACTION_SCENE = Scene(
    title="==== ОПЕРАЦИЯ С МНОЖЕСТВАМИ ====",
    has_input=True,
    console_strings=[

    ],
)

ACTION_DONE_SCENE = Scene(
    title="============ МЕНЮ ============",
    has_input=False,
    console_strings=[

    ],
)

LIST_OF_SETS_SCENE = Scene(
    title="======= СПИСОК МНОЖЕСТВ =======",
    has_input=False,
    console_strings=[

    ],
)
