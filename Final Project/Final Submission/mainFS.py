# Partho Probal (24121287)
# Sadia Sunjana Shashee (22201656)
# Tanjum Khondoker (22201481)

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# ===== COLORS MODULE =====
divisor = 255 # Color Divisor

# Planet color
URANUS_BLUE = (135/divisor, 206/divisor, 235/divisor)

# UFO Hero Spaceship colors
UFO_BLACK = (200/divisor, 200/divisor, 200/divisor) # Main body
UFO_WHITE = (128/divisor, 128/divisor, 128/divisor) # Hands/arms
UFO_LIGHT_GREY = (100/divisor, 0/divisor, 0/divisor) # Ball Small circle
UFO_GUN_GREY = (128/divisor, 128/divisor, 128/divisor)  # Gun color

# Hero Attacker Enemy colors
ENEMY_BLUE = (0/divisor, 0/divisor, 255/divisor)  # Main body
ENEMY_BLACK = (0/divisor, 0/divisor, 0/divisor)   # Legs
ENEMY_YELLOW = (255/divisor, 255/divisor, 0/divisor)  # Turret

# Planet Attacker Enemy colors
PLANET_ATTACKER_ORANGE = (255/divisor, 165/divisor, 0/divisor)  # Main body
PLANET_ATTACKER_GREEN = (0/divisor, 255/divisor, 0/divisor)     # Sword/wood/pusher

# Boss Enemy Colors
BOSS_RED = (255/divisor, 0/divisor, 0/divisor)  # Main body
BOSS_WHITE = (255/divisor, 255/divisor, 255/divisor)  # Hands/arms
BOSS_BALL_COLOR = (255/divisor, 255/divisor, 0/divisor)  # Hand balls
BOSS_GUN_COLOR = (128/divisor, 0/divisor, 128/divisor)  # Gun color

# Health & Ammo Pickup Box Colors
HEALTH_BOX_COLOR = (1, 1, 1)  # White cube
AMMO_BOX_COLOR = (75/divisor, 83/divisor, 32/divisor)  # Army green cube

# ===== MODELS MODULE =====
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

# Global game state tracking
game_over_state = False
current_wave_state = 1

# Global Vars Misc
CHEAT_SPEED_MULTIPLIER = 3
is_paused = False
game_win = False # Did we win the game?

def drawPlanet(radius, pos_x=0, pos_y=0, pos_z=0):
    glPushMatrix()
    glTranslatef(pos_x, pos_y, pos_z) # Planet x, y, z
    
    glColor3f(URANUS_BLUE[0], URANUS_BLUE[1], URANUS_BLUE[2])
    
    glutSolidSphere(radius, 50, 50)  # Radius, Stack space x, y
    
    glPopMatrix()

# Body parts start
def drawUfoBody():
    if game_over_state:
        glColor3f(0, 0, 0)  # Black when game over
    else:
        glColor3f(UFO_BLACK[0], UFO_BLACK[1], UFO_BLACK[2])
    glutSolidSphere(50, 30, 30) 

def drawUfoHand():
    # Dark gray when game over
    if game_over_state:
        glColor3f(0.2, 0.2, 0.2)  # Dark gray when game over
    else:
        glColor3f(UFO_WHITE[0], UFO_WHITE[1], UFO_WHITE[2])
    gluCylinder(gluNewQuadric(), 5, 3, 60, 10, 10)  

def drawUfoCircle():
    # Dark gray when game over
    if game_over_state:
        glColor3f(0.1, 0.1, 0.1)  # Very dark gray when game over
    else:
        glColor3f(UFO_LIGHT_GREY[0], UFO_LIGHT_GREY[1], UFO_LIGHT_GREY[2])
    glutSolidSphere(30, 20, 20)

def drawUfoGun():
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
        # Game over takes priority over cheat mode
        if game_over_state:
            glColor3f(0, 0, 0)  # Black when game over
        else:
            glColor3f(0, 1, 0)  # Green in cheat mode
    else:
        # Black when game over, otherwise normal color
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
    # Darker when game over
    if game_over_state:
        glColor3f(0.05, 0.05, 0.15)  # Very dark blue when game over
    else:
        glColor3f(ENEMY_BLUE[0], ENEMY_BLUE[1], ENEMY_BLUE[2])
    glutSolidSphere(40, 30, 30) 

def drawEnemyLeg():
    # Darker when game over
    if game_over_state:
        glColor3f(0.1, 0.1, 0.1)  # Very dark when game over
    else:
        glColor3f(ENEMY_BLACK[0], ENEMY_BLACK[1], ENEMY_BLACK[2])
    gluCylinder(gluNewQuadric(), 6, 3, 50, 10, 10)  

def drawEnemyTurret():
    # Darker when game over
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
    # Darker when game over
    if game_over_state:
        glColor3f(0.15, 0.1, 0.05)  # Dark orange when game over
    else:
        glColor3f(PLANET_ATTACKER_ORANGE[0], PLANET_ATTACKER_ORANGE[1], PLANET_ATTACKER_ORANGE[2])
    glutSolidSphere(35, 30, 30) 

def drawPlanetAttackerSword():
    # Darker when game over
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
    # Darker when game over
    if game_over_state:
        glColor3f(0.3, 0, 0)  # Dark red when game over
    else:
        glColor3f(BOSS_RED[0], BOSS_RED[1], BOSS_RED[2])  
    glutSolidSphere(75, 30, 30)  # Larger than hero (75 size)

def drawBossHand():
    # Darker when game over
    if game_over_state:
        glColor3f(0.4, 0.4, 0.4)  # Dark gray when game over
    else:
        glColor3f(BOSS_WHITE[0], BOSS_WHITE[1], BOSS_WHITE[2])  
    gluCylinder(gluNewQuadric(), 7.5, 4.5, 90, 10, 10)  # Bigger

def drawBossCircle():
    # Darker when game over
    if game_over_state:
        glColor3f(0.2, 0.2, 0.4)  # Dark version when game over
    else:
        glColor3f(BOSS_BALL_COLOR[0], BOSS_BALL_COLOR[1], BOSS_BALL_COLOR[2])  
    glutSolidSphere(45, 20, 20)  # Bigger Hamd ball 

def drawBossGun():
    # Darker when game over
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
    # Conditional rendering based on wave
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
    # Don't render ammo boxes in Wave 3 (only mega power-ups allowed)
    if current_wave_state == 3:
        return  # Don't draw anything
    
    glPushMatrix()
    
    glTranslatef(pos_x, pos_y, pos_z)
    
    glColor3f(AMMO_BOX_COLOR[0], AMMO_BOX_COLOR[1], AMMO_BOX_COLOR[2])
    glutSolidCube(30)  # Khaki green = size 30
    
    glPopMatrix()

# Functions to update game state
def setGameOverState(is_game_over):
    global game_over_state
    game_over_state = is_game_over

def setCurrentWave(wave_number):
    global current_wave_state
    current_wave_state = wave_number

# Helper function to check if we should render pickups
def shouldRenderPickup(pickup_type):
    # Don't render any regular pickups in Wave 3
    if current_wave_state == 3:
        return False
    
    # For health/ammo pickups, we can also check game over state
    if game_over_state:
        return False
    
    return True

# ===== ENEMY_AI MODULE =====
import random
import math

# Enemy shooting Globals
enemy_bullets = []
boss_bullets = []
ENEMY_FIRE_RATE = 1.0  # 1 bullet per second
BOSS_FIRE_RATE = 1.0

def initPlanetAttackers(count=2):
    planet_attackers = []
    
    for _ in range(count):
        planet_attackers.append(initSinglePlanetAttacker())
    
    return planet_attackers

# Planet Attacker Enemy
def movePlanetAttackers(planet_attackers, planet_x=0, planet_y=-1600):
    limit = 570  # GRID_LEN - 30 (600 - 30 = 570)
    
    for i in range(len(planet_attackers)):
        
        if len(planet_attackers[i]) == 3:
            ex, ey, erot = planet_attackers[i]
            charging_state = "approaching"
            charge_timer = 0
            planet_attackers[i] = [ex, ey, erot, charging_state, charge_timer]
        
        ex, ey, erot, charging_state, charge_timer = planet_attackers[i]
        
        # Calculate distance to planet
        dx = planet_x - ex
        dy = planet_y - ey
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 0:
            norm_dx = dx / dist
            norm_dy = dy / dist
        else:
            norm_dx = 0
            norm_dy = 0
        
        
        angle_to_planet = math.degrees(math.atan2(dy, dx)) - 90
        erot = angle_to_planet
        
        # Battering Ram Mechanics
        if charging_state == "approaching":
            # Move toward planet
            ex += norm_dx * 2  
            ey += norm_dy * 2
            
            # If getting close to planet, start backing
            if dist < 1200:  
                charging_state = "backing"
                charge_timer = 30  
        
        elif charging_state == "backing":
            # Move away from planet
            ex -= norm_dx * 2  # Back away faster
            ey -= norm_dy * 2
            
            charge_timer -= 1
            
            if charge_timer <= 0:
                # Start charging attack
                charging_state = "charging"
                charge_timer = 25  # Shorter charge time
        
        elif charging_state == "charging":
            # Charge toward planet at high speed
            ex += norm_dx * 5  # Faster charge speed
            ey += norm_dy * 5
            charge_timer -= 1
            
            # If charge timer runs out or we hit planet, reset
            if charge_timer <= 0 or dist < 1035:  # Planet radius (1000) + attacker radius (35)
                charging_state = "approaching"
        
        
        if ex < -limit:
            ex = -limit
        elif ex > limit:
            ex = limit
        
        min_y = -2000  
        max_y = limit
        
        if ey < min_y:
            ey = min_y
            # If hitting bottom boundary, reset state
            if charging_state == "charging":
                charging_state = "approaching"
        elif ey > max_y:
            ey = max_y
        
        # Update the attacker
        planet_attackers[i] = [ex, ey, erot, charging_state, charge_timer]
    
    return planet_attackers

# Boss Enemy Ai
def initBoss():
    half = 600  # GRID_LEN
    limit = 570  # GRID_LEN - 30
    
    # Spawn From a Random wall
    side = random.choice([0, 1, 2, 3])
    
    if side == 0:  # Top wall
        x = random.uniform(-half, half)
        y = limit
        rot = 180
    elif side == 1:  # Bottom wall
        x = random.uniform(-half, half)
        y = -limit
        rot = 0
    elif side == 2:  # Left wall
        x = -limit
        y = random.uniform(-half, half)
        rot = 270
    else:  # Right wall
        x = limit
        y = random.uniform(-half, half)
        rot = 90
    
    return [x, y, rot]

def updateBossPosition():
    global boss_x, boss_y, boss_rot
    
    if not boss_active:
        return
    
    boss_x, boss_y, boss_rot = moveBoss(
        boss_x, boss_y, boss_rot, 
        player_x, player_y, 
        ENEMY_SPEED  # regular enemy speed for testing
    )

# Only 1 Planet Attacker will spawn helper method
def initSinglePlanetAttacker():
    half = 600  # GRID_LEN
    limit = 570  # GRID_LEN - 30 (600 - 30 = 570)
    
    # Spawn from front wall (y = half = 600)
    x = random.uniform(-half, half)
    y = limit  # Front wall position (y = 570, just inside the wall)
    rot = 180  # Facing downward toward planet
    
    return [x, y, rot]

# QTE Helper Method
def checkBossQTE(boss_health):
    if boss_health <= 0:
        return True
    return False

# Boss and Enemy Shooting Mechanics
def enemyShoot(enemy_x, enemy_y, enemy_rot, player_x, player_y, last_shot_time, current_time):
    if current_time - last_shot_time < ENEMY_FIRE_RATE:
        return enemy_bullets, last_shot_time
    
    # Calculate direction to player
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    dist = math.sqrt(dx*dx + dy*dy)
    
    if dist > 0:
        dx /= dist
        dy /= dist
    
    # Start position
    start_x = enemy_x
    start_y = enemy_y
    
    enemy_bullets.append([start_x, start_y, dx, dy, "enemy"])
    last_shot_time = current_time
    
    return enemy_bullets, last_shot_time

