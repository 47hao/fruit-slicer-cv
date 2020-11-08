from cmu_112_graphics import *
#from shapely.geometry import Point
#from shapely.geometry.polygon import Polygon

import orderClockwise
import centroid
import Fruit
import blade
import random
#import slicing
import time
import sliceFunction

#point = Point(0.5, 0.5)
#polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
#print(polygon.contains(point))

fruitOutlines = [
    [(-50,0),(-35,35),(0,50),(35,35),(50,0),(35,-35),(0,-50),(-35,-35)],
    [(-50,0),(-35,30),(0,40),(35,30),(50,0),(35,-30),(0,-40),(-35,-30)],
    [(-50,0),(-35,30),(0,40),(35,30),(50,0),(35,-30),(0,-40),(-35,-30)],
    [(-50,0),(-28,28),(0,50),(28,28),(50,0),(35,-35),(0,-50),(-35,-35)]
]

fruitTypes = [
    "orange",
    "lemon",
    "lime",
    "strawberry"
]

def getFruit():
    i = random.randint(0,3)
    return (fruitTypes[i],fruitOutlines[i])

def appStarted(app):
    initFruits(app)

    blade.init(app)
    #TEMPORARY!!!
    app.slice=[None,None]

    app.score = 0
    app.lastWave = time.time()
    app.timeBetweenWaves = 5
    app.numFruits = 3

def initFruits(app):
    app.fruits = []
    #p = [(-50,0),(-35,35),(0,50),(35,35),(50,0),(35,-35),(0,-50),(-35,-35)]
    (f, outline) = getFruit()
    createWave(app,2)
    app.sliced = False
    app.grav = 0.3

def createWave(app,numFruits):
    waveFruits = []
    for i in range(numFruits):
        (f, outline) = getFruit()
        xCoord = random.randint(0,app.width)
        dx,dy = random.randint(-8,8), -random.randint(15,20)
        if(xCoord < app.width/2):
            dx = abs(dx)
        else:
            dx = -abs(dx)
        newFruit = Fruit.Fruit(outline, (xCoord,app.height), (dx,dy), f, True)
        waveFruits.append(newFruit)

    app.fruits.extend(waveFruits)

def mousePressed(app, event):
    bladeMouse(app, event)
    #fruitTest(app)

    #TEMPORARY
    start = (event.x, event.y)
    app.slice[0] = start

def bladeMouse(app, event):
    if (not app.mousePress):
        app.mousePress = True
        #app.startpos = (event.x, event.y)
        #app.blade.append(app.startpos)
        app.t0 = time.time()

def keyPressed(app, event):
    pass
def cleanFruits(app):
    i = 0
    while i<len(app.fruits):
        (x,y) = app.fruits[i].pos
        if(y > app.height + 100):
            app.fruits.pop(i)
        else:
            i += 1

def mouseReleased(app, event):
    app.mousePress = False
    blade.resetBladeCount(app,event)
    cleanFruits(app)

def sliceAllFruits(app):
    i = 0
    j = 0
    for j in range(len(app.blade)-1):
        p0, p1 = app.blade[j], app.blade[j+1]
        while i < len(app.fruits):
            f = app.fruits[i]
            (x,y) = f.pos
            globPoints = Fruit.localToGlobal(f.points, x, y)
            if(sliceFunction.sliceIntersectsPolygon(globPoints,p0,p1)):
                sliceFruit(app, f, i, p0, p1, app.width, app.height)
                i += 1
                app.score += 1
            i += 1

def sliceFruit(app, f, i, p0, p1, w, h):
    (f1, f2) = f.slice(p0, p1, w,h)
    app.fruits.pop(i)
    app.fruits.insert(i,f2)
    app.fruits.insert(i,f1)

def mouseDragged(app,event):
    app.lastMouseX, app.lastMouseY = event.x, event.y
    if (app.mousePress):
        #app.t1 = time.time()
        #app.bladeCounter += 1
        x1,y1 = (event.x,event.y)
        blade.insertBlade(app,0,(x1,y1))
        sliceAllFruits(app)

def timerFired(app):
    app.timerDelay = 10
    doStep(app)       
            
def doStep(app):

    if((time.time() - app.lastWave) > app.timeBetweenWaves):
        app.numFruits = 2 + app.score//30
        if(app.numFruits > 8):
            app.numFruits = 8
        createWave(app,app.numFruits)
        app.lastWave = time.time()

    blade.stepBlade(app)
    for f in app.fruits:
        f.move(app.grav)

def redrawAll(app, canvas):
    drawBackdrop(app, canvas)
    drawFruits(app, canvas)
    blade.drawBlade(app,canvas)
    drawScore(app,canvas)

def drawScore(app,canvas):
    message = f"{app.score}"
    margin = 10
    canvas.create_text(margin, app.height-margin, text= message,
                     font='Arial 60 bold', fill = "white", anchor = "sw")

def drawBackdrop(app, canvas):
    c = 40
    canvas.create_rectangle(0,0,app.width,app.height,fill=rgbString(c,c,c))

def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

def drawFruits(app, canvas):
    for f in app.fruits:
        (cx, cy) = f.pos
        coords = Fruit.localToGlobal(f.points, cx,cy)
        c = "black"
        if(f.fruitType == "orange"):
            c = "orangered"
        elif(f.fruitType == "lemon"):
            c = "gold"
        elif(f.fruitType == "lime"):
            c = "forestgreen"
        elif(f.fruitType == "strawberry"):
            c = "firebrick"
        canvas.create_polygon(coords, fill=c,width=4)

runApp(width=1100, height=800)


    





