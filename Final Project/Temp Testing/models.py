from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Colors defined inline instead of importing colors module
URANUS_BLUE = (0.4, 0.6, 0.9)
UFO_BLACK = (0.1, 0.1, 0.1)
UFO_WHITE = (0.9, 0.9, 0.9)
UFO_LIGHT_GREY = (0.7, 0.7, 0.7)
UFO_GUN_GREY = (0.5, 0.5, 0.5)
ENEMY_BLUE = (0.2, 0.2, 0.8)
ENEMY_BLACK = (0.05, 0.05, 0.05)
ENEMY_YELLOW = (0.9, 0.9, 0.1)
PLANET_ATTACKER_ORANGE = (0.9, 0.5, 0.1)
PLANET_ATTACKER_GREEN = (0.2, 0.8, 0.2)
BOSS_RED = (0.8, 0.1, 0.1)
BOSS_WHITE = (0.95, 0.95, 0.95)
BOSS_BALL_COLOR = (0.3, 0.3, 0.8)
BOSS_GUN_COLOR = (0.4, 0.4, 0.9)
HEALTH_BOX_COLOR = (1.0, 1.0, 1.0)
AMMO_BOX_COLOR = (0.94, 0.90, 0.55)  # Khaki green

# NEW: Global game state tracking
game_over_state = False
current_wave_state = 1

def drawPlanet(radius, pos_x=0, pos_y=0, pos_z=0):
    glPushMatrix()
    glTranslatef(pos_x, pos_y, pos_z) # Planet x, y, z
    
    glColor3f(URANUS_BLUE[0], URANUS_BLUE[1], URANUS_BLUE[2])
    
    glutSolidSphere(radius, 50, 50)  # Radius, Stack space x, y
    
    glPopMatrix()

# Body parts start
def drawUfoBody():
    # NEW: Black color when game over
    if game_over_state:
        glColor3f(0, 0, 0)  # Black when game over
    else:
        glColor3f(UFO_BLACK[0], UFO_BLACK[1], UFO_BLACK[2])
    glutSolidSphere(50, 30, 30) 

def drawUfoHand():
    # NEW: Dark gray when game over
    if game_over_state:
        glColor3f(0.2, 0.2, 0.2)  # Dark gray when game over
    else:
        glColor3f(UFO_WHITE[0], UFO_WHITE[1], UFO_WHITE[2])
    gluCylinder(gluNewQuadric(), 5, 3, 60, 10, 10)  

def drawUfoCircle():
    # NEW: Dark gray when game over
    if game_over_state:
        glColor3f(0.1, 0.1, 0.1)  # Very dark gray when game over
    else:
        glColor3f(UFO_LIGHT_GREY[0], UFO_LIGHT_GREY[1], UFO_LIGHT_GREY[2])
    glutSolidSphere(30, 20, 20)

def drawUfoGun():
    # NEW: Dark gray when game over
    if game_over_state:
        glColor3f(0.3, 0.3, 0.3)  # Gray when game over
    else:
        glColor3f(UFO_GUN_GREY[0], UFO_GUN_GREY[1], UFO_GUN_GREY[2])
    glTranslatef(0, 0, 30)  
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 8, 4, 50, 10, 10)  # Gun: base radius 8, top 4, length 50
    glRotatef(90, 1, 0, 0)
    
# Body parts end

def drawHeroUfo(pos_x=0, pos_y=0, pos_z=120, rotation=0, cheat_mode = False):
    glPushMatrix()
    
    glTranslatef(pos_x, pos_y, pos_z)
    glRotatef(rotation, 0, 0, 1)
    
    # Cheat mode color to regular mode
    if cheat_mode:
        # NEW: Game over takes priority over cheat mode
        if game_over_state:
            glColor3f(0, 0, 0)  # Black when game over
        else:
            glColor3f(0, 1, 0)  # Green in cheat mode
    else:
        # NEW: Black when game over, otherwise normal color
        if game_over_state:
            glColor3f(0, 0, 0)  # Black when game over
        else:
            glColor3f(UFO_BLACK[0], UFO_BLACK[1], UFO_BLACK[2])
    
    glutSolidSphere(50, 30, 30) 
    
    drawUfoBody()
    
    # Hand 1 (Right)
    glPushMatrix()
    glTranslatef(60, 0, 0)
    glRotatef(90, 0, 1, 0)
    drawUfoHand()
    glPopMatrix()
    
    # Hand 2 (Left)
    glPushMatrix()
    glTranslatef(-60, 0, 0)  
    glRotatef(-90, 0, 1, 0)  
    drawUfoHand()
    glPopMatrix()
    
    # Hand Balls
    glPushMatrix()
    glTranslatef(120, 0, 0)  # Right hand ball
    drawUfoCircle()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-120, 0, 0)  # Left hand ball
    drawUfoCircle()  
    glPopMatrix()
    
    glPushMatrix()
    drawUfoGun()
    glPopMatrix()
    
    glPopMatrix()
    
    