def bossShoot(boss_x, boss_y, boss_rot, player_x, player_y, last_boss_shot, current_time):
    if current_time - last_boss_shot < BOSS_FIRE_RATE:
        return boss_bullets, last_boss_shot
    
    # Calculate direction to player
    dx = player_x - boss_x
    dy = player_y - boss_y
    dist = math.sqrt(dx*dx + dy*dy)
    
    if dist > 0:
        dx /= dist
        dy /= dist
    
    # Slower bullet speed for boss
    start_x = boss_x
    start_y = boss_y
    
    boss_bullets.append([start_x, start_y, dx * 0.5, dy * 0.5, "boss"])
    last_boss_shot = current_time
    
    return boss_bullets, last_boss_shot

def moveEnemyBullets():
    global enemy_bullets
    
    new_bullets = []
    
    for bullet_data in enemy_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            bx, by, dx, dy = bullet_data
            bullet_type = "enemy"
        
        bx += dx * 15  # Enemy bullet speed
        by += dy * 15
        
        # Remove if out of bounds
        limit = 800
        if -limit <= bx <= limit and -limit <= by <= limit:
            new_bullets.append([bx, by, dx, dy, bullet_type])
    
    enemy_bullets = new_bullets
    return enemy_bullets

def moveBossBullets():
    global boss_bullets
    
    new_bullets = []
    
    for bullet_data in boss_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            bx, by, dx, dy = bullet_data
            bullet_type = "boss"
        
        bx += dx * 10  # Boss bullet speed (slower)
        by += dy * 10
        
        limit = 800
        if -limit <= bx <= limit and -limit <= by <= limit:
            new_bullets.append([bx, by, dx, dy, bullet_type])
    
    boss_bullets = new_bullets
    return boss_bullets

def getEnemyBullets():
    return enemy_bullets

def getBossBullets():
    return boss_bullets

def resetEnemyShooting():
    global enemy_bullets, boss_bullets, last_enemy_shot, last_boss_shot
    
    enemy_bullets = []
    boss_bullets = []
    last_enemy_shot = 0
    last_boss_shot = 0

# ===== COLLISION MODULE =====
import math

def hitTest(bx, by, ex, ey):
    b_rad = 7.5
    e_rad = 50
    
    dist = math.sqrt((bx - ex) ** 2 + (by - ey) ** 2)
    
    return dist < (b_rad + e_rad)

def handleHits(bullets, enemy_list, planet_attacker_list, boss_x, boss_y, boss_health, boss_active, pickups, score, game_over, current_wave=1, player_has_mega_weapon=False):
    if not bullets:
        return bullets, enemy_list, planet_attacker_list, boss_health, boss_active, pickups, score, game_over
    
    new_bullets = []
    new_enemies = enemy_list.copy()
    new_planet_attackers = planet_attacker_list.copy()
    
    for bullet_data in bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            bx, by, dx, dy = bullet_data
            bullet_type = "normal"
        
        hit = False
        
        # Mega bullet damage
        damage = 400 if bullet_type == "mega" else 1
        
        # Check boss hit
        if boss_active:
            dx_boss = bx - boss_x
            dy_boss = by - boss_y
            boss_dist = math.sqrt(dx_boss*dx_boss + dy_boss*dy_boss)
            
            if boss_dist < (7.5 + 75):
                boss_health -= damage
                hit = True
                if boss_health <= 0:
                    boss_health = 0
        
        # Check regular enemy hits
        if not hit:
            for i in range(len(new_enemies)):
                ex, ey, erot = new_enemies[i]
                
                dx_enemy = bx - ex
                dy_enemy = by - ey
                enemy_dist = math.sqrt(dx_enemy*dx_enemy + dy_enemy*dy_enemy)
                
                if enemy_dist < (7.5 + 50):
                    # Wave 3: No health pickups
                    # After mega weapon: No regular ammo pickups
                    if current_wave != 3:  # Waves 1 & 2
                        pickups.append([ex, ey, "health"])
                    
                    if not player_has_mega_weapon:  # No ammo if has mega weapon
                        pickups.append([ex, ey, "ammo"])
                    
                    # Need to define newEnemy function
                    new_enemies[i] = newEnemy()
                    score += damage
                    hit = True
                    break
        
        # Check planet attacker enemy hits
        if not hit:
            for i in range(len(new_planet_attackers)):
                
                if len(new_planet_attackers[i]) == 3:
                    ex, ey, erot = new_planet_attackers[i]
                else:
                    ex, ey, erot, charging_state, charge_timer = new_planet_attackers[i]
                
                dx_enemy = bx - ex
                dy_enemy = by - ey
                enemy_dist = math.sqrt(dx_enemy*dx_enemy + dy_enemy*dy_enemy)
                
                if enemy_dist < (7.5 + 35):
                    # Wave 3: No health pickups
                    # After mega weapon: No regular ammo pickups
                    if current_wave != 3:  # Waves 1 & 2
                        pickups.append([ex, ey, "health"])
                    
                    if not player_has_mega_weapon:  # No ammo if has mega weapon
                        pickups.append([ex, ey, "ammo"])
                    
                    new_planet_attackers[i] = initSinglePlanetAttacker()
                    score += damage
                    hit = True
                    break
        
        if not hit:
            if bullet_type == "mega":
                new_bullets.append([bx, by, dx, dy, "mega"])
            else:
                new_bullets.append([bx, by, dx, dy])
    
    bullets = new_bullets
    enemy_list = new_enemies
    planet_attacker_list = new_planet_attackers
    return bullets, enemy_list, planet_attacker_list, boss_health, boss_active, pickups, score, game_over


def handlePickups(pickups, player_x, player_y, life, player_ammo):
    if not pickups:
        return pickups, life, player_ammo
    
    new_pickups = []
    
    for i in range(len(pickups)):
        px, py, ptype = pickups[i]
        
        dx = px - player_x
        dy = py - player_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < 300:
            if ptype == "health":
                life += 1
            elif ptype == "ammo":
                player_ammo += 5
        else:
            new_pickups.append([px, py, ptype])
    
    pickups = new_pickups
    return pickups, life, player_ammo

def playerHit(enemy_list, planet_attacker_list, boss_x, boss_y, boss_active, player_x, player_y, life, game_over, bullets, player_has_mega_shield=False, mega_shield_health=0):
    # Check boss collision
    if boss_active:
        dx = boss_x - player_x
        dy = boss_y - player_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < (75 + 18):
            if player_has_mega_shield:
                # Return mega shield health to update it
                damage = 300  # Boss collision damage
                return enemy_list, planet_attacker_list, life, game_over, bullets, damage
            else:
                life -= 300  # Boss collision damage = 300
                if life <= 0:
                    game_over = True
                    life = 0
                    bullets = []
                return enemy_list, planet_attacker_list, life, game_over, bullets, 0
    
    # Check regular enemy collisions
    for i in range(len(enemy_list)):
        ex, ey, erot = enemy_list[i]
        dx = ex - player_x
        dy = ey - player_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < 50:
            if player_has_mega_shield:
                # Return damage amount
                damage = 3 * getEnemyDamageMultiplier()  # Wave damage multiplier
                enemy_list[i] = newEnemy()
                return enemy_list, planet_attacker_list, life, game_over, bullets, damage
            else:
                life -= 3  # Regular enemy damage = 3
                if life <= 0:
                    game_over = True
                    life = 0
                    bullets = []
                
                enemy_list[i] = newEnemy()
                return enemy_list, planet_attacker_list, life, game_over, bullets, 0
    
    # Check planet attacker enemy collisions
    for i in range(len(planet_attacker_list)):
        if len(planet_attacker_list[i]) == 3:
            ex, ey, erot = planet_attacker_list[i]
        else:
            ex, ey, erot, charging_state, charge_timer = planet_attacker_list[i]
        
        dx = ex - player_x
        dy = ey - player_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < (35 + 18):
            if player_has_mega_shield:
                # Return damage amount
                damage = 6 * getEnemyDamageMultiplier()  # Wave damage multiplier
                planet_attacker_list[i] = initSinglePlanetAttacker()
                return enemy_list, planet_attacker_list, life, game_over, bullets, damage
            else:
                life -= 6  # Planet attacker damage = 6
                if life <= 0:
                    game_over = True
                    life = 0
                    bullets = []
                
                planet_attacker_list[i] = initSinglePlanetAttacker()
                return enemy_list, planet_attacker_list, life, game_over, bullets, 0
    
    return enemy_list, planet_attacker_list, life, game_over, bullets, 0

# Planet Hit collision
def planetHit(planet_attacker_list, planet_health, game_over):
    if game_over:
        return planet_attacker_list, planet_health
    
    planet_x = 0
    planet_y = -1600
    planet_radius = 1000
    
    for i in range(len(planet_attacker_list)):
        if len(planet_attacker_list[i]) == 3:
            ex, ey, erot = planet_attacker_list[i]
            charging_state = "approaching"
        else:
            ex, ey, erot, charging_state, charge_timer = planet_attacker_list[i]
        
        # Calculate distance to planet center
        dx = ex - planet_x
        dy = ey - planet_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        collision_distance = planet_radius + 35  # Planet radius + attacker radius
        if dist < collision_distance and charging_state == "charging":
            planet_health -= 3
            
            # debug code for testing
            print(f"PLANET HIT! Damage: 3, New health: {planet_health}")
            
            planet_attacker_list[i] = initSinglePlanetAttacker()
    
    return planet_attacker_list, planet_health

def enemyBulletPlanetHit(enemy_bullets, planet_health):
    if not enemy_bullets:
        return planet_health
    
    planet_x = 0
    planet_y = -1600
    planet_radius = 1000
    
    for bullet_data in enemy_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            continue
        
        # Calculate distance to planet
        dx_planet = bx - planet_x
        dy_planet = by - planet_y
        dist = math.sqrt(dx_planet*dx_planet + dy_planet*dy_planet)
        
        # Enemy bullet hits planet
        if dist < planet_radius + 10:
            planet_health -= 1  # Enemy bullet damage to planet
    
    return planet_health

# ===== HEALTHBAR MODULE =====
def drawHealthbar(player_x, player_y, PLAYER_HEIGHT, life, game_over, HEALTH_ORANGE, player_has_mega_shield=False, mega_shield_health=0):
    if game_over:
        return
    
    glPushMatrix()
    
    glTranslatef(player_x, player_y, 120 + PLAYER_HEIGHT + 50)
    
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-30, -5, 0)
    glVertex3f(30, -5, 0)
    glVertex3f(30, 5, 0)
    glVertex3f(-30, 5, 0)
    glEnd()
    
    # Mega shield health (cyan color)
    if player_has_mega_shield and mega_shield_health > 0:
        glColor3f(0, 1, 1)  # Cyan for mega shield
        health_width = 60 * (mega_shield_health / 1000.0)  # Mega shield max = 1000
    else:
        # Normal health (orange)
        glColor3f(HEALTH_ORANGE[0], HEALTH_ORANGE[1], HEALTH_ORANGE[2])
        health_width = 60 * (life / 5.0)  # Normal health max = 5
    
    glBegin(GL_QUADS)
    glVertex3f(30 - health_width, -4, 1)
    glVertex3f(30, -4, 1)
    glVertex3f(30, 4, 1)
    glVertex3f(30 - health_width, 4, 1)
    glEnd()
    
    glPopMatrix()
    
# Planet Health Bar (Big and Fat)
def drawPlanetHealthBar(planet_health, planet_max_health=100, HEALTH_ORANGE=(1, 0.65, 0)):
    if planet_health <= 0:
        return
    
    glPushMatrix()
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1250, 0, 1000)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    
    bar_x = 625
    bar_y = 950   
    
    # bg (gray)
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(bar_x - 200, bar_y - 20)
    glVertex2f(bar_x + 200, bar_y - 20)
    glVertex2f(bar_x + 200, bar_y + 20)
    glVertex2f(bar_x - 200, bar_y + 20)
    glEnd()
    
    # Health fill (orange)
    health_percentage = planet_health / planet_max_health
    health_width = 400 * health_percentage
    
    glColor3f(HEALTH_ORANGE[0], HEALTH_ORANGE[1], HEALTH_ORANGE[2])
    glBegin(GL_QUADS)
    glVertex2f(bar_x - 200, bar_y - 15)
    glVertex2f(bar_x - 200 + health_width, bar_y - 15)
    glVertex2f(bar_x - 200 + health_width, bar_y + 15)
    glVertex2f(bar_x - 200, bar_y + 15)
    glEnd()
    
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glPopMatrix()

