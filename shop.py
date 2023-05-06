import pygame

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Shop')

# Define font
font = pygame.font.SysFont(None, 30)

# Define items
items = [
    {
        'name': 'Item 1',
        'price': 10,
        'image': pygame.image.load('./Assets/item1.jpeg')
    },
    {
        'name': 'Item 2',
        'price': 20,
        'image': pygame.image.load('./Assets/item2.jpeg')
    },
    {
        'name': 'Item 3',
        'price': 30,
        'image': pygame.image.load('./Assets/item3.jpeg')
    },

    {
        'name': 'Item 4',
        'price': 30,
        'image': pygame.image.load('./Assets/item3.jpeg')
    },

    {
        'name': 'Item 5',
        'price': 30,
        'image': pygame.image.load('./Assets/item3.jpeg')
    },
    
    {
        'name': 'Item 6',
        'price': 30,
        'image': pygame.image.load('./Assets/item3.jpeg')
    },
    # Add more items here...
    {
        'name': 'Item 13',
        'price': 130,
        'image': pygame.image.load('./Assets/item13.jpeg')
    },
    {
        'name': 'Item 14',
        'price': 140,
        'image': pygame.image.load('./Assets/item14.jpeg')
    },
    {
        'name': 'Item 15',
        'price': 150,
        'image': pygame.image.load('./Assets/item15.jpeg')
    }
]


# Define inventory
inventory = []


# Define function to draw items on the screen
def draw_items(scroll_y):
    x = 50
    y = 100 - scroll_y
    row_height = 250
    item_width = 150
    item_height = 200
    margin = 35 # margins between items 
    for i, item in enumerate(items):
        row = i // 4
        col = i % 4
        item_x = x + col * (item_width + margin)
        item_y = y + row * row_height
        # Create new surface with desired item size
        item_surface = pygame.Surface((item_width, item_height))
        # Blit item image onto new surface
        item_image = pygame.transform.scale(item['image'], (item_width, item_height))
        item_surface.blit(item_image, (0, 0))
        name_text = font.render(item['name'], True, BLACK)
        price_text = font.render('$' + str(item['price']), True, BLACK)
        item_surface.blit(name_text, (10, item_height-50))
        item_surface.blit(price_text, (10, item_height-25))
         # Draw buy button
        button_rect = pygame.Rect(70, item_height-28, 70, 25)
        pygame.draw.rect(item_surface, WHITE, button_rect)
        if item in inventory:
            button_text = font.render('Bought', True, BLACK)
        else: 
            button_text = font.render('Buy', True, BLACK)
        button_text_rect = button_text.get_rect()
        button_text_rect.center = button_rect.center
        item_surface.blit(button_text, button_text_rect)
        
        # Draw item surface onto screen
        screen.blit(item_surface, (item_x, item_y))

# event handler
def handle_events(scroll_y):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for i, item in enumerate(items):
                x = 50
                y = 100 - scroll_y
                row_height = 250
                item_width = 150
                item_height = 200
                margin = 35 # margins between items 
                # Create new surface with desired item size
                item_surface = pygame.Surface((item_width, item_height))        
                button_rect = pygame.Rect(70, item_height-28, 70, 25)
                
                # Adjust button coordinates to take into account position of item on screen
                item_x = x + (i % 4) * (item_width + margin)
                item_y = y + (i // 4) * row_height
                button_rect.x = item_x + button_rect.x
                button_rect.y = item_y + button_rect.y

                if button_rect.collidepoint(pos) and event.button == 1 and item not in inventory:
                    print(f"You bought {item['name']} for $ {item['price']}")
                    inventory.append(item)
                    print(inventory)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: # Scroll up
                scroll_y = max(scroll_y - 20, 0)
            elif event.button == 5: # Scroll down
                scroll_y += 20
    return scroll_y



# Main game loop
scroll_y = 0
running = True
while running:
    # Draw menu
    screen.fill(WHITE)
    title_text = font.render("Shop", True, BLACK)
    title_text_rect = title_text.get_rect()
    title_text_rect.center = (WINDOW_WIDTH // 2, 50-scroll_y)
    screen.blit(title_text, title_text_rect)
    draw_items(scroll_y)
    scroll_y = handle_events(scroll_y)

    # Update the screen
    pygame.display.flip()

# Clean up
pygame.quit()