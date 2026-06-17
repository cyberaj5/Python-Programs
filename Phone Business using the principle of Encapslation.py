class PhoneBusiness:
    def __init__(self, brand, model, selling_price, cost_price):
        self.brand = brand
        self.model = model
        self.selling_price = selling_price
        self.__cost_price = cost_price 

    def get_phone_details(self):
        """Returns public phone details"""
        return f"Brand: {self.brand}, Model: {self.model}, Selling Price: ${self.selling_price}"
    
    def get_profit(self):
        """Calculates the profit without exposing cost price"""
        profit = self.selling_price - self.__cost_price
        return f"Profit: ${profit}"
    
phone = PhoneBusiness("Itel", "itel P30 ", 1200, 800)
print(phone.get_phone_details()) 
print(phone.get_profit())  
