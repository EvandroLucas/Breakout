import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import math
import random
import sys
from random import randrange


display = (1200,900 )
displayWindow = (1200,800 )
gridSizeH=12.4
gridSizeV=(gridSizeH/3)*2
fov = 45
brickColNum = 40
brickRowNum = 8
tileSize=gridSizeH/brickColNum


colorBlue =         (0, 0, 1)
colorGreen =        (0, 1, 0)
colorRed =          (1, 0, 0)
colorYellow =       (1, 1, 0)
colorPink =         (1, 0, 1)
colorWhite =        (1, 1, 1)
colorBlack =        (0, 0, 0)
colorDarkGrey =     (0.1, 0.1, 0.1)

brickColors = [colorBlue,colorGreen,colorRed,colorPink,colorYellow]
maxPaddleSpeed = 2
minBallSpeed = 0.2
maxBallSpeed = 0.6


def drawText(position, textString, size):     
    pygame.init() # now use display and fonts
    font = pygame.font.Font (None, size)
    textSurface = font.render(textString, True, (255,255,255,255),(25,25,25,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)   
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def getRandomStartingAngle():
    return random.randint(30,151)


def tupleColor(colorTuple):
    glColor3f(colorTuple[0],colorTuple[1],colorTuple[2])

def drawHalfBrickLeft(x,y,colorTuple=colorWhite):
    marginPercentage = 10 / 100
    margin =  tileSize * marginPercentage

    glBegin(GL_QUADS)

    tupleColor(colorTuple)

    BottomLeftX = tileSize * y
    BottomLeftY = tileSize * x
    aux1 = BottomLeftY+tileSize
    aux2 = BottomLeftX+tileSize

    glVertex2f(BottomLeftY  + margin, BottomLeftX    + margin) # top left
    glVertex2f(aux1         - margin, BottomLeftX    + margin) # bottom left
    glVertex2f(aux1         - margin, aux2           ) # bottom right
    glVertex2f(BottomLeftY  + margin, aux2           ) # top right

    glEnd()

def drawHalfBrickRight(x,y,colorTuple=colorWhite):
    marginPercentage = 10 / 100
    margin =  tileSize * marginPercentage

    glBegin(GL_QUADS)

    tupleColor(colorTuple)

    BottomLeftX = tileSize * y
    BottomLeftY = tileSize * x
    aux1 = BottomLeftY+tileSize
    aux2 = BottomLeftX+tileSize

    glVertex2f(BottomLeftY  + margin, BottomLeftX    ) # top left
    glVertex2f(aux1         - margin, BottomLeftX    ) # bottom left
    glVertex2f(aux1         - margin, aux2           - margin) # bottom right
    glVertex2f(BottomLeftY  + margin, aux2           - margin) # top right

    glEnd()

def drawBrickOnFrame(x,y,colorTuple=colorWhite):
    
    drawHalfBrickLeft(x,y,colorTuple)
    drawHalfBrickRight(x,y+1,colorTuple)

def drawSquareOnFrame(xPos,yPos,colorTuple=colorWhite):

    x = yPos
    y = xPos


    marginPercentage = 90 / 100
    marginTop    =  tileSize * marginPercentage
    marginBottom =  tileSize * marginPercentage
    marginLeft   =  tileSize * marginPercentage
    marginRight  =  tileSize * marginPercentage

    glBegin(GL_QUADS)

    tupleColor(colorTuple)

    BottomLeftX = tileSize * x
    BottomLeftY = tileSize * y
    aux1 = BottomLeftX+tileSize
    aux2 = BottomLeftY+tileSize 

    glVertex2f(BottomLeftX  + marginLeft,  BottomLeftY  + marginTop     ) # top left
    glVertex2f(aux1         - marginLeft,  BottomLeftY  + marginBottom  ) # bottom left
    glVertex2f(aux1         - marginRight, aux2         - marginBottom  ) # bottom right
    glVertex2f(BottomLeftX  + marginRight, aux2         - marginTop     ) # top right

    glEnd()

def drawFrame(gridSizeH,gridSizeV):
    glBegin(GL_LINES)

    # Left line 
    glColor3f(1, 1, 1)

    glVertex3fv(( 0, 0, 0))
    glVertex3fv(( 0, gridSizeV, 0))
    # Top Line
    glVertex3fv(( 0, gridSizeV, 0))
    glVertex3fv(( gridSizeH, gridSizeV, 0))
    # Right Line
    glVertex3fv(( gridSizeH, gridSizeV, 0))
    glVertex3fv(( gridSizeH, 0, 0))
    # Bottom Line
    glVertex3fv(( 0, 0, 0))
    glVertex3fv(( gridSizeH, 0, 0))

    glEnd()

def drawPaddle(x):
    colorTuple=colorWhite
    y = 22

    marginPercentage = 10 / 100
    margin =  tileSize * marginPercentage

    glBegin(GL_QUADS)

    tupleColor(colorTuple)

    BottomLeftX = tileSize * x
    BottomLeftY = tileSize * y
    aux1 = BottomLeftY+tileSize
    aux2 = BottomLeftX+tileSize

    glVertex2f(BottomLeftY  + margin, BottomLeftX    ) # top left
    glVertex2f(aux1         - margin, BottomLeftX    ) # bottom left
    glVertex2f(aux1         - margin, aux2    + (tileSize*3)       ) # bottom right
    glVertex2f(BottomLeftY  + margin, aux2    + (tileSize*3)       ) # top right

    glEnd()

def movePaddle(pos, padPos, padSpeed):

    print(pos[0])
    maxPaddleSpeed = 1.5
    padSpeed = (pos[0]-600)/240
    padSpeed = min(padSpeed,maxPaddleSpeed)
    padSpeed = max(padSpeed,maxPaddleSpeed * (-1))

    padPos = padPos + padSpeed
    padPos = max(padPos, 0)
    padPos = min(padPos, 36)

    print("PadSpeed = " + str(padSpeed))
    print("PadPos = " + str(padPos))

    drawPaddle(max(padPos,0))

    return (padPos,padSpeed)

def movePaddleV2(pos, padPosx, padSpeed):
    
    
    truePos = round(pos[0]/ 30,4)

    distance = round(truePos - padPosx - 2,4)
    padSpeed = pow(distance/5,2)
    
    if distance < 0:
        padSpeed = padSpeed * (-1)

    padSpeed = max(min(padSpeed,maxPaddleSpeed),maxPaddleSpeed * (-1))
    padSpeed = round(padSpeed,3)

    padPosx = round(min(max(padPosx + padSpeed, 0), 36),3)

    return (padPosx,padSpeed)

def movePaddleInverted(pos, padPosx, padSpeed):
    newPos = pos
    newPos[0] = 1200 - pos[0]
    return movePaddleV2(newPos,padPosx, padSpeed)

def dealWithBallOnBordersAndPaddle(ballPos,ballAngle,ballSpeed,padPos,padSpeed,lifes):

    # print("BallPos:  " + str(ballPos))
    # print("BallAng:  " + str(ballAngle))
    # print("PadSpeed: " + str(padSpeed))


    if ballPos[1] >= 26.5 : # Bola passou, perdeu
        print("PERDEU")
        lifes -= 1
        ballAngle = newAngle(getRandomStartingAngle())
        ballPos = [20,10]
        pygame.time.wait(10)
        print("ANGULO: " + str(ballAngle))
    elif 0 < ballAngle < 180 and ballPos[1] >= padPos[1]+0.8:
        print("Já era...")
    elif ballPos[1] >= padPos[1]-0.5 and (padPos[0]-1+padSpeed) < ballPos[0] < (padPos[0] + 4 + padSpeed):
        print("Bateu")
        print("PadSpeed: " + str(padSpeed))
        print("  Ang Atual: " + str(ballAngle))
        print("  Ang Inverso: " + str(newAngle(ballAngle*(-1))))
        print("  Ang Adicional: " + str(newAngle(padSpeed*45)))
        ballAngle = newAngle(ballAngle*(-1)  + (padSpeed*45))
        print("  Ang Final: " + str(ballAngle))
        if 0 < ballAngle < 180:
            ballAngle = newAngle(ballAngle*(-1))
        ballPos[1] = padPos[1] - 0.5
        # ballSpeed = changeBallSpeed(ballSpeed,padSpeed)
        print("ANGULO: " + str(ballAngle))
    elif ballPos[0] < 0  and 90 < ballAngle < 180: # Bola bateu no lado esquerdo descendo
        print("Canto esquerdo descendo")
        ballAngle = newAngle(180 - ballAngle)
        ballPos[0] = 0.0001
        print("ANGULO: " + str(ballAngle))
    elif ballPos[0] < 0  and 180 < ballAngle < 270: # Bola bateu no lado esquerdo subindo
        print("Canto esquerdo subindo")
        ballAngle = newAngle(180 - ballAngle)
        ballPos[0] = 0.0001
        print("ANGULO: " + str(ballAngle))
    elif ballPos[0] > 39 and 0 < ballAngle < 90: # Bola bateu no lado direito descendo
        print("Canto direito descendo")
        ballAngle = newAngle(180 - ballAngle)
        ballPos[0] = 39
        print("ANGULO: " + str(ballAngle))
    elif ballPos[0] > 39  and 270 < ballAngle < 360: # Bola bateu no lado direito subindo
        print("Canto direito subindo")
        ballAngle = newAngle(180 - ballAngle)
        ballPos[0] = 39
        print("ANGULO: " + str(ballAngle))
    elif ballPos[1] < 0  : # Bola bateu em cima
        print("Teto")
        ballAngle = newAngle(ballAngle*(-1))
        ballPos[1] = 0.001
        print("ANGULO: " + str(ballAngle))

    return (ballPos,ballAngle,ballSpeed,padPos,lifes)

def dealWithBallOnBricks(ballPos,ballAngle,ballSpeed,padPos,bricks,bricksLeft):


    brickPosy = math.floor(ballPos[1])
    brickPosx = math.floor(ballPos[0]/2)

    if brickPosx < 20 and brickPosy < 8:
        # print("Brick COOORD: " + str(brickPosy) + "," + str(brickPosx),flush=True)
        if bricks[brickPosy][brickPosx] != colorDarkGrey:
            bricks[brickPosy][brickPosx] = colorDarkGrey
            ballAngle = newAngle(ballAngle*(-1))
            bricksLeft -= 1
            # ballSpeed = changeBallSpeed(ballSpeed,2)

    return ballPos,ballAngle,ballSpeed,padPos,bricks,bricksLeft

def newAngle(angle):

    if angle >= 0:
        newAngle = angle % 360
    else:
        newAngle = angle + 360

    if 180 <= newAngle <= 200:
        newAngle = 200

    if 340 <= newAngle <= 360:
        newAngle = 340

    if 0 <= newAngle <= 20:
        newAngle = 20

    if 160 < newAngle <= 180:
        newAngle = 160

    return newAngle

def changeBallSpeed(ballSpeed,changeFactor):
    maxBallSpeed = 1
    minBallSpeed = 0.1

    if changeFactor < 0:
        changeFactor = changeFactor * (-1)

    if changeFactor >= 1.5:
        newSpeed = ballSpeed + changeFactor/9
    else:
        newSpeed = ballSpeed - ((maxPaddleSpeed - changeFactor)/9)

    return min(max(newSpeed,minBallSpeed),maxBallSpeed)


def setupOpenGL():
    gluPerspective(fov, (displayWindow[0]/displayWindow[1]), 0, 10)
    glClearColor(0.1,0.1,0.1,0.1)
    glRotatef(-90,0,0,1)
    glTranslatef(gridSizeV/(-2),gridSizeH/(-2),-10)

def main():

    print("Hello World!")
    print ("Display: " + str(display))

    pygame.display.set_mode(display, DOUBLEBUF|OPENGL|HWSURFACE)
    pygame.mouse.set_visible(True)
    setupOpenGL()

    bricks = [[random.choice(brickColors) for x in range(20)] for y in range(8)] 

    padPos = [18,22]
    padSpeed = 0

    # ballAngle = 30
    ballSpeed = minBallSpeed
    ballPos = [20,10]
    ballAngle = getRandomStartingAngle()
    lifes = 3
    bricksLeft = 160
    game_over = False
    print("ANGULO: " + str(ballAngle))
    paused = True
    pauseOnNextCycle = False
    while True:

        if pauseOnNextCycle :
            paused = True

        glClearColor(0.1, 0.1, 0.1, 0.1 );
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 1 == event.button:
                    if paused : 
                        print("Game Resumed")
                        paused = False
                        game_over = False
                        pauseOnNextCycle = False
                    elif not paused:
                        print("Game Paused")
                        paused = True
                if 3 == event.button:
                    if paused : 
                        print("Game Resumed")
                        game_over = False
                        paused = False
                        pauseOnNextCycle = True
                    elif not paused:
                        print("Game Paused")
                        paused = True
                    print("Game Status: ")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    bricks = [[random.choice(brickColors) for x in range(20)] for y in range(8)] 
                    padPos = [18,22]
                    padSpeed = 0
                    ballSpeed = minBallSpeed
                    ballPos = [20,10]
                    ballAngle = getRandomStartingAngle()
                    paused = True
                    game_over = False
                    bricksLeft = 160
                if event.key == pygame.K_q:
                    sys.exit(0)

        for i in range(0,8):
            for j in range(0,20):
                drawBrickOnFrame(i,j*2,bricks[i][j])

        drawFrame(gridSizeV,gridSizeH)
        pos = pygame.mouse.get_pos()

    
        # Paddle
        if not paused: 
            newPosAndSpeed = movePaddleV2(pos,padPos[0],padSpeed)
            padPos[0] = newPosAndSpeed[0]
            padSpeed = newPosAndSpeed[1]
        drawPaddle(padPos[0])

        #Ball
        if not game_over:
            drawSquareOnFrame(ballPos[0],ballPos[1])

        if not paused: 
            ballPos = [ballPos[0],ballPos[1]]
            ballPos[0] = ballPos[0] + (ballSpeed * math.cos(np.radians(ballAngle)))
            ballPos[1] = ballPos[1] + (ballSpeed * math.sin(np.radians(ballAngle)))

            newBallStatus = dealWithBallOnBricks(ballPos,ballAngle,ballSpeed,padPos,bricks,bricksLeft)
            ballPos     = newBallStatus[0]
            ballAngle   = newBallStatus[1]
            ballSpeed   = newBallStatus[2]
            padPos      = newBallStatus[3]
            bricks      = newBallStatus[4]
            bricksLeft  = newBallStatus[5]

            newBallStatus = dealWithBallOnBordersAndPaddle(ballPos,ballAngle,ballSpeed,padPos,padSpeed,lifes)
            ballPos     = newBallStatus[0]
            ballAngle   = newBallStatus[1]
            ballSpeed   = newBallStatus[2]
            padPos      = newBallStatus[3]
            if newBallStatus[4] < lifes:
                pygame.time.wait(500)
            lifes       = newBallStatus[4]

            ballSpeed = ((ballSpeed) +  ((((160 - bricksLeft)/160)*(maxBallSpeed-minBallSpeed)) + minBallSpeed))  / 2

        drawText((8,11.5,0),str(lifes),32)

        drawText((8,0.3,0),"" + str(160 - bricksLeft) + "/" + str(20*8),32)

        displaySpeed = (((ballSpeed - minBallSpeed)/(maxBallSpeed-minBallSpeed)) * 99) + 1
        displaySpeed = round(displaySpeed,1)

        drawText((8,2,0),"Speed: " + str(displaySpeed),32)

        if game_over : 
            drawText((4,3.5,0),"GAME OVER",128)
            
        if lifes == 0 :
            game_over = True
            bricks = [[random.choice(brickColors) for x in range(20)] for y in range(8)] 
            padPos = [18,22]
            padSpeed = 0
            ballSpeed = minBallSpeed
            ballPos = [20,10]
            ballAngle = getRandomStartingAngle()
            lifes = 3
            paused = True
            bricksLeft = 160

        pygame.display.flip()
        pygame.time.wait(1)
        pygame.event.pump()



main()
