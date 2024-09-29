from dataclasses import dataclass
from typing import Callable


@dataclass
class Line:
    text: str


@dataclass
class Option(Line):
    keybind: str
    event: Callable


@dataclass
class Input(Line):
    event: Callable


@dataclass
class ConsoleString:
    y: int
    x: int
    line: Line


@dataclass
class Scene:
    title: str
    has_input: bool
    console_strings: list[ConsoleString]
