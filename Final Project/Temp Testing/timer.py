from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Global timer vars
GAME_DURATION = 60  # Total game timer
time_remaining = GAME_DURATION
timer_active = False
timer_id = None  # GLUT timer ID
is_timer_paused = False  # Pause state for timer
cheat_mode_timer = False  # Cheat mode for timer
callback_running = False  # Prevent multiple callbacks
last_callback_time = 0  # Track last callback time

# Timer started method
def start_timer():
    global time_remaining, timer_active, timer_id, is_timer_paused, cheat_mode_timer, callback_running, last_callback_time
    
    # Always stop any existing timer first
    stop_timer()
    
    time_remaining = GAME_DURATION
    timer_active = True
    is_timer_paused = False
    cheat_mode_timer = False
    callback_running = False
    last_callback_time = glutGet(GLUT_ELAPSED_TIME)
    
    print(f"Timer started: {time_remaining} seconds remaining")
    
    # Start fresh timer callback
    timer_id = glutTimerFunc(1000, timer_callback, 0)

def timer_callback(value):
    global time_remaining, timer_active, timer_id, is_timer_paused, cheat_mode_timer, callback_running, last_callback_time
    
    current_time = glutGet(GLUT_ELAPSED_TIME)
    
    # Prevent multiple simultaneous callbacks
    if callback_running:
        return
    
    if not timer_active:
        return
    
    # Ensure at least 900ms has passed since last callback (prevent fast timers)
    if current_time - last_callback_time < 900:
        # Too soon, reschedule
        timer_id = glutTimerFunc(100, timer_callback, 0)
        return
    
    callback_running = True
    last_callback_time = current_time
    
    try:
        # Check if timer is paused
        if is_timer_paused:
            # Schedule next check but don't decrement time
            if timer_active:
                timer_id = glutTimerFunc(1000, timer_callback, 0)
            callback_running = False
            return
        
        # Reduce time by 1 second
        time_remaining -= 1
        
        print(f"Timer tick: {time_remaining} seconds remaining, Cheat Mode: {cheat_mode_timer}")
        
        # If time is up, check what to do
        if time_remaining <= 0:
            time_remaining = 0
            
            # In cheat mode, keep timer at 0 but continue running
            if cheat_mode_timer:
                print("Cheat Mode: Timer at 0 but game continues")
                # Keep timer active but at 0
                if timer_active:
                    timer_id = glutTimerFunc(1000, timer_callback, 0)
                callback_running = False
                return
            else:
                # Normal mode: stop timer
                timer_active = False
                print("Time's up!")
                callback_running = False
                return
        
        # Schedule next callback
        if timer_active and not is_timer_paused:
            timer_id = glutTimerFunc(1000, timer_callback, 0)
    except Exception as e:
        print(f"Timer callback error: {e}")
    finally:
        callback_running = False

# Pause timer function
def pause_timer():
    global is_timer_paused, timer_id, callback_running
    
    if timer_active:
        is_timer_paused = True
        print("Timer paused")
        
        # Cancel any pending callbacks
        callback_running = False

# Resume timer function
def resume_timer():
    global is_timer_paused, timer_id, callback_running, last_callback_time
    
    if timer_active and is_timer_paused:
        is_timer_paused = False
        last_callback_time = glutGet(GLUT_ELAPSED_TIME)
        print("Timer resumed")
        
        # Reset callback flag and schedule immediately
        callback_running = False
        timer_id = glutTimerFunc(0, timer_callback, 0)

# Toggle pause function
def toggle_timer_pause():
    if is_timer_paused:
        resume_timer()
    else:
        pause_timer()

# Enable cheat mode for timer
def enable_cheat_mode():
    global cheat_mode_timer, time_remaining, timer_active, callback_running
    cheat_mode_timer = True
    print(f"Timer cheat mode enabled: Time will count down but game won't end")
    
    # Ensure timer is active
    if not timer_active:
        start_timer()
    else:
        timer_active = True
        callback_running = False

# Disable cheat mode for timer
def disable_cheat_mode():
    global cheat_mode_timer, callback_running
    cheat_mode_timer = False
    callback_running = False
    print("Timer cheat mode disabled")

# Toggle cheat mode for timer
def toggle_cheat_mode():
    global cheat_mode_timer, time_remaining, timer_active, callback_running
    cheat_mode_timer = not cheat_mode_timer
    if cheat_mode_timer:
        print(f"Timer cheat mode: ON (Time will count down but game won't end)")
        
        if not timer_active:
            start_timer()
        else:
            timer_active = True
            callback_running = False
    else:
        callback_running = False
        print("Timer cheat mode: OFF")

# Time up method (game over)
def stop_timer():
    global timer_active, timer_id, is_timer_paused, cheat_mode_timer, callback_running, last_callback_time
    
    timer_active = False
    is_timer_paused = False
    cheat_mode_timer = False
    callback_running = False
    timer_id = None
    last_callback_time = 0

# Reset timer after Game restart
def reset_timer():
    global time_remaining, timer_active, timer_id, is_timer_paused, cheat_mode_timer, callback_running, last_callback_time
    
    # Stop any existing timer first
    stop_timer()
    
    time_remaining = GAME_DURATION
    is_timer_paused = False
    cheat_mode_timer = False
    callback_running = False
    last_callback_time = 0

# Display on the screen
def draw_timer():
    if not timer_active:
        return
    
    # Save current matrices
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1250, 0, 1000)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Calculate position (top center)
    timer_x = 625
    timer_y = 50
    
    # Timer bg for better visual
    if cheat_mode_timer:
        glColor3f(0, 0, 0)
    elif is_timer_paused:
        glColor3f(0.2, 0.1, 0)
    elif time_remaining <= 10:
        glColor3f(0.2, 0, 0)
    else:
        glColor3f(0.2, 0.2, 0.2)
    
    glBegin(GL_QUADS)
    glVertex2f(timer_x - 60, timer_y - 25)
    glVertex2f(timer_x + 60, timer_y - 25)
    glVertex2f(timer_x + 60, timer_y + 25)
    glVertex2f(timer_x - 60, timer_y + 25)
    glEnd()
    
    # Text color based on state
    if cheat_mode_timer:
        import time
        blink = int(time.time() * 3) % 2
        if blink:
            glColor3f(0, 1, 0)
        else:
            glColor3f(0, 0.7, 0)
    elif is_timer_paused:
        import time
        blink = int(time.time() * 2) % 2
        if blink:
            glColor3f(1, 0.5, 0)
        else:
            glColor3f(0.8, 0.4, 0)
    elif time_remaining <= 10:
        import time
        blink = int(time.time() * 2) % 2
        if blink:
            glColor3f(1, 0, 0)
        else:
            glColor3f(0.8, 0, 0)
    else:
        glColor3f(1, 1, 1)
    
    minutes = time_remaining // 60
    seconds = time_remaining % 60
    timer_text = f"{minutes:02d}:{seconds:02d}"
    
    if is_timer_paused:
        timer_text = f"{minutes:02d}:{seconds:02d} (PAUSED)"
    elif cheat_mode_timer:
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

# Helper Methods
def get_time_remaining():
    return time_remaining

def is_timer_active():
    return timer_active

def is_timer_paused_state():
    return is_timer_paused

def is_timer_cheat_mode():
    return cheat_mode_timer

def is_timer_expired():
    if cheat_mode_timer:
        return False
    return time_remaining <= 0

def update_timer():
    pass
