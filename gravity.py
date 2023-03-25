# basic with trails
# with quad trees
# 3d


import pygame
import numpy as np
import math

# g m M / R^2
width, height = 1280, 720
pobs = np.array([-width/2, -height/2])
move_speed = 200
G = 15
speedup = 4
f = 5
trail_length = 400
show_trails = False
trail_points = set()
trail_phase = {}

mode = 0 

# 1. DEFINING AND INITIALIZING BODIES

# body has mass, position, velocity, acceleration
class body:
    def __init__(self, m = 1.0, p=[0.0, 0.0], v= [0.0, 0.0]):
        self.m = m
        self.r = 3 * m ** (1/3)
        self.p = np.array(p)
        self.v = np.array(v)
        self.a = np.array([0,0])

body_list = []


# sample with custom properties in xy
# def init_rect_sample(size=100, position=[0,0, 20.0,70.0], velocity=[0.0,0.0, 1.0,1.0],  m= [3,0], spin=0.0):
#     px = np.random.normal(0, position[2], size)        # calculate spin velocity based on px, py
#     py = np.random.normal(0, position[3], size)
#     vx = np.random.normal(velocity[0], velocity[2], size)
#     vy = np.random.normal(velocity[1], velocity[3], size)
#     m = np.abs(np.random.normal(m[0], m[1], size) )

#     vy += spin*(px)
#     vx -= spin*(py)
#     px += position[0]
#     py += position[1]

#     for i in range(size):
#         body_list.append(body(m=m[i], p= (px[i], py[i]), v= (vx[i], vy[i]) ) )

# radial sample
def init_radial_sample(size=100, position=[0,0] ,radius = [100,40], speed = [5,2], mass = [3,0]):
    theta = np.random.random_sample(size) * 2* np.pi
    direction = np.sign(radius[0])
    r = np.abs(np.random.normal(abs(radius[0]), abs(radius[1]), size))
    s = np.random.normal(speed[0], speed[1], size)
    #s = s/(np.sqrt(np.abs(r))+4)
    s = s+ 0.5*np.sqrt(G*size*mass[0]*1/(r+5))  # initial speed based on radius, G and mass of set
    s = s*direction

    px= r*np.cos(theta)+position[0]
    py= r*np.sin(theta) +position[1]
    vx= -s*np.sin(theta)
    vy= s*np.cos(theta)
    m = np.abs(np.random.normal(mass[0], mass[1], size))

    for i in range(size):
        body_list.append(body(m=m[i], p= (px[i], py[i]), v= (vx[i], vy[i]) ))


# initial particles
#body_list.append(body(m=100,px=300))
#init_rect_sample(50, position=[-400,0, 50,100], spin=-0.02)
#init_radial_sample(100, position=[-500,0], radius=[100,50], speed=[0,1])
#init_radial_sample(100, position=[200,0], radius=[-100,50], speed=[0,1])
init_radial_sample(10, position=[0,0], radius=[200,90], speed=[0,0])


# 2. HELPER FUNCTIONS

def in_frame(px, py):
    return (px>=pobs[0] and px < pobs[0]+width and py >= pobs[1] and py< pobs[1] + height)

# add masses and combine properties
def combine(first, second):
    first_frac = first.m / (first.m + second.m)
    second_frac = second.m / (first.m + second.m)

    first.p = first_frac * first.p + second_frac * second.p
    first.v = first_frac * first.v + second_frac * second.v
    first.a = first_frac * first.a + second_frac * second.a

    first.m += second.m
    first.r = 3 * first.m ** (1/3)
    body_list.remove(second)

def unit_vector(x):
    return x/(x[0]**2 + x[1]**2)**(1/2)

# def collide(first, second, e):
#     u = unit_vector(second.p - first.p)     # normal
#     v1 = np.dot(first.v, u)                 # velocities along normal
#     v2 = np.dot(second.v, u)
#     vcm = (v1 * first.m + v2 * second.m)/(first.m + second.m) #go to centre of mass frame
#     delta_v1 = -(1+e)*(v1-vcm)              # change in velocity along normal
#     delta_v2 = -(1+e)*(v2-vcm)
#     first.v += delta_v1 * u
#     second.v += delta_v2 * u

#     pcm = (first.p * first.m + second.p* second.m)/(first.m + second.m)
#     first.p = pcm - np.dot(first.r, u)
#     second.p = pcm + np.dot(second.r, u)    # just touching

# 3. PHYSICS SIMULATION

