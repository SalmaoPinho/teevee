import pygame
from config import DEFS

SCREEN = None
SHEET = None
PROPSYS = None
SPRITE_LOADER = None
crt_texture = None

def init_graphics(screen, sheet, propsys):
    global SCREEN, SHEET, PROPSYS, SPRITE_LOADER, crt_texture, crt_overlay
    SCREEN = screen
    SHEET = sheet
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
    position=(14, 36),
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
    size=(46, 34),
    angle=90,
    )
    
    return SPRITE_LOADER

class spriteLoader:
    def __init__(self):
        self.sprites = {}
        # self.ps estava faltando no código original, assumindo que deveria ser o PROPSYS global
        
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
            SCREEN.blit(sprite, (x, y))
            return True
        return False
    def draw_sprite_centered(self, key, x_percent, y_percent):
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
        
        SPRITE_LOADER.create_sprite(
            key="frame",
            position=(0, 0),
            size=(22, 36),
            scale=DEFS["width"]/100
        )
        SPRITE_LOADER.create_sprite(
            key="mouths",
            position=(0, 0),
            size=(22, 36),
            scale=DEFS["width"]/100
        )
        self.eyes = "open"  # Exemplo de estado dos olhos
        self.mouth = "happy"  # Exemplo de estado emocional
    def draw(self):
        # Frame
        SPRITE_LOADER.draw_sprite_centered("frame", DEFS['center_x'], DEFS['center_y'])
        # Olhos
        SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(6,22),size=(3,5))
        SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(13,22),size=(3,5))
        # Boca
        pos1=(6,28)
        self.mouth="happy"
        if self.mouth=="smile":
            for (i) in range(3):
                SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(pos1[0]+i, pos1[1]+i),size=(10-i*2,2))
        elif self.mouth=="happy":
            for (i) in range(3):
                SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(pos1[0]+i, pos1[1]+i),size=(10-i*2,2),outlines=i)
        elif self.mouth=="sad":
            for (i) in range(3):
                SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(pos1[0]+i, pos1[1]+2-i),size=(10-i*2,2),outlines=i)
        elif self.mouth=="openmouth":
            for (i) in range(3):
                SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(pos1[0]+i-1, pos1[1]+i-1),size=(12-i*2,1),color=(0,0,0))
                SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(pos1[0]+i, pos1[1]+i),size=(10-i*2,1),color=(0,0,0))
        elif self.mouth=="neutral":
            SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(pos1[0], pos1[1]+1),size=(10,1))
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


