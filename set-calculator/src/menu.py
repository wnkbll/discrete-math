import os

from src.types import Scene, Option, Input


def clear() -> None:
    os.system("cls") if os.name == "nt" else os.system("clear")


def __draw_header() -> None:
    print("Лабораторная работа #1 | Теория множеств: основные операции")
    print("Source code: https://github.com/wnkbll/set-wrapper")


def __draw_scene_with_input(scene: Scene) -> None:
    for console_string in scene.console_strings:
        line = console_string.line
        text = line.text
        if isinstance(line, Option):
            key = line.keybind
            print(f"[{key}] - {text}")
        else:
            print(f"{text}")

    response = input("\n>> ")

    for console_string in scene.console_strings:
        if isinstance(console_string.line, Input):
            return console_string.line.event(response)


def draw(scene: Scene, *args):
    clear()
    __draw_header()

    print(f"\n{scene.title}\n")

    if scene.has_input:
        return __draw_scene_with_input(scene)

    for console_string in scene.console_strings:
        line = console_string.line
        text = line.text
        if isinstance(line, Option):
            key = line.keybind
            print(f"[{key}] - {text}")
        else:
            print(f"{text}")

    print("\n\n[0] - Выход")

    while True:
        response = input("\n>> ")

        if response == "0":
            clear()
            return None

        for console_string in scene.console_strings:
            line = console_string.line
            if isinstance(line, Option):
                if response == line.keybind:
                    return line.event(*args)
