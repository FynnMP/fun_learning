from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from PIL import ImageTk, Image
import random

# Create the roulette window
window = tk.Tk()

# Set the window title
window.title("Roulette")

# Set the window size
window.geometry("1000x750")

# Set the window colour
window.configure(bg="green")

# This means that a new window is opened over the "original" one. 
class NewWindowDescr(Toplevel):

    def __init__(self, master = None, description = None):

        super().__init__(master = window) # The Tkinter (Tk()) element which is the underlying the initiation window 
        self.title("Help Terminal") # The top level window caption
        self.geometry("700x300") # Size of the window
        self.configure(background="darkgrey") # Background color of the window 
        # Creating different text elements:
        titel = Label(self, text ="Instructions for Roulette", font = "Helvetica 18 bold", foreground="black", background="darkgrey") # Titel text and all the specifics
        titel.place(relx = 0.5, rely = 0.1, anchor = CENTER) # Determining the position of the textelement "titel"
        descr = Label(self, text = description, font = "Helvetica 14", foreground="black", background="darkgrey") # Description text and all the specifics
        descr.place(relx = 0.5, rely = 0.5, anchor = CENTER) # Determining the position of the textelement "descr"

# setting style of all widgets
style = Style()
#style.theme ('aqua', 'clam', 'alt', 'default', 'classic') (used default) --> possibility to select different
style.theme_use('default')
# Title of the games and text of the widgets text 
style.configure("button1.TButton", font="Helvetica 16 bold", background="#9FD0DD", foreground="black", padding=(10, 25, 10, 25)) # Buttons
style.configure("button2.TButton", font="Helvetica 8 bold", background="#B2B2B2", foreground="black") # Buttons

# Add a label to the window
titel = tk.Label(window, text="Welcome to Roulette!", font=("Arial", 20), bg="green") # define how the label should look like
titel.pack() # add the label to the window

# Add an image to the window
roulette_img = ImageTk.PhotoImage(Image.open("./graphic/roulette/roulette.png")) # select the image
image_label = Label(image=roulette_img) # add the image to the label
image_label.pack() # add the label to the window

# Add the label that asks the user what he wants to bet on
what_kind_of_bet = tk.Label(window, text="What kind of bet do you want to do?", font=("Arial", 16), bg="green")
what_kind_of_bet.place(x=350, y=450) # place the label on the window

# Add a field where the user can give input
entry1 = tk.Entry(window, fg='black', bg="gray", font=('Arial', 14), borderwidth=4)
entry1.place(x=700, y=450) # place the entry field on the window

# Add a label with feedback to the entry1
label_feedback_entry1 = tk.Label(window, text="", font=("Arial", 8), bg="green")
label_feedback_entry1.place(x=700, y=485)



# Help Button
btn = Button(window, text="Possible Inputs",style="button2.TButton")
btn.place(x = 400, y=500, anchor=CENTER)
btn.bind("<Button>", lambda e: NewWindowDescr(window,
    "Number: \t \t Type in the number.\n"
    "Colour: \t \t Type in the colour: 'red' or 'black'.\n"
    "Even-odd: \t Type in either 'even' or 'odd'.\n"
    "1to18-19to36: \t Type in either '1to18' or '19to36'.\n"
    "1st 2nd 3rd 12: \t Type in either '1st 12', '2nd 12' or '3rd 12'.\n"
    "2 to 1: \t \t Type in either 'top row', 'middle row' or 'bottom row'.\n"
))


# Add the label that asks the user how much he wants to bet
how_much = tk.Label(window, text="How much do you want to bet?", font=("Arial", 16), bg="green")
how_much.place(x=350, y=570)

# Add a field where the user can give input
entry2 = tk.Entry(window, fg='black', bg="gray", font=('Arial', 14), borderwidth=4)
entry2.place(x=700, y=570) # place the entry field on the window

# Add a label with feedback to the entry2
label_feedback_entry2 = tk.Label(window, text="", font=("Arial", 8), bg="green")
label_feedback_entry2.place(x=700, y=605)

# Add the variable current_balance
current_balance = 100

# Add a label with the current balance
text_current_balance = tk.Label(window, text="Current Balance:", font=("Arial", 16), bg="green")
text_current_balance.place(x=350, y=640)

# Add a label with the actual number of the current balance
display_current_balance = tk.Label(window, text="$"+str(current_balance), font=("Arial", 16, "bold"), bg="green")
display_current_balance.place(x=520, y=640)

# Create a list with valid user inputs
valid_entries = ['red', 'black', 'even', 'odd', '1to18', '19to36', '1st 12', '2nd 12', '3rd 12', 'top row', 'middle row', 'bottom row']
# Create another list with the valid user inputs, which are numbers
valid_entries_numbers =[] # the list is empty at first
for i in range(37): # then all the numbers which are valid are appended to the list
    valid_entries_numbers.append(i)

# Define the group of numbers, which will be important in finding out whether the user won or not
red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
top_row = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
middle_row = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
bottom_row = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]

# Define a feedback label
feedback = tk.Label(window, text="", font=("Arial", 14), bg="green")
feedback.place(x=30, y=600)

