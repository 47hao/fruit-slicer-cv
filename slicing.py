from cmu_112_graphics import *

def appStarted(app):
    app.polygonList = [(50,50),(100,50),(100,100),(50,100)]
    app.slicepolygon = [(0,75),(500,75),(500,500),(0,500)]
    

def mousePressed(app, event):
    app.polygonList = clip(app.polygonList, app.slicepolygon)

def redrawAll(app, canvas):
    polygonDrawList = []
    for x,y in app.polygonList:
        polygonDrawList.append(x)
        polygonDrawList.append(y)

    canvas.create_polygon(polygonDrawList)

# from http://rosettacode.org/wiki/Sutherland-Hodgman_polygon_clipping#Python
def clip(subjectPolygon, clipPolygon):
   def inside(p):
      return(cp2[0]-cp1[0])*(p[1]-cp1[1]) > (cp2[1]-cp1[1])*(p[0]-cp1[0])
 
   def computeIntersection():
      dc = [ cp1[0] - cp2[0], cp1[1] - cp2[1] ]
      dp = [ s[0] - e[0], s[1] - e[1] ]
      n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
      n2 = s[0] * e[1] - s[1] * e[0] 
      n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
      return [(n1*dp[0] - n2*dc[0]) * n3, (n1*dp[1] - n2*dc[1]) * n3]
 
   outputList = subjectPolygon
   cp1 = clipPolygon[-1]
 
   for clipVertex in clipPolygon:
      cp2 = clipVertex
      inputList = outputList
      outputList = []
      s = inputList[-1]
 
      for subjectVertex in inputList:
         e = subjectVertex
         if inside(e):
            if not inside(s):
               outputList.append(computeIntersection())
            outputList.append(e)
         elif inside(s):
            outputList.append(computeIntersection())
         s = e
      cp1 = cp2
   return(outputList)

runApp(width=512, height=512)