from src.set_wrapper import SetWrapper


class Context:
    left_border: int = -30
    right_border: int = 30
    current_set_name: str = ""
    sets: dict[str, SetWrapper] = {}


context = Context()
