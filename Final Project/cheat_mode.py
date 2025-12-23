from OpenGL.GL import *
from OpenGL.GLUT import *
import time
import math

cheat_on = False
cheat_time = 0
normal_speed = 10
cam_x = 0
cam_y = 500
cam_z = 500

def init_cheat(speed, cx, cy, cz):
    global cheat_on, cheat_time, normal_speed, cam_x, cam_y, cam_z
    cheat_on = False
    cheat_time = 0
    normal_speed = speed
    cam_x = cx
    cam_y = cy
    cam_z = cz

def toggle_cheat():
    global cheat_on, cheat_time
    
    cheat_on = not cheat_on
    
    if cheat_on:
        cheat_time = time.time()
        print("CHEAT ON")

def update_cheat():
    global cheat_on
    
    if not cheat_on:
        return 9999, 9999, 9999, normal_speed
    
    return 9999, 9999, 9999, normal_speed * 3

def update_camera(px, py, pr):
    global cheat_on, cheat_time, cam_x, cam_y, cam_z
    
    if not cheat_on:
        return cam_x, cam_y, cam_z
    
    t = time.time() - cheat_time
    
    tx = px - 100 * math.sin(math.radians(pr))
    ty = py + 100 * math.cos(math.radians(pr))
    
    cam_x += (tx - cam_x) * 0.3
    cam_y += (ty - cam_y) * 0.3
    
    pulse = math.sin(t * 3) * 50
    cam_z = 500 + pulse
    
    return cam_x, cam_y, cam_z

def get_color():
    global cheat_on, cheat_time
    
    if not cheat_on:
        return None
    
    t = time.time() - cheat_time
    p = math.sin(t * 2)
    
    return (0.2 + 0.8*abs(p), 1.0, 0.2 + 0.8*abs(p))

def draw_cheat():
    global cheat_on, cheat_time
    
    if not cheat_on:
        return
    
    glColor3f(0.0, 1.0, 0.0)
    glRasterPos2f(10, 600)
    text = "CHEAT MODE"
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def handle_key(key):
    if key == b'c' or key == b'C':
        toggle_cheat()
        return True
    return False

def is_on():
    global cheat_on
    return cheat_on
