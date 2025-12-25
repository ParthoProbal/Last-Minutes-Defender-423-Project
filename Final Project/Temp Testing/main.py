from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import models
import enemy_ai
import collision
import healthBar
import timer
import waveSystem
import megaPowerUps
import QTE
import sys  # Added for exit functionality


WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 1000
divisor = 255 

camera_pos = (0,500,500)
fovY = 120
rand_var = 423

GRID_LEN = 600  

# Color stuff
CHECKER_COLOR = (172/divisor, 120/divisor, 186/divisor) # Lavender
# Add this with other colors
HEALTH_ORANGE = (255/divisor, 165/divisor, 0/divisor)

# Wall colors
LIGHT_GREEN = (57/divisor, 255/divisor, 20/divisor)
BLUE_ROYAL = (65/divisor, 105/divisor, 225/divisor)
CYAN = (0/divisor, 255/divisor, 255/divisor)

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
planet_attacker_list = enemy_ai.initPlanetAttackers(PLANET_ATTACKER_COUNT)

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
planet_health = 100
planet_max_health = 100

# game state
bullets_shot = 0
life = 5
score = 0
missed_shots = 0
game_over = False
MAX_MISS = 10

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
player_max_health = 5  # For testing for now

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

# NEW: Game pause state
is_paused = False

# NEW: Camera mode (first-person/third-person toggle)
camera_mode = "third_person"  # "third_person" or "first_person"

# NEW: Camera distance for arrow keys
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
                glColor3f(1, 1, 1)
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
    glColor3f(1, 1, 1)
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
        
        # NEW: Change player to black when game over
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
    
    # NEW: Change player to black when game over
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
        models.drawHeroAttacker(ex, ey, 120 + PLAYER_HEIGHT, erot)
        # Health Bar for every enemy
        healthBar.drawEnemyHealthbar(ex, ey, 120 + PLAYER_HEIGHT)

# Draw Func for player attacking     
def drawPlanetAttackers():
    if game_over:
        return
    
    for planet_attacker in planet_attacker_list:
        if len(planet_attacker) == 3:
            ex, ey, erot = planet_attacker
        else:
            ex, ey, erot, charging_state, charge_timer = planet_attacker
        
        models.drawPlanetAttacker(ex, ey, 120 + PLAYER_HEIGHT, erot)
        healthBar.drawPlanetAttackerHealthbar(ex, ey, 120 + PLAYER_HEIGHT)
        

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
            wave_speed = ENEMY_SPEED * waveSystem.getEnemySpeedMultiplier()
            ex += (dx / dist) * wave_speed
            ey += (dy / dist) * wave_speed
        
        # Always face the player
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
def moveBoss():
    global boss_x, boss_y, boss_rot
    
    if not boss_active:
        return
    
    
    boss_x, boss_y, boss_rot = enemy_ai.moveBoss(
        boss_x, boss_y, boss_rot, 
        player_x, player_y, 
        ENEMY_SPEED  # regular enemy speed for testing
    )
    
def initBoss():
    global boss_x, boss_y, boss_rot, boss_active, boss_health
    
    # From Enemy.py
    boss_x, boss_y, boss_rot = enemy_ai.initBoss()
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
            models.drawHealthBox(px, py, 50)  # Health Pickup Box
        elif ptype == "ammo":
            models.drawAmmoBox(px + 40, py + 40, 50)    # Ammo Pickup Box
    

