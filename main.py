import json, csv, random, threading, queue
import pygame
from product import Product, PerishableProduct
from inventory import Inventory
from store import Store
from employee import Employee
from customer import Customer


class TextInputBox:
    def __init__(self, x, y, w, h, font, prompt=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color("black")
        self.text = ""
        self.font = font
        self.active = True
        self.prompt = prompt

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return None

    def draw(self, screen):
        txt_surface = self.font.render(f"{self.prompt}{self.text}", True, self.color)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def draw_start_screen(screen, font):
    start_image = pygame.image.load("gamedata/assets/start.png")
    start_image = pygame.transform.scale(start_image, (1000, 600))
    screen.blit(start_image, (0, 0))
    start_button = pygame.image.load("gamedata/assets/start_button.png")
    start_button = pygame.transform.scale(start_button, (400, 160))
    start_button_rect = start_button.get_rect(center=(800, 450))
    screen.blit(start_button, start_button_rect)
    pygame.display.flip()
    return start_button_rect


def show_register_screen(screen):
    register_image = pygame.image.load("gamedata/assets/register.png")
    register_image = pygame.transform.scale(register_image, (1000, 600))
    screen.blit(register_image, (0, 0))
    pygame.display.flip()
    pygame.time.delay(2000)  


def get_user_input(screen, font, prompt, budget, current_bg):
    input_box = TextInputBox(100, 100, 600, 50, font, prompt)
    clock = pygame.time.Clock()
    while True:
        if current_bg == "r":
            register_image = pygame.image.load("gamedata/assets/register.png")
            register_image = pygame.transform.scale(register_image, (1000, 600))
            screen.blit(register_image, (0, 0))
        elif current_bg == "i":
            inventory_image = pygame.image.load("gamedata/assets/shop.png")
            inventory_image = pygame.transform.scale(inventory_image, (1000, 600))
            screen.blit(inventory_image, (0, 0))
        
        budget_text = font.render(f"Budget: ${budget:.2f}", True, pygame.Color("black"))
        screen.blit(budget_text, (50, 20))
        pygame.display.flip()

        input_box.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            result = input_box.handle_event(event)
            if result is not None:
                return result
        clock.tick(30)


pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Fruit Store Simulation")
font = pygame.font.SysFont(None, 36)


start_button_rect = draw_start_screen(screen, font)
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if start_button_rect.collidepoint(event.pos):
                show_register_screen(screen)
                waiting = False
                break


current_bg = "r"
budget = 2000
playedbefore = get_user_input(screen, font, "Have you played before? (y/n): ", budget, current_bg).lower() == "y"
products_list = []
employeelist = []
customer_list = []

if playedbefore:
    with open("userdata/inventory.json") as file:
        products = json.load(file)
        for product in products:
            if len(product) == 4:
                product = PerishableProduct(product[0], product[1], product[2], product[3])
            else:
                product = Product(product[0], product[1], product[2])
            products_list.append(product)

    with open("userdata/budget.txt") as txtfile:
        budget = float(txtfile.read())

    with open("userdata/employee.csv") as cfile:
        csv_reader = csv.DictReader(cfile)
        for row in csv_reader:
            elevel = int(row["level"])
            eff = random.uniform({1: 0.5, 2: 2.7, 3: 9.7}[elevel], {1: 1.2, 2: 3.5, 3: 11.3}[elevel])
            salary = {1: 100, 2: 500, 3: 2500}[elevel]
            employee = Employee(salary, eff, elevel)
            employeelist.append(employee)


today = get_user_input(screen, font, "What is today's date? (mm/dd/yy): ", budget, current_bg)
print("Welcome to the store simulation!")
gamestarted = True
inventory = Inventory(products_list, today)
store = Store(inventory, employeelist)
store.budget = budget

while gamestarted:
    store.save(store.inventory.products)
    action = get_user_input(screen, font, "(i)nventory, (h)ire, (o)pen, (q)uit: ", store.budget, current_bg).lower()

    if action == "i":
        current_bg = "i"
        task = get_user_input(screen, font, "(b)uy, (r)emove, (v)iew, (q)uit: ", store.budget, current_bg).lower()
        if task == "b":
            store.inventory.save(inventory.products)
            with open("gamedata/products.csv") as file:
                fruit_options = []
                fruit_prices = []
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    fruit_options.append(row["name"])
                    fruit_prices.append(row["price"])

            for i in range(len(fruit_options)):
                print(f"{i}: {fruit_options[i]} - ${fruit_prices[i]}")

            name_index = int(get_user_input(screen, font, "Which product? Index: ", store.budget, current_bg))
            name = fruit_options[name_index]
            amount = int(get_user_input(screen, font, "How many? ", store.budget, current_bg))
            price = float(fruit_prices[name_index])
            expiration_date = get_user_input(screen, font, "When does it expire? (mm/dd/yy): ", store.budget, current_bg)
            month, day, year = expiration_date.split("/")
            perishableproduct = PerishableProduct(name, amount, price, (month, day, year))
            store.inventory.add_product(perishableproduct)
            store.budget -= price * amount
            store.inventory.display_inventory()
            print(f"You currently have ${store.budget}")
            current_bg = "r"

        elif task == "r":
            store.inventory.save(store.inventory.products)
            index = int(get_user_input(screen, font, "Enter the index to delete (start at 1): ", store.budget, current_bg)) - 1
            store.inventory.remove_product(index)
            store.inventory.display_inventory()
            current_bg = "r"

        elif task == "v":
            store.inventory.display_inventory()
            current_bg = "r"

        elif task == "q":
            store.inventory.save(store.inventory.products)
            current_bg = "r"

    elif action == "h":
        task = get_user_input(screen, font, "(h)ire, (f)ire, or (q)uit: ", store.budget, current_bg)
        if task == "h":
            elevel = int(get_user_input(screen, font, "Hire level 1 ($1000), 2 ($5000), 3 ($25000): ", store.budget, current_bg))
            eff = random.uniform({1: 0.5, 2: 2.7, 3: 9.7}[elevel], {1: 1.2, 2: 3.5, 3: 11.3}[elevel])
            salary = {1: 100, 2: 500, 3: 2500}[elevel]
            employee = Employee(salary, eff, elevel)
            employeelist.append(employee)
            store.budget -= salary

        elif task == "f":
            for idx, employee in enumerate(employeelist):
                print(f"{idx}: {employee}")
            tofire = get_user_input(screen, font, "Index to fire or 'c' to cancel: ", store.budget, current_bg)
            if tofire != "c":
                del employeelist[int(tofire)]

    elif action == "o":
        for _ in range(15):
            customer = Customer()
            customer_list.append(customer)
        for customer in customer_list:
            customer.add_cart()
        print("Helping customers!")
        for customer in customer_list:
            result = store.checkout(customer)
            if result is True:
                customer_list.remove(customer)
            else:
                budget += result
        for employee in employeelist:
            store.budget -= employee.salary
        print(f"Your budget is ${store.budget}")

    elif action == "q":
        store.save(store.inventory.products)
        break

    if store.budget < 0:
        print(f"you had ${store.budget}\nyou went poor")
        break