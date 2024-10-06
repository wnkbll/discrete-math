class Set:
    def __init__(self, set_: set):
        self.set: set = set_

    def __repr__(self):
        return self.set.__repr__() if len(self.set) > 0 else "{ null }"

    def __rshift__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __invert__(self):
        pass

    def __xor__(self, other):
        pass


class SetWrapper(Set):
    def __init__(self, set_: set):
        super().__init__(set_)

    def __rshift__(self, other: Set) -> bool:
        return self.set.issubset(other.set)

    def __mul__(self, other: Set) -> Set:
        return SetWrapper(self.set.intersection(other.set))

    def __add__(self, other: Set) -> Set:
        return SetWrapper(self.set.union(other.set))

    def __sub__(self, other: Set) -> Set:
        return SetWrapper(self.set.difference(other.set))

    def __invert__(self) -> Set:
        __set = self.set

        for i in range(-30, 31):
            if i not in __set:
                __set.add(i)

        return SetWrapper(__set)

    def __xor__(self, other: Set) -> Set:
        return SetWrapper(self.set.symmetric_difference(other.set))

    def add(self, elem) -> None:
        return self.set.add(elem)
