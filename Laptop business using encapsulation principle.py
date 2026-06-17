class LaptopBusiness:
    def __init__(self, brand, model, price):
        self.__brand = brand
        self.__model = model
        self.__price = price

    def get_brand(self):
        return self.__brand

    def set_brand(self, brand):
        self.__brand = brand

    def get_model(self):
        return self.__model

    def set_model(self, model):
        self.__model = model

    def get_price(self):
        return self.__price

    def set_price(self, price):
        if price > 0:
            self.__price = price
        else:
            raise ValueError("Price must be positive")

    def display_info(self):
        print(f"Brand: {self.__brand}, Model: {self.__model}, Price: ${self.__price}")
        
laptop = LaptopBusiness("Dell", "XPS 15", 1500)
laptop.display_info()

laptop.set_price(1600)
print(f"Updated Price: ${laptop.get_price()}")