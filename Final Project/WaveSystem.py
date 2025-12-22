import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *

class WaveSystem:
    def __init__(self):
        self.WAVE_1_START = 0
        self.WAVE_1_END = 20
        self.WAVE_2_START = 20
        self.WAVE_2_END = 35
        self.WAVE_3_START = 35
        self.WAVE_3_END = 60
        
        self.current_wave = 1
        self.wave_start_time = 0
        self.game_time = 0
        self.enemy_speed_multiplier = 1.0
        self.enemy_damage_multiplier = 1.0
        self.boss_spawned = False
        self.wave_active = True

def run_wave_system(enemy_list, ENEMY_SPEED, GRID_LEN, planet_attacker_list, 
                    initEnemies, initBoss, boss_active, boss_x, boss_y, 
                    boss_rot, boss_health, BOSS_HEALTH, player_x, player_y):
    """Main function to handle all wave system operations"""
    
    wave = WaveSystem()
    
    # Initialize if needed
    if wave.wave_start_time == 0:
        wave.wave_start_time = time.time()
    
    # Update game time
    wave.game_time = time.time() - wave.wave_start_time
    
    # Handle wave transitions and effects
    return handle_wave_transitions(wave, enemy_list, ENEMY_SPEED, planet_attacker_list, 
                                  initEnemies, initBoss, boss_active, boss_x, boss_y, 
                                  boss_rot, boss_health, BOSS_HEALTH, player_x, player_y)

def handle_wave_transitions(wave, enemy_list, ENEMY_SPEED, planet_attacker_list, 
                           initEnemies, initBoss, boss_active, boss_x, boss_y, 
                           boss_rot, boss_health, BOSS_HEALTH, player_x, player_y):
    """Handle all wave transitions and effects"""
    
    # Wave 1: 0-20 seconds
    if wave.current_wave == 1 and wave.game_time >= wave.WAVE_1_END:
        print("=== WAVE 2 STARTED! ===")
        print("- Enemies now have 2x movement speed")
        print("- Enemies now have 2x damage")
        wave.current_wave = 2
        wave.enemy_speed_multiplier = 2.0
        wave.enemy_damage_multiplier = 2.0
        
        # Apply speed boost to all existing enemies
        for enemy in enemy_list:
            # Enemies will move faster in the moveEnemies function using multiplier
            pass
            
        return {
            'wave': 2,
            'speed_multiplier': 2.0,
            'damage_multiplier': 2.0,
            'message': "WAVE 2: ENEMIES ENRAGED!"
        }
    
    # Wave 2: 20-35 seconds  
    elif wave.current_wave == 2 and wave.game_time >= wave.WAVE_2_END:
        print("=== FINAL WAVE STARTED! ===")
        print("- BOSS HAS APPEARED!")
        print("- No new regular enemies will spawn")
        print("- Planet hunters remain active")
        wave.current_wave = 3
        
        # No new regular enemies spawn in Wave 3
        # Boss will be activated separately
        
        return {
            'wave': 3,
            'spawn_boss': True,
            'no_new_enemies': True,
            'message': "FINAL WAVE: DEFEAT THE BOSS!"
        }
    
    # Wave 3: 35-60 seconds - Boss wave
    elif wave.current_wave == 3:
        # Check if time's up
        if wave.game_time >= wave.WAVE_3_END:
            return {
                'wave': 3,
                'time_up': True,
                'message': "TIME'S UP!"
            }
        
        # Check if boss should spawn
        if not wave.boss_spawned:
            wave.boss_spawned = True
            initBoss()
            return {
                'wave': 3,
                'boss_spawned': True,
                'boss_active': True,
                'message': "BOSS ENGAGED!"
            }
    
    # Return current wave status
    return {
        'wave': wave.current_wave,
        'game_time': wave.game_time,
        'time_remaining': get_time_remaining(wave),
        'total_time_remaining': wave.WAVE_3_END - wave.game_time,
        'speed_multiplier': wave.enemy_speed_multiplier,
        'damage_multiplier': wave.enemy_damage_multiplier,
        'boss_spawned': wave.boss_spawned,
        'allow_pickups': wave.current_wave < 3,
        'allow_health_pickups': wave.current_wave < 3,
        'allow_ammo_pickups': wave.current_wave < 3  # Will be overridden if mega weapon acquired
    }

def get_time_remaining(wave):
    """Get time remaining in current wave"""
    if wave.current_wave == 1:
        return max(0, wave.WAVE_1_END - wave.game_time)
    elif wave.current_wave == 2:
        return max(0, wave.WAVE_2_END - wave.game_time)
    elif wave.current_wave == 3:
        return max(0, wave.WAVE_3_END - wave.game_time)
    return 0

def draw_wave_hud(wave_status):
    """Draw all wave-related HUD elements"""
    
    # Draw wave number
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    glRasterPos2f(20, 980)
    wave_text = f"WAVE {wave_status['wave']}"
    for char in wave_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    
    # Draw time remaining
    glColor3f(1.0, 1.0, 1.0)  # White
    if wave_status['wave'] == 1:
        time_text = f"Next Wave: {int(wave_status['time_remaining'])}s"
        glRasterPos2f(20, 950)
    elif wave_status['wave'] == 2:
        time_text = f"BOSS IN: {int(wave_status['time_remaining'])}s (ENEMIES 2x!)"
        glRasterPos2f(20, 950)
    elif wave_status['wave'] == 3:
        time_text = f"TIME: {int(wave_status['total_time_remaining'])}s - DEFEAT BOSS!"
        glRasterPos2f(20, 950)
    
    for char in time_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
    
    # Draw wave-specific warnings
    if 'message' in wave_status:
        glColor3f(1.0, 0.5, 0.0)  # Orange
        glRasterPos2f(500, 950)
        for char in wave_status['message']:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    
    # Draw boss health bar if in wave 3
    if wave_status['wave'] == 3 and wave_status.get('boss_active', False):
        draw_boss_health_bar()

def draw_boss_health_bar():
    """Draw boss health bar at bottom of screen"""
    boss_health = 800  # This would come from your boss object
    max_health = 1000
    
    # Background
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(200, 50)
    glVertex2f(1050, 50)
    glVertex2f(1050, 80)
    glVertex2f(200, 80)
    glEnd()
    
    # Health fill
    health_percent = boss_health / max_health
    glColor3f(1.0, 0.0, 0.0)  # Red
    glBegin(GL_QUADS)
    glVertex2f(200, 50)
    glVertex2f(200 + 850 * health_percent, 50)
    glVertex2f(200 + 850 * health_percent, 80)
    glVertex2f(200, 80)
    glEnd()
    
    # Boss label
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(210, 60)
    boss_text = "BOSS"
    for char in boss_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
    
    # Health text
    health_text = f"{boss_health}/{max_health}"
    glRasterPos2f(900, 60)
    for char in health_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

def reset_wave_system():
    """Reset wave system to initial state"""
    wave = WaveSystem()
    wave.current_wave = 1
    wave.wave_start_time = time.time()
    wave.game_time = 0
    wave.enemy_speed_multiplier = 1.0
    wave.enemy_damage_multiplier = 1.0
    wave.boss_spawned = False
    wave.wave_active = True
    print("Wave system reset to Wave 1")
    return wave