def shoot():
    global bullets_shot, player_ammo, last_mega_shot_time, player_has_mega_weapon, mega_weapon_ammo
    
    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    
    # Mega Weapon logic
    if player_has_mega_weapon and waveSystem.getCurrentWave() == 3:
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
        else:  # For backward compatibility
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
        # Instead of being inside the player, position it a bit behind
        camera_distance = 50  # Distance behind player for better view
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
        # Original cheat vision logic (if you want to keep it)
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
    global is_paused, fps_mode  # CHANGED from camera_mode to fps_mode
    
    if not game_over:
        # Show pause indicator
        if is_paused:
            draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 50, "GAME PAUSED - Press P to resume", GLUT_BITMAP_HELVETICA_18)
        
        # Show mega shield health or normal health
        if player_has_mega_shield:
            draw_text(10, WINDOW_HEIGHT - 30, f"Mega Shield: {mega_shield_health}/1000")
        else:
            draw_text(10, WINDOW_HEIGHT - 30, f"Life: {life}")
        
        draw_text(10, WINDOW_HEIGHT - 60, f"Score: {score}")
        draw_text(10, WINDOW_HEIGHT - 90, f"Missed: {missed_shots}/{MAX_MISS}")
        
        # Show mega weapon ammo or normal ammo
        if player_has_mega_weapon:
            draw_text(10, WINDOW_HEIGHT - 120, f"Mega Ammo: {mega_weapon_ammo}/10")
        else:
            draw_text(10, WINDOW_HEIGHT - 120, f"Ammo: {player_ammo}")
        
        draw_text(10, WINDOW_HEIGHT - 150, f"Planet Health: {planet_health}/100")
        
        # Time ui in game
        time_left = timer.get_time_remaining()
        minutes = time_left // 60
        seconds = time_left % 60
        
        # Show timer status in cheat mode
        if cheat_active:
            draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 30, f"Time: {minutes:02d}:{seconds:02d} (CHEAT)")
        else:
            draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 30, f"Time: {minutes:02d}:{seconds:02d}")
        
        # Wave display
        draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 60, f"Wave: {current_wave}")
        
        # Camera mode display - UPDATED
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
        draw_text(10, WINDOW_HEIGHT - 90, "Press R to restart")
        

def resetAll():
    global life, score, missed_shots, game_over
    global player_x, player_y, player_rot
    global bullets, enemy_list, pickups, player_ammo
    global cheat_active, cheat_vision, fps_mode  # CHANGED from camera_mode to fps_mode
    global planet_attacker_list, planet_health
    global current_wave, player_has_mega_weapon, player_has_mega_shield, mega_weapon_ammo
    global boss_x, boss_y, boss_rot, boss_active, boss_health
    global last_mega_shot_time, mega_shield_health
    global is_paused, camera_distance, camera_pos  # REMOVED camera_mode
    
    # PROPER timer reset sequence
    timer.stop_timer()  # Stop any running timer
    timer.reset_timer()  # Reset timer variables
    timer.start_timer()  # Start fresh timer (with 1 second delay)
    
    life = 5
    score = 0
    missed_shots = 0
    game_over = False
    
    player_x = 0
    player_y = 0
    player_rot = 0
    
    bullets = []
    enemy_list = []
    planet_attacker_list = enemy_ai.initPlanetAttackers(PLANET_ATTACKER_COUNT)
    pickups = []  
    player_ammo = 10
    planet_health = 100
    
    cheat_active = False
    cheat_vision = False
    fps_mode = False
    
    is_paused = False
    camera_mode = "third_person"
    camera_distance = 500
    camera_pos = (0, camera_distance, camera_distance)
    
    waveSystem.resetWaveSystem()
    megaPowerUps.resetMegaPowerUps()
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
    
    QTE.resetQTE()
    qte_active = False
    qte_triggered = False
    
    enemy_ai.resetEnemyShooting()
    enemy_last_shot_times = []
    last_boss_shot_time = 0
    
    timer.disable_cheat_mode()
    
    printStats()
    

def cheat():
    global cheat_active, life, player_ammo, planet_health, mega_shield_health
    
    if not cheat_active:
        return
    
    # Infinite health (for mega shield too)
    if player_has_mega_shield:
        mega_shield_health = 9999
    else:
        life = 9999
    
    # Infinite ammo
    if not player_has_mega_weapon:
        player_ammo = 99999
    else:
        megaPowerUps.mega_weapon_ammo = 10
    
    # Infinite planet health
    planet_health = 99999
    
    # Enable timer cheat mode
    timer.enable_cheat_mode()
    

