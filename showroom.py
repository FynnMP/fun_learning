import pygame
import os

# Initialize pygame
pygame.init()

# Set the screen size and title
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Showroom")

# Get a list of all the image files in the directory
image_dir = "./Assets/"
items = [
    {
        'name': 'Car 1',
        'price': 10,
        'image': 'item1.jpeg'
    },
    {
        'name': 'Car 2',
        'price': 20,
        'image': 'item2.png'
    },
    {
        'name': 'Car 3',
        'price': 30,
        'image': 'item3.png'
    },
    {
        'name': 'Car 4',
        'price': 30,
        'image': 'item3.png'
    },
    {
        'name': 'Car 5',
        'price': 30,
        'image': 'item3.png'
    },
    {
        'name': 'Car 6',
        'price': 30,
        'image': 'item3.png'
    },
    {
        'name': 'Watch',
        'price': 130,
        'image': 'item13.jpeg'
    },
    {
        'name': 'Boat 1',
        'price': 140,
        'image': 'item14.jpeg'
    },
    {
        'name': 'Boat 2',
        'price': 150,
        'image': 'item15.jpeg'
    }
]

# Load the images into a list of pygame surfaces
images = []
for item in items:
    img_path = os.path.join(image_dir, item['image'])
    img = pygame.image.load(img_path).convert()
    img = pygame.transform.scale(img, (screen_width, screen_height))
    images.append(img)

# Set the starting image index to 0
current_image = 0

# Start the main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exec(open("./menu.py").read())
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Move to the previous image
                current_image = (current_image - 1) % len(images)
            elif event.key == pygame.K_RIGHT:
                # Move to the next image
                current_image = (current_image + 1) % len(images)

    # Draw the current image onto the screen
    screen.blit(images[current_image], (0, 0))
    pygame.display.flip()

# Quit pygame
pygame.quit()
