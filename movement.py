# movement.py

import game_screen
from pgzero.builtins import keys
from game_screen import movement, movement_speed

def update_movement():
    if not game_screen.protagonist_visible:
        return

    thor = game_screen.thor
    half_width = thor.width // 2
    half_height = thor.height // 2

    # ✅ DEFINA OS LIMITES DO MAPA AQUI
    min_x = half_width
    max_x = game_screen.WIDTH - half_width
    min_y = 200 + half_height
    max_y = game_screen.MAP_HEIGHT - 200 - half_height

    # --- LÓGICA DE MOVIMENTO ---

    # Movimento horizontal
    if movement["left"]:
        thor.x -= movement_speed
        game_screen.last_direction = "left"  # CORRIGIDO
        if thor.x < min_x:
            thor.x = min_x
            
    if movement["right"]:
        thor.x += movement_speed
        game_screen.last_direction = "right" # CORRIGIDO
        if thor.x > max_x:
            thor.x = max_x

    # Movimento vertical
    if movement["up"]:
        game_screen.thor_world_y -= movement_speed
        game_screen.last_direction = "up" # CORRIGIDO
        if game_screen.thor_world_y < min_y:
            game_screen.thor_world_y = min_y
            
    if movement["down"]:
        game_screen.thor_world_y += movement_speed
        game_screen.last_direction = "down" # CORRIGIDO
        if game_screen.thor_world_y > max_y:
            game_screen.thor_world_y = max_y