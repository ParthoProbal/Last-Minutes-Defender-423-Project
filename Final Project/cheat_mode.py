import time
import math
from OpenGL.GL import *
from OpenGL.GLUT import *

class CheatMode:
    def __init__(self):
        self.cheat_active = False
        self.cheat_activation_time = 0
        self.original_player_speed = 0
        self.original_enemy_speed = 0
        
        # Cheat properties
        self.CHEAT_PLAYER_SPEED_MULTIPLIER = 3.0
        self.CHEAT_PLAYER_HEALTH = 9999
        self.CHEAT_PLAYER_AMMO = 9999
        self.CHEAT_PLANET_HEALTH = 9999
        self.CHEAT_SPACESHIP_COLOR = (0.0, 1.0, 0.0)  # Green
        
        # Camera cheat effects
        self.super_speed_camera = False
        self.camera_zoom_multiplier = 1.5

def run_cheat_mode(player_stats, planet_health, enemy_stats, 
                  camera_pos, player_x, player_y, player_rot, key_pressed):
    """Main function to handle all cheat mode operations"""
    
    cheat = CheatMode()
    
    # Toggle cheat mode if 'C' key pressed
    if key_pressed == ord('c') or key_pressed == ord('C'):
        cheat.cheat_active = not cheat.cheat_active
        
        if cheat.cheat_active:
            cheat.cheat_activation_time = time.time()
            cheat.original_player_speed = player_stats.get('speed', 10)
            cheat.original_enemy_speed = enemy_stats.get('speed', 1)
            print("=== CHEAT MODE ACTIVATED ===")
        else:
            print("=== CHEAT MODE DEACTIVATED ===")
    
    # Apply cheat effects if active
    if cheat.cheat_active:
        player_stats = apply_player_cheats(cheat, player_stats)
        planet_health = apply_planet_cheats(cheat, planet_health)
        enemy_stats = apply_enemy_cheats(cheat, enemy_stats)
        camera_pos = apply_camera_cheats(cheat, camera_pos, player_x, player_y, player_rot)
    
    # Draw cheat mode HUD
    draw_cheat_hud(cheat)
    
    # Return modified values
    return {
        'cheat_active': cheat.cheat_active,
        'player_stats': player_stats,
        'planet_health': planet_health,
        'enemy_stats': enemy_stats,
        'camera_pos': camera_pos,
        'spaceship_color': get_cheat_spaceship_color(cheat),
        'qte_disabled': cheat.cheat_active,  # QTE disabled in cheat mode
        'boss_vulnerable': True  # Boss can be destroyed normally in cheat mode
    }

def apply_player_cheats(cheat, player_stats):
    """Apply all cheat effects to player"""
    if not cheat.cheat_active:
        return player_stats
    
    # Infinite health
    player_stats['health'] = cheat.CHEAT_PLAYER_HEALTH
    player_stats['max_health'] = cheat.CHEAT_PLAYER_HEALTH
    
    # Infinite ammo
    player_stats['ammo'] = cheat.CHEAT_PLAYER_AMMO
    player_stats['max_ammo'] = cheat.CHEAT_PLAYER_AMMO
    
    # Super speed
    player_stats['speed'] = cheat.original_player_speed * cheat.CHEAT_PLAYER_SPEED_MULTIPLIER
    
    # No fire delay
    player_stats['fire_delay'] = 0.05  # Very fast firing
    
    # Special cheat abilities
    player_stats['auto_aim'] = True
    player_stats['bullet_homing'] = True
    player_stats['piercing_shots'] = True
    
    return player_stats

def apply_planet_cheats(cheat, planet_health):
    """Apply cheat effects to planet"""
    if not cheat.cheat_active:
        return planet_health
    
    # Infinite planet health
    return cheat.CHEAT_PLANET_HEALTH

def apply_enemy_cheats(cheat, enemy_stats):
    """Apply cheat effects to enemies"""
    if not cheat.cheat_active:
        return enemy_stats
    
    # Enemies are weaker in cheat mode
    enemy_stats['speed'] = enemy_stats.get('speed', 1) * 0.5  # 50% slower
    enemy_stats['damage'] = enemy_stats.get('damage', 1) * 0.25  # 25% damage
    enemy_stats['health'] = enemy_stats.get('health', 1) * 0.5  # 50% health
    
    # Boss specific cheats
    enemy_stats['boss_speed'] = enemy_stats.get('boss_speed', 1) * 0.3
    enemy_stats['boss_damage'] = enemy_stats.get('boss_damage', 1) * 0.1
    
    return enemy_stats

