from dataclasses import dataclass
from typing import Callable


@dataclass
class Condition:
    dividers: list[int]
    left_border: int = -30
    right_border: int = 30
    is_in_naturals: bool = False
    is_in_integers: bool = False


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
