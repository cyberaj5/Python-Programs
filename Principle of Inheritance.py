class Animal:
 def __init__(self,name):
  self.name = name
def  make_sound(self):
 return "some generic sounds"
class Dog (Animal):
 def make_sound(self):
  return "woof"
class Cat (Animal):
 def make_sound(self):
  return "meow"
dog=Dog ("Buddy")
cat=Cat("Whiskers")
print(dog.name, "Says",dog.make_sound())
print(cat.name, "Says",cat.make_sound())