class Matrix:
    def __init__(self, array: list[list[int | float]]) -> None:
        self.array: list[list[int | float]] = array

        self.lines: int = len(array)
        self.columns: int = len(array[0])

        self.main_diagonal: list[int | float] = [array[i][i] for i in range(self.lines)]

    @property
    def reflexivity(self) -> bool:
        if sum(self.main_diagonal) == self.columns:
            return True

        return False

    @property
    def irreflexivity(self) -> bool:
        if sum(self.main_diagonal) == 0:
            return True

        return False

    @property
    def properties(self) -> dict[str, str | None]:
        result: dict[str, str | None] = {}

        if self.reflexivity:
            result["reflexivity"] = "reflexive"
        elif self.irreflexivity:
            result["reflexivity"] = "irreflexive"
        else:
            result["reflexivity"] = None

        return result
