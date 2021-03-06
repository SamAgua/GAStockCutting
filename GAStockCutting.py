import time  # for pause during graphic display
import random
import sys

# import tkFont  # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/fonts.html
random.seed(time.time()) # Initialize internal state of the random number generator.

#NUMBER_OF_PIECES = 6  # HARDCODED
#STOCK_WIDTH = 800  # HARDCODED  Width of stock
#STOCK_HEIGHT = 400  # HARDCODED  Height of stock =
NUMBER_OF_GENERATIONS = 10  # HARDCODED Number of generations of evolution
POPULATION_SIZE = 10  # HARDCODED Number of individuals in population

piece_colors = ["gold", "deepskyblue", "green3", "tan1", "orchid1",
                "purple1", "red2", "palegreen", "goldenrod", "thistle2", "lightblue3",
                "thistle"]

''' 
Definition of a class Piece that has data members:
        xcoord  X coordinate of the upper left corner
        ycoord  Y coordinate of the upper left corner
        . . . (other values as desired)
        
Create an object of the class Piece using     Piece(x, y, ...)
Place an object of the class Piece into a list   myList.append(myPiece)
'''


class Piece:
    def __init__(self, xcoord, ycoord):  # Add other values to this list
        self.x = xcoord
        self.y = ycoord

    def setX(self, xcoord):
        self.x = xcoord

    def setY(self, ycoord):
        self.y = ycoord

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    # As you wish, define other function members of class Piece
    # to return other individual values or a set of several
    # values within a tuple or list.


'''
Create a Piece object in a dictionary data structure, using the parameters
for the piece position.
TBD -- this places the piece within the stock (as opposed to putting
at least the UL corner but not necessarily the LR corner in stock)
'''


# https://www.w3schools.com/python/python_dictionaries.asp
def makeRectObj(w, h, x1, y1, c):
    return {"width": w, "height": h, "color": c,
            "x1": x1, "y1": y1,
            "x2": x1 + w, "y2": y1 + h}  # Return a dictionary object


def switchRects(p1, rect1, p2, rect2):
    swtch = p1[rect1]
    p1[rect1] = p2[rect2]
    p2[rect2] = swtch


# Read data from a file if a file is given on the command line.
# Open the file and read it into the list "content"
if (len(sys.argv) > 1):  # A command-line argument exists; assume it is an input filename
    filename = sys.argv[1]
# This section not genuinely indented, but necessary for comment
else:  # Prompt for input filename
    #filename = input("\n\n\tPlease type an input data file name: ")
    filename = "Test1Data.txt"

    try:
        with open(filename) as f:
            content = f.readlines()
    except FileNotFoundError:
        sys.exit('Could not find file ' + filename)

    STOCK_WIDTH = int(content[0])
    STOCK_HEIGHT = int(content[1])
    NUMBER_OF_PIECES = 5

    # Data in file is expected to be, on separate lines as shown:
    #       Width of stock
    #       Height of stock
    #       Number of pieces to be cut from stock
    #       Width Height   of piece 0
    #       Width Height   of piece 1
    #               . . .
    #       Width Height   of piece (N-1)
    #
    # Show the data of the input data file, one word at a time
    for i in range(0, len(content)):
        line = content[i].split()
        for j in range(0, len(line)):
            print(str(line[j]))
        # print()



# Use tkinter to display stock and pieces
from tkinter import *

root = Tk()
canvas = Canvas(root, width=STOCK_WIDTH, height=STOCK_HEIGHT, bg='khaki')
canvas.pack()



''' Initialize and display POPULATION_SIZE number of pieces.
TBD -- Initially, create all pieces of _size_ 200x200, 
at _positions_ TBD.  
TBD -- this places the piece within the stock (as opposed to putting
at least the UL corner but not necessarily the LR corner in stock)
'''


population = [0 for i in range(POPULATION_SIZE)]
for indiv_count in range(POPULATION_SIZE):
    individual = [0 for j in range(NUMBER_OF_PIECES)]

    #for piece_count in range(NUMBER_OF_PIECES):
    for piece_count in range(0, 5):
        line = content[piece_count+3].split()
        w = int(line[0])  # TBD HARDCODED
        h = int(line[1])  # TBD HARDCODED
        c = piece_colors[piece_count]  # TBD -- need more colors when more pieces
        x1 = random.randint(0, STOCK_WIDTH - w)  # piece is within stock
        y1 = random.randint(0, STOCK_HEIGHT - h)  # piece is within stock

        # An individual is an array of dictionary objects
        individual[piece_count] = makeRectObj(w, h, x1, y1, c)
        # print(individual[piece_count])
        # print("        Piece ", piece_count, " x1 is ", (individual[piece_count]).get("x1"))

        # TBD  -- display the  first individual
        # in general, display the fittest individual of this generation
        if indiv_count == 0:
            canvas.create_rectangle(x1, y1, x1 + w, y1 + h, fill=c, outline='black')
            canvas.update()
            time.sleep(0.02)  # HARDCODED

        # print("individual  is ", individual)
        # print()

    # The population is an array of individual objects
    population[indiv_count] = individual
    print("population[", indiv_count, "] is ", population[indiv_count])
    print()
    # print("Piece ", piece_count, " x1 is ", (population[piece_count]).get("x1")
    # print("Piece ", piece_count, " x1 is ", (population[piece_count])["x1"]
    # print("Piece ", piece_count, " x1 is ", (population[piece_count])["x1"]
    # print(population[piece_count])["x1"]

    # print()



