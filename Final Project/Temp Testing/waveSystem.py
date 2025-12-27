# Wave Variables
current_wave = 1
wave_started = False
WAVE1_END = 40
WAVE2_END = 25
WAVE3_END = 0
enemy_speed_multiplier = 1.0
enemy_damage_multiplier = 1.0
boss_active_wave3 = False

# Add pause variable
wave_paused = False

def updateWaveSystem(time_remaining):
    global current_wave, wave_started, enemy_speed_multiplier, enemy_damage_multiplier, boss_active_wave3
    global wave_paused
    
    # Don't update if paused
    if wave_paused:
        return current_wave
    
    # Your existing wave logic...
    if time_remaining > WAVE1_END:
        new_wave = 1
        enemy_speed_multiplier = 1.0
        enemy_damage_multiplier = 1.0
    elif time_remaining > WAVE2_END:
        new_wave = 2
        enemy_speed_multiplier = 2.0
        enemy_damage_multiplier = 2.0
    else:
        new_wave = 3
        enemy_speed_multiplier = 2.0
        enemy_damage_multiplier = 2.0
        boss_active_wave3 = True
    
    if new_wave != current_wave:
        current_wave = new_wave
        wave_started = True
        print(f"WAVE {current_wave} STARTED!")
        
        if current_wave == 3:
            print("FINAL WAVE! BOSS INCOMING!")
    
    return current_wave

# Add pause functions
def pauseWaveSystem():
    global wave_paused
    wave_paused = True

def resumeWaveSystem():
    global wave_paused
    wave_paused = False

def isWavePaused():
    return wave_paused

# Keep all other existing functions as is...
def getEnemySpeedMultiplier():
    return enemy_speed_multiplier

def getEnemyDamageMultiplier():
    return enemy_damage_multiplier

def getCurrentWave():
    return current_wave

def isBossWave():
    return current_wave == 3 and boss_active_wave3

def shouldSpawnPickups():
    # No pickups in wave 3, and check pause
    if wave_paused:
        return False
    return current_wave != 3

def getWaveDamage(enemy_type, base_damage):
    if wave_paused:
        return base_damage
        
    damage = base_damage * enemy_damage_multiplier
    
    if enemy_type == "shooter":
        return int(damage)
    elif enemy_type == "planet_attacker":
        return int(damage * 1.5)
    elif enemy_type == "boss":
        return 200
    
    return int(damage)

def getWaveSpeed(base_speed):
    if wave_paused:
        return base_speed
    return base_speed * enemy_speed_multiplier

def resetWaveSystem():
    global current_wave, wave_started, enemy_speed_multiplier, enemy_damage_multiplier, boss_active_wave3
    global wave_paused
    
    current_wave = 1
    wave_started = False
    enemy_speed_multiplier = 1.0
    enemy_damage_multiplier = 1.0
    boss_active_wave3 = False
    wave_paused = False