def apply_camera_cheats(cheat, camera_pos, player_x, player_y, player_rot):
    """Apply cheat effects to camera"""
    if not cheat.cheat_active:
        return camera_pos
    
    # Super-speed camera tracking
    x, y, z = camera_pos
    
    # Camera follows player more aggressively
    target_x = player_x - 100 * math.sin(math.radians(player_rot))
    target_y = player_y + 100 * math.cos(math.radians(player_rot))
    target_z = 150  # Higher vantage point
    
    # Smooth interpolation
    x += (target_x - x) * 0.3
    y += (target_y - y) * 0.3
    z += (target_z - z) * 0.3
    
    # Camera zoom effect
    if cheat.super_speed_camera:
        z *= 0.7  # Zoom in during super speed
    
    return (x, y, z)

def get_cheat_spaceship_color(cheat):
    """Get the special color for spaceship in cheat mode"""
    if not cheat.cheat_active:
        return None
    
    # Create a pulsing green effect
    pulse = (time.time() - cheat.cheat_activation_time) * 2
    r = 0.2 + 0.8 * abs(math.sin(pulse))  # Pulsing red
    g = 1.0  # Always full green
    b = 0.2 + 0.8 * abs(math.cos(pulse))  # Pulsing blue
    
    return (r, g, b)

def draw_cheat_hud(cheat):
    """Draw cheat mode HUD indicators"""
    if not cheat.cheat_active:
        return
    
    # Draw "CHEAT MODE" banner
    glColor3f(0.0, 1.0, 0.0)  # Bright green
    glRasterPos2f(20, 920)
    cheat_text = ">>> CHEAT MODE ACTIVE <<<"
    for char in cheat_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    
    # Draw cheat effects list
    effects = [
        "Infinite Player Health",
        "Infinite Ammo",
        "Super Movement Speed",
        "Infinite Planet Health",
        "Auto-Aim Enabled",
        "Homing Bullets",
        "Piercing Shots",
        "QTE Disabled",
        "Boss Vulnerable"
    ]
    
    glColor3f(0.5, 1.0, 0.5)  # Light green
    for i, effect in enumerate(effects):
        glRasterPos2f(40, 880 - i * 20)
        for char in effect:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
    
    # Draw timer
    cheat_duration = time.time() - cheat.cheat_activation_time
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    glRasterPos2f(1100, 920)
    duration_text = f"CHEAT TIME: {int(cheat_duration)}s"
    for char in duration_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

def apply_cheat_to_bullets(bullets, cheat_active):
    """Apply cheat effects to bullets"""
    if not cheat_active:
        return bullets
    
    # Make bullets homing in cheat mode
    for bullet in bullets:
        # Add homing property
        bullet['homing'] = True
        bullet['damage'] *= 2  # Double damage
        bullet['speed'] *= 1.5  # 50% faster
        bullet['piercing'] = True  # Goes through multiple enemies
    
    return bullets

def handle_cheat_collisions(collision_result, cheat_active):
    """Modify collision results in cheat mode"""
    if not cheat_active:
        return collision_result
    
    # In cheat mode, player doesn't take damage
    if 'player_damage' in collision_result:
        collision_result['player_damage'] = 0
    
    # Planet doesn't take damage
    if 'planet_damage' in collision_result:
        collision_result['planet_damage'] = 0
    
    # Enemies take extra damage
    if 'enemy_damage' in collision_result:
        collision_result['enemy_damage'] *= 3
    
    # Boss takes massive damage
    if 'boss_damage' in collision_result:
        collision_result['boss_damage'] *= 5
    
    return collision_result

def get_cheat_mode_status():
    """Get current cheat mode status"""
    cheat = CheatMode()
    return {
        'active': cheat.cheat_active,
        'activation_time': cheat.cheat_activation_time,
        'duration': time.time() - cheat.cheat_activation_time if cheat.cheat_active else 0,
        'effects': {
            'infinite_health': cheat.cheat_active,
            'infinite_ammo': cheat.cheat_active,
            'super_speed': cheat.cheat_active,
            'invincible_planet': cheat.cheat_active,
            'qte_disabled': cheat.cheat_active
        }
    }

def reset_cheat_mode():
    """Reset cheat mode to initial state"""
    cheat = CheatMode()
    cheat.cheat_active = False
    cheat.cheat_activation_time = 0
    print("Cheat mode reset")
    return cheat