'''
This is the main GA loop, performing the evolutionary sequence of
operations: Evaluation, Selection, Crossover, Mutation.
Remember:
        A POPULATION is a set of POPULATION_SIZE individuals.
        An INDIVIDUAL is a set of PIECE_COUNT pieces.
'''

for looper in range(NUMBER_OF_GENERATIONS):

    # EVALUATE ALL INDIVIDUALS
    fitness = [0 for i in range(POPULATION_SIZE)]
    fit_count = 0
    for indiv in population:
        compGrid = [[0 for i in range(STOCK_WIDTH)] for j in range(STOCK_HEIGHT)]
        sum_fitness = 0
        for piece in indiv:
            x1 = piece.get("x1")
            print(x1)
            x2 = piece.get("x2")
            y1 = piece.get("y1")
            y2 = piece.get("y2")
            for m in range(y1, y2 + 1):
                for n in range(x1, x2 + 1):
                    if compGrid[m][n] == 0:
                        compGrid[m][n] = 1
                        sum_fitness += 1
        fitness[fit_count] = ((STOCK_HEIGHT * STOCK_WIDTH) - sum_fitness)
        fit_count += 1
        print(fitness)

    # Display all pieces in their new position.
    # In general, display the fittest individual of this generation.
    # In this demo, display only the first individual.
    # Clear the display by re-drawing the background with no elements
    canvas.create_rectangle(0, 0, STOCK_WIDTH, STOCK_HEIGHT, fill='khaki')
    fittest_index = fitness.index(min(fitness))
    display_individual = population[fittest_index]  # display this individual, which is a list of dictionary

    print("fittest index is ", fittest_index)
    for piece_count in range(NUMBER_OF_PIECES):
        canvas.create_rectangle(display_individual[piece_count].get("x1"),
                                display_individual[piece_count].get("y1"),
                                display_individual[piece_count].get("x2"),
                                display_individual[piece_count].get("y2"),
                                fill=display_individual[piece_count].get("color"),
                                outline="black")
        # tkFont.Font(family='Helvetica',size=36, weight='bold') # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/fonts.html
        canvas.create_text(display_individual[piece_count].get("x1") + 20,
                           display_individual[piece_count].get("y1") + 20,
                           text=str(piece_count))

    canvas.update()
    time.sleep(1)  # HARDCODED TIME -- pause briefly between generations

    # SELECT INDIVIDUALS FOR REPRODUCTION IN THE NEXT GENERATION
    p1 = random.randint(0, 9)
    p2 = random.randint(0, 9)
    while (p1 == p2):
        p2 = random.randint(0, 9)
    ind_1 = population[p1]
    ind_2 = population[p2]
    # CROSSOVER OPERATION FOR INDIVIDUALS
    switchRects(ind_1, random.randint(0, 5), ind_2, random.randint(0, 5))

    p1 = random.randint(0, 9)
    p2 = random.randint(0, 9)
    while (p1 == p2):
        p2 = random.randint(0, 9)
    ind_1 = population[p1]
    ind_2 = population[p2]
    switchRects(ind_1, random.randint(0, 5), ind_2, random.randint(0, 5))

    # MUTATION OPERATION FOR INDIVIDUALS
    # In general, select with some randomness "several" individuals upon which
    # to perform mutation of "some" (one or more) characteristics.
    # TBD This demo is hardcoded to change only the first characteristic of the first individual.
    mutating_individual = population[random.randint(0, 9)]  # mutating_individual is a list of dictionary
    # print()
    # print("mutating indiv is ", mutating_individual)
    print()
    mutating_characteristic = mutating_individual[random.randint(0, 5)]
    # print(" mutating_characteristic is ", mutating_characteristic)
    # print()

    prev_value = mutating_characteristic.get("x1")
    new_value = prev_value + 5  # Mutate by incrementing
    mutating_characteristic["x1"] = new_value
    prev_value = mutating_characteristic.get("x2")
    new_value = prev_value + 5  # Mutate by incrementing
    mutating_characteristic["x2"] = new_value

mainloop()  # Graphics loop -- This statement follows all other statements
