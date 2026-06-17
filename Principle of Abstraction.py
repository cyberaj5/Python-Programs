from abc import ABC, abstractmethod
class Animal(ABC):
    def make_sound(self):
        """Abstract method to be implemented by subclasses"""
        pass
class Dog(Animal):
    def make_sound(self):
        return "WOOF"
class Cat(Animal):
    def make_sound(self):
        return "MEOW"

dog = Dog()
cat = Cat()
print(dog.make_sound())
print(cat.make_sound())