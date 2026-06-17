class Animal:
    def make_sound(self):
        pass
class Dog(Animal):
    def make_sound(self):
        return "WOOf WOOF WOOF !!!"
class Cat(Animal):
    def make_sound(self):
        return "MEEOOWW MEEOOWW !!"
#Polymorphysics is the ability of an entity to have multiple forms 
def animal_sound(animal):
    print(animal.make_sound())
dog = Dog()
cat = Cat()
animal_sound(dog)  
animal_sound(cat)  
#  though we began with the princinciple of inheritance but getting to line 11 We introduced the principle of polymorphysics 
# We have a class Which is animal and under that class we have other sub
