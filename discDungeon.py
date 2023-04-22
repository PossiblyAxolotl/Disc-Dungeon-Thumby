import thumby
import math
import random

thumby.saveData.setName("Disc Dungeon")
thumby.display.setFPS(60)

# art
# sawMap: width: 16, height: 8
sawMap = bytearray([85,254,127,230,103,254,127,170,170,127,254,103,230,127,254,85])

saws = []

pX, pY, pS = 0,0,1 # pS = playerSpeed

score = 0
scoreY, scoreYlerp = -10, 3

def lerp(a, b, t):
    return (1 - t) * a + t * b

def addSaw(amount):
    sprSaw = thumby.Sprite(8,8,sawMap,random.randint(2,thumby.display.width-10),random.randint(2,thumby.display.height-10))
    sprSaw.dir = random.randint(0,359)
    sprSaw.aniCounter = random.randint(0,2)
    sprSaw.setFrame(random.randint(0,1))
    sprSaw.speed = 0.5
    sprSaw.xdir = 1
    sprSaw.ydir = 1
    saws.append(sprSaw)

def updateSaws():
    for saw in saws:
        # move in direction
        saw.x += math.sin(math.radians(saw.dir)) * saw.speed * saw.xdir
        saw.y -= math.cos(math.radians(saw.dir)) * saw.speed * saw.ydir
        
        # collide with walls
        if saw.x < 2: 
            saw.xdir *= -1
            saw.x = 2
        elif saw.x > thumby.display.width-10: 
            saw.xdir *= -1
            saw.x = thumby.display.width-10
        if saw.y < 2: 
            saw.ydir *= -1
            saw.y = 2
        elif saw.y > thumby.display.height-10: 
            saw.ydir *= -1
            saw.y = thumby.display.height-10
        
        # animate
        saw.aniCounter += 1
        if saw.aniCounter > 3:
            saw.setFrame(saw.getFrame()+1)
            saw.aniCounter = 0
        
        # draw
        thumby.display.drawSprite(saw)

addSaw(1)
addSaw(1)
addSaw(1)

while True:
    thumby.display.fill(0)
    
    # Input
    if thumby.actionPressed():
        pS = 0.5
    else:
        pS = 1
        
    if thumby.buttonU.pressed():
        pY -= pS
    elif thumby.buttonD.pressed():
        pY += pS
    if thumby.buttonL.pressed():
        pX -= pS
    elif thumby.buttonR.pressed():
        pX += pS
        
    # Bounds
    if pX < 2: pX = 2
    if pX > thumby.display.width-5: pX = thumby.display.width-5
    if pY < 2: pY = 2
    if pY > thumby.display.height-5: pY = thumby.display.height-5
    
    if pY < 10: 
        scoreYlerp = -10 
    else: 
        scoreYlerp = 3
    
    scoreY = lerp(scoreY,scoreYlerp,0.1)
    
    # drawing
    updateSaws()
    
    thumby.display.drawRectangle(0,0,thumby.display.width-1, thumby.display.height-1, 1)
    
    thumby.display.drawRectangle(round(pX), round(pY), 2,2, 1)
    
    thumby.display.drawText(str(score),3,round(scoreY),1)
    
    # update screen
    thumby.display.update() 

    