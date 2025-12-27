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
