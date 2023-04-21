import thumby

thumby.display.setFPS(60)

enemies = []

pX, pY = 0,0

while True:
    thumby.display.fill(0) # clear
    
    # Input
    if thumby.buttonU.pressed():
        pY -= 1
    elif thumby.buttonD.pressed():
        pY += 1
    if thumby.buttonL.pressed():
        pX -= 1
    elif thumby.buttonR.pressed():
        pX += 1
        
    # Bounds
    if pX < 2: pX = 2
    if pX > thumby.display.width-5: pX = thumby.display.width-5
    if pY < 2: pY = 2
    if pY > thumby.display.height-5: pY = thumby.display.height-5
    
    thumby.display.drawRectangle(0,0,thumby.display.width-1, thumby.display.height-1, 1)
    
    thumby.display.drawRectangle(pX, pY, 2,2, 1)
    
    thumby.display.update() # update screen