# Hero Attacker Enemy
def drawEnemyBody():
    # NEW: Darker when game over
    if game_over_state:
        glColor3f(0.05, 0.05, 0.15)  # Very dark blue when game over
    else:
        glColor3f(ENEMY_BLUE[0], ENEMY_BLUE[1], ENEMY_BLUE[2])
    glutSolidSphere(40, 30, 30) 

def drawEnemyLeg():
    # NEW: Darker when game over
    if game_over_state:
        glColor3f(0.1, 0.1, 0.1)  # Very dark when game over
    else:
        glColor3f(ENEMY_BLACK[0], ENEMY_BLACK[1], ENEMY_BLACK[2])
    gluCylinder(gluNewQuadric(), 6, 3, 50, 10, 10)  

def drawEnemyTurret():
    # NEW: Darker when game over
    if game_over_state:
        glColor3f(0.3, 0.3, 0.1)  # Dark yellow when game over
    else:
        glColor3f(ENEMY_YELLOW[0], ENEMY_YELLOW[1], ENEMY_YELLOW[2])
    glTranslatef(0, 0, 30)  
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 8, 4, 40, 10, 10)
    glRotatef(90, 1, 0, 0)

def drawHeroAttacker(pos_x=0, pos_y=0, pos_z=120, rotation=0):
    glPushMatrix()
    
    glTranslatef(pos_x, pos_y, pos_z)
    glRotatef(rotation, 0, 0, 1)
    
    drawEnemyBody()
    
    # Leg 1 (Right, 180 degrees backwards)
    glPushMatrix()
    glTranslatef(30, 0, -40)  
    glRotatef(180, 0, 0, 1)  
    drawEnemyLeg()
    glPopMatrix()
    
    # Leg 2 (Left, 180 degrees backwards)
    glPushMatrix()
    glTranslatef(-30, 0, -40)  
    glRotatef(180, 0, 0, 1)  
    drawEnemyLeg()
    glPopMatrix()
    
    # Turret
    glPushMatrix()
    drawEnemyTurret()
    glPopMatrix()
    
    glPopMatrix()
    
    
# Planet Attacker Enemy
def drawPlanetAttackerBody():
    # NEW: Darker when game over
    if game_over_state:
        glColor3f(0.15, 0.1, 0.05)  # Dark orange when game over
    else:
        glColor3f(PLANET_ATTACKER_ORANGE[0], PLANET_ATTACKER_ORANGE[1], PLANET_ATTACKER_ORANGE[2])
    glutSolidSphere(35, 30, 30) 

def drawPlanetAttackerSword():
    # NEW: Darker when game over
    if game_over_state:
        glColor3f(0.1, 0.2, 0.1)  # Dark green when game over
    else:
        glColor3f(PLANET_ATTACKER_GREEN[0], PLANET_ATTACKER_GREEN[1], PLANET_ATTACKER_GREEN[2])
    glTranslatef(0, 0, 30)  
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 10, 2, 60, 10, 10)  # Pusher, Wide base (10), narrow tip (2), length 60
    glRotatef(90, 1, 0, 0)

def drawPlanetAttacker(pos_x=0, pos_y=0, pos_z=120, rotation=0):
    glPushMatrix()
    
    glTranslatef(pos_x, pos_y, pos_z)
    glRotatef(rotation, 0, 0, 1)
    
    drawPlanetAttackerBody()
    
    # Sword/wood for pushing planet
    glPushMatrix()
    drawPlanetAttackerSword()
    glPopMatrix()
    
    glPopMatrix()
    
    
