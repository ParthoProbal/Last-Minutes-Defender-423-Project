from OpenGL.GL import *
import random

stars = []

def init_space():
    global stars
    stars = []
    for i in range(150):
        stars.append((
            random.uniform(-2000, 2000),
            random.uniform(-2000, 2000),
            random.uniform(-1800, 200)
        ))

def draw_space():
    glPointSize(2.0)
    glColor3f(1.0, 1.0, 1.0)
    
    glBegin(GL_POINTS)
    for x, y, z in stars:
        glVertex3f(x, y, z)
    glEnd()

def update_space():
    pass
