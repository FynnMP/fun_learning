from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from PIL import ImageTk, Image
import random
from graphic.roulette.loading_animation import CircularProgressbar
import json

# Create the roulette window
window = tk.Tk()

# Set the window title
window.title("Roulette")

# Set the window size
window.geometry("1000x600")

# Set the window colour
window.configure(bg="#018137")

# This means that a new window is opened over the "original" one. 
class NewWindowDescr(Toplevel):

    def __init__(self, master = None, description = None):

        super().__init__(master = window) # The Tkinter (Tk()) element which is the underlying the initiation window 
        self.title("Help Terminal") # The top level window caption
        self.geometry("700x300") # Size of the window
        self.configure(background="darkgrey") # Background color of the window 
        # Creating different text elements:
        titel = Label(self, text ="Instructions for Roulette", font = "Helvetica 14 bold", foreground="black", background="darkgrey") # Titel text and all the specifics
        titel.place(relx = 0.5, rely = 0.1, anchor = CENTER) # Determining the position of the textelement "titel"
        descr = Label(self, text = description, font = "Helvetica 10", foreground="black", background="darkgrey") # Description text and all the specifics
        descr.place(relx = 0.5, rely = 0.5, anchor = CENTER) # Determining the position of the textelement "descr"

# setting style of all widgets
style = Style()
#style.theme ('aqua', 'clam', 'alt', 'default', 'classic') (used default) --> possibility to select different
style.theme_use('default')
# Title of the games and text of the widgets text 
style.configure("button1.TButton", font="Helvetica 16 bold", background="#9FD0DD", foreground="black", padding=(10, 25, 10, 25)) # Buttons
style.configure("button2.TButton", font="Helvetica 8 bold", background="#B2B2B2", foreground="black") # Buttons

# Add a label to the window
titel = tk.Label(window, text="Welcome to Roulette!", font=("Arial", 20), bg="#018137") # define how the label should look like
titel.pack() # add the label to the window

# Add an image to the window
roulette_img = ImageTk.PhotoImage(Image.open("./graphic/roulette/roulette.png")) # select the image
image_label = Label(image=roulette_img) # add the image to the label
image_label.pack() # add the label to the window

# Add the label that asks the user what he wants to bet on
what_kind_of_bet = tk.Label(window, text="What kind of bet do you want?", font=("Arial", 16), bg="#018137") # define how the label should look
what_kind_of_bet.place(x=320, y=410) # place the label on the window

# Add a field where the user can give input
entry1 = tk.Entry(window, fg='black', bg="gray", font=('Arial', 14), borderwidth=4) # define how the label should look
entry1.place(x=750, y=410) # place the entry field on the window

# Add a label with feedback to the entry1
label_feedback_entry1 = tk.Label(window, text="", font=("Arial", 8), bg="#018137") # define how the label should look
label_feedback_entry1.place(x=750, y=445) # place the label on the window



# Help Button
btn = Button(window, text="Possible Inputs",style="button2.TButton")
btn.place(x = 380, y=460, anchor=CENTER) # place the button on the window
btn.bind("<Button>", lambda e: NewWindowDescr(window,
    "Number: \t \t Type in the number.\n"
    "Colour: \t \t Type in the colour: 'red' or 'black'.\n"
    "Even-odd: \t Type in either 'even' or 'odd'.\n"
    "1to18-19to36: \t Type in either '1to18' or '19to36'.\n"
    "1st 2nd 3rd 12: \t Type in either '1st 12', '2nd 12' or '3rd 12'.\n"
    "2 to 1: \t \t Type in either 'top row', 'middle row' or 'bottom row'.\n"
))


# Add the label that asks the user how much he wants to bet
how_much = tk.Label(window, text="How much do you want to bet?", font=("Arial", 16), bg="#018137") # define how the label should look like
how_much.place(x=320, y=500) # place the label on the windwow

