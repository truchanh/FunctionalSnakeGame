from random import randint
import pygame as pg
from pygame.constants import (
    DOUBLEBUF,HWSURFACE,    
    WINDOWCLOSE,QUIT,
    KEYDOWN,KEYUP,K_RIGHT,K_LEFT,K_UP,K_DOWN
    )
pg.init()
pg.display.set_caption('sn4k8')

def randomise_fruit_position():
    '''
	;generate fruit at random location
    ;with the help of randint method inside
    ;the random module/library and don't
    ;forget the left and right bounds
    ;of randint() also included
    '''
    fruit_left = randint(0,CELLCOL-1)*CELLSIZE
    fruit_top  = randint(0,CELLROW-1)*CELLSIZE
    fruit_rect = pg.Rect(fruit_left,fruit_top,CELLSIZE,CELLSIZE)
    return fruit_rect


def display_score(info,color,pos):
    font = pg.font.SysFont('comicsansms',13)
    score_surf = font.render(info,True,color)
    score_rect = score_surf.get_rect(topleft=pos)
    win.blit(score_surf,score_rect)


def draw_grid():
    '''
    ;draw a 2d grid board by
    ;using 2d list-comprehension technique
    ;quite difficult to read
    ;also using waldrus operator ```:=```
    ;to assign variables in the comprehension target
    ;NOTE that we don't want to draw any
    ;lines at the edges of the screen (left and right, top and bottom)
    '''
    [[(x:=j*CELLSIZE,
       y:=i*CELLSIZE,
       pg.draw.line(win,LINE_COLOR,(x,0),(x,dims[1]),1),
       pg.draw.line(win,LINE_COLOR,(0,y),(dims[0],y),1))
      for j in range(1,CELLCOL,1)]
     for i in range(1,CELLROW,1)]


def draw_fruit():
    pg.draw.rect(win,FRUIT_COLOR,fruit_rect)


def draw_snake():
    for col,row in snake_pos:
        snake_rect = col*CELLSIZE,row*CELLSIZE,CELLSIZE,CELLSIZE
        pg.draw.rect(win,SNAKE_COLOR,snake_rect,0)


def on_keydown(key):
    '''
    ;when the user press a key/when a key is being pressed
    '''
    global snake_direction
    
    if key == K_LEFT:
        if snake_direction != MOVE_RIGHT:
            snake_direction = MOVE_LEFT
    elif key == K_RIGHT:
        if snake_direction != MOVE_LEFT:
            snake_direction = MOVE_RIGHT
    elif key == K_UP:
        if snake_direction != MOVE_DOWN:
            snake_direction = MOVE_UP
    elif key == K_DOWN:
        if snake_direction != MOVE_UP:
            snake_direction = MOVE_DOWN

#### LET'S DEFINE SOME COLORS CONSTANT ####
LINE_COLOR = '#101010'
FRUIT_COLOR = 'red'
SNAKE_COLOR = 'green'
#### 2D VECTORS FOR MOVING OUR SNAKE ####
NOT_MOVE   = [ 0, 0]
MOVE_RIGHT = [ 1, 0]
MOVE_LEFT  = [-1, 0]
MOVE_UP    = [ 0,-1]
MOVE_DOWN  = [ 0, 1]
#### BASIC SETUP VIDEO MODES ####
FPS = 60
CELLSIZE = 20
CELLCOL = 32
CELLROW = 24
dims = CELLCOL*CELLSIZE,CELLROW*CELLSIZE
flags = DOUBLEBUF|HWSURFACE
bpp = pg.display.mode_ok(dims,flags)
win = pg.display.set_mode(dims,flags,bpp)
clk = pg.time.Clock()  ##create a Clock object to keep track of time in game

snake_pos = [(3,10),(4,10),(5,10)]  ##each tuple format: (column,row)
snake_direction = NOT_MOVE
SNAKE_MOVE = pg.event.custom_type()
pg.time.set_timer(SNAKE_MOVE,65)  ##triggers after every n millisec.

fruit_rect = randomise_fruit_position()  ##initial position of the fruit when game start

#### MAIN GAME LOOP ####
add_snake_segment = False
done = False
while not done:
    clk.tick(FPS)  ##limits the framerate
    for e in pg.event.get():
        if e.type in (QUIT,WINDOWCLOSE):
            done = True
        elif e.type == KEYDOWN and not e.type == KEYUP:
            on_keydown(e.key)
        elif e.type == SNAKE_MOVE:
            if snake_direction != NOT_MOVE:
                if not add_snake_segment:
                    pos_cpy = snake_pos[1:]  ##take everything except the tail
                else:
                    pos_cpy = snake_pos[:]
                    add_snake_segment = False
                new_head_col = pos_cpy[-1][0]+snake_direction[0]
                new_head_row = pos_cpy[-1][1]+snake_direction[1]
                new_head_direction = [new_head_col, new_head_row]
                pos_cpy.append(new_head_direction)
                snake_pos = pos_cpy.copy()  ##applying changes to the real snake body position
    win.fill('black')  ##clearing the screen
    #### DRAW EVERYTHING BELOW ####
    draw_fruit()
    draw_snake()
    draw_grid()
    #### DETECTING COLLISIONS ####

    ##datas need for collisions detection
    snake_head_col,snake_head_row = snake_pos[-1]
    fruit_col,fruit_row = fruit_rect.left//CELLSIZE,fruit_rect.top//CELLSIZE

    ##snake eats fruit
    if (snake_head_col,snake_head_row) == (fruit_col,fruit_row):
        fruit_rect = randomise_fruit_position()
        if (fruit_col,fruit_row) in snake_pos:
            continue
        add_snake_segment = True
    
    ##our snake hits either one of the four edges of the screen(left,right,top,bottom)
    if not snake_head_col in range(0,CELLCOL) or\
       not snake_head_row in range(0,CELLROW):
        print('collide with wall')
        done = True

    ##our snake hits itself
    for body_col,body_row in snake_pos[:-1]:
        if (snake_head_col,snake_head_row) == (body_col,body_row):
            print('oops:<')
            done = True
    
    ##update player' score
    score = len(snake_pos)-3

    ##max snake' length reached
    if len(snake_pos)>=CELLCOL*CELLROW:
        done = True
        break
    
    display_score(str(score),'white',(0,0))
    pg.display.flip()
pg.quit()
print('you\'re score is',score)