# Define a label with the next steps
next_steps = tk.Label(window, text="", font=("Arial", 10), bg="green")
next_steps.place(x=30, y=640)

# Add a label to display the number
win_number = tk.Label(window, text="You have not played yet.", font=("Arial", 14), bg="green")
win_number.place(x=90, y=600)

# Define a function which happens, when the spin button is clicked
def spin():
    # get the global variables
    global current_balance
    global display_current_balance

    # assign the two user inputs
    kind_of_bet = entry1.get()
    bet_amount = entry2.get()
    try: 
        bet_amount = int(bet_amount) # change the user input to int
    except ValueError:
        label_feedback_entry2.config(text="Please enter a number.", fg="red", bg="white") # tell the user that he has to change his bet amount

    
    # check if user input is a valid kind of bet
    try:
        if kind_of_bet in valid_entries or int(kind_of_bet) in valid_entries_numbers:
            label_feedback_entry1.config(text="Great! - You entered a valid kind of bet.", fg="black", bg="green") # tell the user that he entered a valid input
        else:
            label_feedback_entry1.config(text="Please enter a valid kind of bet.", fg="red", bg="white") # tell the user that he has to change his input
            return
    except ValueError:
        label_feedback_entry1.config(text="Please enter a valid kind of bet.", fg="red", bg="white") # tell the user that he has to change his input
        return

    # check if user input is a valid amount
    try:
        if isinstance(bet_amount, int):
            if bet_amount > 0: # the bet amount has to be more than zero
                if bet_amount <= current_balance: # the bet amount can not be higher than his current balance
                    label_feedback_entry2.config(text="Great! - You entered a valid amount.", fg="black", bg="green") # tell the user that he entered a valid input
                    current_balance = current_balance - bet_amount # adapt the current balance
                    display_current_balance.config(text=current_balance)
                else:
                    label_feedback_entry2.config(text="You don't have enough coins for this bet. Please change the amount.", fg="red", bg="white") # tell the user that he has to change his bet amount
                    return
    except ValueError:
        label_feedback_entry2.config(text="Not enough money left.", fg="red", bg="white") # tell the user that he has to change his bet amount
        return

   

    # spin the roulette wheel
    winning_number = random.randint(0, 36)
    # depending on the number it is displayed in another colour
    if winning_number in red_numbers:
        win_number.config(text=winning_number, bg="red")
    elif winning_number in black_numbers:
        win_number.config(text=winning_number, bg="black", fg="white")
    elif winning_number == 0:
        win_number.config(text=winning_number, bg="green")

    # determine whether the user has won or not
    # when the user bets on the colour
    if kind_of_bet == 'red' and isinstance(bet_amount, int):
        if winning_number in red_numbers:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (2 * bet_amount) # change the current amount
            display_current_balance.config(text=current_balance) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost
    elif kind_of_bet == 'black' and isinstance(bet_amount, int):
        if winning_number in black_numbers:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (2 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")

    # when the user bets on even or odd
    elif kind_of_bet == 'even' and isinstance(bet_amount, int):
        if winning_number % 2 == 0:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (2 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == 'odd' and isinstance(bet_amount, int):
        if winning_number % 2 != 0:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (2 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")

    # when the user bets on low or high number
    elif kind_of_bet == '1to18' and isinstance(bet_amount, int):
        if winning_number <= 18 & winning_number != 0:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (2 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == '19to36' and isinstance(bet_amount, int):
        if winning_number > 18 & winning_number != 0:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (2 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")

    # when the user bets on a third of the numbers
    elif kind_of_bet == '1st 12' and isinstance(bet_amount, int):
        if winning_number <= 12 & winning_number != 0:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == '2nd 12' and isinstance(bet_amount, int):
        if winning_number > 12 & winning_number <= 24:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == '3rd 12' and isinstance(bet_amount, int):
        if winning_number > 24:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")

    # when the user bets on a row
    elif kind_of_bet == 'top row' and isinstance(bet_amount, int):
        if winning_number in top_row:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == 'middle row' and isinstance(bet_amount, int):
        if winning_number in middle_row:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")
    elif kind_of_bet == 'bottom row' and isinstance(bet_amount, int):
        if winning_number in bottom_row:
            feedback.config(text="Congratulations you won!")
            current_balance = current_balance + (3 * bet_amount)
            display_current_balance.config(text=current_balance)
        else:
            feedback.config(text="You lost!")

    # when the user bets on a number
    else:
        if isinstance(bet_amount, int):
            if int(kind_of_bet) == winning_number:
                feedback.config(text="Congratulations you won!")
                current_balance = current_balance + (36 * bet_amount)
                display_current_balance.config(text=current_balance)
            else:
                feedback.config(text="You lost!")
            
    # Tell the user how he can proceed
    next_steps.config(text="If you want to play again, \n" 
                            "enter your new bet and press 'spin' again.")

# Add a spin-button to the window
spin_button = Button(window, text="Spin", style="button1.TButton", command=spin)
spin_button.place(x=95, y=450) # place the button on the window

# Start the main event loop
window.mainloop()
