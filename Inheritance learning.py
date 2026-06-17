class Animal:
    def __init__(self, name):
        self.name= name 
    def make_sound(self):
        return "creature sounds"
class Dog(Animal):
    def make_sound(self):
        return "woof"
class Cat(Animal):
    def make_sound(self):
        return "meow"

dog= Dog("oscar")
cat= Cat("simba")
print (dog.name, "says", dog.make_sound())
print (cat.name, "says", cat.make_sound())