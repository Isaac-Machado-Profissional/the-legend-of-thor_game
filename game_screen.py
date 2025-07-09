import math
from pygame import Rect
from pgzero import clock
from pgzero.actor import Actor
from pgzero import music

import fonts
from utils.center_text import center_text
from enemy import Mushroom

WIDTH = 1280
HEIGHT = 720
UI_RESERVED_HEIGHT = 40  # espaço reservado pro HUD
FULLSCREEN = True
MAP_HEIGHT = 2400  # altura total do mapa
camera_offset_y = 0

# Inicializa o Thor(protagonista):
thor = Actor("thor/idle/down/thor_idle_down-0")
thor.midbottom = (WIDTH // 2, HEIGHT // 2)
thor_world_y = MAP_HEIGHT - HEIGHT // 2 # Inicializa a posição vertical do personagem no mundo
thor_max_health = 3
thor_current_health = thor_max_health

# Idle animations:
thor_idle_down_frames = [f"thor/idle/down/thor_idle_down-{i}" for i in range(12)]
thor_idle_left_frames = [f"thor/idle/left/thor_idle_left-{i}" for i in range(11)] 
thor_idle_right_frames = [f"thor/idle/right/thor_idle_right-{i}" for i in range(11)]
thor_idle_up_frames = [f"thor/idle/up/thor_idle_up-{i}" for i in range(8)]
last_direction = "down"
# Run animations:
thor_run_down_frames = [f"thor/run/down/thor_run_down-{i}" for i in range(7)]
thor_run_up_frames = [f"thor/run/up/thor_run_up-{i}" for i in range(7)]
thor_run_left_frames = [f"thor/run/left/thor_run_left-{i}" for i in range(9)]
thor_run_right_frames = [f"thor/run/right/thor_run_right-{i}" for i in range(9)]

def generate_initial_enemies():
    """
    Cria e retorna uma lista de inimigos em posições predefinidas.
    """
    return [
        Mushroom(x=WIDTH // 2 + 200, y=MAP_HEIGHT - HEIGHT // 2),
        Mushroom(x=WIDTH // 2 - 50, y=MAP_HEIGHT - HEIGHT // 2 + 50),
        Mushroom(x=WIDTH // 2 - 100, y=MAP_HEIGHT - HEIGHT // 2 + 80),
        Mushroom(x=WIDTH // 2 - 40, y=MAP_HEIGHT - HEIGHT // 2 + 1500),
        Mushroom(x=WIDTH // 2 - 25, y=MAP_HEIGHT - HEIGHT // 2 + 900),
        Mushroom(x=WIDTH // 2 - 30, y=MAP_HEIGHT - HEIGHT // 2 + 2000),
        
    ]

enemies = generate_initial_enemies()

# Botões do menu
button_play = Rect((20, HEIGHT - 180), (140, 40))
button_configuration = Rect((20, HEIGHT - 120), (140, 40))
button_back_from_settings = Rect((20, 20), (140, 40))
button_mute_music = Rect((WIDTH/2 - 150, HEIGHT/2), (300, 50))
button_exit = Rect((20, HEIGHT - 60), (140, 40))
button_retry = Rect((WIDTH/2 - 150, HEIGHT/2 + 20), (300, 50))
button_back_to_menu = Rect((WIDTH/2 - 150, HEIGHT/2 + 80), (300, 50))

# Estados do jogo
primary_text_schedule = True
second_text_schedule = False
protagonist_visible = False
protagonist_float_phase = 0.2
music_muted = False

# Movimento do personagem
movement = {
    "up": False,
    "down": False,
    "left": False,
    "right": False
}

movement_speed = 2


def show_protagonist():
    """
    Mostra o protagonista na tela.
    """
    global protagonist_visible
    protagonist_visible = True

def update_protagonist():
    """
    Atualiza o estado da animação do protagonista.
    Esta função verifica o estado do movimento e atualiza a animação do Thor de acordo.
    """
    
    global protagonist_float_phase
    if not protagonist_visible:
        return

    active_animation = None
    animation_speed = 0.2  # Velocidade padrão para animação idle

    # --- LÓGICA DE SELEÇÃO DE ANIMAÇÃO ---
    #  Verifica primeiro se o personagem está se MOVENDO
    if movement["down"]:
        active_animation = thor_run_down_frames
        animation_speed = 0.2 # Animação de caminhada é mais rápida
    elif movement["up"]:
        active_animation = thor_run_up_frames
        animation_speed = 0.2
    elif movement["left"]:
        active_animation = thor_run_left_frames
        animation_speed = 0.2
    elif movement["right"]:
        active_animation = thor_run_right_frames
        animation_speed = 0.2
    
    # Se NENHUMA tecla de movimento está pressionada, usa a animação IDLE
    else:
        if last_direction == "down":
            active_animation = thor_idle_down_frames
        elif last_direction == "up":
            active_animation = thor_idle_up_frames
        elif last_direction == "left":
            active_animation = thor_idle_left_frames
        elif last_direction == "right":
            active_animation = thor_idle_right_frames
    
    # Garante que sempre haja uma animação para evitar erros
    if active_animation is None:
        active_animation = thor_idle_down_frames

    # --- ATUALIZA O FRAME DA ANIMAÇÃO ESCOLHIDA ---
    protagonist_float_phase += animation_speed
    frame_index = int(protagonist_float_phase) % len(active_animation)
    thor.image = active_animation[frame_index]


def draw_health(screen):
    """
    Desenhar a barra de vida do Thor.
    """
    for i in range(thor_current_health):
        x = 10 + i * 32
        y = 10
        screen.blit("ui/heart", (x, y))


def update_enemies(dt):
    """
    Atualize a lógica dos inimigos.
    Esta função percorre a lista de inimigos, atualizando sua lógica e verificando se o personagem foi atingido.
    """
    global thor_current_health
    
    for enemy in enemies:
        # ALTERAÇÃO AQUI: Passe 'thor_world_y' como um argumento extra
        damage_dealt = enemy.update(dt, thor, thor_world_y)
        
        if damage_dealt > 0:
            thor_current_health -= damage_dealt
            if thor_current_health < 0:
                thor_current_health = 0


def draw_menu(screen):
    """ 
    Desenhar tela de menu.
    Esta função exibe os botões de jogar, ajustes e sair.
    """
    screen.blit("background/map1", (0, -camera_offset_y))

    screen.draw.filled_rect(button_play, color=(226, 214, 214))
    fonts.on_game_text(screen, "Jogar", center=button_play.center)

    screen.draw.filled_rect(button_configuration, color=(226, 214, 214))
    fonts.on_game_text(screen, "Ajustes", center=button_configuration.center)
    
    screen.draw.filled_rect(button_exit, color=(226, 214, 214))
    fonts.on_game_text(screen, "Sair", center=button_exit.center)


def draw_settings(screen):
    """ 
    Desenhar tela de ajustes.
    Esta função exibe os botões de voltar e de ligar/desligar a música.
    """
    screen.blit("background/map1", (0, -camera_offset_y))

    center_text(screen, "Ajustes", WIDTH, 100, fontsize=60) # Ajustei a altura do texto
    
    screen.draw.filled_rect(button_back_from_settings, color=(226, 214, 214))
    fonts.on_game_text(screen, "Voltar", center=button_back_from_settings.center)
    
    screen.draw.filled_rect(button_mute_music, color=(226, 214, 214))
    if music_muted:
        fonts.on_game_text(screen, "Ligar música", center=button_mute_music.center)
    else:
        fonts.on_game_text(screen, "Desligar música", center=button_mute_music.center)
    
    
def draw_game(screen):
    """
    Desenhar tela do jogo.
    Esta função desenha o fundo, o Thor e os inimigos na tela.
    """

    global camera_offset_y
    screen.clear()
    screen.blit("background/map1", (0, -camera_offset_y))

    # Desenha os textos da interface
    if primary_text_schedule:
        center_text(screen, "Midgard", WIDTH, HEIGHT, fontsize=40)
    if second_text_schedule:
        center_text(screen, "Você é o Thor, Deus do Trovão ou o Deus do Martelo?", WIDTH, HEIGHT, fontsize=20)

    # Apenas desenha os personagens se eles estiverem visíveis
    if protagonist_visible:
        # Calcula a posição do Thor na tela
        thor_screen_y = thor_world_y - camera_offset_y
        thor.midbottom = (thor.x, thor_screen_y)
        
        # Desenha o Thor e a vida
        thor.draw()
        draw_health(screen)
        
        # ✨ CORREÇÃO AQUI: Este laço agora desenha os inimigos ✨
        for enemy in enemies:
            enemy.draw(screen, camera_offset_y)



# Game over tela
def draw_game_over(screen):
    """
    Desenha a tela do Game Over.
    Esta função exibe uma mensagem de Game Over e botões para reiniciar ou voltar ao menu.
    """
    # Primeiro, desenha o estado final do jogo para ficar de fundo
    draw_game(screen)
    
    # O último número (150) é o nível de transparência
    overlay = Rect(0, 0, WIDTH, HEIGHT)
    screen.draw.filled_rect(overlay, (180, 0, 0, 50))
    
    center_text(screen, "Você Morreu", WIDTH, HEIGHT - 100, fontsize=100)
    
    # Desenha os botões
    screen.draw.filled_rect(button_retry, color=(226, 214, 214))
    fonts.on_game_text(screen, "Tentar Novamente", center=button_retry.center, fontsize=30)

    screen.draw.filled_rect(button_back_to_menu, color=(226, 214, 214))
    fonts.on_game_text(screen, "Voltar ao Menu", center=button_back_to_menu.center, fontsize=30)


def reset_game():
    """
    Começar novamente o jogo.
    """
    global thor_current_health, thor_world_y, enemies
    
    # Reseta a vida do Thor
    thor_current_health = thor_max_health
    
    # Reseta a posição do Thor
    thor_world_y = MAP_HEIGHT - HEIGHT // 2
    thor.pos = (WIDTH // 2, HEIGHT // 2)
    
    # Reseta os inimigos para suas posições iniciais (recriando a lista)
    enemies = generate_initial_enemies()
    
    # Reinicia a música do jogo
    if not music_muted:
        music.play("soundtrack_02")
        music.set_volume(0.5)
    else:
        music.stop()


def hide_primary_text_schedule():
    """
    Esconde o texto inicial da tela(MIDGARD).
    """
    
    global primary_text_schedule
    primary_text_schedule = False

def hide_second_text_schedule():
    """
    Esconde o segundo texto da tela, dando indício ao nome da possível missão.
    """
    
    global second_text_schedule
    second_text_schedule = False
    clock.schedule(show_protagonist, 0.2)

def show_second_text_schedule():
    global second_text_schedule
    second_text_schedule = True
    clock.schedule(hide_second_text_schedule, 10.0)


def check_menu_click(pos):
    if button_play.collidepoint(pos):
        return "game"
    
    if button_configuration.collidepoint(pos):
        return "settings" 
        
    return "menu"