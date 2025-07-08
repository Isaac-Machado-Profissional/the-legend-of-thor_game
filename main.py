import pgzrun
from pgzero import music
import game_screen
import movement

# Configurações iniciais
FULLSCREEN_OPTION = False
SCREEN_OPTION = "menu"
WIDTH = game_screen.WIDTH
HEIGHT = game_screen.HEIGHT




game_screen.primary_text_schedule = True

def update():
   
    if game_screen.protagonist_visible:
        movement.update_movement()
        game_screen.update_protagonist()
    
    MAP_HEIGHT = game_screen.MAP_HEIGHT

    ideal_offset = game_screen.thor_world_y - HEIGHT // 2
    min_offset = 0
    max_offset = MAP_HEIGHT - HEIGHT

    game_screen.camera_offset_y = max(min_offset, min(max_offset, ideal_offset))
            
   

def draw():
    if SCREEN_OPTION == "menu":
        game_screen.draw_menu(screen)
    elif SCREEN_OPTION == "game":
        game_screen.draw_game(screen)

def on_mouse_down(pos):
    global SCREEN_OPTION

    if SCREEN_OPTION == "menu":
        SCREEN_OPTION = game_screen.check_menu_click(pos)

        if SCREEN_OPTION == "game":
            music.play("soundtrack_02")
            music.set_volume(0.5)
            game_screen.primary_text_schedule = True
            game_screen.second_text_schedule = False

            # Oculta o texto inicial depois de 3 segundos
            clock.schedule(game_screen.hide_primary_text_schedule, 3.0)
            clock.schedule(game_screen.show_second_text_schedule, 3.0)

    if game_screen.button_exit.collidepoint(pos):
        exit()

def on_key_down(key):
    if key == keys.W:
        game_screen.movement["up"] = True
    if key == keys.S:
        game_screen.movement["down"] = True
    if key == keys.A:
        game_screen.movement["left"] = True
    if key == keys.D:
        game_screen.movement["right"] = True

def on_key_up(key):
    if key == keys.W:
        game_screen.movement["up"] = False
    if key == keys.S:
        game_screen.movement["down"] = False
    if key == keys.A:
        game_screen.movement["left"] = False
    if key == keys.D:
        game_screen.movement["right"] = False

pgzrun.go()
