import pygame as pg

import sys,time,random
pg.init()
SCREEN_WIDTH=800
SCREEN_HEIGHT=600

win = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
paddle = pg.Rect(SCREEN_WIDTH/2-50,SCREEN_HEIGHT-15-10,100,15)
clock = pg.time.Clock()

font = pg.font.Font('arial.ttf', 32)
scoreText = font.render('Score: 0', True, (0,255,0), (0,0,0))
scoreTextRect = scoreText.get_rect()
scoreTextRect.x=10
scoreTextRect.y=10

font2 = pg.font.Font('arial.ttf', 64)
gameOverText = font2.render('Game Over', True, (255,0,0), (0,0,0))
gameOverTextRect = gameOverText.get_rect()
gameOverTextRect.center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
Game_Running=True
dt=0
old=time.time()
BALL_X= paddle.x+50
BALL_Y=paddle.y-8
MIN_BALL_SPEED=5
MAX_BALL_SPEED=9
BALL_X_SPEED=0
BALL_Y_SPEED=0
BOX_SPEED=10
TARGET_FPS=60
GAME_STARTED=False
SCORE=0

def updateScore():
    global SCORE,scoreText
    SCORE+=1
    scoreText = font.render(f'Score: {SCORE}', True, (0,255,0), (0,0,0))

def checkcollision():
    global SCREEN_WIDTH,paddle,BALL_X,BALL_Y,BALL_X_SPEED,BALL_Y_SPEED,GAME_STARTED
    if paddle.x<0:
        paddle.x=0
    elif paddle.x+100>SCREEN_WIDTH:
        paddle.x=SCREEN_WIDTH-100 
    if BALL_X-8<=0 or BALL_X+8>=SCREEN_WIDTH:
        BALL_X_SPEED=-BALL_X_SPEED
    if BALL_Y-8<=0:
        BALL_Y_SPEED=-BALL_Y_SPEED   

    #Ball hits the paddle
    if BALL_Y+8>=paddle.y-5 and GAME_STARTED==True and BALL_X>paddle.x and BALL_X<paddle.x+100:
        BALL_Y-=15
        BALL_Y_SPEED=-BALL_Y_SPEED
        updateScore()
    elif BALL_Y+8>paddle.y:
        gameOver()

def gameOver():
    global Game_Running
    Game_Running=False


while True:
    new=time.time()
    dt=new-old
    old=new
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_SPACE:
                GAME_STARTED=True
                BALL_Y-=10
                sign=random.randint(0,1)
                BALL_Y_SPEED=-random.randint(MIN_BALL_SPEED,MAX_BALL_SPEED)
                BALL_X_SPEED=random.randint(MIN_BALL_SPEED,MAX_BALL_SPEED)
                if sign==0:
                    BALL_X_SPEED=-BALL_X_SPEED
    
    if Game_Running==True:
        checkcollision()
        key=pg.key.get_pressed()
        if key[pg.K_LEFT]:
            paddle.x-=BOX_SPEED*dt*TARGET_FPS
            if GAME_STARTED==False:
                BALL_X=paddle.x+50
        elif key[pg.K_RIGHT]:
            paddle.x+=BOX_SPEED*dt*TARGET_FPS
            if GAME_STARTED==False:
                BALL_X=paddle.x+50

     
    

    
        win.fill("black")
        pg.draw.rect(win,"white",paddle)
        if GAME_STARTED==False:
            pg.draw.circle(win,"green",(BALL_X,BALL_Y),8)       
        else:
            BALL_X+=BALL_X_SPEED*dt*TARGET_FPS
            BALL_Y+=BALL_Y_SPEED*dt*TARGET_FPS
            pg.draw.circle(win,"green",(BALL_X,BALL_Y),8)

    else:
        win.blit(gameOverText,gameOverTextRect)

    win.blit(scoreText,scoreTextRect)            
    pg.display.update()
    clock.tick(60)
