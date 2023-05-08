# %%
#Slotmachine Version X


import turtle
import random
import time

# Set up the screen
wn = turtle.Screen()
wn.title("Slot Machine")
wn.bgcolor("red")  # Changed background color to very bright red
wn.setup(width=0.7, height=0.7)  # Set screen size to 70% of user's screen

# Initialize player points
player_points = 50

# Calculate dimensions of screen
screen_width = turtle.window_width()
screen_height = turtle.window_height()

# Create the shapes with doubled size
shape1 = turtle.Turtle()
shape1.speed(0)
shape1.penup()
shape1.goto(-screen_width/4, 0)  # Set position based on screen size
shape1.shapesize(screen_height/200)  # Set size based on screen height
shape1.pendown()

shape2 = turtle.Turtle()
shape2.speed(0)
shape2.penup()
shape2.goto(0, 0)
shape2.shapesize(screen_height/200)  # Set size based on screen height
shape2.pendown()

shape3 = turtle.Turtle()
shape3.speed(0)
shape3.penup()
shape3.goto(screen_width/4, 0)  # Set position based on screen size
shape3.shapesize(screen_height/200)  # Set size based on screen height
shape3.pendown()

# Create the text
text = turtle.Turtle()
text.speed(0)
text.penup()
text.goto(0, screen_height/3)  # Set position based on screen size
text.shapesize(screen_height/400)  # Set size based on screen height
text.color("black")
text.write("Press start to spin", align="center", font=("Verdana", int(screen_height/30), "normal"))
text.hideturtle()

# Create the points text
points_text = turtle.Turtle()
points_text.speed(0)
points_text.penup()
points_text.goto(0, -screen_height/3)  # Set position based on screen size
points_text.shapesize(screen_height/400)  # Set size based on screen height
points_text.color("black")
points_text.write(f"Points: {player_points}", align="center", font=("Verdana", int(screen_height/30), "normal"))
points_text.hideturtle()

# Create the done text
done = turtle.Turtle()
done.speed(0)
done.penup()
done.goto(0, -screen_height/5)  # Set position based on screen size
done.shapesize(screen_height/400)  # Set size based on screen height
done.hideturtle()

# Update points display
def update_points():
    points_text.clear()
    points_text.write(f"Points: {player_points}", align="center", font=("Verdana", int(screen_height/30), "normal"))

# Spin function
def spin():
    global x, y, z
    x = random.randint(1, 3)
    y = random.randint(1, 3)
    z = random.randint(1, 3)
    # Shape 1 change
    if x == 1:
        shape1.shape("triangle")
        shape1.color("green")
    elif x == 2:
        shape1.shape("circle")
        shape1.color("blue")
    elif x == 3:
        shape1.shape("square")
        shape1.color("green")
    # Shape 2 change
    if y == 1:
        shape2.shape("triangle")
        shape2.color("green")
    elif y == 2:
        shape2.shape("circle")
        shape2.color("blue")
    elif y == 3:
        shape2.shape("square")
        shape2.color("purple")
    # Shape 3 change
    if z == 1:
        shape3.shape("triangle")
        shape3.color("green")
    elif z == 2:
        shape3.shape("circle")
        shape3.color("blue")
    elif z == 3:
        shape3.shape("square")
        shape3.color("purple")

# Spin2 function
def spin2():
    global player_points
    if player_points >= 2:
        player_points -= 2
        update_points()
        for action in range(10):
            spin()
            time.sleep(0.3)
        spin3()
    elif player_points == 0:
        done.write("Game Over", align="center", font=("Verdana", 20, "bold"))
        time.sleep(1.9)
        done.clear()

# Spin3 function
def spin3():
    global player_points
    if x == y and x == z:
        player_points += 25
        update_points()
        done.write("YOU WON!", align="center", font=("Verdana", 20, "bold"))
        time.sleep(1.9)
        done.clear()
    else:
        done.write("No luck this time...", align="center", font=("Verdana", 20, "bold"))
        time.sleep(1.9)
        done.clear()

# Button to start
def on_button_click(x, y):
    if 240 < x < 300 and -200 < y < -160:
        spin2()

# Create the start button
start_button = turtle.Turtle()
start_button.speed(0)
start_button.penup()
start_button.goto(270, -180)
start_button.color("black")
start_button.write("START", align="center", font=("Verdana", 14, "normal"))
start_button.hideturtle()

wn.onclick(on_button_click)

# Main game loop
while True:
    wn.update()  

# %%



