import thumby
import math
import random

thumby.saveData.setName("Disc Dungeon")
thumby.display.setFPS(60)

# art
# sawMap: width: 16, height: 8
sawMap = bytearray([85,254,127,230,103,254,127,170,170,127,254,103,230,127,254,85])
# targetMap: width: 8, height: 8
targetMap = bytearray([126,129,189,165,165,189,129,126])

saws = []
targets = []
particles = []

pX, pY, pS = thumby.display.width/2-1,thumby.display.height/2-1,1 # pS = playerSpeed

score = 0
scoreY, scoreYlerp = -10, 3

frame = 0
loop = 0
looptime = 300

tarCountdown = random.randint(5, 15)

speed = 0.2
#amnt = 1

def lerp(a, b, t):
    return (1 - t) * a + t * b

def die():
    thumby.saveData.setItem("lastScore", score)
    if thumby.saveData.hasItem("highScore"):
        if thumby.saveData.getItem("highScore") < score:
            thumby.saveData.setItem("highScore", score)
    else:
        thumby.saveData.setItem("highScore", score)
        thumby.saveData.save()
        thumby.reset()

def addParts(_x,_y, amount): # 0=x,1=y,2=size,3=dirx,4=diry
    for i in range(0, amount):
        direction = math.radians(random.randint(0, 359))
        part = [_x,_y,random.randint(1,6),math.sin(direction),-math.cos(direction)]
        particles.append(part)

def drawParticles():
    for part in particles:
        #if frame % 2 == 0:
        thumby.display.drawFilledRectangle(round(part[0]),round(part[1]),math.ceil(part[2]),math.ceil(part[2]),1)
        part[0] += part[3]
        part[1] += part[4]
        
        part[2] -= 0.2
        if part[2] <= 0:
            particles.remove(part)

def addSaws(amount):
    for i in range(0, amount):
        sprSaw = thumby.Sprite(8,8,sawMap,random.randint(2,thumby.display.width-10),random.randint(2,thumby.display.height-10))
        sprSaw.dir = math.radians(random.randint(0,359))
        sprSaw.aniCounter = random.randint(0,2)
        sprSaw.setFrame(random.randint(0,1))
        sprSaw.speed = speed
        sprSaw.lifespan = random.randint(5,20)
        sprSaw.active = 0
        sprSaw.xdir = math.sin(sprSaw.dir)
        sprSaw.ydir = math.cos(sprSaw.dir)
        saws.append(sprSaw)
        addParts(sprSaw.x,sprSaw.y,8)

def spawnTarget():
    sprTar = thumby.Sprite(8,8,targetMap,random.randint(2,thumby.display.width-10),random.randint(2,thumby.display.height-10))
    sprTar.lifespan = 600
    targets.append(sprTar)
    addParts(sprTar.x,sprTar.y,4)
    
def updateSaws():
    for saw in saws:
        # lifespan
        if saw.lifespan < 0:
            global scoreY
            global score
            #scoreY -= 2
            #score += 1
            saws.remove(saw)
            continue
        
        # move in direction
        saw.x += saw.speed * saw.xdir
        saw.y -= saw.speed * saw.ydir
        
        # collide with walls
        if saw.x < 1: 
            saw.xdir *= -1
            saw.x = 1
            saw.lifespan -= 1
            thumby.audio.play(200,20)
        elif saw.x > thumby.display.width-9: 
            saw.xdir *= -1
            saw.lifespan -= 1
            saw.x = thumby.display.width-9
            thumby.audio.play(200,20)
        if saw.y < 1: 
            saw.ydir *= -1
            saw.y = 1
            saw.lifespan -= 1
            thumby.audio.play(200,20)
        elif saw.y > thumby.display.height-9: 
            saw.ydir *= -1
            saw.y = thumby.display.height-9
            saw.lifespan -= 1
            thumby.audio.play(200,20)
        
        # animate
        saw.aniCounter += 1
        if saw.aniCounter > 3:
            saw.setFrame(saw.getFrame()+1)
            saw.aniCounter = 0

        if saw.active < 60: # if inactive then add to active timer
            saw.active += 1
        # death
        elif saw.x +1 <= pX and saw.x + 6 >= pX and saw.y +1 <= pY and saw.y + 6 >= pY:
            die()

        # draw
        thumby.display.drawSprite(saw)

def updateTargets():
    for tar in targets:
        tar.lifespan -= 1
        if tar.lifespan <= 0:
            targets.remove(tar)
            continue
        if tar.x +1 <= pX and tar.x + 6 >= pX and tar.y +1 <= pY and tar.y + 6 >= pY:
            global score
            score += 10
            thumby.audio.play(300,100)
            targets.remove(tar)
            addParts(tar.x,tar.y,2)
        
        if frame % 2 == 0:
            thumby.display.drawSprite(tar)

addSaws(1)

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
    
    # Score
    if pY < 10 and pX < 3 + 6*len(str(score)): 
        scoreYlerp = -10 
    else: 
        scoreYlerp = 3
    
    if frame >= 60:
        frame = 0
        score += 1
        scoreY -= 2
        speed += 0.01
        looptime -= 1
        #amnt += 0.02
        #if amnt > 3: amnt = 5
        if looptime < 30: looptime = 30
        if speed > 1: speed = 1
        tarCountdown -= 1
    if loop >= looptime:
        loop = 0
        addSaws(1)
    if tarCountdown <= 0:
        tarCountdown = random.randint(5, 15)
        spawnTarget()
    
    scoreY = lerp(scoreY,scoreYlerp,0.1)
    
    # Drawing
    updateTargets()
    updateSaws()
    drawParticles()
    
    thumby.display.drawRectangle(0,0,thumby.display.width-1, thumby.display.height-1, 1)
    
    thumby.display.drawRectangle(round(pX), round(pY), 2,2, 1)
    
    thumby.display.drawText(str(score),3,round(scoreY),1)
    
    # Update screen
    thumby.display.update() 
    
    frame += 1
    loop += 1
    