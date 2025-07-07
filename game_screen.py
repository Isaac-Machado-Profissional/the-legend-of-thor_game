import fonts
from utils.center_text import center_text
from pygame import Rect
from pgzero import clock
from pgzero.actor import Actor
import math

WIDTH = 600
HEIGHT = 400
FULLSCREEN = False


button_play = Rect((20, HEIGHT - 120), (140, 40))
button_ajustes = Rect((20, HEIGHT - 60), (140, 40))


primary_text_schedule = True
second_text_schedule = False
protagonist_visible = False
protagonist_float_phase = 0

thor = Actor("thor_idle")
thor.midbottom = (WIDTH // 2, HEIGHT //2)
thor_base_y = HEIGHT - 50  # valor global

movement = {
    "up": False,
    "down": False,
    "left": False,
    "right": False
}

movement_speed = 2

# Função para exibir o protagonista:
def show_protagonist():
    global protagonist_visible
    protagonist_visible = True


# Thor respirando:
def update_protagonist():
    global protagonist_float_phase
    if protagonist_visible:
        protagonist_float_phase += 0.1
        offset = math.sin(protagonist_float_phase) * 3
        thor.y = thor_base_y + offset

# Menu do jogo:
def draw_menu(screen):
    screen.fill((130, 219, 157))
    screen.draw.filled_rect(button_play, color=(226, 214, 214))
    fonts.on_game_text(screen, "Jogar", center=button_play.center)

    screen.draw.filled_rect(button_ajustes, color=(226, 214, 214))
    fonts.on_game_text(screen, "Ajustes", center=button_ajustes.center)
    

# Tela de jogo:
def draw_game(screen):
    screen.fill((130, 219, 157))
    
    if primary_text_schedule:
        # Chamando WIDTH e HEIGHT assim pois criei uma utils de center text
        center_text(screen, "Tela de Jogo", WIDTH, HEIGHT, fontsize=40 ) 
    
    if second_text_schedule: 
        center_text(screen, "Você é o Thor, Deus do Trovão ou o Deus do Martelo?", WIDTH, HEIGHT, fontsize=20)

    if protagonist_visible:
        thor.draw()

# Funções abaixo para controlar a visibilidade do texto, podendo intercalar para escrever na tela do jogo:
def hide_primary_text_schedule():
    global primary_text_schedule
    primary_text_schedule = False
    
def hide_second_text_schedule():
    global second_text_schedule
    second_text_schedule = False
    clock.schedule(show_protagonist, 3.0)  # Exibe o protagonista após 3 segundos
    
def show_second_text_schedule():
    global second_text_schedule
    second_text_schedule = True
    
    clock.schedule(hide_second_text_schedule, 3.0)
    
# Função para verificar o clique no menu:
def check_menu_click(pos):
    if button_play.collidepoint(pos):
        return "game"
    return "menu"