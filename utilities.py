import pygame
import os
import configparser
def initialize():
    global SCREEN,DEFS, SHEET, PROPSYS,SPRITE_LOADER
    definitions = configparser.ConfigParser()
    definitions.read('defs.ini')
    DEFS = {
        key: float(value) for key, value in definitions.items('SCREEN')
    }
    SCREEN = pygame.display.set_mode((int(DEFS['width']), int(DEFS['height'])))
    SHEET= pygame.image.load("assets/spritesheet.png").convert_alpha()
    PROPSYS=ProportionalSystem(DEFS['width'], DEFS['height'])
    SPRITE_LOADER = spriteLoader()
    return SCREEN,DEFS, SHEET, PROPSYS,SPRITE_LOADER

class TeeVee:
    def __init__(self):
        SPRITE_LOADER.create_sprite(
            key="frame",
            position=(0, 0),
            size=(22, 36),
            scale=DEFS["width"]/150
        )
        SPRITE_LOADER.create_sprite(
            key="mouths",
            position=(0, 0),
            size=(22, 36),
            scale=DEFS["width"]/150
        )
        self.emote = "happy"  # Exemplo de estado emocional
    def draw(self):
        #frame
        SPRITE_LOADER.draw_sprite_centered("frame", DEFS['center_x'], DEFS['center_y'])
        #eyes
        SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(6,22),size=(3,5))
        SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(13,22),size=(3,5))
        #mouth
        lines=0
        if self.emote=="happy":
            lines=3
        elif self.emote=="sad":
            lines=1
        for (i) in range(lines):
            SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(6+i,29+i),size=(10-i*2,1))
        

        return True
    
        
class ProportionalSystem:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def px_to_percent_x(self, pixels):
        """Converte pixels para porcentagem na largura"""
        return pixels / self.screen_width
    
    def px_to_percent_y(self, pixels):
        """Converte pixels para porcentagem na altura"""
        return pixels / self.screen_height
    
    def percent_to_px_x(self, percent):
        """Converte porcentagem para pixels na largura"""
        return int(percent * self.screen_width)
    
    def percent_to_px_y(self, percent):
        """Converte porcentagem para pixels na altura"""
        return int(percent * self.screen_height)
    
    def get_position(self, x_percent, y_percent):
        """Retorna posição em pixels a partir de porcentagens"""
        return (
            self.percent_to_px_x(x_percent),
            self.percent_to_px_y(y_percent)
        )
    
    def get_size(self, width_percent, height_percent):
        """Retorna tamanho em pixels a partir de porcentagens"""
        return (
            self.percent_to_px_x(width_percent),
            self.percent_to_px_y(height_percent)
        )
    
    def get_rect(self, x_percent, y_percent, width_percent, height_percent):
        """Retorna um Rect com coordenadas proporcionais"""
        return pygame.Rect(
            self.percent_to_px_x(x_percent),
            self.percent_to_px_y(y_percent),
            self.percent_to_px_x(width_percent),
            self.percent_to_px_y(height_percent)
        )
class Button:
    def __init__(self, x_percent, y_percent, width_percent, height_percent, 
                 text, color=(128, 128, 128), font_size_percent=0.1):
        """
        Botão com coordenadas proporcionais
        
        Args:
            x_percent, y_percent: Posição em porcentagem (0.0 a 1.0)
            width_percent, height_percent: Tamanho em porcentagem (0.0 a 1.0)
            text: Texto do botão
            color: Cor normal do botão
            hover_color: Cor quando o mouse está sobre
            font_size_percent: Tamanho da fonte em porcentagem da altura da tela
        """
        
        # Converte porcentagens para pixels (usa o sistema proporcional global)
        x_px = PROPSYS.percent_to_px_x(x_percent)
        y_px = PROPSYS.percent_to_px_y(y_percent)
        width_px = PROPSYS.percent_to_px_x(width_percent)
        height_px = PROPSYS.percent_to_px_y(height_percent)
        
        self.rect = pygame.Rect(x_px, y_px, width_px, height_px)
        self.text = text
        self.color = color
        self.current_color = color
        self.hovering=False
        
        # Tamanho da fonte proporcional
        font_size = int(PROPSYS.percent_to_px_y(font_size_percent))
        self.font = pygame.font.Font("assets/fonts/bmspace.ttf", font_size)
        self.text_surface = self.font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
        # Armazena as porcentagens para redimensionamento
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.width_percent = width_percent
        self.height_percent = height_percent
        self.font_size_percent = font_size_percent
    
    def draw(self,screen):
        """Desenha o botão na superfície"""
        pygame.draw.rect(screen, self.color, self.rect, 10,)
        screen.blit(self.text_surface, self.text_rect)
    
    def update_font(self, scale=1):
        # Atualiza fonte
        font_size = int(PROPSYS.percent_to_px_y(self.font_size_percent*scale))
        self.font = pygame.font.Font("assets/fonts/bmspace.ttf", font_size)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def check_hover(self, pos):
        """Verifica se o mouse está sobre o botão"""
        if self.rect.collidepoint(pos):
            self.hovering=True
            self.update_font(scale=1.2)
            return True
        else:
            if self.hovering:
                self.update_font()
                self.hovering = False
            return False
    
    def is_clicked(self, pos, event):
        """Verifica se o botão foi clicado"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                return True
        return False
    
    def get_percent_position(self):
        """Retorna a posição atual em porcentagem"""
        return (self.x_percent, self.y_percent)
    
    def get_percent_size(self):
        """Retorna o tamanho atual em porcentagem"""
        return (self.width_percent, self.height_percent)
class spriteLoader:
    def __init__(self):
        self.sprites = {}
    def create_sprite(self, key, position, size, scale=1.0):
        x, y = position
        width, height = size
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(SHEET, (0, 0), (x, y, width, height))
        if scale != 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            sprite = pygame.transform.scale(sprite, (new_width, new_height))
        self.sprites[key] = {
            "sprite": sprite,
            "size": (width, height),
            "position": position,
            "scale": scale,
            }
        return sprite
    
    def draw_sprite_proportional(self, key, x_percent, y_percent):
        """Desenha sprite usando coordenadas proporcionais"""
        if not self.ps:
            print("Erro: Sistema proporcional não configurado")
            return False
            
        sprite = self.sprites.get(key)
        if sprite:
            x = self.ps.percent_to_px_x(x_percent)
            y = self.ps.percent_to_px_y(y_percent)
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
    def draw_relative_to_sprite(self, sprite,startpos,size):
        # Calcula a posição do frame na tela (centralizado)
        dic=self.sprites.get(sprite)
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
        pygame.draw.rect(SCREEN, (255, 255, 255), rect)
        return True
        
    def get_sprite(self, key):
        return self.sprites.get(key)
