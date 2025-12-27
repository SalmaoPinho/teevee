import pygame
from config import DEFS

SCREEN = None
SHEET = None
PROPSYS = None
SPRITE_LOADER = None
crt_texture = None

def init_graphics(screen, sheet, propsys,glock):
    global SCREEN, SHEET, PROPSYS, SPRITE_LOADER, crt_texture, crt_overlay, GLOCK
    SCREEN = screen
    SHEET = sheet
    GLOCK = glock
    PROPSYS = propsys
    SPRITE_LOADER = spriteLoader()
    crt_overlay = pygame.Surface((int(DEFS['width']), int(DEFS['height'])), pygame.SRCALPHA)
    SPRITE_LOADER.create_sprite(
    key="crt_frame",
    position=(101, 0),
    size=(16, 16),
    scale=DEFS["crtsize"]/16,
    alpha=50
    )
    # Carrega sprites de controle
    SPRITE_LOADER.create_sprite(
    key="skip",
    position=(23, 0),
    size=(19, 17),
    scale=1,
    )
    SPRITE_LOADER.create_sprite(
    key="back",
    position=(23, 0),
    size=(19, 17),
    scale=1,
    angle=180
    )
    SPRITE_LOADER.create_sprite(
    key="play",
    position=(0, 37),
    size=(13, 13),
    )
    SPRITE_LOADER.create_sprite(
    key="pause",
    position=(25, 19),
    size=(13, 15),
    scale=1,
    )
    
    # Sprites de clima
    SPRITE_LOADER.create_sprite(
    key="temperature",
    position=(43, 26),
    size=(11, 27),
    )
    SPRITE_LOADER.create_sprite(
    key="disk",
    position=(43, 0),
    size=(25, 25),
    )
    SPRITE_LOADER.create_sprite(
    key="ram",
    position=(69, 0),
    size=(32, 19),
    angle=90,
    )
    SPRITE_LOADER.create_sprite(
    key="net",
    position=(15, 36),
    size=(29, 24),
    )
    SPRITE_LOADER.create_sprite(
    key="sun",
    position=(55, 25),
    size=(49, 50),
    )
    SPRITE_LOADER.create_sprite(
    key="water",
    position=(108, 34),
    size=(20, 32),
    )
    SPRITE_LOADER.create_sprite(
    key="shuffle",
    position=(117, 0),
    size=(42, 34),
    angle=90,
    )
    
    return SPRITE_LOADER

class spriteLoader:
    def __init__(self):
        self.sprites = {}
        # Assume que deveria ser o PROPSYS global
        
    def create_sprite(self, key, position, size, scale=1.0, alpha=255, angle=0):
        x, y = position
        width, height = size
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(SHEET, (0, 0), (x, y, width, height))
        if angle != 0:
            sprite = pygame.transform.rotate(sprite, angle)
        if scale != 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            sprite = pygame.transform.scale(sprite, (new_width, new_height))
        if alpha != 255:
            sprite.set_alpha(alpha)
        self.sprites[key] = {
            "sprite": sprite,
            "size": (width, height),
            "position": position,
            "scale": scale,
            "alpha": alpha
            }
        return sprite
    
    def draw_sprite_proportional(self, key, x_percent, y_percent):
        """Desenha sprite usando coordenadas proporcionais"""
        if not PROPSYS:
            print("Erro: Sistema proporcional não configurado")
            return False
            
        sprite = self.sprites.get(key)
        if sprite:
            x = PROPSYS.percent_to_px_x(x_percent)
            y = PROPSYS.percent_to_px_y(y_percent)
            SCREEN.blit(sprite['sprite'], (x, y))
            return True
        return False
    def draw_sprite_centered(self, key, x_percent=0.5, y_percent=0.5):
        """Desenha sprite centralizado nas coordenadas proporcionais"""
        sprite = self.sprites.get(key)["sprite"]
        if sprite:
            x = PROPSYS.percent_to_px_x(x_percent) - sprite.get_width() // 2
            y = PROPSYS.percent_to_px_y(y_percent) - sprite.get_height() // 2
            SCREEN.blit(sprite, (x, y))
            return True
        return False
    def draw_relative_to_sprite(self, key,startpos,size,color=(255,255,255),outlines=0):
        # Calcula a posição do frame na tela (centralizado)
        dic=self.sprites.get(key)
        sprite = dic["sprite"]
        frame_width = sprite.get_width()
        frame_height = sprite.get_height()
        frame_x = PROPSYS.percent_to_px_x(DEFS['center_x']) - frame_width // 2
        frame_y = PROPSYS.percent_to_px_y(DEFS['center_y']) - frame_height // 2
        
        # Calcula a posição do retângulo relativa ao frame
        sprite_width,sprite_height = dic["size"]
        rect_x = frame_x + (startpos[0]/sprite_width * frame_width)
        rect_y = frame_y + (startpos[1]/sprite_height * frame_height)
        rect_width = size[0]/sprite_width * frame_width
        rect_height = size[1]/sprite_height * frame_height
        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        pygame.draw.rect(SCREEN, color, rect)       
        
        if outlines:
            startpos=(startpos[0],startpos[1]-1)
            size=(size[0],size[1])
            self.draw_relative_to_sprite(key,startpos,size,color=(0,0,0))  
        return True
    def draw_overlay(self,key):
        sprite = self.sprites.get(key)["sprite"]
        for y in range(0, int(DEFS['height']),int(DEFS['crtsize'])):
            for x in range(0, int(DEFS['width']),int(DEFS['crtsize'])):
                SCREEN.blit(sprite, (x, y))
                        
    def get_sprite(self, key):
        return self.sprites.get(key)

