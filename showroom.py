import pygame
import os
import json

# Initialize pygame
pygame.init()

# Set the screen size and title
screen_width = 750
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill("white")
pygame.display.set_caption("Showroom")
font = pygame.font.SysFont("arial", 20)

# prepare error message
text = font.render('Nothing to see here. First buy things in the shop.', True, "black")
text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

with open("inventory.json", "r") as inventory:
            inventory = json.load(inventory)

# Load the images into a list of pygame surfaces
images = []
for item in inventory:
    img = pygame.image.load(inventory[item]["image_show"]).convert()
    img = pygame.transform.scale(img, (500, 500))
    images.append(img)

# Set the starting image index to 0
current_image = 0

# Start the main game loop
running = True
while running:


    # Arrow right and left
    arrow_left = pygame.image.load("./graphic/shop/arrow_left.png")
    arrow_right = pygame.image.load("./graphic/shop/arrow_right.png")

    left_button_rect = arrow_left.get_rect()
    left_button_rect.center = (50, screen_height/2)

    right_button_rect = arrow_right.get_rect()
    right_button_rect.center = (700, screen_height/2)
    
   

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEMOTION:
            # Check if mouse is hovering over arrow_left
            if left_button_rect.collidepoint(event.pos):
                # Draw circle around arrow_left
                pygame.draw.circle(screen, "black", left_button_rect.center, 20, 2)
            elif right_button_rect.collidepoint(event.pos):
                pygame.draw.circle(screen, "black", right_button_rect.center, 20, 2)
            else: 
                pygame.draw.circle(screen, "white", left_button_rect.center, 20, 2)
                pygame.draw.circle(screen, "white", right_button_rect.center, 20, 2)


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Move to the previous image
                if len(images) > 0:
                    current_image = (current_image - 1) % len(images)
            elif event.key == pygame.K_RIGHT:
                # Move to the next image
                if len(images) > 0:
                    current_image = (current_image + 1) % len(images)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if left_button_rect.collidepoint(event.pos):
                if len(images) > 0:
                    current_image = (current_image - 1) % len(images)
            elif right_button_rect.collidepoint(event.pos):
                if len(images) > 0:
                    current_image = (current_image + 1) % len(images)

    # Draw the current image onto the screen
    if len(images) > 0:
        screen.blit(images[current_image], (125, 50))
    else: 
        screen.blit(text, text_rect)


    screen.blit(arrow_left, left_button_rect)
    screen.blit(arrow_right, right_button_rect)



    pygame.display.flip()

# Quit pygame
pygame.quit()