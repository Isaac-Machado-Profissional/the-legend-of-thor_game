WIDTH = 600
HEIGHT = 400
FULLSCREEN = False
MODE_FONT = "bitcount"
MODE_FONTSIZE = 25

SCREEN_OPTION = "menu"

button_play = Rect((20, HEIGHT - 120), (140, 40))
button_ajustes = Rect((20, HEIGHT - 60), (140, 40))

def onGameText(text, **kwargs):
    paramms = {
        "fontname": MODE_FONT,
        "fontsize": MODE_FONTSIZE,
        "color": "black"
    }
    paramms.update(kwargs)
    screen.draw.text(text, (WIDTH // 2, HEIGHT // 2), anchor=(0.5, 0.5), **paramms)

def draw():
    screen.fill((130, 219, 157))

    if SCREEN_OPTION == "menu":
        screen.draw.filled_rect(button_play, color=(226, 214, 214))
        onGameText("Jogar", center=button_play.center)

        screen.draw.filled_rect(button_ajustes, color=(226, 214, 214))
        onGameText("Ajustes", center=button_ajustes.center)

    elif SCREEN_OPTION == "game":
        onGameText("Tela de Jogo", center=(WIDTH // 2, HEIGHT // 2), fontsize=40)

def on_mouse_down(pos):
    global SCREEN_OPTION
    if SCREEN_OPTION == "menu":
        if button_play.collidepoint(pos):
            SCREEN_OPTION = "game"
