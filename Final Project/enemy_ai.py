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