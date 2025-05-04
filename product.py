class Product:
    
    def __init__(self, name, amount, price):
        self.name = name
        self.amount = amount
        self._price = price
    
    @property
    def price(self):
        return self._price
    
    def __str__(self):
        printstring = self.name + " x " + str(self.amount) + ", ppu is $" + str(self.price)
        return printstring
    
class PerishableProduct(Product):
    
    def __init__(self, name, amount, price, date):
        super().__init__(name, amount, price)
        self.expiration_date = date

    def expired(self, current_date):
        tmonth, tday, tyear = current_date.split("/")
        emonth, eday, eyear, = self.expiration_date
        
        if int(eyear) < int(tyear):
            return True
        elif int(eyear) > int(tyear):
            return False
        elif int(emonth) < int(tmonth):
            return True
        elif int(emonth) == int(tmonth):
            if int(eday) < int(tday):
                return True
        else:
            return False
    
    
    def __str__(self):
        month, day, year = self.expiration_date
        printstring = self.name + " x " + str(self.amount) + ", ppu is $" + str(self.price) + "     EXPIRES: " + str(month) + "/" + str(day) + "/" + str(year)
        return printstring
