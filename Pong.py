# Implementation of classic arcade game 'Pong'

# Addons:
#	1. Changed background frame color.
#	2. Changed paddle colors.
#	3. Changed ball color.
#	4. Changed midline and gutter colors.
#	5. Added buttons to start game and reset scores.
#	6. Fixed space between scores when Player1's score becomes >=10

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [random.randrange(120,240), random.randrange(60,180)]
    
    if(direction == RIGHT):
        ball_vel[1] = -ball_vel[1]
    if(direction == LEFT):
        ball_vel[0] = -ball_vel[0]
        ball_vel[1] = -ball_vel[1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    paddle1_pos = HEIGHT / 2  
    paddle2_pos = HEIGHT / 2  
    paddle1_vel = 0  
    paddle2_vel = 0  
    score1 = 0  
    score2 = 0  
    if score1 >= score2:  
        spawn_ball(LEFT)  
    else:  
        spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "#FFFF33")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "#FFFF33")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "#FFFF33")
        
    # update ball
    # code to check top/bottom bounds
    if(ball_pos[1]<=BALL_RADIUS) or (ball_pos[1]>=HEIGHT-BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        
    # code to check left/right bounds
    if ball_pos[0] <= BALL_RADIUS:    
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1]<=paddle1_pos + HALF_PAD_HEIGHT:    
            ball_vel[0] = -ball_vel[0]    
            ball_vel[0] = ball_vel[0] * 1.1    
            ball_vel[1] = ball_vel[1] * 1.1    
        else:    
            spawn_ball(RIGHT)    
            score2 += 1    
    elif ball_pos[0] >= WIDTH-BALL_RADIUS:    
        if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:    
            ball_vel[0] = -ball_vel[0]    
            ball_vel[0] = ball_vel[0] * 1.1    
            ball_vel[1] = ball_vel[1] * 1.1    
        else:    
            spawn_ball(LEFT)    
            score1 += 1  
          
    ball_pos[0]+=ball_vel[0]/60    
    ball_pos[1]+=ball_vel[1]/60
        
    # draw ball
    canvas.draw_circle(ball_pos, 20, 3, "#FF3300", "#66FF66")
    
    # update paddle's vertical position, keep paddle on the screen
    if HALF_PAD_HEIGHT <= paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:  
        paddle1_pos += paddle1_vel
        
    if HALF_PAD_HEIGHT <= paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:  
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], PAD_WIDTH, "#FF3300")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], PAD_WIDTH, "#00FF7F")  
    
    # draw scores
    if score1<10:
        canvas.draw_text(str(score1) + "       " + str(score2), (WIDTH / 2 - 100, 40), 36, "Yellow", "monospace")
    elif score1>9:
        canvas.draw_text(str(score1) + "       " + str(score2), (WIDTH / 2 - 122, 40), 36, "Yellow", "monospace")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 10  
    if key == simplegui.KEY_MAP['s']:    
        paddle1_vel = vel    
    elif key == simplegui.KEY_MAP['w']:    
        paddle1_vel = -vel    
    elif key == simplegui.KEY_MAP['up']:    
        paddle2_vel = -vel    
    elif key == simplegui.KEY_MAP['down']:    
        paddle2_vel = vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:    
        paddle1_vel = 0    
    elif key == simplegui.KEY_MAP['w']:    
        paddle1_vel = 0    
    elif key == simplegui.KEY_MAP['up']:    
        paddle2_vel = 0    
    elif key == simplegui.KEY_MAP['down']:    
        paddle2_vel = 0

def start_button_handler():
    new_game()
    frame.start()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
start_button = frame.add_button("Start Game!", start_button_handler, 150)
reset_button = frame.add_button("Reset Scores!", new_game, 150)
frame.set_canvas_background('#808080 ')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
# used button handler to start, hence function defined above