# Gravity Simulator
This is a 2D simulator for Newtonian gravity.

Controls:
- W/A/S/D - move camera
- E/R - slowdown or speedup time
- T - toggle trails
- M - switch spawning modes (single or cluster)
- X - eraser
- C - clear all bodies
- P - pause

In single spawning,
drag and drop to launch an object in that direction. The farther the mouse is dragged, the higher the speed of the object.
The radius of the objects can be adjusted with - or + keys.

In cluster spawning, 
objects are spawned in a disc. If the position of the initial click lies on a body, then the disc tends to revolve around it. 
The number of the objects can be adjusted with - or + keys.
The farther the mouse is dragged horizontally, the greater is the radius of the disc.
Dragging the mouse left or right also determines the direction of revolution.
The farther the mouse is dragged vertically, the greater is the deviation in radius of the disc.

Example: Epicycles in a three body system
![epicycles](https://user-images.githubusercontent.com/97620191/227765857-8f45b225-15cd-45d7-8d9b-1bda6e688c1b.png)

To generate a moving cluster- spawn a single moving body, pause and spawn a cluster around it. \
Example: A moving cluster being deflected by a heavy body
![deflection](https://user-images.githubusercontent.com/97620191/227765853-73df75ee-7a18-4b65-9c19-4f9e0e187948.png)