def simulate():
    # apply newton's law of gravitation
    for first in body_list:
        first.a = 0
        for second in body_list:
            if first == second:
                continue
            disp = second.p - first.p                       # vector along line joining two bodies
            dist = (disp[0]**2 + disp[1]**2) **(1/2)        # distance between pair of bodies
            if(dist < 0.7*(first.r + second.r) ):
                combine(first, second)
            else:
                first.a += G* second.m * disp / (dist**3)        # update acceleration

    # recalculate p,v
    for obj in body_list:    
        obj.v += obj.a * dt*f  # update velocity
        obj.p += obj.v * dt*f  # update position

        if(show_trails and in_frame(obj.p[0], obj.p[1])):
            trail_points.add( (obj.p[0], obj.p[1]) )
            trail_phase[(obj.p[0], obj.p[1])] = trail_length  + obj.r         # add trails

# pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
paused = False
dt = 0

# 4. DISPLAY AND CONTROLS

mousedown = False
erase = False
cursor_color = ["cyan", "blue", "yellow"]
eraser_radius = 20

while running: 
    # wipe away anything from last frame
    screen.fill("black")

    if not paused:
        # fast forward frames without drawing
        for i in range(int(speedup)):
            simulate()

    # age and show the trail phases
    trail_copy = [x for x in trail_points]
    for t in trail_copy:
        if not paused: 
            trail_phase[t] -= speedup       # trail ages
        if(trail_phase[t] < 0):
            trail_points.remove(t)      # trail gets over
        if(show_trails==True and in_frame(t[0], t[1])):
            pygame.draw.circle(screen, "navy", (t[0]-pobs[0], t[1]-pobs[1]), 1)       # display trail
        
    for obj in body_list:   
        if(in_frame(obj.p[0], obj.p[1])):
            pygame.draw.circle(screen, "white", obj.p - pobs, obj.r)         # draw body


    cursor_pos = np.array(pygame.mouse.get_pos())
    if erase:
        pygame.draw.circle(screen, "gray", cursor_pos, radius=eraser_radius, width=1)
    else:
        pygame.draw.circle(screen, cursor_color[mode], cursor_pos, radius=6, width=1)

    if mousedown:
        endp = np.array(pygame.mouse.get_pos())
        if erase:
            pygame.draw.circle(screen, "gray", endp, eraser_radius)
            for b in body_list:
                disp = b.p - (pobs +endp)                      # vector along line joining two bodies
                dist = (disp[0]**2 + disp[1]**2) **(1/2) 
                if(dist<eraser_radius): body_list.remove(b)
        elif mode==0:
            pygame.draw.line(screen, start_pos=startp, end_pos=endp, color="cyan")
        elif mode==1:
            pygame.draw.line(screen, start_pos=startp, end_pos= (endp[0], startp[1]) , color="blue")
            pygame.draw.line(screen, start_pos=endp, end_pos= (endp[0], startp[1]) , color="blue")
        elif mode==2:
            pygame.draw.line(screen, start_pos=startp, end_pos=endp, color="yellow")


    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                show_trails = not show_trails
                if show_trails == False:
                    trail_points.clear()
            
            if event.key == pygame.K_c:
                body_list.clear()
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_m:
                mode = (mode+1)%3
            if event.key == pygame.K_x:
                erase = not erase

        if event.type == pygame.MOUSEBUTTONDOWN:
            startp = np.array(pygame.mouse.get_pos())
            mousedown = True
            

        if event.type == pygame.MOUSEBUTTONUP:
            endp = np.array(pygame.mouse.get_pos())
            if erase:
                pass
            elif mode==0:
                body_list.append(body(m=5,p = startp + pobs, v = (endp-startp)*0.05 ))
            elif mode==1:
                init_radial_sample(10, position=startp +pobs, radius= (endp-startp)*0.5, speed=[1,1])
            elif mode==2:
                body_list.append(body(m=100,p = startp + pobs, v = (endp-startp)*0.05 ))
            mousedown = False

    keys = pygame.key.get_pressed()
    # fast forward rate
    if keys[pygame.K_e] and speedup > 1:
        speedup -= speedup*dt 
        if(speedup<1): speedup = 1
    if keys[pygame.K_r] and speedup <=15:
        speedup += speedup*dt 

    if keys[pygame.K_a]:
        pobs[0] -= move_speed*dt 
    if keys[pygame.K_d]:
        pobs[0] += move_speed*dt 
    if keys[pygame.K_s]:
        pobs[1] += move_speed*dt 
    if keys[pygame.K_w]:
        pobs[1] -= move_speed*dt 

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics
    dt = clock.tick(60) / 1000

pygame.quit()