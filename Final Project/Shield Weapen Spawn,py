from OpenGL.GL import *
from OpenGL.GLUT import *
import random

weapon_pos = [random.randint(-200, 200), 0, random.randint(-200, 200)]
shield_pos = [random.randint(-200, 200), 0, random.randint(-200, 200)]

weapon_active = True
shield_active = True

def draw_mega_weapon():
    glPushMatrix()
    glTranslatef(*weapon_pos)
    glColor3f(1.0, 0.2, 0.2)    
    glutSolidCube(20)          
    glPopMatrix()


def draw_mega_shield():
    glPushMatrix()
    glTranslatef(*shield_pos)
    glColor3f(0.2, 0.6, 1.0)   
    glutSolidSphere(15, 30, 30)
    glPopMatrix()


def check_powerup_collision(player_pos):
    global weapon_active, shield_active

    if weapon_active and distance(player_pos, weapon_pos) < 25:
        weapon_active = False
        return "WEAPON"

    if shield_active and distance(player_pos, shield_pos) < 25:
        shield_active = False
        return "SHIELD"

    return None


def distance(a, b):
    return ((a[0]-b[0])**2 + (a[2]-b[2])**2) ** 0.5