# Enemy Health Bar (Small Red Bar)
def drawEnemyHealthbar(enemy_x, enemy_y, enemy_z):
    glPushMatrix()
    
    glTranslatef(enemy_x, enemy_y, enemy_z + 100)  # Above enemy
    
    # Bg (smaller than player bar)
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-20, -3, 0)
    glVertex3f(20, -3, 0)
    glVertex3f(20, 3, 0)
    glVertex3f(-20, 3, 0)
    glEnd()
    
    # Health fill (red for enemies)
    glColor3f(1, 0, 0)  # Red
    glBegin(GL_QUADS)
    glVertex3f(-20, -2, 1)
    glVertex3f(20, -2, 1)
    glVertex3f(20, 2, 1)
    glVertex3f(-20, 2, 1)
    glEnd()
    
    glPopMatrix()

# Planet Attacker Health Bar (Small Orange Bar)
def drawPlanetAttackerHealthbar(enemy_x, enemy_y, enemy_z):
    glPushMatrix()
    
    glTranslatef(enemy_x, enemy_y, enemy_z + 80)  # Above planet attacker
    
    # Background
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-15, -3, 0)
    glVertex3f(15, -3, 0)
    glVertex3f(15, 3, 0)
    glVertex3f(-15, 3, 0)
    glEnd()
    
    # Health full for planet attackers
    glColor3f(1, 0.5, 0)  # Orange color
    glBegin(GL_QUADS)
    glVertex3f(-15, -2, 1)
    glVertex3f(15, -2, 1)
    glVertex3f(15, 2, 1)
    glVertex3f(-15, 2, 1)
    glEnd()
    
    glPopMatrix()
    
# Boss Health Bar (Big and at Bottom)
def drawBossHealthBar(boss_health, boss_max_health=1000, BOSS_NAME="SKY CAPTAIN"):
    if boss_health <= 0:
        return
    
    glPushMatrix()
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1250, 0, 1000)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Position at bottom center
    bar_x = 625
    bar_y = 80   
    
    # Boss Name
    glColor3f(1, 1, 1)  # White
    glRasterPos2f(bar_x - 50, bar_y + 50)
    for ch in BOSS_NAME:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    # Background (dark red)
    glColor3f(0.5, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(bar_x - 300, bar_y - 20)
    glVertex2f(bar_x + 300, bar_y - 20)
    glVertex2f(bar_x + 300, bar_y + 20)
    glVertex2f(bar_x - 300, bar_y + 20)
    glEnd()
    
    # Health fill (bright red)
    health_percentage = boss_health / boss_max_health
    health_width = 600 * health_percentage
    
    glColor3f(1, 0, 0)  # Red
    glBegin(GL_QUADS)
    glVertex2f(bar_x - 300, bar_y - 15)
    glVertex2f(bar_x - 300 + health_width, bar_y - 15)
    glVertex2f(bar_x - 300 + health_width, bar_y + 15)
    glVertex2f(bar_x - 300, bar_y + 15)
    glEnd()
    
    # Health text
    health_text = f"{boss_health}/{boss_max_health}"
    glColor3f(1, 1, 1)
    glRasterPos2f(bar_x - 30, bar_y - 5)
    for ch in health_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glPopMatrix()

# ===== TIMER MODULE =====
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
            timer_id = glutTimerFunc(1000, timer_callback, 0)
        return
    
    if qte_active:
        if timer_active:
            timer_id = glutTimerFunc(1000, timer_callback, 0)
        return
    
    time_remaining -= 1
    
    if time_remaining <= 0:
        time_remaining = 0
        if not cheat_mode_active:
            timer_active = False
    
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

def is_timer_expired():
    global time_remaining, timer_active
    return time_remaining <= 0 and timer_active

def update_timer():
    pass

# ===== WAVE SYSTEM MODULE =====
# Wave Variables
current_wave = 1
wave_started = False
WAVE1_END = 40 # 40
WAVE2_END = 25 # 25
WAVE3_END = 0
enemy_speed_multiplier = 1.0
enemy_damage_multiplier = 1.0
boss_active_wave3 = False

# Add pause variable
wave_paused = False

def updateWaveSystem(time_remaining):
    global current_wave, wave_started, enemy_speed_multiplier, enemy_damage_multiplier, boss_active_wave3
    global wave_paused
    
    # Don't update if paused
    if wave_paused:
        return current_wave
    
    if time_remaining > WAVE1_END:
        new_wave = 1
        enemy_speed_multiplier = 1.0
        enemy_damage_multiplier = 1.0
    elif time_remaining > WAVE2_END:
        new_wave = 2
        enemy_speed_multiplier = 2.0
        enemy_damage_multiplier = 2.0
    else:
        new_wave = 3
        enemy_speed_multiplier = 2.0
        enemy_damage_multiplier = 2.0
        boss_active_wave3 = True
    
    if new_wave != current_wave:
        current_wave = new_wave
        wave_started = True
        print(f"WAVE {current_wave} STARTED!")
        
        if current_wave == 3:
            print("FINAL WAVE! BOSS INCOMING!")
    
    return current_wave

# Add pause functions
def pauseWaveSystem():
    global wave_paused
    wave_paused = True

def resumeWaveSystem():
    global wave_paused
    wave_paused = False

def isWavePaused():
    return wave_paused

def getEnemySpeedMultiplier():
    return enemy_speed_multiplier

def getEnemyDamageMultiplier():
    return enemy_damage_multiplier

def getCurrentWave():
    return current_wave

def isBossWave():
    return current_wave == 3 and boss_active_wave3

def shouldSpawnPickups():
    # No pickups in wave 3, and check pause
    if wave_paused:
        return False
    return current_wave != 3

def getWaveDamage(enemy_type, base_damage):
    if wave_paused:
        return base_damage
        
    damage = base_damage * enemy_damage_multiplier
    
    if enemy_type == "shooter":
        return int(damage)
    elif enemy_type == "planet_attacker":
        return int(damage * 1.5)
    elif enemy_type == "boss":
        return 200
    
    return int(damage)

def getWaveSpeed(base_speed):
    if wave_paused:
        return base_speed
    return base_speed * enemy_speed_multiplier

def resetWaveSystem():
    global current_wave, wave_started, enemy_speed_multiplier, enemy_damage_multiplier, boss_active_wave3
    global wave_paused
    
    current_wave = 1
    wave_started = False
    enemy_speed_multiplier = 1.0
    enemy_damage_multiplier = 1.0
    boss_active_wave3 = False
    wave_paused = False

# ===== MEGA POWERUPS MODULE =====
import random
import math

# Mega Power-Up Variables
mega_weapon_spawned = False
mega_shield_spawned = False
player_has_mega_weapon = False
player_has_mega_shield = False
mega_weapon_ammo = 10
mega_shield_health = 0
last_ammo_regeneration = 0
mega_weapon_pickup = []  # [x, y]
mega_shield_pickup = []  # [x, y]

def spawnMegaPowerUps():
    global mega_weapon_spawned, mega_shield_spawned, mega_weapon_pickup, mega_shield_pickup
    
    if not mega_weapon_spawned:
        half = 600
        limit = 570
        
        x = random.uniform(-limit, limit)
        y = random.uniform(-limit, limit)
        
        mega_weapon_pickup = [x, y]
        mega_weapon_spawned = True
        print("Mega Weapon spawned!")
    
    if not mega_shield_spawned:
        half = 600
        limit = 570
        
        x = random.uniform(-limit, limit)
        y = random.uniform(-limit, limit)
        
        mega_shield_pickup = [x, y]
        mega_shield_spawned = True
        print("Mega Shield spawned!")

def drawMegaWeaponPickup():
    if not mega_weapon_spawned or player_has_mega_weapon:
        return
    
    glPushMatrix()
    glTranslatef(mega_weapon_pickup[0], mega_weapon_pickup[1], 50)
    
    glColor3f(1, 0, 1)  # Purple color for mega weapon
    glutSolidCube(40)
    
    glPopMatrix()

def drawMegaShieldPickup():
    if not mega_shield_spawned or player_has_mega_shield:
        return
    
    glPushMatrix()
    glTranslatef(mega_shield_pickup[0], mega_shield_pickup[1], 50)
    
    glColor3f(0, 1, 1)  # Cyan color for mega shield
    glutSolidSphere(25, 20, 20)
    
    glPopMatrix()

def handleMegaPickups(player_x, player_y, life, player_ammo, time_remaining):
    global mega_weapon_spawned, mega_shield_spawned
    global player_has_mega_weapon, player_has_mega_shield
    global mega_weapon_ammo, mega_shield_health
    
    # Mega Weapon pickup check
    if mega_weapon_spawned and not player_has_mega_weapon:
        dx = mega_weapon_pickup[0] - player_x
        dy = mega_weapon_pickup[1] - player_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < 300:  # Pickup radius
            player_has_mega_weapon = True
            mega_weapon_ammo = 10
            print("MEGA WEAPON ACQUIRED!")
    
    # Mega Shield pickup check
    if mega_shield_spawned and not player_has_mega_shield:
        dx = mega_shield_pickup[0] - player_x
        dy = mega_shield_pickup[1] - player_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < 300:  # Pickup radius
            player_has_mega_shield = True
            mega_shield_health = 1000
            print("MEGA SHIELD ACQUIRED! Health: 1000")
    
    return life, player_ammo

def megaWeaponShoot():
    global mega_weapon_ammo
    
    if not player_has_mega_weapon or mega_weapon_ammo <= 0:
        return []
    
    mega_weapon_ammo -= 1
    print(f"Mega Weapon fired! Ammo: {mega_weapon_ammo}/10")
    
    return True

def regenerateMegaAmmo(current_time):
    global mega_weapon_ammo, last_ammo_regeneration
    
    if not player_has_mega_weapon or mega_weapon_ammo >= 10:
        return
    
    if mega_weapon_ammo < 3:
        if current_time - last_ammo_regeneration >= 3:  # Every 3 seconds
            regen_amount = random.randint(1, 3)
            mega_weapon_ammo = min(mega_weapon_ammo + regen_amount, 10)
            last_ammo_regeneration = current_time
            print(f"Mega Weapon ammo regenerated: +{regen_amount}")

def getMegaShieldHealth():
    return mega_shield_health

def takeMegaShieldDamage(damage):
    global mega_shield_health
    
    if player_has_mega_shield:
        mega_shield_health -= damage
        if mega_shield_health < 0:
            mega_shield_health = 0
        return mega_shield_health
    return 0

def resetMegaPowerUps():
    global mega_weapon_spawned, mega_shield_spawned
    global player_has_mega_weapon, player_has_mega_shield
    global mega_weapon_ammo, mega_shield_health
    global mega_weapon_pickup, mega_shield_pickup, last_ammo_regeneration
    
    mega_weapon_spawned = False
    mega_shield_spawned = False
    player_has_mega_weapon = False
    player_has_mega_shield = False
    mega_weapon_ammo = 10
    mega_shield_health = 0
    last_ammo_regeneration = 0
    mega_weapon_pickup = []
    mega_shield_pickup = []

# ===== QTE MODULE =====
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
qte_start_glut_time = 0

# QTE Helper Methods
def isQTEActive():
    return qte_active

def getQTEResult():
    return qte_result

def resetQTEState():
    global qte_active, qte_key, qte_time_remaining, qte_start_time, qte_result
    global qte_triggered
    
    qte_active = False
    qte_triggered = False
    qte_key = ""
    qte_time_remaining = qte_time_total
    qte_start_time = 0
    qte_result = None
    
    # Resume gameplay if it was paused
    global wave_paused
    if wave_paused:
        wave_paused = False
    
    # Resume timer if it was paused
    resume_timer()
    
    print("QTE state fully reset")

def startQTE():
    global qte_active, qte_key, qte_time_remaining, qte_start_time, qte_result, qte_start_glut_time
    
    qte_active = True
    qte_key = random.choice(qte_keys)
    qte_time_remaining = qte_time_total
    qte_start_time = time.time()
    qte_start_glut_time = glutGet(GLUT_ELAPSED_TIME)
    qte_result = None

def updateQTE():
    global qte_active, qte_time_remaining, qte_result, qte_start_glut_time
    
    if not qte_active:
        return
    
    current_glut_time = glutGet(GLUT_ELAPSED_TIME)
    elapsed_seconds = (current_glut_time - qte_start_glut_time) / 1000.0
    qte_time_remaining = qte_time_total - elapsed_seconds
    
    if qte_time_remaining <= 0:
        qte_active = False
        qte_result = "lose"

def handleQTEKey(key):
    global qte_active, qte_result
    if not qte_active:
        return False
    
    key_char = key.upper()
    
    if key_char == qte_key:
        qte_active = False
        qte_result = "win"
        wave_paused = False
        resume_timer()
        return True
    else:
        qte_active = False
        qte_result = "lose"
        wave_paused = False
        resume_timer()
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
    
    box_x = 625
    box_y = 500
    
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(box_x - 100, box_y - 100)
    glVertex2f(box_x + 100, box_y - 100)
    glVertex2f(box_x + 100, box_y + 100)
    glVertex2f(box_x - 100, box_y + 100)
    glEnd()
    
    glColor3f(1, 1, 1)
    glRasterPos2f(box_x - 10, box_y + 20)
    for ch in qte_key:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(box_x - 80, box_y - 80)
    glVertex2f(box_x + 80, box_y - 80)
    glVertex2f(box_x + 80, box_y - 60)
    glVertex2f(box_x - 80, box_y - 60)
    glEnd()
    
    time_percentage = qte_time_remaining / qte_time_total
    
    if time_percentage > 0.5:
        glColor3f(0, 1, 0)
    elif time_percentage > 0.25:
        glColor3f(1, 1, 0)
    else:
        glColor3f(1, 0, 0)
    
    bar_width = 160 * time_percentage
    glBegin(GL_QUADS)
    glVertex2f(box_x - 80, box_y - 75)
    glVertex2f(box_x - 80 + bar_width, box_y - 75)
    glVertex2f(box_x - 80 + bar_width, box_y - 65)
    glVertex2f(box_x - 80, box_y - 65)
    glEnd()
    
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

WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 1000
divisor = 255 

camera_pos = (0,500,500)
fovY = 120
rand_var = 423

GRID_LEN = 600  

# Color stuff
CHECKER_COLOR = (128/divisor, 128/divisor, 128/divisor) # Grey
# Add this with other colors
HEALTH_ORANGE = (255/divisor, 165/divisor, 0/divisor)

# Wall colors
LIGHT_GREEN = (0/divisor, 0/divisor, 0/divisor)
BLUE_ROYAL = (0/divisor, 0/divisor, 0/divisor)
CYAN = (0/divisor, 0/divisor, 0/divisor)

# player stuff (My Fav Leon!)
PLAYER_HEIGHT = 45
BLONDE = (210/divisor, 180/divisor, 140/divisor)
RED = (255/divisor, 0/divisor, 0/divisor)
NAVY = (0/divisor, 0/divisor, 128/divisor)
BLACK = (0/divisor, 0/divisor, 0/divisor)

# enemies (Mr X)
GREY_LIGHT = (200/divisor, 200/divisor, 200/divisor)
GREY_DARK = (50/divisor, 50/divisor, 50/divisor)

# movement vars
PLAYER_SPEED = 10
player_x = 0
player_y = 0
player_rot = 0

# enemies stuff
ENEMY_COUNT = 3 
ENEMY_SPEED = 1
enemy_list = [] 

# planet attacker enemy stuff
planet_attacker_list = []
PLANET_ATTACKER_COUNT = 2
planet_attacker_list = initPlanetAttackers(PLANET_ATTACKER_COUNT)

# animation stuff
enemy_scale = 1.0
PULSE_SPEED = 0.005
pulse_dir = PULSE_SPEED

# bullets (Ya ka boom boom!)
BULLET_VEL = 20 
bullets = []

# camera
CAM_SPEED = 10
fps_mode = False

# cheat mode stuff
cheat_active = False
CHEAT_TURN = 5
cheat_vision = False
CHEAT_SPEED_MULTIPLIER = 3

# firing stuff
last_fired = {}
FIRE_DELAY = 0.1

# Planet Stuff
planet_health = 1000
planet_max_health = 1000

# game state
bullets_shot = 0
life = 100
score = 0
missed_shots = 0
game_over = False
MAX_MISS = 100000

# Wave and Mega Power-Up Variables
current_wave = 1
player_has_mega_weapon = False
player_has_mega_shield = False
mega_shield_health = 0
mega_weapon_ammo = 10
last_mega_shot_time = 0
MEGA_FIRE_DELAY = 2.0  # 2 seconds per shot

# Boss Variables
BOSS_HEALTH = 1000
boss_x = 0
boss_y = 0
boss_rot = 0
boss_active = False  # Will activate in Wave 3
boss_health = BOSS_HEALTH
# Ammo and Health Pickup Variables
pickups = []  # Tuple of [x, y, type] "health" or "ammo"
player_ammo = 10  # Player ammo count
player_max_health = 100  # For testing for now

# Wave and Power-Up Variables
current_wave = 1
player_has_mega_weapon = False
player_has_mega_shield = False
mega_shield_health = 0

# QTE Variables
qte_active = False
qte_triggered = False

# Enemy shooting vars
ENEMY_BULLET_SPEED = 15
BOSS_BULLET_SPEED = 10
last_enemy_shot_time = 0
last_boss_shot_time = 0
enemy_last_shot_times = []
last_boss_shot_time = 0

# Game pause state
is_paused = False

# Camera mode (first-person/third-person toggle)
camera_mode = "third_person"  # "third_person" or "first_person"

# Camera distance for arrow keys
CAMERA_DISTANCE_SPEED = 20
camera_distance = 500  # Initial camera distance

def draw_text(x, y, text, font = GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def drawCheckerboard():
    cell = GRID_LEN / 6.5
    half = GRID_LEN
    
    glBegin(GL_QUADS)
    
    for row in range(13):
        for col in range(13):
            x1 = -half + (col * cell)
            x2 = x1 + cell
            y1 = -half + (row * cell)
            y2 = y1 + cell
            
            if (row + col) % 2 == 0:
                glColor3f(0, 0, 0)
            else:
                glColor3f(CHECKER_COLOR[0], CHECKER_COLOR[1], CHECKER_COLOR[2])
            
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
    glEnd()
    

def drawWalls():
    wall_height = 100
    half = GRID_LEN
    
    glBegin(GL_QUADS)
    
    # front
    glColor3f(LIGHT_GREEN[0], LIGHT_GREEN[1], LIGHT_GREEN[2])
    glVertex3f(-half, half, 0)
    glVertex3f(half, half, 0)
    glVertex3f(half, half, wall_height)
    glVertex3f(-half, half, wall_height)
    
    # left
    glColor3f(0, 0, 0)
    glVertex3f(half, half, 0)
    glVertex3f(half, -half, 0)
    glVertex3f(half, -half, wall_height)
    glVertex3f(half, half, wall_height)
    
    # back
    glColor3f(BLUE_ROYAL[0], BLUE_ROYAL[1], BLUE_ROYAL[2])
    glVertex3f(half, -half, 0)
    glVertex3f(-half, -half, 0)
    glVertex3f(-half, -half, wall_height)
    glVertex3f(half, -half, wall_height)
    
    # right
    glColor3f(CYAN[0], CYAN[1], CYAN[2])
    glVertex3f(-half, -half, 0)
    glVertex3f(-half, half, 0)
    glVertex3f(-half, half, wall_height)
    glVertex3f(-half, -half, wall_height)
    
    glEnd()
    

def head():
    glColor3f(BLONDE[0], BLONDE[1], BLONDE[2])
    glutSolidSphere(18, 20, 20)
    

def body():
    glColor3f(NAVY[0], NAVY[1], NAVY[2])
    glScalef(1.5, 0.8, 2.0)
    glutSolidCube(40)
    glScalef(1/1.5, 1/0.8, 1/2.0)
    

def leg(side):
    glColor3f(BLACK[0], BLACK[1], BLACK[2])
    if side == "left":
        glTranslatef(-15, 0, 0)
    else:  # right
        glTranslatef(30, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 10, 70, 10, 10)
    

def arm(side):
    glColor3f(BLACK[0], BLACK[1], BLACK[2])
    if side == "left":
        glTranslatef(-20, 0, 0)
        glRotatef(-90, 1, 0, 0)
    else:
        glTranslatef(40, 0, 0)
        glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 6, 3, 50, 10, 10)
    if side == "left":
        glRotatef(90, 1, 0, 0)
    else:
        glRotatef(90, 1, 0, 0)
        

def weapon():
    glColor3f(RED[0], RED[1], RED[2])
    glTranslatef(0, 0, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 80, 10, 10)
    glRotatef(90, 1, 0, 0)
    

def drawPlayer():
    if game_over:
        drawDeadPlayer()
    else:
        glPushMatrix()
        
        glTranslatef(player_x, player_y, 120 + PLAYER_HEIGHT)
        glRotatef(player_rot, 0, 0, 1)
        glTranslatef(0, 0, 10)
        
        # Change player to black when game over
        if game_over:
            glColor3f(0, 0, 0)  # Black for game over
        else:
            glColor3f(BLONDE[0], BLONDE[1], BLONDE[2])
        head()
        
        glTranslatef(0, 0, -65)
        body()
        
        glPushMatrix()
        glTranslatef(0, 0, 20)
        arm("left")
        arm("right")
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 0, 20)
        weapon()
        glPopMatrix()
        
        glTranslatef(0, 0, -110)
        leg("left")
        leg("right")
        
        glPopMatrix()
    

