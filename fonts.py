WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False

MODE_FONT = "bitcount"
MODE_FONTSIZE = 25

def on_game_text(screen, text, **kwargs):
    paramms = {
        "fontname": MODE_FONT,
        "fontsize": MODE_FONTSIZE,
        "color": "black"
    }
    paramms.update(kwargs)
    screen.draw.text(text, (WIDTH // 2, HEIGHT // 2), anchor=(0.5, 0.5), **paramms)