import math
import waveSystem

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
        damage = 10 if bullet_type == "mega" else 1
        
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
                    
                    from main import newEnemy
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
                    
                    from enemy_ai import initPlanetAttackers
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
        
        if dist < 100:
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
                damage = 3 * waveSystem.getEnemyDamageMultiplier()  # Wave damage multiplier
                from main import newEnemy
                enemy_list[i] = newEnemy()
                return enemy_list, planet_attacker_list, life, game_over, bullets, damage
            else:
                life -= 3  # Regular enemy damage = 3
                if life <= 0:
                    game_over = True
                    life = 0
                    bullets = []
                
                from main import newEnemy
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
                damage = 6 * waveSystem.getEnemyDamageMultiplier()  # Wave damage multiplier
                from enemy_ai import initPlanetAttackers
                planet_attacker_list[i] = initSinglePlanetAttacker()
                return enemy_list, planet_attacker_list, life, game_over, bullets, damage
            else:
                life -= 6  # Planet attacker damage = 6
                if life <= 0:
                    game_over = True
                    life = 0
                    bullets = []
                
                from enemy_ai import initPlanetAttackers
                planet_attacker_list[i] = initSinglePlanetAttacker()
                return enemy_list, planet_attacker_list, life, game_over, bullets, 0
    
    return enemy_list, planet_attacker_list, life, game_over, bullets, 0

# Helper Method
def initSinglePlanetAttacker():
    import random
    half = 600  # GRID_LEN
    limit = 570  # GRID_LEN - 30 (600 - 30 = 570)
    
    x = random.uniform(-half, half)
    y = limit
    rot = 180
    charging_state = "approaching"
    charge_timer = 0
    
    return [x, y, rot, charging_state, charge_timer]

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