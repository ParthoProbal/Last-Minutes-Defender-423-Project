from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import time

# QTE Variables
qte_active = False
qte_key = ""
qte_time_total = 1  # 1 second total, tweak to change duration
qte_time_remaining = 1
qte_start_time = 0
qte_result = None  # "win" or "lose"
qte_keys = ["W", "A", "S", "D"] # More or different keys can be added

def startQTE():
    global qte_active, qte_key, qte_time_remaining, qte_start_time, qte_result
    
    qte_active = True
    qte_key = random.choice(qte_keys)
    qte_time_remaining = qte_time_total
    qte_start_time = time.time()
    qte_result = None
    
    print(f"QTE STARTED! Press: {qte_key}")

def updateQTE():
    global qte_active, qte_time_remaining, qte_result
    
    if not qte_active:
        return
    
    current_time = time.time()
    elapsed = current_time - qte_start_time
    qte_time_remaining = qte_time_total - elapsed
    
    if qte_time_remaining <= 0:
        qte_active = False
        qte_result = "lose"
        print("QTE FAILED: Timeout!")

def handleQTEKey(key):
    global qte_active, qte_result
    
    if not qte_active:
        return False
    
    key_char = key.upper()
    
    if key_char == qte_key:
        qte_active = False
        qte_result = "win"
        print("QTE SUCCESS! Key pressed correctly.")
        return True
    else:
        qte_active = False
        qte_result = "lose"
        print(f"QTE FAILED: Wrong key. Expected {qte_key}, got {key_char}")
        return False

def drawQTE():
    if not qte_active:
        return
    
    glPushMatrix()
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1250, 0, 1000)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # QTE box position (center)
    box_x = 625
    box_y = 500
    
    # QTE bg (black)
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(box_x - 100, box_y - 100)
    glVertex2f(box_x + 100, box_y - 100)
    glVertex2f(box_x + 100, box_y + 100)
    glVertex2f(box_x - 100, box_y + 100)
    glEnd()
    
    # QTE key (white)
    glColor3f(1, 1, 1)
    glRasterPos2f(box_x - 10, box_y + 20)
    for ch in qte_key:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    # Time bar bg (gray)
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(box_x - 80, box_y - 80)
    glVertex2f(box_x + 80, box_y - 80)
    glVertex2f(box_x + 80, box_y - 60)
    glVertex2f(box_x - 80, box_y - 60)
    glEnd()
    
    # Time bar fill (green to red)
    time_percentage = qte_time_remaining / qte_time_total
    
    if time_percentage > 0.5:
        glColor3f(0, 1, 0)  # Green
    elif time_percentage > 0.25:
        glColor3f(1, 1, 0)  # Yellow
    else:
        glColor3f(1, 0, 0)  # Red
    
    bar_width = 160 * time_percentage
    glBegin(GL_QUADS)
    glVertex2f(box_x - 80, box_y - 75)
    glVertex2f(box_x - 80 + bar_width, box_y - 75)
    glVertex2f(box_x - 80 + bar_width, box_y - 65)
    glVertex2f(box_x - 80, box_y - 65)
    glEnd()
    
    # "PRESS KEY" text
    glColor3f(1, 1, 1)
    glRasterPos2f(box_x - 40, box_y + 60)
    for ch in "PRESS KEY:":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glPopMatrix()

def resetQTE():
    global qte_active, qte_key, qte_time_remaining, qte_start_time, qte_result
    
    qte_active = False
    qte_key = ""
    qte_time_remaining = qte_time_total
    qte_start_time = 0
    qte_result = None

def isQTEActive():
    return qte_active

def getQTEResult():
    return qte_result