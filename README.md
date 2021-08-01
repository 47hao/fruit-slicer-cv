# fruit-slicer-cv
# Computer Vision enabled control, an early prototype of flashlight control for Beat Slicer
# 
# How to run:
# Clone the repository onto your computer. game.py contains the main program file, run it to run the program. You do not need to import modules or install anything. 
#
# The program is run on cmu_112_graphics. 
# https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py
#
# To play:
# Fruits fly up from the bottom of the screen. Drag your mouse over them to slice and get points. You can slice the fruit multiple times.
# 
# Commands:
# Press 't' generate more fruits.
#
# The slicing uses Sutherland-Hodgman polygon clipping. The algorithm can be found here:
# https://rosettacode.org/wiki/Sutherland-Hodgman_polygon_clipping#Python
