import pygame
import os
import configparser
import datetime
def initialize():
    global SCREEN,DEFS, SHEET, PROPSYS,SPRITE_LOADER, GAMECLOCK
    definitions = configparser.ConfigParser()
    definitions.read('defs.ini')
    DEFS = {
        key: float(value) for key, value in definitions.items('SCREEN')
    }
    DEFS.update({
    key: definitions.getboolean('TOGGLE', key) for key in definitions['TOGGLE']
    })
    SCREEN = pygame.display.set_mode((int(DEFS['width']), int(DEFS['height'])))
    SHEET= pygame.image.load("assets/spritesheet.png").convert_alpha()
    PROPSYS=ProportionalSystem(DEFS['width'], DEFS['height'])
    SPRITE_LOADER = spriteLoader()
    global crt_texture,crt_overlay
    crt_texture = pygame.image.load("assets/rgb.png").convert_alpha()
    crt_texture.set_alpha(50)
    crt_overlay = pygame.Surface((DEFS['width'], DEFS['height']), pygame.SRCALPHA)
    crt_texture = pygame.transform.scale(crt_texture, (DEFS['crtsize'], DEFS['crtsize']))
    GAMECLOCK = Glock()
    return SCREEN,DEFS, SHEET, PROPSYS,SPRITE_LOADER, GAMECLOCK
class Glock:
    def __init__(self):
        self.update()
    def update(self):
        now = datetime.datetime.now()
        self.vals={
            'time_12hr': now.strftime("%I:%M:%S %p"),  # 02:30:45 PM
            'time_24hr': now.strftime("%H:%M:%S"),     # 14:30:45
            'time_short': now.strftime("%H:%M"),       # 14:30
            'week_day': now.strftime("%A"),  # Monday
            'short_date': now.strftime("%m/%d/%Y"),      # 01/15/2024
        }
    
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
        #frame
        SPRITE_LOADER.draw_sprite_centered("frame", DEFS['center_x'], DEFS['center_y'])
        #eyes
        SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(6,22),size=(3,5))
        SPRITE_LOADER.draw_relative_to_sprite("frame",startpos=(13,22),size=(3,5))
        #mouth
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
    
#sound player
sounds={
    'click': 'assets/sounds/click.mp3',
    'talk': 'assets/sounds/talk.mp3',
    'cancel' : 'assets/sounds/cancel.mp3',
}
def play_sound(sound):
    """Toca um arquivo de som"""
    if not os.path.isfile(sounds[sound]):
        print(f"Arquivo de som não encontrado: {sounds[sound]}")
        return
    sound = pygame.mixer.Sound(sounds[sound])
    sound.play()
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
class UElement:
    def __init__(self, x_percent=0, y_percent=0, width_percent=1, height_percent=1, 
                 text='', color=None,clickable=False, font_size_percent=0.1,outline_size=5,subelements=None):
        """
        Botão com coordenadas proporcionais
        
        Args:
            x_percent, y_percent: Posição em porcentagem (0.0 a 1.0)
            width_percent, height_percent: Tamanho em porcentagem (0.0 a 1.0)
            text: Texto do botão
            color: Cor normal do botão
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
        self.clickable=clickable
        self.hovering=False
        self.outline_size=outline_size
        
        # Tamanho da fonte proporcional
        font_size = int(PROPSYS.percent_to_px_y(font_size_percent))
        self.font = pygame.font.Font("assets/fonts/bmspace.ttf", font_size)
        self.text_surface = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
        # Armazena as porcentagens para redimensionamento
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.width_percent = width_percent
        self.height_percent = height_percent
        self.font_size_percent = font_size_percent
        self.subelements = {}
        if subelements is not None:
            for subelement_key, subelement_dict in subelements.items():
                # Cria o UElement a partir do dicionário
                self.subelements[subelement_key] = UElement(
                    x_percent=self.x_percent + subelement_dict.get('x_percent', 0) * self.width_percent,
                    y_percent=self.y_percent + subelement_dict.get('y_percent', 0) * self.height_percent,
                    width_percent=self.width_percent * subelement_dict.get('width_percent', 1),
                    height_percent=self.height_percent * subelement_dict.get('height_percent', 1),
                    font_size_percent=subelement_dict.get('font_size_percent', 0.1),
                    text=subelement_dict.get('text', ''),
                    color=subelement_dict.get('color', None),
                    clickable=subelement_dict.get('clickable', False),
                    outline_size=subelement_dict.get('outline_size', 5),
                    subelements=subelement_dict.get('subelements', None) 
                )
                
    def draw(self,screen):
        """Desenha o botão na superfície"""
        text_surface=self.text_surface
        if self.color:
            pygame.draw.rect(screen, self.color, self.rect, self.outline_size, border_radius=30)
        #get first character
        if self.text!='' and self.text[0]=='!':
            self.update_font(newtext=GAMECLOCK.vals.get(self.text[1:], ''))
        screen.blit(text_surface, self.text_rect)
        for subelement_key in self.subelements:
            subelement = self.subelements[subelement_key]
            subelement.draw(screen)
    
    def update_font(self, scale=1,newtext=None):
        # Atualiza fonte
        font_size = int(PROPSYS.percent_to_px_y(self.font_size_percent*scale))
        self.font = pygame.font.Font("assets/fonts/bmspace.ttf", font_size)
        text=self.text if newtext is None else newtext
        self.text_surface = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def check_hover(self, pos):
        """Verifica se o mouse está sobre o botão"""
        if not self.clickable:
            return False
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
        if not self.clickable:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                play_sound('click')
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
        
    def get_sprite(self, key):
        return self.sprites.get(key)
def apply_crt_effect():
    # Limpar a overlay
    crt_overlay.fill((0, 0, 0, 0))
    
    # Aplicar a textura 16x16 repetidamente em toda a tela
    
    for y in range(0, int(DEFS['height']),int(DEFS['crtsize'])):
        for x in range(0, int(DEFS['width']),int(DEFS['crtsize'])):
            crt_overlay.blit(crt_texture, (x, y))
    return crt_overlay