import curses
from collections.abc import Callable

from src.context import context
from src.menu import Menu, draw, draw_header


def __main_menu_handler(option: str) -> Callable:
    def __wrapper(stdscr: curses.window) -> None:
        if option == "create-set":
            stdscr.clear()
            draw_header(stdscr)

            stdscr.addstr(f"\n{SET_CREATION_MENU.title}", curses.color_pair(1))

            stdscr.addstr(5, 0, "Укажите имя множества: ")

            curses.echo()
            string = stdscr.getstr().decode()

            context.sets[string] = set()

            draw(stdscr, SET_CREATION_MENU)
            return None

        if option == "action":
            pass

        if option == "list-of-sets":
            pass

    return __wrapper


def __set_creation_handler(option: str) -> Callable:
    def __wrapper(stdscr: curses.window) -> None:
        if option == "back":
            draw(stdscr, MAIN_MENU)
            return None

        if option == "random":
            pass

        stdscr.addstr(f"\n{option}")
        stdscr.refresh()

    return __wrapper


MAIN_MENU = Menu()
MAIN_MENU.title = "============ МЕНЮ ============"
MAIN_MENU.options = {
    "1": ("Создать новое множество", __main_menu_handler("create-set")),
    "2": ("Выполнить действие с множествами", __main_menu_handler("action")),
    "3": ("Список множеств", __main_menu_handler("list-of-sets")),
}

SET_CREATION_MENU = Menu()
SET_CREATION_MENU.title = "====== СОЗДАТЬ МНОЖЕСТВО ======"
SET_CREATION_MENU.options = {
    "1": ("Случайно", __set_creation_handler("random")),
    "2": ("По условию", __set_creation_handler("keyboard")),
    "3": ("Перечислением", __set_creation_handler("condition")),
    "4": ("Назад", __set_creation_handler("back")),
}