# Add a field where the user can give input
entry2 = tk.Entry(window, fg='black', bg="gray", font=('Arial', 14), borderwidth=4) # define how the entry field should look like
entry2.place(x=750, y=500) # place the entry field on the window

# Add a label with feedback to the entry2
label_feedback_entry2 = tk.Label(window, text="", font=("Arial", 8), bg="#018137") # define how the entry field should look like
label_feedback_entry2.place(x=750, y=535) # place the second entry field on the window

# Add the variable current_balance
with open("wallet.json", "r") as wallet:
    wallet = json.load(wallet)
    current_balance = sum(wallet["money"])

# Add a label with the current balance
text_current_balance = tk.Label(window, text="Current Balance:", font=("Arial", 16), bg="#018137")
text_current_balance.place(x=320, y=560) # place the label on the window

# Add a label with the actual number of the current balance
display_current_balance = tk.Label(window, text="$"+str(current_balance), font=("Arial", 16, "bold"), bg="#018137")
display_current_balance.place(x=550, y=560) # place the label on the window

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
feedback = tk.Label(window, text="", font=("Arial", 14, "bold"), bg="#018137") # define how the label should look like
feedback.place(x=160, y=550, anchor="center") # place the label on the window

# Define a label with the next steps
next_steps = tk.Label(window, text="", font=("Arial", 8), bg="#018137") # define how the label should look like
next_steps.place(x=160, y=580, anchor="center") # place the label on the window

# Add a label to display the number
win_number = tk.Label(window, text="", font=("Arial", 14), bg="#018137") # define how the label should look like
win_number.place(x=160, y=520, anchor="center") # place the label on the window


# Define a function to handle the timing of loading and result after the button is clicked
def spin_button_handler():

    global current_balance
    global display_current_balance

    # assign the two user inputs
    kind_of_bet = entry1.get()
    bet_amount = entry2.get()
    try: 
        bet_amount = int(bet_amount) # change the user input to int
        label_feedback_entry2.config(text="Great! - You entered a valid amount.", fg="black", bg="#018137") # tell the user that he entered a valid input
    except ValueError:
        label_feedback_entry2.config(text="Please enter a number.", fg="red", bg="white") # tell the user that he has to change his bet amount

    
    # check if user input is a valid kind of bet
    try:
        if kind_of_bet in valid_entries or int(kind_of_bet) in valid_entries_numbers:
            label_feedback_entry1.config(text="Great! - You entered a valid kind of bet.", fg="black", bg="#018137") # tell the user that he entered a valid input
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
                    label_feedback_entry2.config(text="Great! - You entered a valid amount.", fg="black", bg="#018137") # tell the user that he entered a valid input
                else:
                    label_feedback_entry2.config(text="You don't have enough coins for this bet.", fg="red", bg="white") # tell the user that he has to change his bet amount
                    return
    except ValueError:
        label_feedback_entry2.config(text="Not enough money left.", fg="red", bg="white")
        return

    try:
        if isinstance(bet_amount, int) and bet_amount>0 and bet_amount<=current_balance and (kind_of_bet in valid_entries or int(kind_of_bet) in valid_entries_numbers):
            # Disable the button
            spin_button.config(state=tk.DISABLED)
            stop_results()
            current_balance = current_balance - bet_amount # adapt the current balance
            display_current_balance.config(text="$"+str(current_balance))
            loading_animation()
            window.after(1870, lambda: stop_loading_animation() or spin() or enable_spin_button())

    except:
        None
    # Enable the button again
    


def enable_spin_button():
    spin_button.config(state=tk.NORMAL)

# create the initial canvas object
myCanvas = None

# Define a function to create the loading animation
def loading_animation():
    global myCanvas
    # create new canvas for loading animation
    myCanvas = tk.Canvas(window, bg="#018137", height=90, width=90, highlightthickness=0)
    myCanvas.place(x=160, y=550, anchor="center")
    progressbar = CircularProgressbar(myCanvas, 0, 0, 90, 90, 15)
    progressbar.start()

