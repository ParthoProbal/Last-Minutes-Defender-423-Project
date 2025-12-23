import math

# Wave Variables
current_wave = 1
wave_started = False
WAVE1_END = 40  #40 # 0-40 seconds
WAVE2_END = 25 #25  # 40-25 seconds
WAVE3_END = 0   # 25-0 seconds
enemy_speed_multiplier = 1.0
enemy_damage_multiplier = 1.0
boss_active_wave3 = False

def updateWaveSystem(time_remaining):
    global current_wave, wave_started, enemy_speed_multiplier, enemy_damage_multiplier, boss_active_wave3
    
    # Calculate wave based on time remaining
    if time_remaining > WAVE1_END:
        new_wave = 1
        enemy_speed_multiplier = 1.0
        enemy_damage_multiplier = 1.0
    elif time_remaining > WAVE2_END:
        new_wave = 2
        enemy_speed_multiplier = 2.0  # 2x speed
        enemy_damage_multiplier = 2.0  # 2x damage
    else:
        new_wave = 3
        enemy_speed_multiplier = 2.0  # Keep 2x from wave 2
        enemy_damage_multiplier = 2.0  # Keep 2x from wave 2
        boss_active_wave3 = True
    
    # Check if wave changed
    if new_wave != current_wave:
        current_wave = new_wave
        wave_started = True
        print(f"WAVE {current_wave} STARTED!")
        
        if current_wave == 3:
            print("FINAL WAVE! BOSS INCOMING!")
    
    return current_wave

def getEnemySpeedMultiplier():
    return enemy_speed_multiplier

def getEnemyDamageMultiplier():
    return enemy_damage_multiplier

def getCurrentWave():
    return current_wave

def isBossWave():
    return current_wave == 3 and boss_active_wave3

def shouldSpawnPickups():
    # No pickups in wave 3 except mega power-ups
    return current_wave != 3

def getWaveDamage(enemy_type, base_damage):
    damage = base_damage * enemy_damage_multiplier
    
    if enemy_type == "shooter":
        return int(damage)
    elif enemy_type == "planet_attacker":
        return int(damage * 1.5)  # Planet attackers deal more damage
    elif enemy_type == "boss":
        return 200  # Boss bullet damage fixed at 200
    
    return int(damage)

def getWaveSpeed(base_speed):
    return base_speed * enemy_speed_multiplier

def resetWaveSystem():
    global current_wave, wave_started, enemy_speed_multiplier, enemy_damage_multiplier, boss_active_wave3
    
    current_wave = 1
    wave_started = False
    enemy_speed_multiplier = 1.0
    enemy_damage_multiplier = 1.0
    boss_active_wave3 = False