# Boss Enemy Parts
def drawBossBody():
    # NEW: Darker when game over
    if game_over_state:
        glColor3f(0.3, 0, 0)  # Dark red when game over
    else:
        glColor3f(BOSS_RED[0], BOSS_RED[1], BOSS_RED[2])  
    glutSolidSphere(75, 30, 30)  # Larger than hero (75 size)

def drawBossHand():
    # NEW: Darker when game over
    if game_over_state:
        glColor3f(0.4, 0.4, 0.4)  # Dark gray when game over
    else:
        glColor3f(BOSS_WHITE[0], BOSS_WHITE[1], BOSS_WHITE[2])  
    gluCylinder(gluNewQuadric(), 7.5, 4.5, 90, 10, 10)  # Bigger

def drawBossCircle():
    # NEW: Darker when game over
    if game_over_state:
        glColor3f(0.2, 0.2, 0.4)  # Dark version when game over
    else:
        glColor3f(BOSS_BALL_COLOR[0], BOSS_BALL_COLOR[1], BOSS_BALL_COLOR[2])  
    glutSolidSphere(45, 20, 20)  # Bigger Hamd ball 

def drawBossGun():
    # NEW: Darker when game over
    if game_over_state:
        glColor3f(0.3, 0.3, 0.6)  # Dark version when game over
    else:
        glColor3f(BOSS_GUN_COLOR[0], BOSS_GUN_COLOR[1], BOSS_GUN_COLOR[2]) 
    glTranslatef(0, 0, 45)  
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 12, 6, 75, 10, 10) 
    glRotatef(90, 1, 0, 0)


# Boss Enemy (Bigger Version of the Hero Spaceship)
def drawBossEnemy(pos_x=0, pos_y=0, pos_z=120, rotation=0):
    glPushMatrix()
    
    glTranslatef(pos_x, pos_y, pos_z)
    glRotatef(rotation, 0, 0, 1)
    
    drawBossBody()
    
    # Hand 1 (Right)
    glPushMatrix()
    glTranslatef(90, 0, 0)  
    glRotatef(90, 0, 1, 0)
    drawBossHand()
    glPopMatrix()
    
    # Hand 2 (Left)
    glPushMatrix()
    glTranslatef(-90, 0, 0)  # Scaled up
    glRotatef(-90, 0, 1, 0)  
    drawBossHand()
    glPopMatrix()
    
    # Hand Balls
    glPushMatrix()
    glTranslatef(180, 0, 0)  # Right hand bal
    drawBossCircle()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-180, 0, 0)  # Left hand ball
    drawBossCircle()  
    glPopMatrix()
    
    # Gun
    glPushMatrix()
    drawBossGun()
    glPopMatrix()
    
    glPopMatrix()
    
# Health Pickup Box
def drawHealthBox(pos_x =0, pos_y=0, pos_z=50):
    # NEW: Conditional rendering based on wave
    # Don't render health boxes in Wave 3
    if current_wave_state == 3:
        return  # Don't draw anything
    
    glPushMatrix()
    
    glTranslatef(pos_x, pos_y, pos_z)
    
    glColor3f(HEALTH_BOX_COLOR[0], HEALTH_BOX_COLOR[1], HEALTH_BOX_COLOR[2])
    glutSolidCube(30)  # White cube = 30 size
    
    glPopMatrix()

# Ammo Pickup Box
def drawAmmoBox(pos_x=0, pos_y=0, pos_z=50):
    # NEW: Conditional rendering based on wave
    # Don't render ammo boxes in Wave 3 (only mega power-ups allowed)
    if current_wave_state == 3:
        return  # Don't draw anything
    
    glPushMatrix()
    
    glTranslatef(pos_x, pos_y, pos_z)
    
    glColor3f(AMMO_BOX_COLOR[0], AMMO_BOX_COLOR[1], AMMO_BOX_COLOR[2])
    glutSolidCube(30)  # Khaki green = size 30
    
    glPopMatrix()

# NEW: Functions to update game state
def setGameOverState(is_game_over):
    global game_over_state
    game_over_state = is_game_over

def setCurrentWave(wave_number):
    global current_wave_state
    current_wave_state = wave_number

# NEW: Helper function to check if we should render pickups
def shouldRenderPickup(pickup_type):
    # Don't render any regular pickups in Wave 3
    if current_wave_state == 3:
        return False
    
    # For health/ammo pickups, we can also check game over state
    if game_over_state:
        return False
    
    return True
