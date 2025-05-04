import json
from product import PerishableProduct, Product

class Inventory:
    
    def __init__(self, products, today):
        self.products = products
        self.today = today
        
    def add_product(self, product):
        self.products.append(product)
        
    def remove_product(self, index):
        del self.products[index]
    
    def display_inventory(self):
        print("--------------------------------------------")
        for product in self.products:
            if isinstance(product, PerishableProduct):
                if product.expired(self.today):
                    print("EXPIRED!!!", product)
                else:
                    print(product)
            else:
                print(product)
    
    def save(self, data):
        with open ("userdata/inventory.json", "w") as file:
            products_list = []
            for product in data:
                if isinstance(product, PerishableProduct):
                    list_product = [product.name, product.amount, product.price, product.expiration_date]
                else:
                    list_product = [product.name, product.amount, product.price]
                products_list.append(list_product)
            json.dump(products_list, file)