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
        self.geometry("600x400")  # Size of the window
        self.configure(background="darkgrey")  # Background color of the window
        # Create different text elements:
        titel = Label(self, text="Help", font="Helvetica 16 bold", foreground="black", background="darkgrey")  # Title text and all the specifics
        titel.place(relx=0.5, rely=0.1, anchor=CENTER)  # Determine the position of the text element "title"
        descr = Label(self, text=description, font="Helvetica 12", foreground="black", background="darkgrey")  # Description text and all the specifics
        descr.place(relx=0.5, rely=0.5, anchor=CENTER)  # Determine the position of the text element "descr"


class NewWindowQ_A(Toplevel):
    def __init__(self, master=None, description=None):
        super().__init__(master=window)  # The Tkinter (Tk()) element which is the underlying the initiation window
        self.title("Questions and Answers")  # The top-level window caption
        self.geometry("900x700")  # Size of the window
        self.configure(background="darkgrey")  # Background color of the window
        # Create different text elements:
        titel = Label(self, text="Questions and Answers", font="Helvetica 12 bold", foreground="black", background="darkgrey")  # Title text and all the specifics
        titel.place(relx=0.5, rely=0.05, anchor=CENTER)  # Determine the position of the text element "title"
        descr = Label(self, text=description, font="Helvetica 8", foreground="black", background="darkgrey")  # Description text and all the specifics
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
                                              "         In the learning section you can earn money by \n"
                                              "         memorizing important concepts of strategic \n"
                                              "         management or corporate finance. \n"
                                              "         You can use that money to visit the Casino \n"
                                              "         and easily multiply it - or loose it all. \n"
                                              "         The money you gained can be used in the shop to \n"
                                              "         buy items, such as watches, cars, \n"
                                              "         boats and art. \n"
                                              "         Don´t forget to inspect your purchased items in a \n" 
                                              "         higher resolution in the showroom."))

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

# Q&A library Button managment 
btn1_1 = Button(window, text="?", style="W.TButton", width=3)
btn1_1.place(relx=rx_button1-0.12, y=dis+dis_lb, anchor=CENTER) # Placement of help button
text_sgmm = "What is management? \n" \
       "    It's a black box, omnipresent and controversial.\n\n" \
       "What are two key drivers of management? \n" \
       "    The two key drivers are uncertainties and insecurities.\n\n" \
       "What is the definition of sensemaking? \n" \
       "    It's a communicative process of the everyday constitution of meaning, relating topics to one another in a way that \n" \
       "    creates meaning, condensing, evaluating.\n\n" \
       "What is the definition of environment? \n" \
       "    It's a space of possibility, expectation and action relevant to the existence of organisational value creation.\n\n" \
       "What is the definition of enactment? \n" \
       "    It's a concretisation and creation process of New Things.\n\n" \
       "What is the definition of resource configuration? \n" \
       "    The possibility space of an organisation must first be developed and then exhausted.\n\n" \
       "What does horizontal plurality mean? \n" \
       "    The need to consider a variety of different possibilities as opportunities.\n\n" \
       "What is the definition of environmental spheres? \n" \
       "    Discourses that are collectively established and institutionally routinised forms of communication.\n\n" \
       "What is at the centre of a controversy? \n" \
       "    There is a tense core issue that subsequently becomes an issue depending on the stakeholders.\n\n" \
       "What is the task of value creation? \n" \
       "    It must contribute to satisfying needs and eliminating scarcity and create benefit.\n\n" \
       "What are three dimensions of a decision? \n" \
       "    Decision necessities, forms of processing, and decision-making ability.\n\n" \
       "What are three measures of success from the operational time horizon? \n" \
       "    Turnover, contribution margins, and margins.\n"

btn1_1.bind("<Button>", lambda e: NewWindowQ_A(window,text_sgmm))


# Define function to run finance memory
def run_finance():
    python_executable = sys.executable
    script_file = "memory_finance.py"
    command = [python_executable, script_file]
    subprocess.run(command, check=True)

# Creating and placing a button to be clicked to start the finance memory
btn1_3 = Button(window, text="Finance", command = run_finance)
btn1_3.place(relx=rx_button3, y=dis+dis_lb, anchor=CENTER)

# Q&A library Button managment 
btn1_31 = Button(window, text="?", style="W.TButton", width=3)
btn1_31.place(relx=rx_button3+0.11, y=dis+dis_lb, anchor=CENTER) # Placement of help button
text_cf = "What is the formula of the capital asset pricing model (CAPM)?\n" \
       "    E(ri) = rf + βi * (E(rm) - rf)\n\n" \
       "What is the beta of the market portfolio?\n" \
       "    It measures the sensitivity of an asset movement compared to the market portfolio.\n\n" \
       "What are three determinants of asset betas?\n" \
       "    Cyclicality, operating leverage, and time horizon of the project.\n\n" \
       "What is the major risk of debt?\n" \
       "    The major risk is the default risk.\n\n" \
       "What is an Initial Public Offering (IPO)?\n" \
       "    It's the process of offering shares of a private corporation to the general public in a new stock issuance.\n\n" \
       "What is asymmetric information in the pecking order theory?\n" \
       "    It affects the choice between internal and external financing and between new issues of debt and equity securities.\n\n" \
       "What is meant by a random walk?\n" \
       "    It's a random process in a discrete period.\n\n" \
       "What are three types of market efficiency?\n" \
       "    Weak-form, semi-strong-form, and strong-form efficiency.\n\n" \
       "What is insider trading?\n" \
       "    Buying or selling a security by someone who has access to material nonpublic information about the security.\n\n" \
       "What are the two definitions of market efficiency?\n" \
       '    "There is no free lunch" and "Price equals value".\n\n' \
       "What is the value at risk (VaR)?\n" \
       "    It's a measure of the risk of loss for investments.\n\n" \
       "What is the expected shortfall?\n" \
       "    It's the average of all losses which are greater or equal to VaR.\n"

btn1_31.bind("<Button>", lambda e: NewWindowQ_A(window,text_cf))

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
