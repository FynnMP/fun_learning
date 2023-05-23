# This is the main file to run our project, make sure that all necessary libraries are installed and the 
# folder strucutre is not changed (see Readme for additional information). 
# Apart from that, just run this file and have fun. 


# Import necessary libraries for creating the menu UI
from tkinter import *
from tkinter.ttk import *
import subprocess, sys
import json

# A class used to place the images/snippets of the games on the screen.
# The class takes the image's directory and the x and y coordinates.
class GameImg:
    def __init__(self, filename, y_pos, x_pos=0):
        dis_x = 300  # Fixed add-on to the x coordinate
        self.im = PhotoImage(file=filename)  # Create a PhotoImage object to use within tkinter
        self.lbl = Label(window, image=self.im)  # Initiate a label to be positioned on the window
        self.lbl.place(x=dis_x + x_pos, y=y_pos * dis + 0.7 * dis, anchor=CENTER)  # Place the label using the defined coordinates with some fixed addition

# The NewWindowDescr class enables the initiation of "top-level" windows
# This means that a new window is opened over the "original" one
class NewWindowDescr(Toplevel):
    def __init__(self, master=None, description=None):
        super().__init__(master=window)  # The Tkinter (Tk()) element which is the underlying the initiation window
        self.title("Help Terminal")  # The top-level window caption
        self.geometry("500x350")  # Size of the window
        self.configure(background="darkgrey")  # Background color of the window
        # Create different text elements:
        titel = Label(self, text="Help", font="Helvetica 18 bold", foreground="black", background="darkgrey")  # Title text and all the specifics
        titel.place(relx=0.5, rely=0.1, anchor=CENTER)  # Determine the position of the text element "title"
        descr = Label(self, text=description, font="Helvetica 14", foreground="black", background="darkgrey")  # Description text and all the specifics
        descr.place(relx=0.5, rely=0.5, anchor=CENTER)  # Determine the position of the text element "descr"

# The actual window for the menu is defined and designed
window = Tk()
# Create a graphical element of the GUI with the background color white
canvas = Canvas(bg="white")
# Determine the size of the window
wgeox, wgeoy = 600, 650

# Putting the HSG logo on the top-left corner
logo = PhotoImage(file="./graphic/menu/logo_new.png")  # Create a PhotoImage element with the HSG logo file
logolbl = Label(window, image=logo)  # Initiate a label with the image to display on the canvas and position it
logolbl.place(x=200, y=30, anchor="nw")  # Position the label with the HSG PhotoImage element

# Create dashed lines to separate the different sections with the title and the games
dis = 120
for i in range(200, wgeoy, dis):
    canvas.create_line(0, i, wgeox, i, dash=(4, 2))
canvas.pack(fill=BOTH, expand=1)

# Distance from line to game title and from line to button
dis_lt = 110
dis_lb = 155

# Using the GameImg class to create the thunbnails for the different games/casino games with the filenames and the y and x coordinates (for details see GameImg class)
learning_im = GameImg("./graphic/menu/learning.png", 1.6)
casino_im = GameImg("./graphic/menu/roulette_icon.png", 2.6)
money_im = GameImg("./graphic/menu/money.png", 3.6)


# setting style of all widgets
style = Style()
style.theme_use('default')
# Title of the games and text of the widgets text 
style.configure("TButton", font="Helvetica 12 bold", background="#9FD0DD", foreground="black") # Buttons
style.configure("W.TButton", font="Helvetica 8 bold", background="#B2B2B2", foreground="black") # Buttons
style.configure("TLabel", font="Helvetica 18 bold", background="white", foreground="#E78200") # Game Titles


# Help Button
btn = Button(window, text="Help",style="W.TButton")
btn.place(relx=0.9, y=30, anchor=CENTER) # Placement of help button
btn.bind("<Button>", lambda e: NewWindowDescr(window,
                                              "         Welcome to our LEARNxCASINO platform. \n"
                                              "         In the Learning section you can earn money by \n"
                                              "         memorizing important concepts of Strategic \n"
                                              "         Management or Accounting. \n"
                                              "         You can use that money to visit the Casino \n"
                                              "         and easily multiply it - or loose it all. \n"
                                              "         The money you gained can be used in the shop to \n"
                                              "         buy fancy items, such as cars, watches, \n"
                                              "         boats, and art. \n"
                                              "         Don´t forget to inspect your purchased items in \n" 
                                              "         high resolution in the showroom."))

