import json, csv, random
from product import Product, PerishableProduct
from inventory import Inventory
from store import Store
from employee import Employee
from customer import Customer
budget = 1000
playedbefore = input("Have you played before? (y/n)     ") == "y"
products_list = []
employeelist = []
customer_list = []
if playedbefore:
    with open ("userdata/inventory.json") as file:
        products = json.load(file)
        for product in products:
            if len(product) == 4:
                product = PerishableProduct(product[0], product[1], product[2], product[3])
            else:
                product = Product(product[0], product[1], product[2])
            products_list.append(product)
    with open("userdata/budget.txt") as txtfile:
        budget = txtfile.read()
        budget = int(budget)
    with open("userdata/employee.csv") as cfile:
        csv_reader = csv.DictReader(cfile)
        for row in csv_reader:
            elevel = int(row["Level"])
            if elevel == 1:
                effiencyrandomizer = random.random(0.5,1.2)
                employee = Employee(100, effiencyrandomizer, 1)
                employeelist.append(employee)
                budget -= employee.salary
            elif elevel == 2:
                effiencyrandomizer = random.random(2.7,3.5)
                employee = Employee(500, effiencyrandomizer, 2)
                employeelist.append(employee)
                budget -= employee.salary
            elif elevel == 3:
                effiencyrandomizer = random.random(9.7,11.3)
                employee = Employee(2500, effiencyrandomizer, 3)
                employeelist.append(employee)
                budget -= employee.salary


today = input("What is today's date? (mm/dd/yy)     ")
print("Welcome to the store simulation!")
gamestarted = True
inventory = Inventory(products_list, today)
store = Store(inventory, employeelist)
store.budget = budget
while gamestarted:
    store.save(store.inventory.products)
    action = input("Would you like to open your (i)nventory, (h)ire a new employee, (o)pen up the store, or (q)uit?").lower()
    
    if action == "i":
        print("--------------------------------------------")
        task = input("Would you like to (b)uy a product, (r)emove a product, (v)iew your inventory, or (q)uit?")
        if task.lower() == "b":
            store.inventory.save(inventory.products)
            with open("gamedata/products.csv") as file:
                fruit_options = []
                fruit_prices = []
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    fruit_options.append(row["name"])
                    fruit_prices.append(row["price"])
            for i in range (0, len(fruit_options)):
                print(fruit_options[i], fruit_prices[i], sep = ":")
            name_index = int(input("Which product would you like to buy? (0-" + str(len(fruit_options) - 1) + ")     "))
            name = fruit_options[name_index]
            amount = int(input("How many would you like to buy?   "))
            price = fruit_prices[name_index]
            perishable = True
            if perishable:
                expiration_date = input("When does it expire? (mm/dd/yy)   ")
                month, day, year = expiration_date.split("/")
                perishableproduct = PerishableProduct(name, amount, price, (month, day, year))
                store.inventory.add_product(perishableproduct)
            else:
                product = Product(name, amount, price)
                store.inventory.add_product(product)
            
            store.budget -= float(price) * amount
            store.inventory.display_inventory()
            print("You currently have $" + str(store.budget))
        elif task.lower() == "r":
            store.inventory.save(store.inventory.products)
            index = int(input("Enter the index of the item you want to delete (first index is 1):   "))
            store.inventory.remove_product(index - 1)
            store.inventory.display_inventory()
        elif task.lower() == "v":
            store.inventory.display_inventory()
        elif task.lower() == "q":
            store.inventory.save(store.inventory.products)

    
    elif action == "h":
        
        print("--------------------------------------------")
        task = input("Would you like to (h)ire an employee, (f)ire an employee, or (q)uit?")
        if task == "h":
            elevel = int(input("Would you like to hire a level 1 ($1000), 2 ($5000), or 3 ($25000) employee?"))
            if elevel == 1:
                effiencyrandomizer = random.random(0.5,1.2)
                employee = Employee(100, effiencyrandomizer, 1)
                employeelist.append(employee)
                budget -= employee.salary
            elif elevel == 2:
                effiencyrandomizer = random.random(2.7,3.5)
                employee = Employee(500, effiencyrandomizer, 2)
                employeelist.append(employee)
                budget -= employee.salary
            elif elevel == 3:
                effiencyrandomizer = random.random(9.7,11.3)
                employee = Employee(2500, effiencyrandomizer, 3)
                employeelist.append(employee)
                budget -= employee.salary
        elif task == "f":
            for employee in employeelist:
                print(employee)
            tofire = input("Which employee would you like to fire? (0-)" + str(len(employeelist - 1)) + ") or c to cancel")
            if tofire == "c":
                pass
            else:
                tofire = int(tofire)
                del employeelist[tofire]

    elif action == "o":
        for i in range (0,4):
            customer = Customer()
            customer_list.append(customer)
        for customer in customer_list:
            customer.add_cart()


    elif action == "q":
        store.save(store.inventory.products)