class TeeVee:
    def __init__(self):
        scal=DEFS["width"]/150
        SPRITE_LOADER.create_sprite(
            key="frame",
            position=(0, 0),
            size=(22, 36),
            scale=scal
        )
        SPRITE_LOADER.create_sprite(
            key="mouth_smile",
            position=(161, 0),
            size=(10, 3),
            scale=scal

        )
        SPRITE_LOADER.create_sprite(
            key="mouth_open",
            position=(161, 3),
            size=(10, 3),
            scale=scal

        )
        SPRITE_LOADER.create_sprite(
            key="mouth_sad",
            position=(161, 6),
            size=(10, 3),
            scale=scal

        )
        SPRITE_LOADER.create_sprite(
            key="mouth_frown",
            position=(161, 9),
            size=(10, 3),
            scale=scal

        )
        SPRITE_LOADER.create_sprite(
            key="mouth_skeptic",
            position=(161, 12),
            size=(10, 3),
            scale=scal
        )
        SPRITE_LOADER.create_sprite(
            key="mouth_midopen",
            position=(161, 15),
            size=(10, 3),
            scale=scal
        )
        SPRITE_LOADER.create_sprite(
            key="eye_open",
            position=(171, 0),
            size=(3, 5),
            scale=scal
        )
        SPRITE_LOADER.create_sprite(
            key="eye_angry",
            position=(171, 5),
            size=(3, 5),
            scale=scal
        )
        SPRITE_LOADER.create_sprite(
            key="eye_closed",
            position=(171, 0),
            size=(3, 1),
            scale=scal
        )
        self.eyes = "eye_closed"
        self.mouth = "mouth_smile"
        # Sistema de animação de fala
        self.x_percent = 0.5
        self.y_percent = 0.35
        self.is_talking = False
        self.talk_text = ""
        self.talk_index = 0
        self.talk_timer = 0
        self.mouth_open = False
        self.frame_offset_y = 0  # Offset vertical para movimento do frame
        self.letter_duration = 100  # Milissegundos por letra
        
        # Sistema de movimento dos olhos (segue o mouse)
        self.eye_offset_x = 0  # Offset horizontal dos olhos (-1, 0, 1)
        self.eye_offset_y = 0  # Offset vertical dos olhos (-1, 0, 1)
        
        # Sistema de detecção de movimento frenético (tontura)
        self.mouse_movements = []  # Lista de posições recentes do mouse
        self.is_dizzy = False  # Se está tonto
        self.dizzy_timer = 0  # Timer para duração da tontura
        self.dizzy_duration = 3000  # Fica tonto por 3 segundos
        self.movement_threshold = 10  # Número de movimentos rápidos para ficar tonto (reduzido de 15)
        
    def start_talking(self, text):
        """Inicia a animação de fala com o texto fornecido"""
        self.is_talking = True
        self.talk_text = text
        self.talk_index = 0
        self.talk_timer = pygame.time.get_ticks()
        self.mouth = "mouth_open"
        
    def update(self):
        """Atualiza a animação de fala e movimento dos olhos"""
        # Atualiza animação de fala
        if self.is_talking:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.talk_timer
            
            if elapsed >= self.letter_duration:
                self.talk_timer = current_time
                self.talk_index += 1
                
                self.mouth_open = not self.mouth_open
                
                if self.mouth_open:
                    self.frame_offset_y = -2
                else:
                    self.frame_offset_y = 2
                
                if self.talk_index >= len(self.talk_text):
                    self.is_talking = False
                    self.mouth_open = False
                    self.frame_offset_y = 0
                    self.mouth = "mouth_smile"
        else:
            self.frame_offset_y = 0
        
        # Atualiza movimento dos olhos para seguir o mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen_width = DEFS['width']
        screen_height = DEFS['height']
        
        # Calcula posição do TeeVee na tela
        tv_x = self.x_percent * screen_width
        tv_y = self.y_percent * screen_height
        
        # Calcula diferença entre mouse e TeeVee
        dx = mouse_x - tv_x
        dy = mouse_y - tv_y
        
        # Detecta movimento frenético do mouse
        current_time = pygame.time.get_ticks()
        
        # Adiciona posição atual à lista com timestamp
        self.mouse_movements.append((mouse_x, mouse_y, current_time))
        
        # Remove movimentos antigos (mais de 1 segundo)
        self.mouse_movements = [(x, y, t) for x, y, t in self.mouse_movements if current_time - t < 1000]
        
        # Verifica se há movimento frenético (muitas mudanças de direção)
        if len(self.mouse_movements) >= self.movement_threshold and not self.is_dizzy:
            # Calcula distância total percorrida
            total_distance = 0
            for i in range(1, len(self.mouse_movements)):
                x1, y1, _ = self.mouse_movements[i-1]
                x2, y2, _ = self.mouse_movements[i]
                total_distance += abs(x2 - x1) + abs(y2 - y1)
            
            # Se percorreu muita distância em pouco tempo, fica tonto
            # Reduzido de 2x para 1x a largura da tela
            if total_distance > screen_width * 2.0:
                self.is_dizzy = True
                
                self.dizzy_timer = current_time
                self.mouse_movements = []  # Limpa lista
                print(f"🌀 TeeVee ficou TONTO! Distância: {total_distance:.0f}px")
        
        # Verifica se deve sair do estado tonto
        if self.is_dizzy and current_time - self.dizzy_timer >= self.dizzy_duration:
            self.is_dizzy = False
        
        # Se está tonto, não segue o mouse (olhos ficam parados com raiva)
        if not self.is_dizzy:
            # Define offset horizontal baseado na posição do mouse
            # Divide a tela em 3 zonas: esquerda (-1), centro (0), direita (1)
            if dx < -screen_width * 0.15:  # Mouse à esquerda
                self.eye_offset_x = -1
            elif dx > screen_width * 0.15:  # Mouse à direita
                self.eye_offset_x = 1
            else:  # Mouse no centro
                self.eye_offset_x = 0
            
            # Define offset vertical baseado na posição do mouse
            # Divide a tela em 3 zonas: cima (-1), centro (0), baixo (1)
            if dy < -screen_height * 0.15:  # Mouse acima
                self.eye_offset_y = -1
            elif dy > screen_height * 0.15:  # Mouse abaixo
                self.eye_offset_y = 1
            else:  # Mouse no centro
                self.eye_offset_y = 0
                
    def draw(self,x_percent,y_percent):
        # Calcula offset Y baseado na animação
        center_y = y_percent
        center_x = x_percent
        if self.is_talking:
            # Adiciona pequeno offset durante a fala
            center_y += self.frame_offset_y / 1000.0  # Converte para porcentagem
        
        # Frame
        SPRITE_LOADER.draw_sprite_centered("frame", x_percent, center_y)
        
        # Olhos com movimento horizontal
        center_y += 0.058
        
        # Se está tonto, usa olhos de raiva
        if self.is_dizzy:
            self.eyes = "eye_closed"
        # Senão, pisca normalmente
        elif pygame.time.get_ticks() % 5000 < 200:
            self.eyes = "eye_closed"
        else:
            self.eyes = "eye_open"
        
        # Aplica offset horizontal e vertical para movimento dos olhos
        eye_center_x = center_x-0.025 + (self.eye_offset_x * 0.01)  # Offset de 1% por unidade
        eye_center_y = center_y + (self.eye_offset_y * 0.005)  # Offset vertical
        SPRITE_LOADER.draw_sprite_centered(self.eyes, eye_center_x, eye_center_y)
        
        # Olho esquerdo - pisca diferente, mas também fica com raiva quando tonto
        if self.is_dizzy:
            leye = "eye_closed"
        elif pygame.time.get_ticks() % 7000 < 200:
            leye = "eye_closed"
        else:
            leye = self.eyes
        # Aplica mesmo offset ao olho esquerdo
        left_eye_center_x = center_x+0.025 + (self.eye_offset_x * 0.01)
        left_eye_center_y = center_y + (self.eye_offset_y * 0.005)
        SPRITE_LOADER.draw_sprite_centered(leye, left_eye_center_x, left_eye_center_y)
        center_y+=0.052
        if self.is_talking:
            self.mouth="mouth_midopen" if self.mouth_open else "mouth_open"
            if not self.mouth_open:           
                GLOCK.player.play_sound("talk")

        SPRITE_LOADER.draw_sprite_centered(self.mouth,center_x,center_y)
        
        return True
    
    def draw_rect(self, x, y, w, h, color=(255, 255, 255)):
        """
        Desenha um retângulo relativo ao frame.
        x, y: Posição (0-22, 0-36)
        w, h: Tamanho
        """
        SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x, y), size=(w, h), color=color)