def drawDeadPlayer():
    glPushMatrix()
    
    glTranslatef(player_x, player_y, 70 + PLAYER_HEIGHT)
    glRotatef(90, 1, 0, 0)
    glRotatef(player_rot, 0, 0, 1)
    glTranslatef(0, 0, 10)
    
    # Change player to black when game over
    glColor3f(0, 0, 0)  # Black for game over
    head()
    
    glTranslatef(0, 0, -40)
    body()
    
    glPushMatrix()
    glTranslatef(0, 0, 20)
    arm("left")
    arm("right")
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, 20)
    weapon()
    glPopMatrix()
    
    glTranslatef(0, 0, -110)
    leg("left")
    leg("right")
    
    glPopMatrix()
    

def enemyTop():
    glColor3f(GREY_LIGHT[0], GREY_LIGHT[1], GREY_LIGHT[2])
    glutSolidSphere(20, 20, 20)
    

def enemyBottom():
    glColor3f(GREY_DARK[0], GREY_DARK[1], GREY_DARK[2])
    glutSolidSphere(50, 20, 20)
    

def drawEnemies():
    if game_over:
        return
    
    for ex, ey, erot in enemy_list:
        drawHeroAttacker(ex, ey, 120 + PLAYER_HEIGHT, erot)
        # Health Bar for every enemy
        drawEnemyHealthbar(ex, ey, 120 + PLAYER_HEIGHT)

# Draw Func for player attacking     
def drawPlanetAttackers():
    if game_over:
        return
    
    for planet_attacker in planet_attacker_list:
        if len(planet_attacker) == 3:
            ex, ey, erot = planet_attacker
        else:
            ex, ey, erot, charging_state, charge_timer = planet_attacker
        
        drawPlanetAttacker(ex, ey, 120 + PLAYER_HEIGHT, erot)
        drawPlanetAttackerHealthbar(ex, ey, 120 + PLAYER_HEIGHT)
        

def pulse():
    global enemy_scale, pulse_dir
    
    enemy_scale += pulse_dir

    if enemy_scale > 1.2:
        enemy_scale = 1.2
        pulse_dir = -PULSE_SPEED
    elif enemy_scale < 0.8:
        enemy_scale = 0.8
        pulse_dir = PULSE_SPEED
    

