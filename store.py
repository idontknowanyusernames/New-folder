import csv, random, time

class Store:
    def __init__(self, inventory, employeelist):
        self.inventory = inventory
        self.employees = employeelist
        self.budget = 1000
    
    def save(self, data):
        with open("userdata/budget.txt", "w") as tfile:
            print(self.budget, end = "", file=tfile)
        with open("userdata/employee.csv", "w") as cfile:
            fieldnames = ["level"]
            writer = csv.DictWriter(cfile, fieldnames=fieldnames)
            writer.writeheader()
            for employee in self.employees:
                writer.writerow({"level": employee.level})
        self.inventory.save(data)

    def checkout(self, customer):
        hasemployee = False
        total = 0
        
        while hasemployee != True:
            randomemployee = random.choice(self.employees)
            hasemployee = not randomemployee.occupied
        fruits = []
        fruitsamt = []
        with open("gamedata/products.csv") as file:
            fruit_options = []
            fruit_prices = []
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                fruit_options.append(row["name"])
                fruit_prices.append(row["price"])    
        for item in self.inventory.products:
            fruits.append(item.name)
            fruitsamt.append(item.amount)
        
        for fruit in customer.cart:
            qty = customer.cart[fruit]
            if fruit not in fruits:
                print("A customer has left!")
                return True
            elif qty > fruitsamt[fruits.index(fruit)]:
                print("A customer has left!")
                return True
            else:
                fruitindex = fruit_options.index(fruit)
                price = float(fruit_prices[fruitindex])
                cost = float(fruitsamt[fruits.index(fruit)]) * price
                total += cost

        time.sleep(10 / randomemployee.efficiency)
        randomemployee.occupied = False
        print("A customer has been helped!")
        return total
        
            
            
