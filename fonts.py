WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False

MODE_FONT = "bitcount"
MODE_FONTSIZE = 25

def on_game_text(screen, text, **kwargs):
    """
    Função para desenhar texto na tela do jogo.
    Ideia de ter um padrão de talvez aviso ao jogador, de possíveis eventos do jogo.
    Esta função centraliza o texto na tela e aplica parâmetros de fonte e cor.
    Os parâmetros adicionais podem ser passados como argumentos nomeados (kwargs).
    """
    paramms = {
        "fontname": MODE_FONT,
        "fontsize": MODE_FONTSIZE,
        "color": "black"
    }
    paramms.update(kwargs)
    screen.draw.text(text, (WIDTH // 2, HEIGHT // 2), anchor=(0.5, 0.5), **paramms)