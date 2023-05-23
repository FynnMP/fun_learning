# This python script executes the shop of our LearnXCasino platform, it uses the money earned from the 
# learning parts or gained in the casino.
# Once an item is bought it can be seen in the showroom in a higher resolution.

# import needed modules
import pygame
import json

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Set up the windows height and width
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# set windows caption
pygame.display.set_caption('Shop')

# Define fonts used in the shop
font = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont(None, 20)

# Define items 
# importing/reading it from the shop_items.json file 
with open('shop_items.json', 'r+') as shop_items:
    items = json.load(shop_items)


# Define the inventory 
# importing/reading it from the inventory.json file 
with open("inventory.json", "r") as inventory:
    inventory = json.load(inventory)


# Define the wallet/money which can be used 
# importing it from the wallet.json file 
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
    
    # counter of items to display 
    i = 0

    # logic of placing shop items in a row / column grid 
    for item in items: 
        row = i // 4
        col = i % 4
        item_x = x + col * (item_width + margin)
        item_y = y + row * row_height

        # Create new surface with desired item size
        item_surface = pygame.Surface((item_width, item_height+50))
        
        # Load and transfrom the size of each image
        item_img = pygame.image.load(items[item]['image'])
        item_image = pygame.transform.scale(item_img, (item_width, item_height))
        # Blit each item image onto new surface
        item_surface.blit(item_image, (0, 0))
        # Blit price and name of each shop item 
        name_text = font2.render(items[item]["name"], True, WHITE)
        price_text = font.render('$' + str(items[item]["price"]), True, WHITE)
        item_surface.blit(name_text, (10, item_height+5))
        item_surface.blit(price_text, (10, item_height+25))

        # Draw buy button
        button_rect = pygame.Rect(80, item_height+12, 60, 25)

        # Open inventory.json to get current inventory 
        with open("inventory.json", "r") as inventory:
            inventory = json.load(inventory)
        # if price of a item is higher than the current balance the users has or it was already bought
        # make button grey
        if items[item]["price"] > sum(money) or item in inventory:
            pygame.draw.rect(item_surface, GRAY, button_rect)
        else: 
            pygame.draw.rect(item_surface, WHITE, button_rect)

        # if a item is also in the inventory, the items was already bought, so changing buy button to "bought"
        if item in inventory.keys():
            button_text = font2.render('Bought', True, BLACK)
        else: 
            button_text = font2.render('Buy', True, BLACK)

        # Blit button on screen     
        button_text_rect = button_text.get_rect()
        button_text_rect.center = button_rect.center
        item_surface.blit(button_text, button_text_rect)
            
        # Blit items onto screen
        screen.blit(item_surface, (item_x, item_y))

        # Increase counter by one so next item can be placed according to row / column grid logic (see above)
        i += 1


# Event handler
def handle_events(scroll_y):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # quit shop when window is closed
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # define buying logic and scrolling logic 
            for i, item in enumerate(items):
                x = 40
                y = 100 - scroll_y
                row_height = 250
                item_width = 150
                item_height = 150
                margin = 40 # margins between items 
                # Create new surface with desired size for item and button
                item_surface = pygame.Surface((item_width, item_height+50))        
                button_rect = pygame.Rect(80, item_height+12, 60, 25)
                
                # Adjust button coordinates to take into account position of item on screen
                item_x = x + (i % 4) * (item_width + margin)
                item_y = y + (i // 4) * row_height
                button_rect.x = item_x + button_rect.x
                button_rect.y = item_y + button_rect.y

                # buying logic 
                # if mouse is over buy button and clicked (and the item is not already bought and the user has
                # enough money to buy the item) then the inventory.json gets updated with this new item 
                if button_rect.collidepoint(pos) and event.button == 1 and item not in inventory and sum(money)>= items[item]["price"]:
                   
                    # read inventory.json to get old inventory and add the newly bought item                    
                    with open("inventory.json", "r") as jsonFile:
                        old_inventory = json.load(jsonFile)
                        new_inventory = old_inventory
                        new_inventory[item] = items[item]

                    # overwrite inventory.json with new item included in new inventory 
                    with open("inventory.json", 'w') as jsonFile:
                        json.dump(new_inventory, jsonFile)

                    # update wallet.json to substract the money from the bought item from the users current balance                 
                    # read wallet.json and append the items price to the money list 
                    with open("wallet.json", "r") as jsonFile:
                        wallet = json.load(jsonFile)
                        money_old = wallet["money"]
                        money_new = money_old
                        money_new.append(-items[item]["price"])
                        wallet["money"] = money_new

                    # overwrite old wallet with newly added item price value 
                    with open("wallet.json", "w") as jsonFile:
                        json.dump(wallet, jsonFile)

        # define scrolling logic 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: # Scroll up
                # decrease the y position of all items until they reach the top of the screen 
                scroll_y = max(scroll_y - 30, 0) 
            elif event.button == 5 and scroll_y <= 490: # Scroll down 
                # increas the y position of all items until they reach the bottom of the screen (scroll_y <= 490)
                scroll_y += 30
    return scroll_y



# Start main game loop
scroll_y = 0
running = True
while running:
    screen.fill(WHITE)

    # Get current balance of user from wallet.json
    with open("wallet.json", "r") as wallet:
        wallet = json.load(wallet)
        money = wallet["money"]

    # Draw current balance on screen
    money_text = font.render("Current Balance: " + str(sum(money)) + "$", True, BLACK)
    money_text_rect = money_text.get_rect()
    money_text_rect.center = (WINDOW_WIDTH//2, 50-scroll_y)
    screen.blit(money_text, money_text_rect)

    # draw all items on screen and use scroll logic  
    draw_items(scroll_y)
    scroll_y = handle_events(scroll_y)

    # Update the screen
    pygame.display.update()

pygame.quit()