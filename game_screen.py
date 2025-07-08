import fonts
from utils.center_text import center_text
from pygame import Rect
from pgzero import clock
from pgzero.actor import Actor
import math

WIDTH = 1280
HEIGHT = 720
UI_RESERVED_HEIGHT = 40  # espaço reservado pro HUD

thor = Actor("thor_idle")
thor.midbottom = (WIDTH // 2, HEIGHT // 2)
thor_max_health = 3
thor_current_health = thor_max_health

# 💥 Removido: agora usamos thor_world_y para coordenada vertical real
# thor_base_y = HEIGHT - 50
# thor_min_y = UI_RESERVED_HEIGHT + thor.height // 2
# thor_max_y = HEIGHT - thor.height // 2

FULLSCREEN = True
MAP_HEIGHT = 2800  # altura total do mapa
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
protagonist_float_phase = 0

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
    if protagonist_visible:
        protagonist_float_phase += 0.1

def draw_health(screen):
    for i in range(thor_current_health):
        x = 10 + i * 32
        y = 10
        screen.blit("heart", (x, y))

def draw_menu(screen):
    screen.fill((130, 219, 157))
    screen.draw.filled_rect(button_play, color=(226, 214, 214))
    fonts.on_game_text(screen, "Jogar", center=button_play.center)

    screen.draw.filled_rect(button_configuration, color=(226, 214, 214))
    fonts.on_game_text(screen, "Ajustes", center=button_configuration.center)
    
    screen.draw.filled_rect(button_exit, color=(226, 214, 214))
    fonts.on_game_text(screen, "Sair", center=button_exit.center)

def draw_game(screen):
    global camera_offset_y
    screen.clear()    
    screen.blit("test1", (0, -camera_offset_y))
    
    if primary_text_schedule:
        center_text(screen, "Tela de Jogo", WIDTH, HEIGHT, fontsize=40)
    
    if second_text_schedule:
        center_text(screen, "Você é o Thor, Deus do Trovão ou o Deus do Martelo?", WIDTH, HEIGHT, fontsize=20)

    if protagonist_visible:
        offset = math.sin(protagonist_float_phase) * 3
        # Ajuste: posição vertical baseada no centro da tela    
        thor_screen_y = HEIGHT // 2 + offset
        thor.midbottom = (thor.x, HEIGHT // 2 + offset)
        thor.draw()
        draw_health(screen)

def hide_primary_text_schedule():
    global primary_text_schedule
    primary_text_schedule = False

def hide_second_text_schedule():
    global second_text_schedule
    second_text_schedule = False
    clock.schedule(show_protagonist, 3.0)

def show_second_text_schedule():
    global second_text_schedule
    second_text_schedule = True
    clock.schedule(hide_second_text_schedule, 3.0)

def check_menu_click(pos):
    if button_play.collidepoint(pos):
        return "game"
    return "menu"