def apply_crt_effect():
    # Limpar a overlay
    crt_overlay.fill((0, 0, 0, 0))  # Clear with transparent
    
    # Aplicar a textura CRT repetidamente em toda a tela
    sprite = SPRITE_LOADER.get_sprite("crt_frame")["sprite"]
    for y in range(0, int(DEFS['height']), int(DEFS['crtsize'])):
        for x in range(0, int(DEFS['width']), int(DEFS['crtsize'])):
            crt_overlay.blit(sprite, (x, y))
    
    return crt_overlay
def apply_scanlines(surface, rect, spacing=4, intensity=15, offset=0):
    """Linhas de varredura - efeito retro/CRT com animação"""
    scanlines = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Offset animado para movimento
    animated_offset = int(offset) % spacing
    
    for y in range(-spacing, rect.height + spacing, spacing):
        y_pos = y + animated_offset
        if 0 <= y_pos < rect.height:
            pygame.draw.line(scanlines, (0, 0, 0, intensity), (0, y_pos), (rect.width, y_pos))
    
    surface.blit(scanlines, (0, 0))
    return surface
def apply_barrel_distortion(source_surface, distortion_strength=0.04):
    """
    Aplica distorção de barril a uma superfície (efeito CRT) com interpolação suave
    Otimizado com numpy para melhor performance
    
    Args:
        source_surface: Superfície original
        distortion_strength: Força da distorção (0.0 = sem distorção, 0.5 = muito curvado)
    
    Returns:
        Nova superfície com distorção aplicada
    """
    import math
    import numpy as np
    
    width, height = source_surface.get_size()
    
    # Converte superfície para array numpy
    source_array = pygame.surfarray.array3d(source_surface)
    
    # Cria arrays de coordenadas
    x_coords = np.arange(width)
    y_coords = np.arange(height)
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)
    
    # Centro da tela
    center_x = width / 2
    center_y = height / 2
    
    # Calcula distância do centro (normalizada)
    dx = (x_grid - center_x) / center_x
    dy = (y_grid - center_y) / center_y
    distance = np.sqrt(dx**2 + dy**2)
    
    # Aplica distorção de barril
    distortion_factor = 1 + distortion_strength * (distance ** 2)
    
    # Calcula novas posições
    new_dx = dx * distortion_factor
    new_dy = dy * distortion_factor
    
    source_x = center_x + new_dx * center_x
    source_y = center_y + new_dy * center_y
    
    # Interpolação bilinear
    x0 = np.floor(source_x).astype(int)
    y0 = np.floor(source_y).astype(int)
    x1 = x0 + 1
    y1 = y0 + 1
    
    # Pesos para interpolação
    wx = source_x - x0
    wy = source_y - y0
    
    # Máscara para pixels válidos
    valid_mask = (x0 >= 0) & (x0 < width - 1) & (y0 >= 0) & (y0 < height - 1)
    
    # Cria array de saída
    distorted_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Aplica interpolação apenas para pixels válidos
    for channel in range(3):
        c00 = source_array[x0[valid_mask], y0[valid_mask], channel]
        c10 = source_array[x1[valid_mask], y0[valid_mask], channel]
        c01 = source_array[x0[valid_mask], y1[valid_mask], channel]
        c11 = source_array[x1[valid_mask], y1[valid_mask], channel]
        
        wx_valid = wx[valid_mask]
        wy_valid = wy[valid_mask]
        
        interpolated = (
            c00 * (1 - wx_valid) * (1 - wy_valid) +
            c10 * wx_valid * (1 - wy_valid) +
            c01 * (1 - wx_valid) * wy_valid +
            c11 * wx_valid * wy_valid
        )
        
        distorted_array[valid_mask, channel] = np.clip(interpolated, 0, 255).astype(np.uint8)
    
    # Converte de volta para superfície pygame
    # Transpõe porque surfarray usa (width, height, channels)
    distorted_array_transposed = np.transpose(distorted_array, (1, 0, 2))
    distorted = pygame.surfarray.make_surface(distorted_array_transposed)
    
    return distorted


