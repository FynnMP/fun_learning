import pygame

pygame.init()
# test 

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Learning Platform")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

# Define fonts 123
title_font = pygame.font.SysFont("comicsansms", 72)
menu_font = pygame.font.SysFont("comicsansms", 48)

# Define menu items
menu_items = ["Start Learning", "Casino", "Shop", "Showroom", "Quit"]
selected_item_index = 0

# Define function to draw menu items
def draw_menu_items():
    for i, item in enumerate(menu_items):
        if i == selected_item_index:
            text = menu_font.render(item, True, black)
        else:
            text = menu_font.render(item, True, gray)
        text_rect = text.get_rect()
        text_rect.center = (screen_width // 2, 200 + i * 75)
        screen.blit(text, text_rect)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, item in enumerate(menu_items):
                text = menu_font.render(item, True, black)
                text_rect = text.get_rect()
                text_rect.center = (screen_width // 2, 200 + i * 75)
                if text_rect.collidepoint(mouse_pos) and event.button == 1:
                    if i == 0:
                        exec(open("./memory.py").read())
                    elif i == 1:
                        exec(open("./slot_machine.py").read())
                    elif i == 2:
                        exec(open("./shop.py").read())
                    elif i == 3:
                        exec(open("./showroom.py").read())
                    elif i == 4:
                        running = False

    # Draw menu
    screen.fill(white)
    title_text = title_font.render("Menu", True, black)
    title_text_rect = title_text.get_rect()
    title_text_rect.center = (screen_width // 2, 100)
    screen.blit(title_text, title_text_rect)
    draw_menu_items()

    # Check if mouse is hovering over a menu item
    mouse_pos = pygame.mouse.get_pos()
    for i, item in enumerate(menu_items):
        text = menu_font.render(item, True, black)
        text_rect = text.get_rect()
        text_rect.center = (screen_width // 2, 200 + i * 75)
        if text_rect.collidepoint(mouse_pos):
            text = menu_font.render(item, True, black)
            pygame.draw.rect(screen, black, (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20), 5)
        screen.blit(text, text_rect)

    # Update the screen
    pygame.display.update()

# Clean up
pygame.quit()
