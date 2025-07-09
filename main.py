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

def update(dt):
    """
    Atualiza o estado do jogo
    """
    
    global SCREEN_OPTION

    # Se Pausado: não atualiza nada
    if SCREEN_OPTION in ["menu", "settings", "game_over", "paused"]:
        return

    if SCREEN_OPTION == "game":
        if game_screen.protagonist_visible:
            movement.update_movement()
            game_screen.update_protagonist()
            game_screen.update_enemies(dt)

        # Lógica da câmera
        MAP_HEIGHT = game_screen.MAP_HEIGHT
        ideal_offset = game_screen.thor_world_y - HEIGHT // 2
        min_offset = 0
        max_offset = MAP_HEIGHT - HEIGHT
        game_screen.camera_offset_y = max(min_offset, min(max_offset, ideal_offset))

        if game_screen.thor_current_health <= 0:
            SCREEN_OPTION = "game_over"
            music.fadeout(1.5)


        


def draw():
    """
    Define a tela atual do jogo.
    """
    
    if SCREEN_OPTION == "menu":
        game_screen.draw_menu(screen)
    elif SCREEN_OPTION == "game":
        game_screen.draw_game(screen)
    
    elif SCREEN_OPTION == "settings":
        game_screen.draw_settings(screen)
        
    elif SCREEN_OPTION == "game_over":
        game_screen.draw_game_over(screen)



def on_mouse_down(pos):
    """
    Quando o mouse é pressionado, verifica a posição do clique
    e executa a ação correspondente.
    """
    
    global SCREEN_OPTION

    # --- Lógica de clique para a TELA DE MENU ---
    if SCREEN_OPTION == "menu":
        # Pega o destino do clique ('game', 'settings' ou 'menu')
        destination = game_screen.check_menu_click(pos)
        
        # Se o destino for 'game', muda o estado e reseta o jogo
        if destination == "game":
            SCREEN_OPTION = "game"
            game_screen.reset_game()
            game_screen.primary_text_schedule = True
            game_screen.second_text_schedule = False
            clock.schedule(game_screen.hide_primary_text_schedule, 5)
            clock.schedule(game_screen.show_second_text_schedule, 10)
            
        # ✨ CORREÇÃO AQUI: Se o destino for 'settings', apenas muda o estado
        elif destination == "settings":
            SCREEN_OPTION = "settings"

    # --- Lógica de clique para a TELA DE AJUSTES ---
    elif SCREEN_OPTION == "settings":
        if game_screen.button_back_from_settings.collidepoint(pos):
            SCREEN_OPTION = "menu"
        if game_screen.button_mute_music.collidepoint(pos):
            game_screen.music_muted = not game_screen.music_muted
            if game_screen.music_muted:
                music.set_volume(0)
            else:
                music.set_volume(0.5)

    # --- Lógica de clique para a TELA DE GAME OVER ---
    elif SCREEN_OPTION == "game_over":
        if game_screen.button_retry.collidepoint(pos):
            SCREEN_OPTION = "game"
            game_screen.reset_game()
        if game_screen.button_back_to_menu.collidepoint(pos):
            SCREEN_OPTION = "menu"

    # --- Botão geral de SAIR (funciona em qualquer tela) ---
    if game_screen.button_exit.collidepoint(pos):
        exit()


    # Botão de sair geral
    if game_screen.button_exit.collidepoint(pos):
        exit()


    if game_screen.button_exit.collidepoint(pos):
        exit()

def on_key_down(key):
    """
    Quando uma tecla é pressionada, atualiza o movimento do personagem.
    Esta função é chamada quando uma tecla é pressionada.
    """
    
    if key == keys.W:
        game_screen.movement["up"] = True
    if key == keys.S:
        game_screen.movement["down"] = True
    if key == keys.A:
        game_screen.movement["left"] = True
    if key == keys.D:
        game_screen.movement["right"] = True

def on_key_up(key):
    """
    Quando uma tecla é solta, atualiza o movimento do personagem.
    Esta função é chamada quando uma tecla é solta.
    """
    
    if key == keys.W:
        game_screen.movement["up"] = False
    if key == keys.S:
        game_screen.movement["down"] = False
    if key == keys.A:
        game_screen.movement["left"] = False
    if key == keys.D:
        game_screen.movement["right"] = False

pgzrun.go()


