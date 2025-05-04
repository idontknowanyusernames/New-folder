class Employee:
    def __init__(self, salary, efficiency, level):
        self.salary = salary
        self.efficiency = efficiency
        self.level = level
        self.occupied = False

    def __str__(self):
        printstring = "Level " + str(self.level) + " Employee"
        return printstring