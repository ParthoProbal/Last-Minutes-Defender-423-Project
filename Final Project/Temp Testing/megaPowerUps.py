from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
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