def moveEnemies():
    global enemy_list
    
    limit = GRID_LEN - 30
    
    for i in range(len(enemy_list)):
        ex, ey, erot = enemy_list[i]
        
        dx = player_x - ex
        dy = player_y - ey
        
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 20: 
            wave_speed = ENEMY_SPEED * getEnemySpeedMultiplier()
            ex += (dx / dist) * wave_speed
            ey += (dy / dist) * wave_speed
        
        # Always face the player - FIXED CALCULATION
        angle_to_player = math.degrees(math.atan2(dy, dx)) - 90
        erot = angle_to_player # Enemy rotation
        
        # boundary checks
        if ex < -limit:
            ex = -limit
        if ex > limit:
            ex = limit
        if ey < -limit:
            ey = -limit
        if ey > limit:
            ey = limit
        
        enemy_list[i] = [ex, ey, erot]
        

def initEnemies():
    global enemy_list, enemy_last_shot_times
    
    if not enemy_list:
        half = GRID_LEN
        limit = GRID_LEN - 30
        
        enemy_last_shot_times = []  # Reset shot times
        
        for _ in range(ENEMY_COUNT):
            side = random.choice([0, 1, 2, 3])
            
            if side == 0:
                x = random.uniform(-half, half)
                y = -limit
                rot = 0
            elif side == 1:
                x = random.uniform(-half, half)
                y = limit
                rot = 180
            elif side == 2:
                x = -limit
                y = random.uniform(-half, half)
                rot = 90
            else:
                x = limit
                y = random.uniform(-half, half)
                rot = 270
            
            enemy_list.append([x, y, rot])
            enemy_last_shot_times.append(0)
            
# Boss Move Functions # From Enemy Ai
def moveBoss(boss_x, boss_y, boss_rot, player_x, player_y, boss_speed=1):
    limit = 570  # GRID_LEN - 30
    
    # Move toward player (like regular enemy for now)
    dx = player_x - boss_x
    dy = player_y - boss_y
    
    dist = math.sqrt(dx*dx + dy*dy)
    
    if dist > 20:  # Collision check
        boss_x += (dx / dist) * boss_speed
        boss_y += (dy / dist) * boss_speed
    
    # Always face the player
    angle_to_player = math.degrees(math.atan2(dy, dx)) - 90
    boss_rot = angle_to_player
    
    # boundary checks
    if boss_x < -limit:
        boss_x = -limit
    if boss_x > limit:
        boss_x = limit
    if boss_y < -limit:
        boss_y = -limit
    if boss_y > limit:
        boss_y = limit
    
    return boss_x, boss_y, boss_rot
    
def initBossInGame():
    global boss_x, boss_y, boss_rot, boss_active, boss_health
    
    # From Enemy.py
    boss_x, boss_y, boss_rot = initBoss()
    boss_active = True
    boss_health = BOSS_HEALTH
            

def newEnemy():
    half = GRID_LEN
    limit = GRID_LEN - 30
    
    side = random.choice([0, 1, 2, 3])
    
    if side == 0:
        x = random.uniform(-half, half)
        y = -limit
        rot = 0
    elif side == 1:
        x = random.uniform(-half, half)
        y = limit
        rot = 180
    elif side == 2:
        x = -limit
        y = random.uniform(-half, half)
        rot = 90
    else:
        x = limit
        y = random.uniform(-half, half)
        rot = 270
    
    return [x, y, rot]
    

def drawBullet(bx, by, bullet_type="normal"):
    if bullet_type == "mega":
        glColor3f(1, 0, 1)  # Purple for mega bullets
        bullet_size = 25
    else:
        glColor3f(1, 1, 0)  # Yellow for normal bullets
        bullet_size = 15
    
    glPushMatrix()
    glTranslatef(bx, by, 120 + PLAYER_HEIGHT - 40)
    glutSolidCube(bullet_size)
    glPopMatrix()
    

# Pickup Draw Method
def drawPickups():
    if game_over:
        return
    
    for px, py, ptype in pickups:
        if ptype == "health":
            drawHealthBox(px, py, 50)  # Health Pickup Box
        elif ptype == "ammo":
            drawAmmoBox(px + 40, py + 40, 50)    # Ammo Pickup Box
    

def shoot():
    global bullets_shot, player_ammo, last_mega_shot_time, player_has_mega_weapon, mega_weapon_ammo
    
    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    
    # Mega Weapon logic
    if player_has_mega_weapon and getCurrentWave() == 3:
        # Check fire delay for mega weapon
        if current_time - last_mega_shot_time < MEGA_FIRE_DELAY:
            print(f"Mega Weapon cooling down: {MEGA_FIRE_DELAY - (current_time - last_mega_shot_time):.1f}s")
            return
        
        if mega_weapon_ammo <= 0:
            print("Mega Weapon out of ammo!")
            return
        
        angle = math.radians(player_rot)
        start_x = player_x - 30 * math.sin(angle)
        start_y = player_y + 30 * math.cos(angle)
        
        dx = -math.sin(angle)
        dy = math.cos(angle)
        
        bullets.append([start_x, start_y, dx, dy, "mega"])  # Tag as mega bullet
        mega_weapon_ammo -= 1
        last_mega_shot_time = current_time
        bullets_shot += 1
        print(f"Mega Weapon fired! Ammo: {mega_weapon_ammo}/10")
        return
    
    # Regular weapon logic
    if player_ammo <= 0:
        print("Out of ammo!")
        return
    
    angle = math.radians(player_rot)
    start_x = player_x - 30 * math.sin(angle)
    start_y = player_y + 30 * math.cos(angle)
    
    dx = -math.sin(angle)
    dy = math.cos(angle)
    
    bullets.append([start_x, start_y, dx, dy, "normal"])  # Tag as normal bullet
    bullets_shot += 1
    player_ammo -= 1
    printStats()
    

def moveBullets():
    global bullets, missed_shots, game_over
    
    if game_over:
        bullets = []
        return
    
    limit = GRID_LEN + 100
    
    new_list = []
    
    for bullet_data in bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            bx, by, dx, dy = bullet_data
            bullet_type = "normal"
        
        bx += dx * BULLET_VEL
        by += dy * BULLET_VEL
        
        if -limit <= bx <= limit and -limit <= by <= limit:
            new_list.append([bx, by, dx, dy, bullet_type])
        else:
            missed_shots += 1
            printStats()
            
            if missed_shots >= MAX_MISS:
                game_over = True
                missed_shots = MAX_MISS
                bullets = []
    
    bullets = new_list
    

def showBullets():
    if game_over:
        return
    
    for bullet_data in bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            bx, by, dx, dy = bullet_data
            bullet_type = "normal"
        
        if bullet_type == "mega":
            glColor3f(1, 0, 1)  # Purple
            size = 25
        else:
            glColor3f(1, 1, 0)  # Yellow
            size = 15
        
        glPushMatrix()
        glTranslatef(bx, by, 120 + PLAYER_HEIGHT - 40)
        glutSolidCube(size)
        glPopMatrix()
    

# camera stuff
cam_fixed = None
look_fixed = None

def cameraFPS():
    global camera_pos, player_x, player_y, player_rot, cheat_vision, cheat_active, fps_mode, cam_fixed, look_fixed
    
    if fps_mode:
        # Calculate camera position for first-person view
        angle = math.radians(player_rot)
        
        # Position camera at player's eye level (slightly above and behind)
        camera_distance = 50  # Distance behind player
        eye_height = 80  # Eye level height
        
        # Calculate camera position (behind and above player)
        cam_x = player_x - camera_distance * math.sin(angle)
        cam_y = player_y + camera_distance * math.cos(angle)
        cam_z = 120 + PLAYER_HEIGHT + eye_height  # Eye level
        
        # Calculate look-at point (where player is aiming)
        look_distance = 200  # How far ahead to look
        look_x = player_x - look_distance * math.sin(angle)
        look_y = player_y + look_distance * math.cos(angle)
        look_z = cam_z - 20  # Look slightly downward
        
        gluLookAt(cam_x, cam_y, cam_z, 
                  look_x, look_y, look_z, 
                  0, 0, 1)
        
    elif fps_mode and cheat_active and not cheat_vision:
        # Original cheat vision logic
        if cam_fixed is None:
            angle = math.radians(player_rot)
            off_x = -30 * math.sin(angle)
            off_y = 30 * math.cos(angle)
            cam_fixed = (
                player_x + off_x,
                player_y + off_y,
                115 + PLAYER_HEIGHT
            )
            look_fixed = (
                player_x - 200 * math.sin(angle),
                player_y + 200 * math.cos(angle),
                0
            )
        
        cx, cy, cz = cam_fixed
        lx, ly, lz = look_fixed
        gluLookAt(cx, cy, cz, lx, ly, lz, 0, 0, 1)
    else:
        # Third-person view (original code)
        cam_fixed = None
        look_fixed = None
        angle = math.radians(player_rot)
        off_x = -30 * math.sin(angle)
        off_y = 30 * math.cos(angle)
        cx = player_x + off_x
        cy = player_y + off_y
        cz = 115 + PLAYER_HEIGHT
        
        lx = player_x - 200 * math.sin(angle)
        ly = player_y + 200 * math.cos(angle)
        
        gluLookAt(cx, cy, cz, lx, ly, 0, 0, 0, 1)


def drawUI():
    global life, score, missed_shots, game_over, planet_health
    global current_wave, player_has_mega_weapon, player_has_mega_shield, mega_shield_health
    global is_paused, fps_mode
    global game_win, boss_active
    
    if game_win:
        draw_text(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 + 100, "VICTORY ACHIEVED!", GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 50, "BOSS DEFEATED!", GLUT_BITMAP_HELVETICA_18)
        draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, f"FINAL SCORE: {score}")
        time_bonus = get_time_remaining() * 10
        draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 30, f"TIME BONUS: +{time_bonus}")
        draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 60, f"TOTAL: {score + time_bonus}")
        draw_text(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 120, "Press R to play again")
        return
    
    if not game_over:
        if is_paused:
            draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 50, "GAME PAUSED - Press P to resume", GLUT_BITMAP_HELVETICA_18)
        
        if player_has_mega_shield:
            draw_text(10, WINDOW_HEIGHT - 30, f"Mega Shield: {mega_shield_health}/1000")
        else:
            draw_text(10, WINDOW_HEIGHT - 30, f"Life: {life}")
        
        draw_text(10, WINDOW_HEIGHT - 60, f"Score: {score}")
        draw_text(10, WINDOW_HEIGHT - 90, f"Missed: {missed_shots}/{MAX_MISS}")
        
        if player_has_mega_weapon:
            draw_text(10, WINDOW_HEIGHT - 120, f"Mega Ammo: {mega_weapon_ammo}/10")
        else:
            draw_text(10, WINDOW_HEIGHT - 120, f"Ammo: {player_ammo}")
        
        draw_text(10, WINDOW_HEIGHT - 150, f"Planet Health: {planet_health}/100")
        
        time_left = get_time_remaining()
        minutes = time_left // 60
        seconds = time_left % 60
        
        if cheat_active:
            draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 30, f"Time: {minutes:02d}:{seconds:02d} (CHEAT)")
        else:
            draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 30, f"Time: {minutes:02d}:{seconds:02d}")
        
        draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 60, f"Wave: {current_wave}")
        
        if fps_mode:
            draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 120, "Camera: First Person")
        else:
            draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 120, "Camera: Third Person")
    
        if boss_active:
            draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 90, f"BOSS: {boss_health}")
    else:
        draw_text(10, WINDOW_HEIGHT - 30, f"GAME OVER! Score: {score}")
        if planet_health <= 0:
            draw_text(10, WINDOW_HEIGHT - 60, "Planet Destroyed!")
        elif boss_active and boss_health <= 0:
            draw_text(10, WINDOW_HEIGHT - 60, "BOSS DEFEATED!")
        elif get_time_remaining() <= 0 and not cheat_active:
            draw_text(10, WINDOW_HEIGHT - 60, "TIME'S UP!")
        draw_text(10, WINDOW_HEIGHT - 90, "Press R to restart")
        

