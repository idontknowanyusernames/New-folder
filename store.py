import csv

class Store:
    def __init__(self, inventory, employeelist, budget):
        self.inventory = inventory
        self.employees = employeelist
        self.budget = budget
    
    def save(self, data):
        with open("userdata/budget.txt", "w") as tfile:
            print(self.budget, file=tfile)
        with open("userdata/employees.csv", "w") as cfile:
            fieldnames = ["level"]
            writer = csv.DictWriter(cfile, fieldnames=fieldnames)
            writer.writeheader()
            for employee in self.employees:
                writer.writerow({"level": employee.level})
        self.inventory.save(data)

