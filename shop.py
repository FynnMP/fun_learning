import pygame
import json

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Shop')

# Define font
font = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont(None, 20)

# Define items
with open('shop_items.json', 'r+') as shop_items:
    items = json.load(shop_items)


# Define inventory 
with open("inventory.json", "r") as inventory:
    inventory = json.load(inventory)



# Define wallet 
with open("wallet.json", "r") as wallet:
    wallet = json.load(wallet)
    money = wallet["money"]

# Define function to draw items on the screen
def draw_items(scroll_y):
    x = 40
    y = 100 - scroll_y
    row_height = 250
    item_width = 150
    item_height = 150
    margin = 40 # margins between items
    
    # counter of items to display at correct position
    i = 0

    for item in items: 
        row = i // 4
        col = i % 4
        item_x = x + col * (item_width + margin)
        item_y = y + row * row_height
        # Create new surface with desired item size
        item_surface = pygame.Surface((item_width, item_height+50))
        # Blit item image onto new surface
        item_img = pygame.image.load(items[item]['image'])
        item_image = pygame.transform.scale(item_img, (item_width, item_height))
        item_surface.blit(item_image, (0, 0))
        name_text = font2.render(items[item]["name"], True, WHITE)
        price_text = font.render('$' + str(items[item]["price"]), True, WHITE)
        item_surface.blit(name_text, (10, item_height+5))
        item_surface.blit(price_text, (10, item_height+25))

        # Draw buy button
        button_rect = pygame.Rect(80, item_height+12, 60, 25)
        # grey buy button if to little money or already bought
        with open("inventory.json", "r") as inventory:
            inventory = json.load(inventory)
        if items[item]["price"] > sum(money) or item in inventory:
            pygame.draw.rect(item_surface, GRAY, button_rect)
        else: 
            pygame.draw.rect(item_surface, WHITE, button_rect)

        if item in inventory.keys():
            button_text = font2.render('Bought', True, BLACK)
        else: 
            button_text = font2.render('Buy', True, BLACK)
        button_text_rect = button_text.get_rect()
        button_text_rect.center = button_rect.center
        item_surface.blit(button_text, button_text_rect)
            
        # Draw item surface onto screen
        screen.blit(item_surface, (item_x, item_y))

        i += 1


# event handler
def handle_events(scroll_y):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for i, item in enumerate(items):
                x = 40
                y = 100 - scroll_y
                row_height = 250
                item_width = 150
                item_height = 150
                margin = 40 # margins between items 
                # Create new surface with desired item size
                item_surface = pygame.Surface((item_width, item_height+50))        
                button_rect = pygame.Rect(80, item_height+12, 60, 25)
                
                # Adjust button coordinates to take into account position of item on screen
                item_x = x + (i % 4) * (item_width + margin)
                item_y = y + (i // 4) * row_height
                button_rect.x = item_x + button_rect.x
                button_rect.y = item_y + button_rect.y

                # buying logic 
                if button_rect.collidepoint(pos) and event.button == 1 and item not in inventory and sum(money)>= items[item]["price"]:
                    # update json inventory with newly bought item                    
                    with open("inventory.json", "r") as jsonFile:
                        old_inventory = json.load(jsonFile)
                        new_inventory = old_inventory
                        new_inventory[item] = items[item]
                    with open("inventory.json", 'w') as jsonFile:
                        json.dump(new_inventory, jsonFile)

                    # update json wallet with newly bought item                    
                    with open("wallet.json", "r") as jsonFile:
                        wallet = json.load(jsonFile)
                        money_old = wallet["money"]
                        money_new = money_old
                        money_new.append(-items[item]["price"])
                        wallet["money"] = money_new

                    with open("wallet.json", "w") as jsonFile:
                        json.dump(wallet, jsonFile)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: # Scroll up
                scroll_y = max(scroll_y - 20, 0)
            elif event.button == 5 and scroll_y <= 490: # Scroll down and stop at bottom
                scroll_y += 20
    return scroll_y



# Main game loop
scroll_y = 0
running = True
while running:
    screen.fill(WHITE)

    # Get current bank account
    with open("wallet.json", "r") as wallet:
        wallet = json.load(wallet)
        money = wallet["money"]
    # Draw current bank account
    money_text = font.render("Current Balance: " + str(sum(money)) + "$", True, BLACK)
    money_text_rect = money_text.get_rect()
    money_text_rect.center = (WINDOW_WIDTH//2, 50-scroll_y)
    screen.blit(money_text, money_text_rect)

    draw_items(scroll_y)
    scroll_y = handle_events(scroll_y)

    # Update the screen
    pygame.display.update()

# Clean up
pygame.quit()