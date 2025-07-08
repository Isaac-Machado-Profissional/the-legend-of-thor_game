import game_screen
from pgzero.builtins import keys
from game_screen import movement, movement_speed

# Limites da área jogável (ajustado para considerar o mundo, não a tela)
def update_movement():
    if not game_screen.protagonist_visible:
        return

    thor = game_screen.thor
    half_width = thor.width // 2
    half_height = thor.height // 2

    # Limites do mapa
    min_x = half_width // 2
    max_x = game_screen.WIDTH - thor.width // 2

    min_y = 200 + half_height
    max_y = game_screen.MAP_HEIGHT - 200 - half_height

    # Movimento vertical com limite
    if movement["up"] and game_screen.thor_world_y - movement_speed >= min_y:
        game_screen.thor_world_y -= movement_speed
    elif movement["up"]:
        game_screen.thor_world_y = min_y

    if movement["down"] and game_screen.thor_world_y + movement_speed <= max_y:
        game_screen.thor_world_y += movement_speed
    elif movement["down"]:
        game_screen.thor_world_y = max_y

    # Movimento horizontal com limite
    if movement["left"] and thor.x - movement_speed >= min_x:
        thor.x -= movement_speed
        
    elif movement["left"]:
        thor.x = min_x

    if movement["right"] and thor.x + movement_speed <= max_x:
        thor.x += movement_speed
    elif movement["right"]:
        thor.x = max_x

    # Respiração
    if movement["up"] or movement["down"]:
        game_screen.protagonist_float_phase += 0.3
    else:
        game_screen.protagonist_float_phase += 0.1