# Define a function to stop the loading animation
def stop_loading_animation():
    global myCanvas
    myCanvas.destroy()


# Define a function which happens, when the spin button is clicked
def spin():
    # get the global variables
    global current_balance
    global display_current_balance

    # assign the two user inputs
    kind_of_bet = entry1.get()
    bet_amount = int(entry2.get())

    
 

   

    # spin the roulette wheel
    winning_number = random.randint(0, 36)
    # depending on the number it is displayed in another colour
    if winning_number in red_numbers:
        win_number.config(text=winning_number, bg="red")
    elif winning_number in black_numbers:
        win_number.config(text=winning_number, bg="black", fg="white")
    elif winning_number == 0:
        win_number.config(text=winning_number, bg="#018137")

    # determine whether the user has won or not
    # when the user bets on the colour
    if kind_of_bet == 'red' and isinstance(bet_amount, int):
        if winning_number in red_numbers:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (2 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost
    elif kind_of_bet == 'black' and isinstance(bet_amount, int):
        if winning_number in black_numbers:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (2 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost

    # when the user bets on even or odd
    elif kind_of_bet == 'even' and isinstance(bet_amount, int):
        if winning_number % 2 == 0:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (2 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str("$"+str(current_balance))) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost
    elif kind_of_bet == 'odd' and isinstance(bet_amount, int):
        if winning_number % 2 != 0:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (2 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost

    # when the user bets on low or high number
    elif kind_of_bet == '1to18' and isinstance(bet_amount, int):
        if winning_number <= 18 & winning_number != 0:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (2 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost
    elif kind_of_bet == '19to36' and isinstance(bet_amount, int):
        if winning_number > 18 & winning_number != 0:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (2 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost

    # when the user bets on a third of the numbers
    elif kind_of_bet == '1st 12' and isinstance(bet_amount, int):
        if winning_number <= 12 & winning_number != 0:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (3 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost
    elif kind_of_bet == '2nd 12' and isinstance(bet_amount, int):
        if winning_number > 12 & winning_number <= 24:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (3 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost
    elif kind_of_bet == '3rd 12' and isinstance(bet_amount, int):
        if winning_number > 24:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (3 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost

    # when the user bets on a row
    elif kind_of_bet == 'top row' and isinstance(bet_amount, int):
        if winning_number in top_row:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (3 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost
    elif kind_of_bet == 'middle row' and isinstance(bet_amount, int):
        if winning_number in middle_row:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (3 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost
    elif kind_of_bet == 'bottom row' and isinstance(bet_amount, int):
        if winning_number in bottom_row:
            feedback.config(text="Congratulations you won!") # tell the user that he won
            current_balance = current_balance + (3 * bet_amount) # change the current amount
            display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
        else:
            feedback.config(text="You lost!") # tell the user that he lost

    # when the user bets on a number
    else:
        if isinstance(bet_amount, int):
            if int(kind_of_bet) == winning_number:
                feedback.config(text="Congratulations you won!") # tell the user that he won
                current_balance = current_balance + (36 * bet_amount) # change the current amount
                display_current_balance.config(text="$"+str(current_balance)) # display the new current amount
            else:
                feedback.config(text="You lost!") # tell the user that he lost
            
    # Tell the user how he can proceed
    next_steps.config(text="If you want to play again, \n" 
                            "enter your new bet and press 'spin' again.")

def stop_results():
    feedback.config(text="")
    next_steps.config(text="")

# Add a spin-button to the window
spin_button = Button(window, text="Spin", style="button1.TButton", command=spin_button_handler) # define how the button should look like
spin_button.place(x=95, y=420) # place the button on the window


# Save current balance to json when closing
def on_closing():
    # update money to be used in shop etc. 
    with open("wallet.json", "w") as jsonFile: 
        money = []
        new_balance = current_balance
        money.append(int(round(float(new_balance))))
        wallet = {}
        wallet["money"] = money
        json.dump(wallet, jsonFile)

    window.destroy()


# Start the main event loop
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
