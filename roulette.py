from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import random

# Create the roulette window
window = tk.Tk()

# Set the window title
window.title("Roulette")

# Set the window size
window.geometry("1000x600")

# Set the window colour
window.configure(bg="green")

# Add a label to the window
titel = tk.Label(window, text="Welcome to Roulette!", font=("Arial", 20), bg="green") # define how the label should look like
titel.pack()

# Add an image to the window
roulette_img = ImageTk.PhotoImage(Image.open("./Assets/Roulette.png")) # select the image
image_label = Label(image=roulette_img)
image_label.pack()

# Add the label that asks the user what he wants to bet on
what_kind_of_bet = tk.Label(window, text="What kind of bet do you want to do?", font=("Arial", 16), bg="green")
what_kind_of_bet.place(x=350, y=400)

# Add a field where the user can give input
entry1 = tk.Entry(window)
entry1.place(x=700, y=400)

# Add a label with feedback to the entry1
label_feedback_entry1 = tk.Label(window, text="", font=("Arial", 8), bg="green")
label_feedback_entry1.place(x=700, y=430)

# Add the label that explains the user his options1
option1 = tk.Label(window, text="(number:                Type in the number.)", font=("Arial", 10), bg="green")
option1.place(x=350, y=420)

# Add the label that explains the user his options2
option2 = tk.Label(window, text="(Colour:                  Type in the colour: 'red' or 'black'.)", font=("Arial", 10), bg="green")
option2.place(x=350, y=435)

# Add the label that explains the user his options3
option3 = tk.Label(window, text="(Even-odd:             Type in either 'even' or 'odd'.)", font=("Arial", 10), bg="green")
option3.place(x=350, y=450)

# Add the label that explains the user his options4
option4 = tk.Label(window, text="(1to18-19to36:       Type in either '1to18' or '19to36'.", font=("Arial", 10), bg="green")
option4.place(x=350, y=465)

# Add the label that explains the user his options5
option5 = tk.Label(window, text="(1st 2nd 3rd 12:     Type in either '1st 12', '2nd 12' or '3rd 12'.)", font=("Arial", 10), bg="green")
option5.place(x=350, y=480)

# Add the label that explains the user his options6
option6 = tk.Label(window, text="(2 to 1:                   Type in either 'top row', 'middle row' or 'bottom row'.)", font=("Arial", 10), bg="green")
option6.place(x=350, y=495)

# Add the label that asks the user how much he wants to bet
how_much = tk.Label(window, text="How much do you want to bet?", font=("Arial", 16), bg="green")
how_much.place(x=350, y=520)

# Add a field where the user can give input
entry2 = tk.Entry(window)
entry2.place(x=700, y=520)

# Add a label with feedback to the entry2
label_feedback_entry2 = tk.Label(window, text="", font=("Arial", 8), bg="green")
label_feedback_entry2.place(x=700, y=550)

# Add a label with the current balance
text_current_balance = tk.Label(window, text="Current Balance: ", font=("Arial", 16), bg="green")
text_current_balance.place(x=30, y=450)

# Add the variable current_balance
current_balance = 100

# Add a label with the actual number of the current balance
display_current_balance = tk.Label(window, text=current_balance, font=("Arial", 16), bg="green")
display_current_balance.place(x=200, y=450)

# Create a list with valid user inputs
valid_entries = ['red', 'black', 'even', 'odd', '1to18', '19to36', '1st 12', '2nd 12', '3rd 12', 'top row', 'middle row', 'bottom row']
# Create another list with the valid user inputs, which are numbers
valid_entries_numbers =[] # the list is empty at first
for i in range(37): # then all the numbers which are valid are appended to the list
    valid_entries_numbers.append(i)

# Define the group of numbers
red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
top_row = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
middle_row = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
bottom_row = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]

# Define a feedback label
feedback = tk.Label(window, text="", font=("Arial", 14), bg="green")
feedback.place(x=30, y=550)

