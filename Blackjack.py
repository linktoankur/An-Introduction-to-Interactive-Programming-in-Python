# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite
CARD_SIZE = (42, 56)
CARD_CENTER = (21, 28)
card_images = simplegui.load_image(
    "https://www.dropbox.com/s/ksvncbio7y3s3yc/card_deck.png?dl=1")

# load table background sprite
BG_SIZE = (500, 350)
BG_CENTER = (250, 175)
BG_image = simplegui.load_image(
    "https://www.dropbox.com/s/cmfbvi09oq0rmmb/table_background.jpg?dl=1")

CARD_BACK_SIZE = (42, 56)
CARD_BACK_CENTER = (21, 28)
card_back = simplegui.load_image(
    "https://www.dropbox.com/s/y4xexkny7haqmad/card_background.png?dl=1")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 
          'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        self.show = True
        self.suit = suit
        self.rank = rank
        self.rotate = (random.random() * 0.2) - 0.1
 
    def __str__(self):
        return self.suit + self.rank
 
    def get_suit(self):
        return self.suit
 
    def get_rank(self):
        return self.rank
 
    def draw(self, canvas, pos):
        if self.show:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, (pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]), CARD_SIZE, self.rotate)
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]), CARD_BACK_SIZE, self.rotate)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = list()
 
    def __str__(self):
        return "Hand contains " + " ".join([str(i) for i in self.cards])
 
    def add_card(self, card):
        self.cards.append(card)
 
    def get_value(self):
        value = 0 
        aces = 0
        for card in self.cards:
            rank = card.get_rank()
            value += VALUES.get(rank)
            if rank == "A":
                aces += 1
        value_10 = value + (10 * aces) - aces
        if value_10 <= 21:
            value = value_10
        return value
 
    def draw(self, canvas, pos):
        i = 0
        for card in self.cards:
            card.draw(canvas, (pos[0] + (30 * i), pos[1]))
            i += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = list()
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
 
    def shuffle(self):
        random.shuffle(self.cards)
 
    def deal_card(self):
        return self.cards.pop()
 
    def __str__(self):
        return "Deck contains " + " ".join([str(i) for i in self.cards])


#define event handlers for buttons
def deal():
    global deck, player, dealer, outcome, in_play, score
    if in_play:
        score -= 50
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    for i in range(2):
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
    dealer.cards[-1].show = False
    in_play = True
    outcome = "Hit or Stand?"

def hit():
    global outcome, in_play, score
    if not in_play:
        return
    player.add_card(deck.deal_card())
    outcome = "Hit or Stand?"
    if player.get_value() > 21:
        outcome = "Busted. New deal?"
        in_play = False
        score -= 50
       
def stand():
    global outcome, in_play, score
    if not in_play:
        return
    dealer.cards[-1].show = True
    while dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())
    
    if player.get_value() == 21:
        outcome = "Blackjack! You win"
    elif (player.get_value() == dealer.get_value() and not player.get_value() == 21):
        outcome = "Equal! Split the bet!"
    elif dealer.get_value() > 21:
        score += 50
        outcome = "Dealer Busted! New deal?"
    elif player.get_value() > dealer.get_value():
        score += 50
        outcome = "You win! New deal?"
    else:
        score -= 50
        outcome = "You lose. New deal?"
    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Initializing the awesome..", (BG_SIZE[0] / 18, BG_CENTER[1]), 20, "White")
    CENTER = tuple(BG_CENTER)
    if len(outcome):
        CENTER = (BG_CENTER[0] - 250, BG_CENTER[1])
    
    canvas.draw_image(BG_image, BG_CENTER, BG_SIZE, CENTER, BG_SIZE)
    text_width = frame.get_canvas_textwidth(outcome, 18)
    canvas.draw_text(outcome, (125 - text_width / 2, 85), 18, "White")
    
    # draw score
    canvas.draw_text("$ "+str(score), (145, 302), 18, "#eeeecc")
    
    # draw hands
    dealer.draw(canvas, (40, 120))
    player.draw(canvas, (40, 212))
 
# Handler for playing with screen buttons instead of canvas buttons    
def mouse(position):
    HANDLERS = (deal, hit, stand)
    COORDS = (((40, 120), (280, 305)), ((40, 120),
             (315, 340)), ((130, 210), (315, 340)))
    i = 0
    for x, y in COORDS:
        if x[0] <= position[0] <= x[1] and y[0] <= position[1] <= y[1]:
            return HANDLERS[i]()  # execute handler
        i += 1

# initialization frame
frame = simplegui.create_frame("Blackjack", BG_SIZE[0] / 2, BG_SIZE[1])

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse)

# get things rolling
deck = Deck()
deck.shuffle()
player = Hand()
dealer = Hand()
frame.start()

# remember to review the gradic rubric