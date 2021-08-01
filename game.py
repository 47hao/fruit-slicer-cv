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

import threading
import camTracker

fruitOutlines = [
    [(0,-50),(-39,-31),(-49,11),(-22,45),(22,45),(49,11),(39,-31)],
    [(-50,0),(-35,30),(0,40),(35,30),(50,0),(35,-30),(0,-40),(-35,-30)],
    [(-50,0),(-35,30),(0,40),(35,30),(50,0),(35,-30),(0,-40),(-35,-30)],
    [(-35,-10),(-15,28),(0,40),(15,28),(35,-10),(25,-35),(0,-40),(-25,-35)]
]

fruitTypes = [
    "orange",
    "lemon",
    "lime",
    "strawberry"
]

def appStarted(app):
    app.targetFPS = 1000
    initFruits(app)

    blade.init(app)

    app.score = 0
    app.lastWave = time.time()
    app.timeBetweenWaves = 5
    app.numFruits = 3
    app.timerDelay = int(max(1000/app.targetFPS, 1.0))
    app.prevTime = time.time()

    #camera tracking variables
    app.debugMode = False #displays marker

    app.camThreshold = .9
    app.cam = camTracker.camTracker()
    app.xPos = 0
    app.yPos = 0

    app.timerTicks = 0#for camera picking
    app.lastTime = 0 #for redraw timing
    app.maxThreads = 8
    app.startupTime = time.time()

def keyPressed(app, event):
#controlling camera sensitivity
    if event.key == 'Up':
        if(app.camThreshold) < .95:
            app.camThreshold += .05
    elif event.key == 'Down':
        if(app.camThreshold) > .5:
            app.camThreshold -= .05
    elif event.key == 'Space':
        app.cam.toggleFilter()

def addBladePoint(app,x,y):
    blade.insertBlade(app,0,(x,y))
    sliceAllFruits(app)

def camTick(app):
    output = app.cam.getCoords(app.camThreshold)
    if(output != None):
        (xScale, yScale) = output
        app.xPos = app.width*(1-xScale) #camera's flipped
        app.yPos = app.height*yScale
        addBladePoint(app,app.xPos,app.yPos)

def getFruit():
    i = random.randint(0,3)
    return (fruitTypes[i],fruitOutlines[i])

def initFruits(app):
    app.fruits = []
    #p = [(-50,0),(-35,35),(0,50),(35,35),(50,0),(35,-35),(0,-50),(-35,-35)]
    (f, outline) = getFruit()
    #createWave(app,2)
    app.sliced = False
    app.grav = 600

def createWave(app,numFruits):
    waveFruits = []
    for i in range(numFruits):
        (f, outline) = getFruit()
        xCoord = random.randint(int(app.width/6),int(app.width*(5/6)))
        dx,dy = float(random.randint(-app.width//10,app.width//10)), -float(random.randint(int(app.height*7/8),app.height))
        if(xCoord < app.width/2):
            dx = abs(dx)
        else:
            dx = -abs(dx)
        newFruit = Fruit.Fruit(outline, (xCoord,app.height), (dx,dy), f, True)
        waveFruits.append(newFruit)

    app.fruits.extend(waveFruits)

def cleanFruits(app):
    i = 0
    while i<len(app.fruits):
        (x,y) = app.fruits[i].pos
        if(y > app.height + 100):
            app.fruits.pop(i)
        else:
            i += 1

def sliceAllFruits(app):
    i = 0
    j = 0
    for j in range(len(app.blade)-1):
        p0, p1 = app.blade[j][0], app.blade[j+1][0]
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


def timerFired(app):
    app.timerTicks += 1
    if app.timerTicks%5 == 0: 
        if(threading.activeCount() < app.maxThreads):# and app.timerTicks%2 == 0):
            thread = camThread(1, "Thread-1", app)
            thread.start()
        #print(threading.activeCount())

    if app.timerTicks%200 == 0:
        cleanFruits(app)  

    doStep(app)
        
            
def doStep(app):
    if((time.time() - app.lastWave) > app.timeBetweenWaves and
        time.time()-app.startupTime > 5):
        app.numFruits = 2 + app.score//30
        if(app.numFruits > 12):
            app.numFruits = 12
        createWave(app,app.numFruits)
        app.lastWave = time.time()

    blade.stepBlade(app)
    for f in app.fruits:
        f.move(app.grav, (time.time()-app.prevTime))
    app.prevTime = time.time()

def drawReferenceMarker(app, canvas):
    r = 10
    canvas.create_oval(app.xPos-r, app.yPos-r, app.xPos+r, app.yPos+r,
                        fill = "red", outline = "")

def redrawAll(app, canvas):
    drawBackdrop(app, canvas)
    drawFruits(app, canvas)
    blade.drawBlade(app,canvas)
    drawScore(app,canvas)
    if(app.debugMode):
        drawReferenceMarker(app,canvas)
    app.lastTime = time.time()

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

class camThread(threading.Thread):
    def __init__(self, threadID, name, game):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.game = game

    def run(self):
        camTick(self.game)

runApp(width=1100, height=800)


    





