from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Global timer vars
GAME_DURATION = 60  # Total game timer
time_remaining = GAME_DURATION
timer_active = False
timer_id = None  # GLUT timer ID
is_timer_paused = False  # NEW: Pause state for timer

# Timer started method
def start_timer():
    global time_remaining, timer_active, timer_id, is_timer_paused
    
    if timer_active:
        return
    
    time_remaining = GAME_DURATION
    timer_active = True
    is_timer_paused = False  # Reset pause state when starting
    
    timer_id = glutTimerFunc(1000, timer_callback, 0)
    print(f"Timer started: {time_remaining} seconds remaining")  # Debug code

def timer_callback(value):
    global time_remaining, timer_active, timer_id, is_timer_paused
    
    if not timer_active:
        return
    
    # NEW: Check if timer is paused
    if is_timer_paused:
        # Schedule next check but don't decrement time
        if timer_active:
            timer_id = glutTimerFunc(100, timer_callback, 0)  # Check more frequently during pause
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

# NEW: Pause timer function
def pause_timer():
    global is_timer_paused
    if timer_active:
        is_timer_paused = True
        print("Timer paused")

# NEW: Resume timer function
def resume_timer():
    global is_timer_paused
    if timer_active and is_timer_paused:
        is_timer_paused = False
        print("Timer resumed")
        # Restart the timer callback
        timer_callback(0)

# NEW: Toggle pause function
def toggle_timer_pause():
    if is_timer_paused:
        resume_timer()
    else:
        pause_timer()

# Time up method (game over)
def stop_timer():
    global timer_active, timer_id, is_timer_paused
    
    timer_active = False
    is_timer_paused = False
    timer_id = None

# Reset timer after Game restart
def reset_timer():
    global time_remaining, timer_active, timer_id, is_timer_paused
    
    timer_active = False
    is_timer_paused = False
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
    
    # NEW: Different color when paused
    if is_timer_paused:
        # Blinking effect or different color for paused state
        import time
        blink = int(time.time() * 2) % 2  # Blink every half second
        if blink:
            glColor3f(1, 0.5, 0)  # Orange when paused and blinking
        else:
            glColor3f(0.8, 0.4, 0)  # Darker orange
    elif time_remaining <= 10:
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
    
    # Reset color for text
    if is_timer_paused:
        glColor3f(1, 0.5, 0)  # Orange text when paused
    elif time_remaining <= 10:
        glColor3f(1, 0, 0)  # Red text for last 10 seconds
    else:
        glColor3f(1, 1, 1)  # White text normally
    
    # Timer format (MM : SS)
    minutes = time_remaining // 60
    seconds = time_remaining % 60
    timer_text = f"{minutes:02d}:{seconds:02d}"  # F string for 2 decimals
    
    # NEW: Add "(PAUSED)" indicator when paused
    if is_timer_paused:
        timer_text = f"{minutes:02d}:{seconds:02d} (PAUSED)"
    
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

# NEW: Check if timer is paused
def is_timer_paused_state():
    return is_timer_paused

def update_timer():

    if is_timer_paused:
        return 
    pass
