import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class MegaPowerups:
    def __init__(self):
        self.mega_weapon_spawned = False
        self.mega_shield_spawned = False
        self.mega_weapon_acquired = False
        self.mega_shield_acquired = False
        self.mega_weapon_ammo = 0
        self.mega_weapon_capacity = 10
        self.last_ammo_regeneration = 0
        self.mega_weapon_position = (0, 0)
        self.mega_shield_position = (0, 0)
        
        # Weapon stats
        self.MEGA_WEAPON_DAMAGE = 200
        self.MEGA_WEAPON_FIRE_DELAY = 2.0
        self.MEGA_WEAPON_BULLET_SPEED = 25
        
        # Shield stats
        self.MEGA_SHIELD_HEALTH = 1000

def run_mega_powerups_system(player_x, player_y, wave_status, player_health, 
                           player_max_health, player_ammo, game_time):
    """Main function to handle all mega power-up operations in Wave 3"""
    
    mega = MegaPowerups()
    events = []
    
    # Only activate in Wave 3
    if wave_status.get('wave', 1) != 3:
        return {
            'events': events,
            'player_health': player_health,
            'player_ammo': player_ammo,
            'mega_weapon_acquired': False,
            'mega_shield_acquired': False
        }
    
    # Spawn mega power-ups at start of Wave 3
    if not mega.mega_weapon_spawned and wave_status.get('wave') == 3:
        spawn_mega_powerups(mega)
    
    # Draw mega power-ups
    draw_mega_powerups_3d(mega)
    
    # Check for pickup collisions
    pickup_result = check_pickup_collisions(mega, player_x, player_y)
    if pickup_result:
        events.append(pickup_result)
        
        if pickup_result['type'] == 'mega_weapon':
            mega.mega_weapon_acquired = True
            mega.mega_weapon_ammo = mega.mega_weapon_capacity
            player_ammo = mega.mega_weapon_ammo
            print(f"MEGA WEAPON ACQUIRED! Damage: {mega.MEGA_WEAPON_DAMAGE}")
            
        elif pickup_result['type'] == 'mega_shield':
            mega.mega_shield_acquired = True
            player_health = mega.MEGA_SHIELD_HEALTH
            player_max_health = mega.MEGA_SHIELD_HEALTH
            print(f"MEGA SHIELD ACQUIRED! Health set to {mega.MEGA_SHIELD_HEALTH}")
    
    # Update ammo regeneration
    if mega.mega_weapon_acquired:
        update_ammo_regeneration(mega, game_time)
        player_ammo = mega.mega_weapon_ammo
    
    # Return updated state
    return {
        'events': events,
        'player_health': player_health,
        'player_max_health': player_max_health,
        'player_ammo': player_ammo,
        'mega_weapon_acquired': mega.mega_weapon_acquired,
        'mega_shield_acquired': mega.mega_shield_acquired,
        'mega_weapon_damage': mega.MEGA_WEAPON_DAMAGE if mega.mega_weapon_acquired else 0,
        'mega_shield_health': mega.MEGA_SHIELD_HEALTH if mega.mega_shield_acquired else 0
    }

def spawn_mega_powerups(mega):
    """Spawn both mega power-ups at random positions"""
    # Spawn mega weapon
    mega.mega_weapon_position = (
        random.randint(-400, 400),
        random.randint(-400, 400)
    )
    mega.mega_weapon_spawned = True
    
    # Spawn mega shield (ensure it's not too close to weapon)
    mega.mega_shield_position = (
        random.randint(-400, 400),
        random.randint(-400, 400)
    )
    # Make sure they're not too close together
    while (abs(mega.mega_shield_position[0] - mega.mega_weapon_position[0]) < 150 and
           abs(mega.mega_shield_position[1] - mega.mega_weapon_position[1]) < 150):
        mega.mega_shield_position = (
            random.randint(-400, 400),
            random.randint(-400, 400)
        )
    mega.mega_shield_spawned = True
    
    print("MEGA POWER-UPS SPAWNED!")
    print(f"Weapon at: {mega.mega_weapon_position}")
    print(f"Shield at: {mega.mega_shield_position}")

def draw_mega_powerups_3d(mega):
    """Draw 3D models for both mega power-ups"""
    # Draw mega weapon if not acquired
    if mega.mega_weapon_spawned and not mega.mega_weapon_acquired:
        draw_mega_weapon_model(mega.mega_weapon_position)
    
    # Draw mega shield if not acquired
    if mega.mega_shield_spawned and not mega.mega_shield_acquired:
        draw_mega_shield_model(mega.mega_shield_position)

