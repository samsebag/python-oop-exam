"""
Bonus - implementation of the UML diagram.

Animal  : abstract class, protected attribute `legs`, protected constructor,
          concrete walk(), abstract eat().
Pet     : interface with get_name(), set_name(name), play().
Spider  : Animal
Cat     : Animal + Pet
Fish    : Animal + Pet (overrides walk(), since a fish has no legs)
"""
from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, legs: int):
        # '#' in the UML = protected -> single underscore in Python
        self._legs = legs

    def walk(self):
        print(f"This animal walks on {self._legs} legs.")

    @abstractmethod
    def eat(self):
        pass


class Pet(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def set_name(self, name: str):
        pass

    @abstractmethod
    def play(self):
        pass


class Spider(Animal):
    def __init__(self):
        super().__init__(8)

    def eat(self):
        print("The spider eats the insects caught in its web.")


class Cat(Animal, Pet):
    # The UML has two constructors: Cat(name) and Cat().
    # Python has no overloading, so a default value covers both.
    def __init__(self, name: str = ""):
        super().__init__(4)
        self._name = name

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def play(self):
        print(f"{self._name or 'The cat'} plays with a ball of yarn.")

    def eat(self):
        print("The cat eats cat food.")


class Fish(Animal, Pet):
    def __init__(self):
        super().__init__(0)
        self._name = ""

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def play(self):
        print(f"{self._name or 'The fish'} swims around the tank.")

    def walk(self):
        print("Fish can't walk, they swim.")

    def eat(self):
        print("The fish eats fish flakes.")
