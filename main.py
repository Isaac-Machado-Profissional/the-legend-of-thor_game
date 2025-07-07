import game_screen

SCREEN_OPTION = "menu"
WIDTH = game_screen.WIDTH
HEIGHT = game_screen.HEIGHT

game_screen.primary_text_schedule = True

def update():
    if game_screen.protagonist_visible:
        game_screen.update_protagonist()

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
            game_screen.primary_text_schedule = True
            game_screen.second_text_schedule = False

            # Oculta o texto inicial depois de 3 segundos (opcional)
            clock.schedule(game_screen.hide_primary_text_schedule, 3.0)

            # Exibe a pergunta depois de 3 segundos
            clock.schedule(game_screen.show_second_text_schedule, 3.0)
            