def keyHandler(key, x, y):
    global player_x, player_y, player_rot
    global cheat_active, cheat_vision, cam_fixed, look_fixed
    global game_over, qte_active
    global is_paused, camera_mode, fps_mode  # ADDED fps_mode to global
    
    # ESC key to exit game
    if key == b'\x1b':  # ESC key
        glutDestroyWindow(glutGetWindow())
        sys.exit(0)
        return
    
    # P key to pause/resume game
    if key == b'p' or key == b'P':
        is_paused = not is_paused
        if is_paused:
            timer.pause_timer()
            print("Game Paused")
        else:
            timer.resume_timer()
            print("Game Resumed")
        return
    
    # F key to switch camera mode - FIXED
    if key == b'f' or key == b'F':
        fps_mode = not fps_mode  # Toggle fps_mode directly
        cam_fixed = None
        look_fixed = None
        if fps_mode:
            print("Camera: First Person")
        else:
            print("Camera: Third Person")
        return
    
    # QTE key handling
    if qte_active and QTE.isQTEActive():
        if key.lower() in [b'w', b'a', b's', b'd']:
            QTE.handleQTEKey(key.decode())
        return
    
    if key == b'r':
        resetAll()
        return
    
    if game_over:
        return
    
    # Don't process movement if game is paused
    if is_paused:
        return
    
    if key == b'c':
        cheat_active = not cheat_active
        cam_fixed = None
        look_fixed = None
        print(f"Cheat Mode: {'ON' if cheat_active else 'OFF'}")
        
        # Toggle timer cheat mode
        if cheat_active:
            timer.enable_cheat_mode()
        else:
            timer.disable_cheat_mode()
    
    if key == b'v':
        cheat_vision = not cheat_vision
        cam_fixed = None
        look_fixed = None
    
    angle = math.radians(player_rot)
    new_x = player_x
    new_y = player_y
    
    # Super movement speed in cheat mode
    speed_multiplier = CHEAT_SPEED_MULTIPLIER if cheat_active else 1.0
    effective_speed = PLAYER_SPEED * speed_multiplier
    
    if key == b'w':
        new_x -= effective_speed * math.sin(angle)
        new_y += effective_speed * math.cos(angle)
    
    if key == b's':
        new_x += effective_speed * math.sin(angle)
        new_y -= effective_speed * math.cos(angle)
    
    # Player can always rotate
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
    global is_paused  # NEW: Added pause state
    
    # NEW: Don't update if game is paused
    if is_paused:
        glutPostRedisplay()
        return
    
    if game_over:
        glutPostRedisplay()
        return
    
    # QTE update
    if QTE.isQTEActive():
        QTE.updateQTE()
        qte_result = QTE.getQTEResult()
        if qte_result == "win":
            # Player wins QTE
            boss_active = False
            score += 500
            print("BOSS DEFEATED! QTE Success!")
        elif qte_result == "lose":
            # Player loses QTE
            game_over = True
            print("GAME OVER! QTE Failed!")
        
        glutPostRedisplay()
        return
    
    # Timer update
    timer.update_timer()
    
    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    time_remaining = timer.get_time_remaining()
    
    # FIXED: Check timer but don't end game if cheat mode is active
    if not cheat_active and timer.is_timer_expired():
        game_over = True
        timer.stop_timer()
        print("Time up, game over")
        glutPostRedisplay()
        return
    
    # Check for QTE trigger (boss health 0)
    if boss_active and boss_health <= 0 and not qte_triggered:
        # QTE bypass in cheat mode
        if cheat_active:
            boss_active = False
            score += 500
            print("BOSS DEFEATED! Cheat Mode bypassed QTE!")
        else:
            qte_triggered = True
            QTE.startQTE()
            qte_active = True
            print("BOSS HEALTH ZERO! QTE Triggered!")
        glutPostRedisplay()
        return
    
    # Wave system
    waveSystem.updateWaveSystem(time_remaining)
    current_wave = waveSystem.getCurrentWave()
    
    if current_time % 5 == 0:
        print(f"Timer: {time_remaining} seconds remaining, Wave: {current_wave}")
    
    # Mega Power Ups in Wave 3
    if current_wave == 3 and not megaPowerUps.mega_weapon_spawned:
        megaPowerUps.spawnMegaPowerUps()
        print("Wave 3: Mega Power Ups spawned!")
    
    # Mega pickups check
    life, player_ammo = megaPowerUps.handleMegaPickups(player_x, player_y, life, player_ammo, time_remaining)
    
    # Update player mega status
    player_has_mega_weapon = megaPowerUps.player_has_mega_weapon
    player_has_mega_shield = megaPowerUps.player_has_mega_shield
    mega_weapon_ammo = megaPowerUps.mega_weapon_ammo
    mega_shield_health = megaPowerUps.mega_shield_health
    
    # Mega ammo regen
    if player_has_mega_weapon:
        megaPowerUps.regenerateMegaAmmo(current_time)
        mega_weapon_ammo = megaPowerUps.mega_weapon_ammo
    
    if not enemy_list:
        initEnemies()
    
    moveEnemies()
    moveBoss()
    moveBullets()
    
    # Check enemy bullets hitting planet
    enemy_bullets = enemy_ai.getEnemyBullets()
    planet_health = collision.enemyBulletPlanetHit(enemy_bullets, planet_health)
    
    old_health = planet_health
    
    # Planet Health Checker - Only end game if not in cheat mode
    if planet_health <= 0 and not cheat_active:
        game_over = True
        planet_health = 0
        glutPostRedisplay()
        return
    elif planet_health <= 0 and cheat_active:
        # In cheat mode, keep planet alive
        planet_health = 1
    
    # Imported from collision.py
    bullets, enemy_list, planet_attacker_list, boss_health, boss_active, pickups, score, game_over = collision.handleHits(
        bullets, enemy_list, planet_attacker_list, boss_x, boss_y, boss_health, boss_active, 
        pickups, score, game_over, current_wave, player_has_mega_weapon
    )
    
    # Regular pickups only in wave 1 and 2
    if waveSystem.shouldSpawnPickups():
        pickups, life, player_ammo = collision.handlePickups(pickups, player_x, player_y, life, player_ammo)
    else:
        # In Wave 3, clear any existing pickups
        pickups = []
    
    planet_attacker_list, planet_health = collision.planetHit(planet_attacker_list, planet_health, game_over)
    
    if planet_health != old_health:
        print(f"Planet health changed: {old_health} -> {planet_health}")
    
    # Player hit with mega shield - BUT NOT IN CHEAT MODE
    if not cheat_active:
        enemy_list, planet_attacker_list, life, game_over, bullets, damage_taken = collision.playerHit(
            enemy_list, planet_attacker_list, boss_x, boss_y, boss_active, player_x, player_y, 
            life, game_over, bullets, player_has_mega_shield, mega_shield_health
        )
    else:
        # In cheat mode, player doesn't take damage from enemy collisions
        damage_taken = 0
        # Call the function but ignore the game_over result
        temp_enemy_list, temp_planet_attacker_list, temp_life, temp_game_over, temp_bullets, temp_damage_taken = collision.playerHit(
            enemy_list, planet_attacker_list, boss_x, boss_y, boss_active, player_x, player_y, 
            life, game_over, bullets, player_has_mega_shield, mega_shield_health
        )
        # Keep the enemy and bullet updates but ignore life/game_over changes
        enemy_list = temp_enemy_list
        planet_attacker_list = temp_planet_attacker_list
        bullets = temp_bullets
    
    # Apply damage to mega shield - but not in cheat mode
    if player_has_mega_shield and damage_taken > 0 and not cheat_active:
        megaPowerUps.takeMegaShieldDamage(damage_taken)
        mega_shield_health = megaPowerUps.mega_shield_health
        print(f"Mega Shield took {damage_taken} damage! Remaining: {mega_shield_health}")
    
    # Wave damage stuff
    if life < old_health and not cheat_active:
        wave_damage = waveSystem.getEnemyDamageMultiplier()
        print(f"Player got hit! Wave {current_wave} damage: {wave_damage}x")
    
    pulse()
    cheat()
    planet_attacker_list = enemy_ai.movePlanetAttackers(planet_attacker_list, 0, -1600)
    
    # Boss in wave 3
    if current_wave == 3 and not boss_active and not qte_triggered:
        initBoss()
        print("BOSS TIME! Wave 3 Boss activated!")
        
    # Enemy and Boss Shooting updation
    # Enemy shooting
    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    
    # Regular enemies shoot
    for i in range(len(enemy_list)):
        ex, ey, erot = enemy_list[i]
        last_shot = enemy_last_shot_times[i] if i < len(enemy_last_shot_times) else 0
        
        enemy_ai.enemy_bullets, new_last_shot = enemy_ai.enemyShoot(
            ex, ey, erot, player_x, player_y, last_shot, current_time
        )
        
        if i < len(enemy_last_shot_times):
            enemy_last_shot_times[i] = new_last_shot
    
    # Boss shoots
    if boss_active:
        enemy_ai.boss_bullets, last_boss_shot_time = enemy_ai.bossShoot(
            boss_x, boss_y, boss_rot, player_x, player_y, last_boss_shot_time, current_time
        )
    
    # Move enemy bullets
    enemy_ai.moveEnemyBullets()
    enemy_ai.moveBossBullets()
    
    # Check enemy bullet hits on player - BUT NOT IN CHEAT MODE
    enemy_bullets = enemy_ai.getEnemyBullets()
    boss_bullets = enemy_ai.getBossBullets()
    
    # Only check player hits if cheat mode is OFF
    if not cheat_active:
        # Check regular enemy bullets
        for bullet_data in enemy_bullets:
            if len(bullet_data) == 5:
                bx, by, dx, dy, bullet_type = bullet_data
            else:
                continue
            
            # Check player hit
            dx_player = bx - player_x
            dy_player = by - player_y
            player_dist = math.sqrt(dx_player*dx_player + dy_player*dy_player)
            
            if player_dist < 25:  # Player hit radius
                if player_has_mega_shield:
                    damage = 1 * waveSystem.getEnemyDamageMultiplier()
                    megaPowerUps.takeMegaShieldDamage(damage)
                    mega_shield_health = megaPowerUps.mega_shield_health
                else:
                    life -= 0.05 # Regular enemy bullet damage
                    if life <= 0:
                        game_over = True
                        life = 0
        
        # Check boss bullets
        for bullet_data in boss_bullets:
            if len(bullet_data) == 5:
                bx, by, dx, dy, bullet_type = bullet_data
            else:
                continue
            
            # Check player hit
            dx_player = bx - player_x
            dy_player = by - player_y
            player_dist = math.sqrt(dx_player*dx_player + dy_player*dy_player)
            
            if player_dist < 25:
                if player_has_mega_shield:
                    damage = 200  
                    megaPowerUps.takeMegaShieldDamage(damage)
                    mega_shield_health = megaPowerUps.mega_shield_health
                else:
                    life = 0 # Boss bullet damage
                    game_over = True
    
    # FIX: In cheat mode, player cannot die from any cause
    if cheat_active:
        if life <= 0:
            life = 1  # Keep at least 1 life
        game_over = False  # Can't game over in cheat mode
    
    glutPostRedisplay()

