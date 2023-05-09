import pygame
import os

# Initialize pygame
pygame.init()

# Set the screen size and title
screen_width = 750
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill("white")
pygame.display.set_caption("Showroom")
font = pygame.font.SysFont(None, 30)


# Get a list of all the image files in the directory
image_dir = "./Assets/"
items = [
    {
        'name': 'Car 1',
        'price': 10,
        'image': 'item1.jpg'
    },
    {
        'name': 'Car 2',
        'price': 20,
        'image': 'item2_show.jpg'
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
        'image': 'item13_show.jpg'
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
    img = pygame.transform.scale(img, (500, 500))
    images.append(img)

# Set the starting image index to 0
current_image = 0

# Start the main game loop
running = True
while running:


    # Arrow right and left
    arrow_text_left = font.render("<", True, "black")
    arrow_text_left_rect = arrow_text_left.get_rect()
    arrow_text_left_rect.center = (30, screen_height/2)
    screen.blit(arrow_text_left, arrow_text_left_rect)

    arrow_text = font.render(">", True, "black")
    arrow_text_rect = arrow_text.get_rect()
    arrow_text_rect.center = (720, screen_height/2)
    screen.blit(arrow_text, arrow_text_rect)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Move to the previous image
                current_image = (current_image - 1) % len(images)
            elif event.key == pygame.K_RIGHT:
                # Move to the next image
                current_image = (current_image + 1) % len(images)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if arrow_text_left_rect.collidepoint(event.pos):
                # Move to the previous image
                current_image = (current_image - 1) % len(images)
            elif arrow_text_rect.collidepoint(event.pos):
                # Move to the next image
                current_image = (current_image + 1) % len(images)

    # Draw the current image onto the screen
    screen.blit(images[current_image], (125, 50))


    

    arrows = ["<", ">"]
    # Hover animation 
    mouse_pos = pygame.mouse.get_pos()
    for i, arrow in enumerate(arrows):
        text = font.render(arrow, True, "black")
        text_rect = text.get_rect()
        text_rect.center = (30+i*740, screen_height/2)
        if text_rect.collidepoint(mouse_pos):
            # Draw the arrow with border
            pygame.draw.rect(screen, "black", (text_rect.x - 5, text_rect.y - 2, text_rect.width + 10, text_rect.height + 2 ), 3)
            screen.blit(text, text_rect)
        else:
            # Redraw rect with white border so it "disappears" after hovering away from it 
            pygame.draw.rect(screen, "white", (text_rect.x - 5, text_rect.y - 5, text_rect.width + 5, text_rect.height + 5), 3)
            screen.blit(text, text_rect)

    pygame.display.flip()

# Quit pygame
pygame.quit()