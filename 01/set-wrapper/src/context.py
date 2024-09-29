class Context:
    left_border: int = -30
    right_border: int = 30
    current_set_name: str = ""
    sets: dict[str, set] = {}


context = Context()
