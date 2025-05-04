import random
class Customer:

    def __init__(self):
        self.cart = {}

    def add_cart(self):
        for i in range (0, random.randint(1,3)):
            fruit = random.choice(["apple", "banana", "coconut", "mango", "orange"])
            quantity = random.randint(1,12)
            if fruit in self.cart:
                self.cart[fruit] += quantity
            else:
                self.cart[fruit] = quantity
    

