# Import needed libraries 
import pygame
import os
import json

# Initialize pygame
pygame.init()

# Set the screen size, background, title and font
screen_width = 750
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill("white")
pygame.display.set_caption("Showroom")
font = pygame.font.SysFont("arial", 20)

# Prepare error message if there are no items to display
text = font.render('Nothing to see here. First buy things in the shop.', True, "black")
text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

# Load inventory data from JSON file
with open("inventory.json", "r") as inventory:
    inventory = json.load(inventory)

# Load the images into a list of pygame surfaces
images = []
for item in inventory:
    # Load the image of each item in the inventory
    img = pygame.image.load(inventory[item]["image_show"]).convert()
    # Scale the image to a fixed size
    img = pygame.transform.scale(img, (500, 500))
    # Add the image to the list
    images.append(img)

# Set the starting image index to 0
current_image = 0

# Start the main game loop
running = True
while running:

    # Load arrow images and define their positions
    arrow_left = pygame.image.load("./graphic/shop/arrow_left.png")
    arrow_right = pygame.image.load("./graphic/shop/arrow_right.png")
    left_button_rect = arrow_left.get_rect()
    left_button_rect.center = (50, screen_height / 2)
    right_button_rect = arrow_right.get_rect()
    right_button_rect.center = (700, screen_height / 2)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit the game if the window close button is clicked
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEMOTION:
            # Check if the mouse is hovering over the left arrow button
            if left_button_rect.collidepoint(event.pos):
                # Draw a circle around the left arrow button to indicate the hover
                pygame.draw.circle(screen, "black", left_button_rect.center, 20, 2)
            # Check if the mouse is hovering over the right arrow button
            elif right_button_rect.collidepoint(event.pos):
                # Draw a circle around the right arrow button to indicate the hover
                pygame.draw.circle(screen, "black", right_button_rect.center, 20, 2)
            else:
                # Draw white circles around the arrow buttons when not hovering
                pygame.draw.circle(screen, "white", left_button_rect.center, 20, 2)
                pygame.draw.circle(screen, "white", right_button_rect.center, 20, 2)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # if there are images to display, show the previous inventory image
                if len(images) > 0:
                    current_image = (current_image - 1) % len(images)
            elif event.key == pygame.K_RIGHT:
                # if there are images to display, show the next inventory image
                if len(images) > 0:
                    current_image = (current_image + 1) % len(images)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the left arrow button is clicked
            if left_button_rect.collidepoint(event.pos):
                # if there are images to display, show the previous inventory image
                if len(images) > 0:
                    current_image = (current_image - 1) % len(images)
            # Check if the right arrow button is clicked
            elif right_button_rect.collidepoint(event.pos):
                # if there are images to display, show the next inventory image
                if len(images) > 0:
                    current_image = (current_image + 1) % len(images)

    # Draw the current image onto the screen
    if len(images) > 0:
        screen.blit(images[current_image], (125, 50))
    else:
        # If there are no images to display, show the error message
        screen.blit(text, text_rect)

    # Draw the arrow buttons on the screen
    screen.blit(arrow_left, left_button_rect)
    screen.blit(arrow_right, right_button_rect)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
