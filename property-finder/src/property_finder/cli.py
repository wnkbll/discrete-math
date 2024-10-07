from pathlib import Path

import typer

from src.property_finder.matrix import Matrix

app = typer.Typer()


class ParamError(Exception):
    pass


def get_matrix_from_file(file: Path, lines: int, columns: int) -> Matrix:
    array: list[list[int | float]] = [[0 for _ in range(columns)] for _ in range(lines)]

    with open(file, "r") as file:
        for line in range(lines):
            string = file.readline().replace("\n", "").strip().split(" ")

            if len(string) != columns:
                print(len(string), columns)
                raise ParamError("Wrong value of column")

            for column, element in enumerate(string):
                value = int(float(element)) if int(float(element)) == float(element) else float(element)
                array[line][column] = value

    return Matrix(array)


@app.command()
def main(file: Path = Path("matrix.txt"), lines: int = 6, columns: int = 6):
    if not file.exists():
        print("No such file or directory")

    try:
        matrix = get_matrix_from_file(file, lines, columns)
        print(matrix.array)
    except ParamError:
        print("Check file path and/or line and column params")
