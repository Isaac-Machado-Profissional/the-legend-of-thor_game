
import game_screen
from pgzero.builtins import keys
from game_screen import movement, movement_speed


def update_movement():
    if not game_screen.protagonist_visible:
        return

    if movement["up"]:
        game_screen.thor_base_y -= game_screen.movement_speed
        
    if movement["down"]:
        game_screen.thor_base_y += game_screen.movement_speed
        
    if movement["left"]:
        game_screen.thor.x -= game_screen.movement_speed
    
    if movement["right"]:
        game_screen.thor.x += game_screen.movement_speed

    if movement["up"] or movement["down"]:
        game_screen.protagonist_float_phase += 0.3 
    else:
        game_screen.protagonist_float_phase += 0.1
