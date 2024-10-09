class Matrix:
    def __init__(self, array: list[list[int | float]]) -> None:
        self.array: list[list[int | float]] = array

        self.lines: int = len(array)
        self.columns: int = len(array[0])

        self.main_diagonal: list[int | float] = [array[i][i] for i in range(self.lines)]

    @property
    def reflexivity(self) -> str | None:
        if sum(self.main_diagonal) == self.columns:
            return "reflexive"

        if sum(self.main_diagonal) == 0:
            return "irreflexive"

        return None

    @property
    def properties(self) -> dict[str, str | None]:
        result: dict[str, str | None] = {
            "reflexivity": self.reflexivity,
        }

        return result
