# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simplegui
import math

# initialize global variables used in your code
compGuess = 0
remGuesses = 0
gameActive = ""


# helper function to start and restart the game
def new_game():
    range100()

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global compGuess
    global remGuesses
    global gameActive
    gameActive = 1
    compGuess = random.randrange(0, 100)
    remGuesses = 7
    print " "
    print "New game. Range is from 0 to 100"
    print "Number of remaining guesses is ",remGuesses
    

def range1000():
    # button that changes range to range [0,1000) and restarts
    global compGuess
    global remGuesses
    global gameActive
    gameActive = 0
    compGuess = random.randrange(0, 1000)
    remGuesses = 10
    print " "
    print "New game. Range is from 0 to 1000"
    print "Number of remaining guesses is ",remGuesses
    

def input_guess(guess):
    # main game logic goes here	
    global compGuess
    global remGuesses
    global gameActive
    guess = int(guess)
    remGuesses -= 1
    
    print " "
    print "Guess was ",guess
    print "Number of remaining guesses is ",remGuesses
    
    if compGuess > guess:
        if remGuesses <= 0:
            print "You ran out of guesses. The number was ",compGuess
            if gameActive:
                range100()
                return
            else:
                range1000()
                return
        print "Higher!"
    
    elif compGuess < guess:
        if remGuesses <= 0:
            print "You ran out of guesses. The number was ",compGuess
            if gameActive:
                range100()
                return
            else:
                range1000()
                return
        print "Lower!"
    
    else:
        print "Correct!"
        if gameActive:
            range100()
        else:
            range1000()
    
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game and start frame
new_game()
f.start()

# always remember to check your completed program against the grading rubric