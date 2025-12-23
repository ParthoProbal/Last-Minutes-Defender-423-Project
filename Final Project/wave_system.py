from OpenGL.GL import *
from OpenGL.GLUT import *
import time

current_wave = 1
wave_start_time = 0
game_time = 0
boss_spawned = False
boss_active = False
boss_health = 1000
time_left = 0

def init_wave_system():
    global current_wave, wave_start_time, game_time, boss_spawned, boss_active, boss_health, time_left
    current_wave = 1
    wave_start_time = time.time()
    game_time = 0
    boss_spawned = False
    boss_active = False
    boss_health = 1000
    time_left = 0

def update_wave():
    global current_wave, game_time, boss_spawned, boss_active, time_left
    
    game_time = time.time() - wave_start_time
    
    if current_wave == 1:
        time_left = 20 - game_time
        if game_time >= 20:
            current_wave = 2
            print("WAVE 2 STARTED")
    
    elif current_wave == 2:
        time_left = 35 - game_time
        if game_time >= 35:
            current_wave = 3
            boss_spawned = True
            boss_active = True
            print("WAVE 3 - BOSS")
    
    elif current_wave == 3:
        time_left = 60 - game_time
        if game_time >= 60:
            print("TIME UP")

def draw_wave():
    global current_wave, time_left, boss_active, boss_health
    
    glColor3f(1, 1, 0)
    glRasterPos2f(10, 780)
    wave_text = f"WAVE {current_wave}"
    for ch in wave_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    glColor3f(1, 1, 1)
    glRasterPos2f(10, 750)
    
    if current_wave == 1:
        text = f"Next: {int(time_left)}s"
    elif current_wave == 2:
        text = f"Boss: {int(time_left)}s"
    elif current_wave == 3:
        text = f"Time: {int(time_left)}s"
    
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
    
    if boss_active:
        draw_boss_bar()

def draw_boss_bar():
    global boss_health
    
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(200, 50)
    glVertex2f(800, 50)
    glVertex2f(800, 80)
    glVertex2f(200, 80)
    glEnd()
    
    percent = boss_health / 1000.0
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(200, 50)
    glVertex2f(200 + 600 * percent, 50)
    glVertex2f(200 + 600 * percent, 80)
    glVertex2f(200, 80)
    glEnd()