# relative placement of titles and buttons for each game / casino game
rx_title = 0.5
rx_button1 = 0.2
rx_button2 = 0.5
rx_button3 = 0.8

############### Learning
# The Learning title is created and then placed using the above specified coordinates and relative positions
l_titel_L = Label(window, text="Learning")
l_titel_L.place(relx=rx_title, y=dis+dis_lt, anchor="center")

# The function to run the management memory 
def run_management():
    python_executable = sys.executable
    script_file = "memory_management.py"
    command = [python_executable, script_file]
    subprocess.run(command, check=True)

# Creating and placing a button to be clicked to start the management memory
btn1 = Button(window, text="Mangement", command = run_management) # Button element with the name Management
btn1.place(relx=rx_button1, y=dis+dis_lb, anchor=CENTER) # placing the button


# Define function to run accounting memory
def run_accounting():
    python_executable = sys.executable
    script_file = "memory_accounting.py"
    command = [python_executable, script_file]
    subprocess.run(command, check=True)

# Creating and placing a button to be clicked to start the accounting memory
btn1_3 = Button(window, text="Finance", command = run_accounting)
btn1_3.place(relx=rx_button3, y=dis+dis_lb, anchor=CENTER)


############### Casino
# The Casino title is created and then placed using the above specified coordinates and relative positions
l_titel_C = Label(window, text="Casino")
l_titel_C.place(relx=rx_title, y=2*dis+dis_lt, anchor="center")

# Define function to run roulette
def run_roulette():
    python_executable = sys.executable
    script_file = "roulette.py"
    command = [python_executable, script_file]
    subprocess.run(command, check=True)
    
# Creating and placing a button to be clicked to start the roulette game
btn2 = Button(window, text="Roulette", command = run_roulette)
btn2.place(relx=rx_button1, y=2*dis+dis_lb, anchor=CENTER)

# Define function to run the slot machine 
def run_slots():
    python_executable = sys.executable
    script_file = "slots.py"
    command = [python_executable, script_file]
    subprocess.run(command, check=True)

# Creating and placing a button to be clicked to start the slot machine
btn2_2 = Button(window, text="Slots", command = run_slots)
btn2_2.place(relx=rx_button3, y=2*dis+dis_lb, anchor=CENTER)



############### Spending Money
# The Spending Money title is created and then placed using the above specified coordinates and relative positions
l_titel_M = Label(window, text="Spending Money")
l_titel_M.place(relx=rx_title, y=3*dis+dis_lt, anchor="center")

# Define function to open the shop
def run_shop():
    python_executable = sys.executable
    script_file = "shop.py"
    command = [python_executable, script_file]
    subprocess.run(command, check=True)

# Creating and placing a button to be clicked to open the shop
btn3 = Button(window, text="Shop", command = run_shop)
btn3.place(relx=rx_button1, y=3*dis+dis_lb, anchor=CENTER)

# Define function to open the showroom
def run_showroom():
    python_executable = sys.executable
    script_file = "showroom.py"
    command = [python_executable, script_file]
    subprocess.run(command, check=True)

# Creating and placing a button to be clicked to open the showroom
btn3_2 = Button(window, text="Showroom", command = run_showroom)
btn3_2.place(relx=rx_button3, y=3*dis+dis_lb, anchor=CENTER)

############### Current Balance 
# load current balance once from json file 
with open("wallet.json", "r") as wallet:
            wallet = json.load(wallet)
            money = wallet["money"]

# define function to consistently update money
def update_balance():
    # Open the JSON file and load the contents
    with open("wallet.json", "r") as wallet:
        wallet = json.load(wallet)
        money = wallet["money"]

    # Update the balance label with the new value
    l_titel_B.config(text="Your current balance is: %d$" % sum(money))
    # Call this function again after 1 second
    window.after(1000, update_balance)

# Create and place the balance label
l_titel_B = Label(window, text="Your current balance is: %d$" % sum(money), background="white", foreground="black", font="Helvetica 12 bold")
l_titel_B.place(relx=rx_title, y=4*dis+dis_lt+13, anchor="center")

# Call the update_balance function to start the loop
update_balance()

# Schedule the function to run the first time
window.after(1, update_balance)


# The before specified window size (wgeox, wgeoy) is now bound to the window
window.geometry(str(wgeox)+"x"+str(wgeoy)+"+10+10") #10 + 10 specifies the position of the window in on the display of the user when opened
window.resizable(0, 0) # Ensure the window is not resizable as not all the elements are adjustable
window.title('Menu') # set the caption for the Inition Window
# Execute tkinter
window.mainloop()
