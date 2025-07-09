import math
from pgzero.actor import Actor

class Mushroom:
    def __init__(self, x, y):
        # --- CARREGANDO OS FRAMES ---
        self.idle_frames = [f"enemy/mushroom/idle/mushroom_idle-{i}" for i in range(1, 7)]
        # NOVO: Carrega os frames de ataque. Ajuste o range se necessário.
        self.attack_frames = [f"enemy/mushroom/attack/mushroom_attack-{i}" for i in range(1, 9)] # Ex: 8 frames de ataque

        # O ator começa com a animação idle
        self.actor = Actor(self.idle_frames[0])

        # --- CONTROLE DE ESTADO E ANIMAÇÃO ---
        self.state = 'perseguindo'  # Estados possíveis: 'perseguindo', 'atacando'
        self.current_frame = 0
        self.animation_interval = 0.15
        self.frame_timer = self.animation_interval

        # Atributos de Posição e Combate
        self.world_x = x
        self.world_y = y
        self.speed = 40
        self.attack_range = 50
        self.attack_damage = 1
        self.attack_cooldown = 2.0
        self.attack_timer = 0.0

    def update(self, dt, player_actor, player_world_y):
        """Função principal que delega a lógica baseada no estado atual."""
        damage_dealt = 0
        if self.state == 'perseguindo':
            self.update_perseguindo_state(dt, player_actor, player_world_y)
        elif self.state == 'atacando':
            damage_dealt = self.update_atacando_state(dt)
        
        return damage_dealt

    def update_perseguindo_state(self, dt, player_actor, player_world_y):
        """Lógica para quando o inimigo está perseguindo ou em idle."""
        # Animação idle
        self.frame_timer -= dt
        if self.frame_timer <= 0:
            self.frame_timer = self.animation_interval
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.actor.image = self.idle_frames[self.current_frame]

        if self.attack_timer > 0:
            self.attack_timer -= dt

        # Lógica de movimento
        player_world_x = player_actor.x
        distance_x = player_world_x - self.world_x
        distance_y = player_world_y - self.world_y
        distance = math.hypot(distance_x, distance_y)

        if distance > self.attack_range:
            if distance > 0:
                direction_x = distance_x / distance
                direction_y = distance_y / distance
            else:
                direction_x, direction_y = 0, 0
            self.world_x += direction_x * self.speed * dt
            self.world_y += direction_y * self.speed * dt
        # Se estiver no alcance e puder atacar, MUDA O ESTADO para 'atacando'
        elif self.attack_timer <= 0:
            self.state = 'atacando'
            self.current_frame = 0  # Reseta o frame para o início da animação de ataque
            self.actor.image = self.attack_frames[self.current_frame] # Mostra o 1º frame do ataque

    def update_atacando_state(self, dt):
        """Lógica para quando o inimigo está executando a animação de ataque."""
        damage_this_frame = 0
        
        self.frame_timer -= dt
        if self.frame_timer <= 0:
            self.frame_timer = self.animation_interval
            self.current_frame += 1

            # Verifica se a animação de ataque terminou
            if self.current_frame >= len(self.attack_frames):
                self.state = 'perseguindo'  # Volta ao estado de perseguição
                self.current_frame = 0    # Reseta o frame para a animação idle
                self.attack_timer = self.attack_cooldown # Inicia o cooldown principal
                self.actor.image = self.idle_frames[self.current_frame]
            else:
                # Causa dano em um frame específico da animação (ex: no 4º frame)
                if self.current_frame == 4:
                    damage_this_frame = self.attack_damage
                
                # Atualiza para o próximo frame da animação de ataque
                self.actor.image = self.attack_frames[self.current_frame]
        
        return damage_this_frame

    def draw(self, screen, camera_offset_y):
        enemy_screen_y = self.world_y - camera_offset_y
        self.actor.pos = (self.world_x, enemy_screen_y)
        if self.actor.bottom > 0 and self.actor.top < screen.height:
            self.actor.draw()