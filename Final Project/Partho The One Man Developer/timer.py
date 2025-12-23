from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Global timer vars
GAME_DURATION = 60  # Total game timer
time_remaining = GAME_DURATION
timer_active = False
timer_id = None  # GLUT timer ID

# Timer started method
def start_timer():
    global time_remaining, timer_active, timer_id
    
    if timer_active:
        return
    
    time_remaining = GAME_DURATION
    timer_active = True
    
    timer_id = glutTimerFunc(1000, timer_callback, 0)
    print(f"Timer started: {time_remaining} seconds remaining")  # Debug code

def timer_callback(value):
    global time_remaining, timer_active, timer_id
    
    if not timer_active:
        return
    
    # Reduce time by 1 second
    time_remaining -= 1
    
    # Debug print
    print(f"Timer tick: {time_remaining} seconds remaining")
    
    # If time is up, stop timer
    if time_remaining <= 0:
        time_remaining = 0
        timer_active = False
        print("Time's up!")
        return
    
    if timer_active:
        timer_id = glutTimerFunc(1000, timer_callback, 0)

# Time up method (game over)
def stop_timer():
    global timer_active, timer_id
    
    timer_active = False
    timer_id = None

# Reset timer after Game restart
def reset_timer():
    global time_remaining, timer_active, timer_id
    
    timer_active = False
    timer_id = None
    time_remaining = GAME_DURATION

# Display on the screen
def draw_timer():
    if time_remaining <= 0:
        return
    
    # Save current matrices
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1250, 0, 1000)  # Match window size
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Calculate position (top center)
    timer_x = 625  # Center of 1250 width window
    timer_y = 50   # 50 pixels from top
    
    # Color (Regular if > 10)
    if time_remaining <= 10:
        glColor3f(1, 0, 0)  # Red for the last 10 sec
    else:
        glColor3f(1, 1, 1)  # Else white
    
    # Timer bg for better visual of the clock
    glColor3f(0.2, 0.2, 0.2)  # Dark gray bg
    glBegin(GL_QUADS)
    glVertex2f(timer_x - 60, timer_y - 25)
    glVertex2f(timer_x + 60, timer_y - 25)
    glVertex2f(timer_x + 60, timer_y + 25)
    glVertex2f(timer_x - 60, timer_y + 25)
    glEnd()
    
    glColor3f(1, 1, 1)
    
    # Timer format (MM : SS)
    minutes = time_remaining // 60
    seconds = time_remaining % 60
    timer_text = f"{minutes:02d}:{seconds:02d}"  # F string for 2 decimals
    
    # Div -> Center
    text_width = len(timer_text) * 10  # Text width
    text_x = timer_x - (text_width // 2)
    
    glRasterPos2f(text_x, timer_y - 5)
    for ch in timer_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))  # Text font
    
    # Restore matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# Helper Methods
def get_time_remaining():
    return time_remaining

def is_timer_active():
    return timer_active

def update_timer():
    pass