def resetAll():
    global life, score, missed_shots, game_over
    global player_x, player_y, player_rot
    global bullets, enemy_list, pickups, player_ammo
    global cheat_active, cheat_vision, fps_mode
    global planet_attacker_list, planet_health
    global current_wave, player_has_mega_weapon, player_has_mega_shield, mega_weapon_ammo
    global boss_x, boss_y, boss_rot, boss_active, boss_health
    global last_mega_shot_time, mega_shield_health
    global is_paused, camera_distance, camera_pos
    global game_win
    global enemy_bullets, boss_bullets
    global qte_active, qte_triggered, qte_result
    
    stop_timer()  
    reset_timer()  
    start_timer()
    
    life = 100
    score = 0
    missed_shots = 0
    game_over = False
    game_win = False
    
    player_x = 0
    player_y = 0
    player_rot = 0
    
    bullets = []
    enemy_bullets = []  
    boss_bullets = []
    enemy_list = []
    planet_attacker_list = initPlanetAttackers(PLANET_ATTACKER_COUNT)
    pickups = []  
    player_ammo = 10
    planet_health = 1000
    
    cheat_active = False
    cheat_vision = False
    fps_mode = False
    
    is_paused = False
    camera_mode = "third_person"
    camera_distance = 500
    camera_pos = (0, camera_distance, camera_distance)
    
    resetWaveSystem()
    resetMegaPowerUps()
    current_wave = 1
    player_has_mega_weapon = False
    player_has_mega_shield = False
    mega_weapon_ammo = 10
    mega_shield_health = 0
    last_mega_shot_time = 0
    
    boss_x = 0
    boss_y = 0
    boss_rot = 0
    boss_active = False
    boss_health = BOSS_HEALTH
    
    # PROPERLY RESET QTE STATE
    qte_active = False
    qte_triggered = False
    qte_result = None
    resetQTE()
    game_win = False
    
    resetEnemyShooting()
    enemy_last_shot_times = []
    last_boss_shot_time = 0
    
    disable_timer_cheat() 
    
    printStats()
    

def cheat():
    global cheat_active, life, player_ammo, planet_health, mega_shield_health
    global mega_weapon_ammo, player_has_mega_weapon, player_has_mega_shield
    global qte_triggered, qte_active, game_win, game_over
    
    if not cheat_active:
        if player_has_mega_shield:
            if mega_shield_health > 1000:
                mega_shield_health = 1000
        else:
            if life > 100:
                life = 100
        
        if planet_health > 1000:
            planet_health = 1000
        
        if player_has_mega_weapon:
            if mega_weapon_ammo > 10:
                mega_weapon_ammo = 10
        else:
            if player_ammo > 10:
                player_ammo = 10
        
        qte_triggered = False
        
        disable_timer_cheat()
        return
    
    if player_has_mega_shield:
        mega_shield_health = 999999
    else:
        life = 999999
    
    if not player_has_mega_weapon:
        player_ammo = 999999
    else:
        mega_weapon_ammo = 10
    
    planet_health = 999999
    
    enable_timer_cheat()
    
def keyHandler(key, x, y):
    global player_x, player_y, player_rot
    global cheat_active, cheat_vision, cam_fixed, look_fixed
    global game_over, qte_active, game_win, score, boss_active
    global is_paused, fps_mode, wave_paused
    
    if key == b'r' or key == b'R':
        resetAll()
        return
    
    if game_win or game_over:
        return
    
    if key == b'p' or key == b'P':
        is_paused = not is_paused
        if is_paused:
            pause_timer()
        else:
            resume_timer()
        return
    
    if key == b'f' or key == b'F':
        fps_mode = not fps_mode
        cam_fixed = None
        look_fixed = None
        return
    
    if qte_active and isQTEActive():
        if key.lower() in [b'w', b'a', b's', b'd']:
            key_char = key.decode().upper()
            
            success = handleQTEKey(key_char)
            
            if success:
                game_win = True
                boss_active = False
                score += 500
                
                if wave_paused:
                    wave_paused = False
                resume_timer()
            else:
                game_over = True
                
                if wave_paused:
                    wave_paused = False
                resume_timer()
            
            return
    
    if key == b'c':
        cheat_active = not cheat_active
        cam_fixed = None
        look_fixed = None
        cheat()
        return
    
    if key == b'v':
        cheat_vision = not cheat_vision
        cam_fixed = None
        look_fixed = None
    
    if is_paused:
        return
    
    angle = math.radians(player_rot)
    new_x = player_x
    new_y = player_y
    
    speed_multiplier = CHEAT_SPEED_MULTIPLIER if cheat_active else 1.0
    effective_speed = PLAYER_SPEED * speed_multiplier
    
    if key == b'w':
        new_x -= effective_speed * math.sin(angle)
        new_y += effective_speed * math.cos(angle)
    
    if key == b's':
        new_x += effective_speed * math.sin(angle)
        new_y -= effective_speed * math.cos(angle)
    
    if key == b'a':
        player_rot += PLAYER_SPEED
    if key == b'd':
        player_rot -= PLAYER_SPEED
    
    limit = GRID_LEN - 30
    if -limit <= new_x <= limit:
        player_x = new_x
    if -limit <= new_y <= limit:
        player_y = new_y
        

def mouseHandler(button, state, x, y):
    global fps_mode, cam_fixed, look_fixed
    
    # Don't process mouse if game is paused
    if is_paused:
        return
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        shoot()
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fps_mode = not fps_mode
        cam_fixed = None
        look_fixed = None
        

def arrowKeys(key, x, y):
    global camera_pos, CAM_SPEED, camera_distance
    
    # Don't process arrow keys if game is paused
    if is_paused:
        return
    
    xc, yc, zc = camera_pos
    
    # Arrow Up/Down for camera distance
    if key == GLUT_KEY_UP:
        camera_distance -= CAMERA_DISTANCE_SPEED
        if camera_distance < 100:  # Minimum distance
            camera_distance = 100
        # Update camera position with new distance
        camera_pos = (xc, camera_distance, camera_distance)
        return
    
    if key == GLUT_KEY_DOWN:
        camera_distance += CAMERA_DISTANCE_SPEED
        if camera_distance > 1000:  # Maximum distance
            camera_distance = 1000
        # Update camera position with new distance
        camera_pos = (xc, camera_distance, camera_distance)
        return
    
    # Original left/right movement
    if key == GLUT_KEY_LEFT:
        xc += CAM_SPEED
    if key == GLUT_KEY_RIGHT:
        xc -= CAM_SPEED
    
    camera_pos = (xc, yc, zc)
    

def printStats():
    print("\n" + "="*50)
    print("GAME UPDATE:")
    print(f"Life: {life}")
    print(f"Shots fired: {bullets_shot}")
    print(f"Missed: {missed_shots}")
    print(f"Score: {score}")
    print("="*50 + "\n")
    

def camSetup():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # Adjust field of view based on camera mode
    if fps_mode:
        # Wider FOV for first-person view
        gluPerspective(90, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 1500)
    else:
        gluPerspective(fovY, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 1500)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Camera mode selection
    if fps_mode:
        cameraFPS()
    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)
        

def update():
    global planet_attacker_list, bullets, enemy_list, score, boss_health, boss_active, pickups, game_over, life, player_ammo, planet_health
    global current_wave, player_has_mega_weapon, player_has_mega_shield, mega_weapon_ammo, mega_shield_health
    global qte_active, qte_triggered
    global enemy_last_shot_times, last_boss_shot_time
    global is_paused, game_win
    global enemy_bullets, boss_bullets
    
    if is_paused or game_win or game_over:
        glutPostRedisplay()
        return
    
    if game_over:
        glutPostRedisplay()
        return
    
    if isQTEActive():
        updateQTE()
        qte_result = getQTEResult()
        if qte_result == "win":
            boss_active = False
            boss_health = 0
            game_win = True
            time_bonus = get_time_remaining() * 10
            score += 500 + time_bonus
            stop_timer()
            bullets = []
            enemy_bullets = []
            boss_bullets = []
            glutPostRedisplay()
            return
        elif qte_result == "lose":
            game_over = True
            glutPostRedisplay()
            return
        else:
            glutPostRedisplay()
            return
    
    update_timer()
    
    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    time_remaining = get_time_remaining()
    
    if not cheat_active and time_remaining <= 0:
        game_over = True
        stop_timer()
        glutPostRedisplay()
        return
    
    if not cheat_active and is_timer_expired():
        game_over = True
        stop_timer()
        glutPostRedisplay()
        return
    
    if boss_active and boss_health <= 0 and not qte_triggered:
        if cheat_active:
            boss_active = False
            score += 500
        else:
            qte_triggered = True
            startQTE()
            qte_active = True
        glutPostRedisplay()
        return
    
    updateWaveSystem(time_remaining)
    current_wave = getCurrentWave()
    
    if int(current_time) % 5 == 0:  
        print(f"Timer: {time_remaining} seconds remaining, Wave: {current_wave}")
    
    if current_wave == 3 and not mega_weapon_spawned:
        spawnMegaPowerUps()
    
    life, player_ammo = handleMegaPickups(player_x, player_y, life, player_ammo, time_remaining)
    
    player_has_mega_weapon = mega_weapon_spawned and player_has_mega_weapon
    player_has_mega_shield = mega_shield_spawned and player_has_mega_shield
    
    if player_has_mega_weapon:
        regenerateMegaAmmo(current_time)
    
    if not enemy_list:
        initEnemies()
    
    moveEnemies()
    updateBossPosition()
    moveBullets()
    
    enemy_bullets = getEnemyBullets()
    planet_health = enemyBulletPlanetHit(enemy_bullets, planet_health)
    
    old_health = planet_health
    
    if planet_health <= 0 and not cheat_active:
        game_over = True
        planet_health = 0
        glutPostRedisplay()
        return
    elif planet_health <= 0 and cheat_active:
        planet_health = 1
    
    bullets, enemy_list, planet_attacker_list, boss_health, boss_active, pickups, score, game_over = handleHits(
        bullets, enemy_list, planet_attacker_list, boss_x, boss_y, boss_health, boss_active, 
        pickups, score, game_over, current_wave, player_has_mega_weapon
    )
    
    if shouldSpawnPickups():
        pickups, life, player_ammo = handlePickups(pickups, player_x, player_y, life, player_ammo)
    else:
        pickups = []
    
    planet_attacker_list, planet_health = planetHit(planet_attacker_list, planet_health, game_over)
    
    if planet_health != old_health:
        print(f"Planet health changed: {old_health} -> {planet_health}")
    
    if not cheat_active:
        enemy_list, planet_attacker_list, life, game_over, bullets, damage_taken = playerHit(
            enemy_list, planet_attacker_list, boss_x, boss_y, boss_active, player_x, player_y, 
            life, game_over, bullets, player_has_mega_shield, mega_shield_health
        )
    else:
        damage_taken = 0
        temp_enemy_list, temp_planet_attacker_list, temp_life, temp_game_over, temp_bullets, temp_damage_taken = playerHit(
            enemy_list, planet_attacker_list, boss_x, boss_y, boss_active, player_x, player_y, 
            life, game_over, bullets, player_has_mega_shield, mega_shield_health
        )
        enemy_list = temp_enemy_list
        planet_attacker_list = temp_planet_attacker_list
        bullets = temp_bullets
    
    if player_has_mega_shield and damage_taken > 0 and not cheat_active:
        takeMegaShieldDamage(damage_taken)
    
    if life < old_health and not cheat_active:
        wave_damage = getEnemyDamageMultiplier()
    
    pulse()
    cheat()
    planet_attacker_list = movePlanetAttackers(planet_attacker_list, 0, -1600)
    
    if current_wave == 3 and not boss_active and not qte_triggered:
        initBossInGame()
    
    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    
    for i in range(len(enemy_list)):
        ex, ey, erot = enemy_list[i]
        last_shot = enemy_last_shot_times[i] if i < len(enemy_last_shot_times) else 0
        
        enemy_bullets, new_last_shot = enemyShoot(
            ex, ey, erot, player_x, player_y, last_shot, current_time
        )
        
        if i < len(enemy_last_shot_times):
            enemy_last_shot_times[i] = new_last_shot
    
    if boss_active:
        boss_bullets, last_boss_shot_time = bossShoot(
            boss_x, boss_y, boss_rot, player_x, player_y, last_boss_shot_time, current_time
        )
    
    moveEnemyBullets()
    moveBossBullets()
    
    enemy_bullets = getEnemyBullets()
    boss_bullets = getBossBullets()
    
    if not cheat_active:
        for bullet_data in enemy_bullets:
            if len(bullet_data) == 5:
                bx, by, dx, dy, bullet_type = bullet_data
            else:
                continue
            
            dx_player = bx - player_x
            dy_player = by - player_y
            player_dist = math.sqrt(dx_player*dx_player + dy_player*dy_player)
            
            if player_dist < 25:
                if player_has_mega_shield:
                    damage = 1 * getEnemyDamageMultiplier()
                    takeMegaShieldDamage(damage)
                else:
                    life -= 0.05
                    if life <= 0:
                        game_over = True
                        life = 0
        
        for bullet_data in boss_bullets:
            if len(bullet_data) == 5:
                bx, by, dx, dy, bullet_type = bullet_data
            else:
                continue
            
            dx_player = bx - player_x
            dy_player = by - player_y
            
            player_dist = math.sqrt(dx_player*dx_player + dy_player*dy_player)
            
            if player_dist < 25:
                if player_has_mega_shield:
                    damage = 200  
                    takeMegaShieldDamage(damage)
                else:
                    life = 0
                    game_over = True
    
    if cheat_active and is_timer_expired():
        boss_active = False
        boss_health = 0
        game_win = True  
        time_bonus = get_time_remaining() * 10
        score += 1000 + time_bonus
        stop_timer()
        bullets = []
        enemy_bullets = []
        boss_bullets = []
        glutPostRedisplay()
        return
    
    if not cheat_active and is_timer_expired():
        game_over = True
        stop_timer()
        glutPostRedisplay()
        return
    
    glutPostRedisplay()

