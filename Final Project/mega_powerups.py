from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

weapon_spawned = False
shield_spawned = False
weapon_got = False
shield_got = False
weapon_x = 0
weapon_y = 0
shield_x = 0
shield_y = 0
weapon_ammo = 0
last_regen = 0

def init_mega():
    global weapon_spawned, shield_spawned, weapon_got, shield_got
    global weapon_x, weapon_y, shield_x, shield_y, weapon_ammo, last_regen
    
    weapon_spawned = False
    shield_spawned = False
    weapon_got = False
    shield_got = False
    weapon_x = 0
    weapon_y = 0
    shield_x = 0
    shield_y = 0
    weapon_ammo = 0
    last_regen = 0

def update_mega():
    global weapon_ammo, last_regen, weapon_got
    
    if not weapon_got:
        return
    
    now = time.time()
    if weapon_ammo < 3 and now - last_regen >= 3.0:
        add = random.randint(1, 3)
        weapon_ammo = min(10, weapon_ammo + add)
        last_regen = now

def spawn_mega():
    global weapon_spawned, shield_spawned, weapon_x, weapon_y, shield_x, shield_y
    
    weapon_x = random.randint(-400, 400)
    weapon_y = random.randint(-400, 400)
    weapon_spawned = True
    
    shield_x = random.randint(-400, 400)
    shield_y = random.randint(-400, 400)
    
    while abs(shield_x - weapon_x) < 150 and abs(shield_y - weapon_y) < 150:
        shield_x = random.randint(-400, 400)
        shield_y = random.randint(-400, 400)
    
    shield_spawned = True

def check_mega(px, py):
    global weapon_got, shield_got, weapon_ammo, weapon_spawned, shield_spawned
    
    if weapon_spawned and not weapon_got:
        dx = px - weapon_x
        dy = py - weapon_y
        d = (dx*dx + dy*dy) ** 0.5
        
        if d < 50:
            weapon_got = True
            weapon_ammo = 10
    
    if shield_spawned and not shield_got:
        dx = px - shield_x
        dy = py - shield_y
        d = (dx*dx + dy*dy) ** 0.5
        
        if d < 50:
            shield_got = True

def draw_mega():
    global weapon_spawned, shield_spawned, weapon_got, shield_got
    
    if weapon_spawned and not weapon_got:
        draw_weapon()
    
    if shield_spawned and not shield_got:
        draw_shield()
    
    if weapon_got:
        draw_weapon_hud()

def draw_weapon():
    global weapon_x, weapon_y
    
    glPushMatrix()
    glTranslatef(weapon_x, weapon_y, 100)
    
    rot = glutGet(GLUT_ELAPSED_TIME) / 1000.0 * 45
    glRotatef(rot, 0, 0, 1)
    
    glColor3f(1.0, 0.84, 0.0)
    glScalef(2.0, 0.5, 0.5)
    glutSolidCube(40)
    glPopMatrix()

def draw_shield():
    global shield_x, shield_y
    
    glPushMatrix()
    glTranslatef(shield_x, shield_y, 100)
    
    rot = glutGet(GLUT_ELAPSED_TIME) / 1000.0 * 30
    glRotatef(rot, 1, 1, 0)
    
    glColor3f(0.0, 0.5, 1.0)
    glutSolidSphere(30, 16, 16)
    glPopMatrix()

def draw_weapon_hud():
    global weapon_ammo
    
    glColor3f(1.0, 0.84, 0.0)
    glRasterPos2f(10, 690)
    text = f"MEGA GUN: {weapon_ammo}/10"
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
