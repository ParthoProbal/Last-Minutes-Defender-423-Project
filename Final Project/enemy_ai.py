import random
import math

# Planet Attacker Enemy
def initPlanetAttackers(count=2):
    planet_attackers = []
    half = 600  # GRID_LEN
    limit = 570  # GRID_LEN - 30 (600 - 30 = 570)
    
    for _ in range(count):
        # Spawn from front wall (y = half = 600) - FIXED
        x = random.uniform(-half, half)
        y = limit  # Front wall position (y = 570, just inside the wall)
        rot = 180  # Facing downward toward planet
        
        planet_attackers.append([x, y, rot])
    
    return planet_attackers

def movePlanetAttackers(planet_attackers, planet_x=0, planet_y=-1600):
    limit = 570  # GRID_LEN - 30 (600 - 30 = 570) - FIXED
    
    for i in range(len(planet_attackers)):
        ex, ey, erot = planet_attackers[i]
        
        # Move toward planet (not player)
        dx = planet_x - ex
        dy = planet_y - ey
        
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 100:  # Stop when close to planet
            ex += (dx / dist) * 2  # Speed 2 toward planet
            ey += (dy / dist) * 2
        
        # Update rotation to face planet
        angle_to_planet = math.degrees(math.atan2(dy, dx)) - 90
        erot = angle_to_planet
        
        # boundary checks
        if ex < -limit:
            ex = -limit
        if ex > limit:
            ex = limit
        if ey < -limit:
            ey = -limit
        if ey > limit:
            ey = limit
        
        planet_attackers[i] = [ex, ey, erot]
    
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