def display():
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    if game_win:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glColor3f(0, 1, 0)
        victory_text = "VICTORY!"
        text_x = WINDOW_WIDTH // 2 - 100
        text_y = WINDOW_HEIGHT // 2 + 100
        
        glRasterPos2f(text_x, text_y)
        for ch in victory_text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch))
        
        glColor3f(1, 1, 1)
        if cheat_active:
            success_text = "Cheat Mode: Boss Defeated!"
        else:
            success_text = "QTE Success! Boss Defeated!"
        
        success_x = WINDOW_WIDTH // 2 - 150
        success_y = WINDOW_HEIGHT // 2 + 50
        
        glRasterPos2f(success_x, success_y)
        for ch in success_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        score_text = f"Final Score: {score}"
        score_x = WINDOW_WIDTH // 2 - 80
        score_y = WINDOW_HEIGHT // 2
        
        glRasterPos2f(score_x, score_y)
        for ch in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glColor3f(1, 1, 0)
        restart_text = "Press R to Restart"
        restart_x = WINDOW_WIDTH // 2 - 70
        restart_y = WINDOW_HEIGHT // 2 - 100
        
        glRasterPos2f(restart_x, restart_y)
        for ch in restart_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glutSwapBuffers()
        return
    
    if game_over:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        qte_failed = qte_result == "lose"
        
        glColor3f(1, 0, 0)
        game_over_text = "GAME OVER"
        text_x = WINDOW_WIDTH // 2 - 100
        text_y = WINDOW_HEIGHT // 2 + 100
        
        glRasterPos2f(text_x, text_y)
        for ch in game_over_text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch))
        
        glColor3f(1, 1, 1)
        if qte_failed:
            reason_text = "QTE Failed! Boss defeated you!"
        elif planet_health <= 0:
            reason_text = "Planet Destroyed!"
        elif life <= 0 or (player_has_mega_shield and mega_shield_health <= 0):
            reason_text = "Spaceship Destroyed!"
        elif is_timer_expired() and not cheat_active:
            reason_text = "Time's Up!"
        else:
            reason_text = "Mission Failed!"
        
        reason_x = WINDOW_WIDTH // 2 - 150
        reason_y = WINDOW_HEIGHT // 2 + 50
        
        glRasterPos2f(reason_x, reason_y)
        for ch in reason_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        score_text = f"Final Score: {score}"
        score_x = WINDOW_WIDTH // 2 - 80
        score_y = WINDOW_HEIGHT // 2
        
        glRasterPos2f(score_x, score_y)
        for ch in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glColor3f(1, 1, 0)
        restart_text = "Press R to Restart"
        restart_x = WINDOW_WIDTH // 2 - 70
        restart_y = WINDOW_HEIGHT // 2 - 50
        
        glRasterPos2f(restart_x, restart_y)
        for ch in restart_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glutSwapBuffers()
        return

    if qte_active and not game_win and not game_over:
        camSetup()
        
        glPointSize(20)
        glBegin(GL_POINTS)
        glVertex3f(-GRID_LEN, GRID_LEN, 0)
        glEnd()

        drawCheckerboard()
        drawWalls()
        
        drawPlanet(1000, 0, -1600, 150)
        drawHeroUfo(player_x, player_y, 120 + PLAYER_HEIGHT, player_rot, cheat_active)
        setGameOverState(game_over)
        setCurrentWave(current_wave)
        drawHealthbar(player_x, player_y, PLAYER_HEIGHT, life, game_over, HEALTH_ORANGE, player_has_mega_shield, mega_shield_health)
        
        if not game_over or planet_health <= 0:
            drawPlanetHealthBar(planet_health, planet_max_health, HEALTH_ORANGE)
        
        drawEnemies()
        
        if boss_active and not game_win:
            drawBossEnemy(boss_x, boss_y, 120 + PLAYER_HEIGHT, boss_rot)
            drawBossHealthBar(boss_health, BOSS_HEALTH, "SKY CAPTAIN")
        
        showBullets()
        drawPickups()
        drawPlanetAttackers()
        
        draw_timer()
        drawUI()
        
        drawQTE()
        
        glutSwapBuffers()
        return

    camSetup()

    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LEN, GRID_LEN, 0)
    glEnd()

    drawCheckerboard()
    drawWalls()
    
    drawPlanet(1000, 0, -1600, 150)
    drawHeroUfo(player_x, player_y, 120 + PLAYER_HEIGHT, player_rot, cheat_active)
    setGameOverState(game_over)
    setCurrentWave(current_wave)
    drawHealthbar(player_x, player_y, PLAYER_HEIGHT, life, game_over, HEALTH_ORANGE, player_has_mega_shield, mega_shield_health)
    if not game_over or planet_health <= 0:
        drawPlanetHealthBar(planet_health, planet_max_health, HEALTH_ORANGE)
    
    drawEnemies()
    
    if boss_active and not game_win:
        drawBossEnemy(boss_x, boss_y, 120 + PLAYER_HEIGHT, boss_rot)
        drawBossHealthBar(boss_health, BOSS_HEALTH, "SKY CAPTAIN")
    
    showBullets()
    drawPickups()
    drawPlanetAttackers()
    
    draw_timer()
    
    drawQTE()
    
    drawUI()
    
    drawMegaWeaponPickup()
    drawMegaShieldPickup()
    
    enemy_bullets = getEnemyBullets()
    for bullet_data in enemy_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            continue
        
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(bx, by, 120 + PLAYER_HEIGHT - 40)
        glutSolidCube(10)
        glPopMatrix()
    
    boss_bullets = getBossBullets()
    for bullet_data in boss_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            continue
        
        glColor3f(1, 0.5, 0)
        glPushMatrix()
        glTranslatef(bx, by, 120 + PLAYER_HEIGHT - 40)
        glutSolidCube(20)
        glPopMatrix()

    glutSwapBuffers()
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Check for win/loss states FIRST
    if game_win:
        # WIN SCREEN
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Draw victory text
        glColor3f(0, 1, 0)
        victory_text = "VICTORY!"
        text_x = WINDOW_WIDTH // 2 - 100
        text_y = WINDOW_HEIGHT // 2 + 100
        
        glRasterPos2f(text_x, text_y)
        for ch in victory_text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch))
        
        # Draw QTE success message or cheat mode message
        glColor3f(1, 1, 1)
        if cheat_active:
            success_text = "Cheat Mode: Boss Defeated!"
        else:
            success_text = "QTE Success! Boss Defeated!"
        
        success_x = WINDOW_WIDTH // 2 - 150
        success_y = WINDOW_HEIGHT // 2 + 50
        
        glRasterPos2f(success_x, success_y)
        for ch in success_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        # Draw score
        score_text = f"Final Score: {score}"
        score_x = WINDOW_WIDTH // 2 - 80
        score_y = WINDOW_HEIGHT // 2
        
        glRasterPos2f(score_x, score_y)
        for ch in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        # Draw restart
        glColor3f(1, 1, 0)
        restart_text = "Press R to Restart"
        restart_x = WINDOW_WIDTH // 2 - 70
        restart_y = WINDOW_HEIGHT // 2 - 100
        
        glRasterPos2f(restart_x, restart_y)
        for ch in restart_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glutSwapBuffers()
        return
    
    if game_over:
        # GAME OVER SCREEN
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Check if QTE was the cause of game over
        qte_failed = qte_result == "lose"
        
        # Draw game over text
        glColor3f(1, 0, 0)
        game_over_text = "GAME OVER"
        text_x = WINDOW_WIDTH // 2 - 100
        text_y = WINDOW_HEIGHT // 2 + 100
        
        glRasterPos2f(text_x, text_y)
        for ch in game_over_text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch))
        
        # Draw reason for loss
        glColor3f(1, 1, 1)
        if qte_failed:
            reason_text = "QTE Failed! Boss defeated you!"
        elif planet_health <= 0:
            reason_text = "Planet Destroyed!"
        elif life <= 0 or (player_has_mega_shield and mega_shield_health <= 0):
            reason_text = "Spaceship Destroyed!"
        elif is_timer_expired() and not cheat_active:
            reason_text = "Time's Up!"
        else:
            reason_text = "Mission Failed!"
        
        reason_x = WINDOW_WIDTH // 2 - 150
        reason_y = WINDOW_HEIGHT // 2 + 50
        
        glRasterPos2f(reason_x, reason_y)
        for ch in reason_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        # Draw score
        score_text = f"Final Score: {score}"
        score_x = WINDOW_WIDTH // 2 - 80
        score_y = WINDOW_HEIGHT // 2
        
        glRasterPos2f(score_x, score_y)
        for ch in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        # Draw restart instruction
        glColor3f(1, 1, 0)
        restart_text = "Press R to Restart"
        restart_x = WINDOW_WIDTH // 2 - 70
        restart_y = WINDOW_HEIGHT // 2 - 50
        
        glRasterPos2f(restart_x, restart_y)
        for ch in restart_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glutSwapBuffers()
        return
    
    camSetup()

    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LEN, GRID_LEN, 0)
    glEnd()

    drawCheckerboard()
    drawWalls()
    
    drawPlanet(1000, 0, -1600, 150)
    drawHeroUfo(player_x, player_y, 120 + PLAYER_HEIGHT, player_rot, cheat_active)
    setGameOverState(game_over)
    setCurrentWave(current_wave)
    drawHealthbar(player_x, player_y, PLAYER_HEIGHT, life, game_over, HEALTH_ORANGE, player_has_mega_shield, mega_shield_health)
    if not game_over or planet_health <= 0:
        drawPlanetHealthBar(planet_health, planet_max_health, HEALTH_ORANGE)
    
    drawEnemies()
    
    if boss_active and not game_win:
        drawBossEnemy(boss_x, boss_y, 120 + PLAYER_HEIGHT, boss_rot)
        drawBossHealthBar(boss_health, BOSS_HEALTH, "SKY CAPTAIN")
    
    showBullets()
    drawPickups()
    drawPlanetAttackers()
    
    draw_timer()
    
    drawQTE()
    
    drawUI()
    
    drawMegaWeaponPickup()
    drawMegaShieldPickup()
    
    # Draw enemy bullets
    enemy_bullets = getEnemyBullets()
    for bullet_data in enemy_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            continue
        
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(bx, by, 120 + PLAYER_HEIGHT - 40)
        glutSolidCube(10)
        glPopMatrix()
    
    # Draw boss bullets  
    boss_bullets = getBossBullets()
    for bullet_data in boss_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            continue
        
        glColor3f(1, 0.5, 0)
        glPushMatrix()
        glTranslatef(bx, by, 120 + PLAYER_HEIGHT - 40)
        glutSolidCube(20)
        glPopMatrix()

    glutSwapBuffers()
    if game_win:
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glColor3f(0, 1, 0)
        victory_text = "VICTORY!"
        text_x = WINDOW_WIDTH // 2 - 100
        text_y = WINDOW_HEIGHT // 2 + 100
        
        glRasterPos2f(text_x, text_y)
        for ch in victory_text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch))
        
        glColor3f(1, 1, 1)
        success_text = "QTE Success! Boss Defeated!"
        success_x = WINDOW_WIDTH // 2 - 150
        success_y = WINDOW_HEIGHT // 2 + 50
        
        glRasterPos2f(success_x, success_y)
        for ch in success_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        score_text = f"Final Score: {score}"
        score_x = WINDOW_WIDTH // 2 - 80
        score_y = WINDOW_HEIGHT // 2
        
        glRasterPos2f(score_x, score_y)
        for ch in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glColor3f(1, 1, 0)
        restart_text = "Press R to Restart"
        restart_x = WINDOW_WIDTH // 2 - 70
        restart_y = WINDOW_HEIGHT // 2 - 100
        
        glRasterPos2f(restart_x, restart_y)
        for ch in restart_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glutSwapBuffers()
        return
    
    if game_over:
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        qte_failed = qte_active and qte_result == "lose"
        
        glColor3f(1, 0, 0)
        game_over_text = "GAME OVER"
        text_x = WINDOW_WIDTH // 2 - 100
        text_y = WINDOW_HEIGHT // 2 + 100
        
        glRasterPos2f(text_x, text_y)
        for ch in game_over_text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch))
        
        glColor3f(1, 1, 1)
        if qte_failed:
            reason_text = "QTE Failed! Boss defeated you!"
        elif planet_health <= 0:
            reason_text = "Planet Destroyed!"
        elif life <= 0 or (player_has_mega_shield and mega_shield_health <= 0):
            reason_text = "Spaceship Destroyed!"
        elif is_timer_expired() and not cheat_active:
            reason_text = "Time's Up!"
        else:
            reason_text = "Mission Failed!"
        
        reason_x = WINDOW_WIDTH // 2 - 150
        reason_y = WINDOW_HEIGHT // 2 + 50
        
        glRasterPos2f(reason_x, reason_y)
        for ch in reason_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        score_text = f"Final Score: {score}"
        score_x = WINDOW_WIDTH // 2 - 80
        score_y = WINDOW_HEIGHT // 2
        
        glRasterPos2f(score_x, score_y)
        for ch in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glColor3f(1, 1, 0)
        restart_text = "Press R to Restart"
        restart_x = WINDOW_WIDTH // 2 - 70
        restart_y = WINDOW_HEIGHT // 2 - 50
        
        glRasterPos2f(restart_x, restart_y)
        for ch in restart_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glutSwapBuffers()
        return
    
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    camSetup()

    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LEN, GRID_LEN, 0)
    glEnd()

    drawCheckerboard()
    drawWalls()
    
    drawPlanet(1000, 0, -1600, 150)
    drawHeroUfo(player_x, player_y, 120 + PLAYER_HEIGHT, player_rot, cheat_active)
    setGameOverState(game_over)
    setCurrentWave(current_wave)
    drawHealthbar(player_x, player_y, PLAYER_HEIGHT, life, game_over, HEALTH_ORANGE, player_has_mega_shield, mega_shield_health)
    if not game_over or planet_health <= 0:
        drawPlanetHealthBar(planet_health, planet_max_health, HEALTH_ORANGE)
    
    drawEnemies()
    
    if boss_active and not game_win:
        drawBossEnemy(boss_x, boss_y, 120 + PLAYER_HEIGHT, boss_rot)
        drawBossHealthBar(boss_health, BOSS_HEALTH, "SKY CAPTAIN")
    
    showBullets()
    drawPickups()
    drawPlanetAttackers()
    
    draw_timer()
    
    drawQTE()
    
    drawUI()
    
    drawMegaWeaponPickup()
    drawMegaShieldPickup()
    
    enemy_bullets = getEnemyBullets()
    for bullet_data in enemy_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            continue
        
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(bx, by, 120 + PLAYER_HEIGHT - 40)
        glutSolidCube(10)
        glPopMatrix()
    
    boss_bullets = getBossBullets()
    for bullet_data in boss_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            continue
        
        glColor3f(1, 0.5, 0)
        glPushMatrix()
        glTranslatef(bx, by, 120 + PLAYER_HEIGHT - 40)
        glutSolidCube(20)
        glPopMatrix()

    glutSwapBuffers()
    # Check win/loss states FIRST
    if game_win:
        # WIN SCREEN - Display win message
        glClearColor(0, 0, 0, 1)  # Black background
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Draw victory text
        glColor3f(0, 1, 0)
        victory_text = "VICTORY!"
        text_x = WINDOW_WIDTH // 2 - 100
        text_y = WINDOW_HEIGHT // 2 + 100
        
        glRasterPos2f(text_x, text_y)
        for ch in victory_text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch))
        
        # Draw QTE success message
        glColor3f(1, 1, 1)  # White text
        success_text = "QTE Success! Boss Defeated!"
        success_x = WINDOW_WIDTH // 2 - 150
        success_y = WINDOW_HEIGHT // 2 + 50
        
        glRasterPos2f(success_x, success_y)
        for ch in success_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        # Draw score
        score_text = f"Final Score: {score}"
        score_x = WINDOW_WIDTH // 2 - 80
        score_y = WINDOW_HEIGHT // 2
        
        glRasterPos2f(score_x, score_y)
        for ch in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        # Draw restart instruction
        glColor3f(1, 1, 0)  # Yellow text
        restart_text = "Press R to Restart"
        restart_x = WINDOW_WIDTH // 2 - 70
        restart_y = WINDOW_HEIGHT // 2 - 100
        
        glRasterPos2f(restart_x, restart_y)
        for ch in restart_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glutSwapBuffers()
        return
    
    if game_over:
        # GAME OVER SCREEN
        glClearColor(0, 0, 0, 1)  # Black background
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set up orthographic projection for 2D text
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Check if QTE was the cause of game over
        qte_failed = qte_active and qte_result == "lose"
        
        # Draw game over text
        glColor3f(1, 0, 0)  # Red for game over
        game_over_text = "GAME OVER"
        text_x = WINDOW_WIDTH // 2 - 100
        text_y = WINDOW_HEIGHT // 2 + 100
        
        glRasterPos2f(text_x, text_y)
        for ch in game_over_text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch))
        
        # Draw reason for loss
        glColor3f(1, 1, 1)  # White text
        if qte_failed:
            reason_text = "QTE Failed! Boss defeated you!"
        elif planet_health <= 0:
            reason_text = "Planet Destroyed!"
        elif life <= 0 or (player_has_mega_shield and mega_shield_health <= 0):
            reason_text = "Spaceship Destroyed!"
        elif is_timer_expired() and not cheat_active:
            reason_text = "Time's Up!"
        else:
            reason_text = "Mission Failed!"
        
        reason_x = WINDOW_WIDTH // 2 - 150
        reason_y = WINDOW_HEIGHT // 2 + 50
        
        glRasterPos2f(reason_x, reason_y)
        for ch in reason_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        # Draw score
        score_text = f"Final Score: {score}"
        score_x = WINDOW_WIDTH // 2 - 80
        score_y = WINDOW_HEIGHT // 2
        
        glRasterPos2f(score_x, score_y)
        for ch in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        # Draw restart instruction
        glColor3f(1, 1, 0)  # Yellow text
        restart_text = "Press R to Restart"
        restart_x = WINDOW_WIDTH // 2 - 70
        restart_y = WINDOW_HEIGHT // 2 - 50
        
        glRasterPos2f(restart_x, restart_y)
        for ch in restart_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glutSwapBuffers()
        return
    
    if game_over or game_win:
        # Black screen when game over/won
        glClearColor(0, 0, 0, 1)  # Black background
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Show game over/win screen
        drawUI() 
        glutSwapBuffers()
        return
    
    # Original display code for normal game
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    camSetup()

    # test point
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LEN, GRID_LEN, 0)
    glEnd()

    drawCheckerboard()
    drawWalls()
    
    
    drawPlanet(1000, 0, -1600, 150) # Planet pos (Radius, x, y, z)
    drawHeroUfo(player_x, player_y, 120 + PLAYER_HEIGHT, player_rot, cheat_active)
    # Update models with game state
    setGameOverState(game_over)
    setCurrentWave(current_wave)
    # Health bars import from healthBar.py
    drawHealthbar(player_x, player_y, PLAYER_HEIGHT, life, game_over, HEALTH_ORANGE, player_has_mega_shield, mega_shield_health)
    if not game_over or planet_health <= 0:
        drawPlanetHealthBar(planet_health, planet_max_health, HEALTH_ORANGE)
    
    drawEnemies()
    
    # Draw boss if Active only
    if boss_active and not game_win:
        drawBossEnemy(boss_x, boss_y, 120 + PLAYER_HEIGHT, boss_rot)
        drawBossHealthBar(boss_health, BOSS_HEALTH, "SKY CAPTAIN")
    
    showBullets()
    drawPickups()
    drawPlanetAttackers()
    
    # From timer
    draw_timer()
    
    # Display QTE
    # Draw QTE if active
    drawQTE()

    
    drawUI()
    
    # Draw mega power-ups
    drawMegaWeaponPickup()
    drawMegaShieldPickup()
    
    # Enemy Shooting things
    # Draw enemy bullets
    enemy_bullets = getEnemyBullets()
    for bullet_data in enemy_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            continue
        
        glColor3f(1, 0, 0)  # Red for enemy bullets
        glPushMatrix()
        glTranslatef(bx, by, 120 + PLAYER_HEIGHT - 40)
        glutSolidCube(10)
        glPopMatrix()
    
    # Draw boss bullets  
    boss_bullets = getBossBullets()
    for bullet_data in boss_bullets:
        if len(bullet_data) == 5:
            bx, by, dx, dy, bullet_type = bullet_data
        else:
            continue
        
        glColor3f(1, 0.5, 0)  # Orange for boss bullets
        glPushMatrix()
        glTranslatef(bx, by, 120 + PLAYER_HEIGHT - 40)
        glutSolidCube(20)
        glPopMatrix()

    glutSwapBuffers()


