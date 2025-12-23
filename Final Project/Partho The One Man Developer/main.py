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


# def handleCollisions():
#     pass  



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
    global enemy_list
    
    if not enemy_list:
        half = GRID_LEN
        limit = GRID_LEN - 30
        
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
    
    if fps_mode and cheat_active and not cheat_vision:
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
    
    if not game_over:
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
        draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 30, f"Time: {minutes:02d}:{seconds:02d}")
        
        # Wave display
        draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 60, f"Wave: {current_wave}")
    
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
    global cheat_active, cheat_vision, fps_mode
    global planet_attacker_list, planet_health
    global current_wave, player_has_mega_weapon, player_has_mega_shield, mega_weapon_ammo
    global boss_x, boss_y, boss_rot, boss_active, boss_health
    global last_mega_shot_time, mega_shield_health
    
    timer.stop_timer()
    timer.start_timer()
    
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
    
    # Reset wave and mega power-ups
    waveSystem.resetWaveSystem()
    megaPowerUps.resetMegaPowerUps()
    current_wave = 1
    player_has_mega_weapon = False
    player_has_mega_shield = False
    mega_weapon_ammo = 10
    mega_shield_health = 0
    last_mega_shot_time = 0
    
    # Reset boss variables
    boss_x = 0
    boss_y = 0
    boss_rot = 0
    boss_active = False
    boss_health = BOSS_HEALTH
    
    printStats()
    

def cheat():
    global player_rot, cheat_active, cheat_vision, last_fired
    
    if not cheat_active:
        return
    
    now = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    
    player_rot += CHEAT_TURN
    
    if cheat_vision and fps_mode and enemy_list:
        closest = enemy_list[0]
        ex, ey, erot = closest
        
        angle_to = math.degrees(math.atan2(ey - player_y, ex - player_x))
        want_angle = angle_to - 90
        
        diff = want_angle - player_rot
        
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        
        if abs(diff) > 30:
            player_rot += CHEAT_TURN * 0.7
        else:
            player_rot += diff * 0.12
    
    for idx, (ex, ey, erot) in enumerate(enemy_list):
        dx = ex - player_x
        dy = ey - player_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 400:
            continue
        
        e_angle = math.degrees(math.atan2(dy, dx))
        gun_angle = (player_rot + 90) % 360
        e_norm = e_angle % 360
        
        angle_diff = abs(gun_angle - e_norm)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        
        if angle_diff < 12:
            if idx not in last_fired:
                shoot()
                last_fired[idx] = now
                break
            elif (now - last_fired[idx]) > FIRE_DELAY:
                shoot()
                last_fired[idx] = now
                break
    

def keyHandler(key, x, y):
    global player_x, player_y, player_rot
    global cheat_active, cheat_vision, cam_fixed, look_fixed
    global game_over
    
    if key == b'r':
        resetAll()
        return
    
    if game_over:
        return
    
    if key == b'c':
        cheat_active = not cheat_active
        cam_fixed = None
        look_fixed = None
    
    if key == b'v':
        cheat_vision = not cheat_vision
        cam_fixed = None
        look_fixed = None
    
    angle = math.radians(player_rot)
    new_x = player_x
    new_y = player_y
    
    if key == b'w':
        new_x -= PLAYER_SPEED * math.sin(angle)
        new_y += PLAYER_SPEED * math.cos(angle)
    
    if key == b's':
        new_x += PLAYER_SPEED * math.sin(angle)
        new_y -= PLAYER_SPEED * math.cos(angle)
    
    if not cheat_active:
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
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        shoot()
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fps_mode = not fps_mode
        cam_fixed = None
        look_fixed = None
        

def arrowKeys(key, x, y):
    global camera_pos, CAM_SPEED
    xc, yc, zc = camera_pos
    
    if key == GLUT_KEY_UP:
        yc -= CAM_SPEED
    if key == GLUT_KEY_DOWN:
        yc += CAM_SPEED
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
    gluPerspective(fovY, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if fps_mode:
        cameraFPS()
    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)
        

def update():
    global planet_attacker_list, bullets, enemy_list, score, boss_health, boss_active, pickups, game_over, life, player_ammo, planet_health
    global current_wave, player_has_mega_weapon, player_has_mega_shield, mega_weapon_ammo, mega_shield_health
    
    if game_over:
        glutPostRedisplay()
        return
    
    # # Timer updation
    timer.update_timer()
    
    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    time_remaining = timer.get_time_remaining()
    
    if (timer.get_time_remaining() <= 0 and timer.is_timer_active()):
        game_over = True
        timer.stop_timer()
        print("Time up, game over")
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
    
    old_health = planet_health
    
    # Planet Health Checker
    if planet_health <= 0:
        game_over = True
        planet_health = 0
        glutPostRedisplay()
        return
    
    # Imported from collision.py
    bullets, enemy_list, planet_attacker_list, boss_health, boss_active, pickups, score, game_over = collision.handleHits(
        bullets, enemy_list, planet_attacker_list, boss_x, boss_y, boss_health, boss_active, pickups, score, game_over
    )
    
    # Regular pickups only in wave 1 and 2
    if waveSystem.shouldSpawnPickups():
        pickups, life, player_ammo = collision.handlePickups(pickups, player_x, player_y, life, player_ammo)
    
    planet_attacker_list, planet_health = collision.planetHit(planet_attacker_list, planet_health, game_over)
    
    if planet_health != old_health:
        print(f"Planet health changed: {old_health} -> {planet_health}")
    
    # Player hit with mega shield
    enemy_list, planet_attacker_list, life, game_over, bullets, damage_taken = collision.playerHit(
        enemy_list, planet_attacker_list, boss_x, boss_y, boss_active, player_x, player_y, 
        life, game_over, bullets, player_has_mega_shield, mega_shield_health
    )
    
    # Apply damage to mega shield
    if player_has_mega_shield and damage_taken > 0:
        megaPowerUps.takeMegaShieldDamage(damage_taken)
        mega_shield_health = megaPowerUps.mega_shield_health
        print(f"Mega Shield took {damage_taken} damage! Remaining: {mega_shield_health}")
    
    # Wave damage stuff
    if life < old_health:
        wave_damage = waveSystem.getEnemyDamageMultiplier()
        print(f"Player got hit! Wave {current_wave} damage: {wave_damage}x")
    
    pulse()
    cheat()
    planet_attacker_list = enemy_ai.movePlanetAttackers(planet_attacker_list, 0, -1600)
    
    # Boss in wave 3
    if current_wave == 3 and not boss_active:
        initBoss()
        print("BOSS TIME! Wave 3 Boss activated!")
    
    glutPostRedisplay()
    

def display():
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
    models.drawHeroUfo(player_x, player_y, 120 + PLAYER_HEIGHT, player_rot)
    
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

    
    drawUI()
    
    # Draw mega power-ups
    megaPowerUps.drawMegaWeaponPickup()
    megaPowerUps.drawMegaShieldPickup()

    glutSwapBuffers()
    

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