def draw_mega_weapon_model(position):
    """Draw 3D model for the mega weapon pickup"""
    glPushMatrix()
    glTranslatef(position[0], position[1], 120)
    
    # Rotating animation
    rotation = glutGet(GLUT_ELAPSED_TIME) / 1000.0 * 45  # 45 degrees per second
    glRotatef(rotation, 0, 0, 1)
    
    # Gold color for weapon
    glColor3f(1.0, 0.84, 0.0)  # Gold
    
    # Main body
    glPushMatrix()
    glScalef(2.0, 0.5, 0.5)
    glutSolidCube(40)
    glPopMatrix()
    
    # Barrel
    glPushMatrix()
    glTranslatef(45, 0, 0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 8, 60, 16, 16)
    glPopMatrix()
    
    # Energy core (glowing)
    glPushMatrix()
    glTranslatef(-20, 0, 0)
    
    # Pulsing glow effect
    pulse = (glutGet(GLUT_ELEMENTS) % 1000) / 1000.0
    glow_intensity = 0.7 + 0.3 * pulse
    
    glColor3f(0.0, glow_intensity, glow_intensity)  # Cyan pulse
    glutSolidSphere(15, 16, 16)
    glPopMatrix()
    
    glPopMatrix()

def draw_mega_shield_model(position):
    """Draw 3D model for the mega shield pickup"""
    glPushMatrix()
    glTranslatef(position[0], position[1], 120)
    
    # Rotating animation
    rotation = glutGet(GLUT_ELAPSED_TIME) / 1000.0 * 30
    glRotatef(rotation, 1, 1, 0)
    
    # Blue energy color
    glColor3f(0.0, 0.5, 1.0)  # Blue
    
    # Outer shield ring
    glutSolidTorus(5, 30, 16, 32)
    
    # Inner energy sphere
    glColor3f(0.2, 0.8, 1.0)  # Light blue
    glutSolidSphere(20, 16, 16)
    
    # Pulsing energy field
    pulse = (glutGet(GLUT_ELAPSED_TIME) % 1000) / 1000.0
    pulse_size = 1.0 + 0.2 * pulse
    
    glColor4f(0.5, 0.8, 1.0, 0.3)  # Semi-transparent
    glPushMatrix()
    glScalef(pulse_size, pulse_size, pulse_size)
    glutSolidSphere(22, 12, 12)
    glPopMatrix()
    
    glPopMatrix()

def check_pickup_collisions(mega, player_x, player_y):
    """Check if player collides with any mega power-up"""
    # Check mega weapon
    if mega.mega_weapon_spawned and not mega.mega_weapon_acquired:
        dx = player_x - mega.mega_weapon_position[0]
        dy = player_y - mega.mega_weapon_position[1]
        distance = (dx*dx + dy*dy) ** 0.5
        
        if distance < 60:  # Collision radius
            return {
                'type': 'mega_weapon',
                'position': mega.mega_weapon_position,
                'message': 'MEGA WEAPON ACQUIRED!'
            }
    
    # Check mega shield
    if mega.mega_shield_spawned and not mega.mega_shield_acquired:
        dx = player_x - mega.mega_shield_position[0]
        dy = player_y - mega.mega_shield_position[1]
        distance = (dx*dx + dy*dy) ** 0.5
        
        if distance < 60:  # Collision radius
            return {
                'type': 'mega_shield',
                'position': mega.mega_shield_position,
                'message': 'MEGA SHIELD ACQUIRED!'
            }
    
    return None

def update_ammo_regeneration(mega, current_time):
    """Regenerate mega weapon ammo when below 3"""
    if mega.mega_weapon_ammo < 3:
        if current_time - mega.last_ammo_regeneration >= 3.0:  # Every 3 seconds
            regen_amount = random.randint(1, 3)
            mega.mega_weapon_ammo = min(mega.mega_weapon_capacity, 
                                       mega.mega_weapon_ammo + regen_amount)
            mega.last_ammo_regeneration = current_time
            
            if regen_amount > 0:
                print(f"Mega Weapon ammo regenerated: +{regen_amount} (Total: {mega.mega_weapon_ammo})")

def use_mega_weapon_ammo(mega):
    """Use one ammo from mega weapon"""
    if mega.mega_weapon_acquired and mega.mega_weapon_ammo > 0:
        mega.mega_weapon_ammo -= 1
        return True
    return False

def draw_mega_powerups_hud(mega_status):
    """Draw HUD elements for mega power-ups"""
    if mega_status.get('mega_weapon_acquired'):
        # Draw mega weapon ammo
        glColor3f(1.0, 0.84, 0.0)  # Gold
        glRasterPos2f(20, 200)
        ammo_text = f"MEGA WEAPON: {mega_status.get('player_ammo', 0)}/{mega_status.get('mega_weapon_capacity', 10)}"
        for char in ammo_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
        
        # Draw damage info
        glRasterPos2f(20, 180)
        damage_text = f"DAMAGE: {mega_status.get('mega_weapon_damage', 0)}"
        for char in damage_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
    
    if mega_status.get('mega_shield_acquired'):
        # Draw mega shield health
        glColor3f(0.0, 0.5, 1.0)  # Blue
        glRasterPos2f(20, 160)
        shield_text = f"MEGA SHIELD: {mega_status.get('player_health', 0)}/{mega_status.get('mega_shield_health', 1000)}"
        for char in shield_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

def reset_mega_powerups():
    """Reset mega power-ups system"""
    mega = MegaPowerups()
    print("Mega power-ups system reset")
    return mega