def display():
    # Check if game over and show black screen
    if game_over:
        # Black screen when game over
        glClearColor(0, 0, 0, 1)  # Black background
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Show game over screen
        drawGameOverScreen()
        glutSwapBuffers()
        return
    
    # Original display code for normal game
    glClearColor(0, 0, 0, 1)  # Your original clear color
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
    
    # imported from models.py
    models.drawPlanet(1000, 0, -1600, 150) # Planet pos (Radius, x, y, z)
    models.drawHeroUfo(player_x, player_y, 120 + PLAYER_HEIGHT, player_rot, cheat_active)
    
    # Health bars import from healthBar.py
    healthBar.drawHealthbar(player_x, player_y, PLAYER_HEIGHT, life, game_over, HEALTH_ORANGE, player_has_mega_shield, mega_shield_health)
    if not game_over or planet_health <= 0:
        healthBar.drawPlanetHealthBar(planet_health, planet_max_health, HEALTH_ORANGE)
    
    drawEnemies()
    
    # Draw boss if Active only
    if boss_active:
        models.drawBossEnemy(boss_x, boss_y, 120 + PLAYER_HEIGHT, boss_rot)
        healthBar.drawBossHealthBar(boss_health, BOSS_HEALTH, "SKY CAPTAIN")
    
    showBullets()
    drawPickups()
    drawPlanetAttackers()
    
    # From timer
    timer.draw_timer()
    
    # Display QTE
    # Draw QTE if active
    QTE.drawQTE()

    
    drawUI()
    
    # Draw mega power-ups
    megaPowerUps.drawMegaWeaponPickup()
    megaPowerUps.drawMegaShieldPickup()
    
    # Enemy Shooting things
    # Draw enemy bullets
    enemy_bullets = enemy_ai.getEnemyBullets()
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
    boss_bullets = enemy_ai.getBossBullets()
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
    elif timer.is_timer_expired() and not cheat_active:
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
    
    timer.start_timer()
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyHandler)
    glutSpecialFunc(arrowKeys)
    glutMouseFunc(mouseHandler)
    glutIdleFunc(update)

    glutMainLoop()


if __name__ == "__main__":
    main()
