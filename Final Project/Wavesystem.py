import time

start_time = time.time()
current_wave = 1
boss_spawned = False

def update_wave(enemies):
    global current_wave, boss_spawned

    elapsed = time.time() - start_time

    if elapsed < 20:
        current_wave = 1

    elif elapsed < 35:
        current_wave = 2
        for e in enemies:
            e["speed"] *= 2
            e["damage"] *= 2


    else:
        current_wave = 3
        if not boss_spawned:
            spawn_boss()
            boss_spawned = True


def spawn_boss():
    print("BOSS APPEARED!")