# Define a label with the next steps
next_steps = tk.Label(window, text="", font=("Arial", 10), bg="green")
next_steps.place(x=30, y=570)

# Add a label to display the number
win_number = tk.Label(window, text="You have not played yet.", font=("Arial", 14), bg="green")
win_number.place(x=140, y=360)

# Define a function which happens, when the spin button is clicked
def spin():
    # get the global variables
    global current_balance
    global display_current_balance

    # assign the two user inputs
    kind_of_bet = entry1.get()
    bet_amount = entry2.get()
    bet_amount = int(bet_amount) # change the user input to int
    
    # check if user input is a valid kind of bet
    try:
        if kind_of_bet in valid_entries or int(kind_of_bet) in valid_entries_numbers:
            label_feedback_entry1.config(text="Great! - You entered a valid kind of bet.", fg="black", bg="green")
        else:
            label_feedback_entry1.config(text="Please enter a valid kind of bet.", fg="red", bg="white")
            return
    except ValueError:
        label_feedback_entry1.config(text="Please enter a valid kind of bet.", fg="red", bg="white")
        return

    # check if user input is a valid amount
    try:
        if bet_amount > 0:
            if bet_amount <= current_balance:
                label_feedback_entry2.config(text="Great! - You entered a valid amount.", fg="black", bg="green")
                current_balance = current_balance - bet_amount
                display_current_balance.config(text=current_balance)
            else:
                label_feedback_entry2.config(text="You don't have enough coins for this bet. Please change the amount.", fg="red", bg="white")
                return
    except ValueError:
        label_feedback_entry2.config(text="You don't have enough coins for this bet. Please change the amount.", fg="red", bg="white")
        return

    # spin the roulette wheel
    winning_number = random.randint(0, 36)
    # depending on the number it is displayed in another colour
    if winning_number in red_numbers:
        win_number.config(text=winning_number, bg="red")
    elif winning_number in black_numbers:
        win_number.config(text=winning_number, bg="black")
    elif winning_number == 0:
        win_number.config(text=winning_number, bg="green")

    # determine whether the user has won or not
    # when the user bets on the colour
    if kind_of_bet == 'red':
        if winning_number in red_numbers:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (2 * bet_amount) # change the current amount
            display_current_balance.config(text=current_balance) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost
    elif kind_of_bet == 'black':
        if winning_number in black_numbers:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (2 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")

    # when the user bets on even or odd
    elif kind_of_bet == 'even':
        if winning_number % 2 == 0:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (2 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == 'odd':
        if winning_number % 2 != 0:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (2 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")

    # when the user bets on low or high number
    elif kind_of_bet == '1to18':
        if winning_number <= 18 & winning_number != 0:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (2 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == '19to36':
        if winning_number > 18 & winning_number != 0:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (2 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")

    # when the user bets on a third of the numbers
    elif kind_of_bet == '1st 12':
        if winning_number <= 12 & winning_number != 0:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == '2nd 12':
        if winning_number > 12 & winning_number <= 24:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == '3rd 12':
        if winning_number > 24:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")

    # when the user bets on a row
    elif kind_of_bet == 'top row':
        if winning_number in top_row:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == 'middle row':
        if winning_number in middle_row:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == 'bottom row':
        if winning_number in bottom_row:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")

    # when the user bets on a number
    else:
        if int(kind_of_bet) == winning_number:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (36 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
            
    # Tell the user how he can proceed
    next_steps.config(text="If you want to play again, enter your new bet and press 'spin' again.")

# Add a spin-button to the window
spin_button = tk.Button(window, text="Spin", borderwidth=2, relief=RAISED, highlightthickness=0, highlightcolor="green", command=spin)
spin_button.place(x=60, y=360)

# define a function that exits the program
def exit_program():
    window.destroy()

# Add an exit-button to the window, which uses the function above
exit_button = tk.Button(window, text="Exit", borderwidth=2, relief=RAISED, highlightthickness=0, highlightcolor="black", command=exit_program)
exit_button.place(x=940, y=30)

# Start the main event loop
window.mainloop()
