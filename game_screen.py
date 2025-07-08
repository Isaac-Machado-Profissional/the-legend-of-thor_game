import fonts
from utils.center_text import center_text
from pygame import Rect
from pgzero import clock
from pgzero.actor import Actor
import math

WIDTH = 1280
HEIGHT = 720
UI_RESERVED_HEIGHT = 40  # espaço reservado pro HUD

thor = Actor("thor/idle/down/thor_idle_down-0")
thor.midbottom = (WIDTH // 2, HEIGHT // 2)
thor_max_health = 3
thor_current_health = thor_max_health
thor_idle_down_frames = [f"thor/idle/down/thor_idle_down-{i}" for i in range(12)]
thor_idle_left_frames = [f"thor/idle/left/thor_idle_left-{i}" for i in range(11)] 
thor_idle_right_frames = [f"thor/idle/right/thor_idle_right-{i}" for i in range(11)]
thor_idle_up_frames = [f"thor/idle/up/thor_idle_up-{i}" for i in range(8)]

last_direction = "down"

# 💥 Removido: agora usamos thor_world_y para coordenada vertical real
# thor_base_y = HEIGHT - 50
# thor_min_y = UI_RESERVED_HEIGHT + thor.height // 2
# thor_max_y = HEIGHT - thor.height // 2

FULLSCREEN = True
MAP_HEIGHT = 2400  # altura total do mapa
camera_offset_y = 0

# Inicializa a posição vertical do personagem no mundo
thor_world_y = MAP_HEIGHT - HEIGHT // 2

# Botões do menu
button_play = Rect((20, HEIGHT - 180), (140, 40))
button_configuration = Rect((20, HEIGHT - 120), (140, 40))
button_exit = Rect((20, HEIGHT - 60), (140, 40))

# Estados do jogo
primary_text_schedule = True
second_text_schedule = False
protagonist_visible = False
protagonist_float_phase = 0.2

# Movimento do personagem
movement = {
    "up": False,
    "down": False,
    "left": False,
    "right": False
}

movement_speed = 2

def show_protagonist():
    global protagonist_visible
    protagonist_visible = True

def update_protagonist():
    global protagonist_float_phase
    if not protagonist_visible:
        return

    # Animação padrão: sempre virado para baixo/frente.
    active_animation = thor_idle_down_frames

    # VERIFICAÇÃO PRINCIPAL:
    # O código abaixo só é executado se o personagem estiver TOTALMENTE PARADO.
    if not movement["left"] and not movement["right"] and not movement["up"] and not movement["down"]:
        # Ok, ele está parado. AGORA SIM, vamos decidir para qual lado ele deve ficar olhando.
        if last_direction == "right":
            active_animation = thor_idle_right_frames
        elif last_direction == "left":
            active_animation = thor_idle_left_frames
        # ✨ NOVO: Adicione a condição para a direção "up"
        elif last_direction == "up":
            active_animation = thor_idle_up_frames
        # Se a última direção for "down" ou qualquer outra coisa, ele usa o padrão.

    # Roda a animação que foi escolhida
    protagonist_float_phase += 0.2
    frame_index = int(protagonist_float_phase) % max(1, len(active_animation))
    thor.image = active_animation[frame_index]


def draw_health(screen):
    for i in range(thor_current_health):
        x = 10 + i * 32
        y = 10
        screen.blit("ui/heart", (x, y))

def draw_menu(screen):
    screen.fill((130, 219, 157))
    screen.draw.filled_rect(button_play, color=(226, 214, 214))
    fonts.on_game_text(screen, "Jogar", center=button_play.center)

    screen.draw.filled_rect(button_configuration, color=(226, 214, 214))
    fonts.on_game_text(screen, "Ajustes", center=button_configuration.center)
    
    screen.draw.filled_rect(button_exit, color=(226, 214, 214))
    fonts.on_game_text(screen, "Sair", center=button_exit.center)

def draw_game(screen):
    global camera_offset_y # Não é mais necessário aqui se você não modificar
    screen.clear()
    screen.blit("background/map1", (0, -camera_offset_y))

    if primary_text_schedule:
        center_text(screen, "Tela de Jogo", WIDTH, HEIGHT, fontsize=40)
    
    if second_text_schedule:
        center_text(screen, "Você é o Thor, Deus do Trovão ou o Deus do Martelo?", WIDTH, HEIGHT, fontsize=20)

    if protagonist_visible:
        # NO MOMENTO DESATIVADO PULINHO DE ANIMAÇÃO ABAIXO:
        # float_offset = math.sin(protagonist_float_phase) * 3
        # ✨ CÁLCULO CORRETO DA POSIÇÃO NA TELA ✨
        # Posição no mundo - Posição da câmera + Efeito de flutuação
        thor_screen_y = thor_world_y - camera_offset_y # + float_offset
        
        # Define a posição do ator usando a coordenada de tela calculada
        thor.midbottom = (thor.x, thor_screen_y)
        thor.draw()
        draw_health(screen)
        
        

def hide_primary_text_schedule():
    global primary_text_schedule
    primary_text_schedule = False

def hide_second_text_schedule():
    global second_text_schedule
    second_text_schedule = False
    clock.schedule(show_protagonist, 0.0)

def show_second_text_schedule():
    global second_text_schedule
    second_text_schedule = True
    clock.schedule(hide_second_text_schedule, 3.0)

def check_menu_click(pos):
    if button_play.collidepoint(pos):
        return "game"
    return "menu"
