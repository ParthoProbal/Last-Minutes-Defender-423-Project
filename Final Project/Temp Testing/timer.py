from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Global timer vars
GAME_DURATION = 60  # Total game timer
time_remaining = GAME_DURATION
timer_active = False
timer_id = None  # GLUT timer ID
is_timer_paused = False  # Pause state for timer
cheat_mode_active = False  # Cheat mode for timer

# Timer started method
def start_timer():
    global time_remaining, timer_active, timer_id, is_timer_paused, cheat_mode_active
    
    if timer_active:
        return
    
    time_remaining = GAME_DURATION
    timer_active = True
    is_timer_paused = False
    cheat_mode_active = False
    
    timer_id = glutTimerFunc(1000, timer_callback, 0)
    print(f"Timer started: {time_remaining} seconds remaining")

def timer_callback(value):
    global time_remaining, timer_active, timer_id, is_timer_paused, cheat_mode_active
    
    if not timer_active:
        return
    
    if is_timer_paused:
        if timer_active:
            timer_id = glutTimerFunc(500, timer_callback, 0)
        return
    
    # ALWAYS decrement the timer regardless of cheat mode
    time_remaining -= 1
    
    print(f"Timer tick: {time_remaining} seconds remaining (Cheat: {cheat_mode_active})")
    
    if time_remaining <= 0:
        time_remaining = 0
        
        # In normal mode: stop timer
        if not cheat_mode_active:
            timer_active = False
            print("Time's up! Game should end.")
        # In cheat mode: just keep it at 0 but don't stop
        else:
            print("Cheat Mode: Timer at 0 but game continues")
    
    # Continue timer if still active (always active in cheat mode even at 0)
    if timer_active and not is_timer_paused:
        timer_id = glutTimerFunc(1000, timer_callback, 0)

def pause_timer():
    global is_timer_paused
    if timer_active:
        is_timer_paused = True
        print("Timer paused")

def resume_timer():
    global is_timer_paused
    if timer_active and is_timer_paused:
        is_timer_paused = False
        print("Timer resumed")

def toggle_timer_pause():
    if is_timer_paused:
        resume_timer()
    else:
        pause_timer()

def enable_timer_cheat():
    global cheat_mode_active
    # DON'T reset time_remaining here!
    cheat_mode_active = True
    print(f"Timer cheat enabled: {time_remaining} seconds")

def disable_timer_cheat():
    global cheat_mode_active
    cheat_mode_active = False
    print(f"Timer cheat disabled: {time_remaining} seconds")

def stop_timer():
    global timer_active, timer_id, is_timer_paused, cheat_mode_active
    
    timer_active = False
    is_timer_paused = False
    cheat_mode_active = False
    timer_id = None

def reset_timer():
    global time_remaining, timer_active, timer_id, is_timer_paused, cheat_mode_active
    
    timer_active = False
    is_timer_paused = False
    cheat_mode_active = False
    timer_id = None
    time_remaining = GAME_DURATION

def draw_timer():
    if time_remaining <= 0:
        return
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1250, 0, 1000)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    timer_x = 625
    timer_y = 50
    
    if is_timer_paused:
        # Use glutGet for time instead of time.time()
        current_ms = glutGet(GLUT_ELAPSED_TIME)
        blink = (current_ms // 500) % 2
        if blink:
            glColor3f(1, 0.5, 0)
        else:
            glColor3f(0.8, 0.4, 0)
    elif cheat_mode_active:
        current_ms = glutGet(GLUT_ELAPSED_TIME)
        blink = (current_ms // 300) % 2
        if blink:
            glColor3f(0, 1, 0)
        else:
            glColor3f(0, 0.7, 0)
    elif time_remaining <= 10:
        glColor3f(1, 0, 0)
    else:
        glColor3f(1, 1, 1)
    
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(timer_x - 60, timer_y - 25)
    glVertex2f(timer_x + 60, timer_y - 25)
    glVertex2f(timer_x + 60, timer_y + 25)
    glVertex2f(timer_x - 60, timer_y + 25)
    glEnd()
    
    if is_timer_paused:
        glColor3f(1, 0.5, 0)
    elif cheat_mode_active:
        glColor3f(0, 1, 0)
    elif time_remaining <= 10:
        glColor3f(1, 0, 0)
    else:
        glColor3f(1, 1, 1)
    
    minutes = time_remaining // 60
    seconds = time_remaining % 60
    timer_text = f"{minutes:02d}:{seconds:02d}"
    
    if is_timer_paused:
        timer_text = f"{minutes:02d}:{seconds:02d} (PAUSED)"
    elif cheat_mode_active:
        timer_text = f"{minutes:02d}:{seconds:02d} (CHEAT)"
    
    text_width = len(timer_text) * 10
    text_x = timer_x - (text_width // 2)
    
    glRasterPos2f(text_x, timer_y - 5)
    for ch in timer_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def get_time_remaining():
    return time_remaining

def is_timer_active():
    return timer_active

def is_timer_paused_state():
    return is_timer_paused

# REMOVE THE DUPLICATE! Only keep one is_timer_expired()
def is_timer_expired():
    global time_remaining, timer_active
    return time_remaining <= 0 and timer_active

def update_timer():
    pass