# Add game over screen function
def drawGameOverScreen():
    # Black background is already set by glClearColor
    
    # Set up orthographic projection for 2D text
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw "GAME OVER" text
    glColor3f(1, 0, 0)  # Red text
    game_over_text = "GAME OVER"
    text_width = len(game_over_text) * 20
    text_x = (WINDOW_WIDTH - text_width) // 2
    text_y = WINDOW_HEIGHT // 2 + 50
    
    glRasterPos2f(text_x, text_y)
    for ch in game_over_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch))
    
    # Draw score
    glColor3f(1, 1, 1)  # White text
    score_text = f"Final Score: {score}"
    score_width = len(score_text) * 15
    score_x = (WINDOW_WIDTH - score_width) // 2
    score_y = WINDOW_HEIGHT // 2
    
    glRasterPos2f(score_x, score_y)
    for ch in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    # Draw restart instruction
    restart_text = "Press R to Restart"
    restart_width = len(restart_text) * 12
    restart_x = (WINDOW_WIDTH - restart_width) // 2
    restart_y = WINDOW_HEIGHT // 2 - 50
    
    glRasterPos2f(restart_x, restart_y)
    for ch in restart_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
    
    # Draw cause of death
    death_cause = ""
    if planet_health <= 0:
        death_cause = "Planet Destroyed!"
    elif life <= 0:
        death_cause = "Spaceship Destroyed!"
    elif missed_shots >= MAX_MISS:
        death_cause = "Too Many Missed Shots!"
    elif is_timer_expired() and not cheat_active:
        death_cause = "Time's Up!"
    
    if death_cause:
        cause_width = len(death_cause) * 12
        cause_x = (WINDOW_WIDTH - cause_width) // 2
        cause_y = WINDOW_HEIGHT // 2 - 100
        
        glColor3f(1, 0.5, 0)  # Orange text
        glRasterPos2f(cause_x, cause_y)
        for ch in death_cause:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy")
    
    start_timer()
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyHandler)
    glutSpecialFunc(arrowKeys)
    glutMouseFunc(mouseHandler)
    glutIdleFunc(update)

    glutMainLoop()


if __name__ == "__main__":
    main()
