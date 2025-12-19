import io
import pygame
import os
from config import DICT, DEFS, getVars
from game_clock import Glock
from graphics import TeeVee
import datetime
import calendar
import copy

# --- Sistema de UI ---
PROPSYS = None
GAME_CLOCK = None
TV = None
glock = None
primary_color = None
background_color = None
secondary_color = None
user_interface = {}
categories = []
MAP_SYSTEM = None

# --- Sistema de Chat ---
chat_input = ""
chat_response = ""
chat_input_active = False  # Se o campo de input está ativo
chat_cursor_timer = 0  # Timer para piscar o cursor
chat_cursor_visible = True  # Se o cursor está visível
waiting_for_response = False  # Se está esperando resposta do Ollama

# --- Sistema de Paginação ---
response_pages = []  # Lista de páginas da resposta
current_page = 0     # Página atual (0-indexed)
max_chars_per_page = 150  # Caracteres por página

def set_tv(tv_instance):
    global TV
    TV = tv_instance

def set_map_system(map_sys):
    global MAP_SYSTEM
    MAP_SYSTEM = map_sys

def split_response_into_pages(text, max_chars=150):
    """Divide texto em páginas de tamanho máximo, respeitando palavras"""
    if len(text) <= max_chars:
        return [text]
    
    pages = []
    words = text.split()
    current_page = ""
    
    for word in words:
        # Tenta adicionar palavra à página atual
        test_page = current_page + word + " "
        if len(test_page) <= max_chars:
            current_page = test_page
        else:
            # Página cheia, salva e começa nova
            if current_page:
                pages.append(current_page.strip())
            current_page = word + " "
    
    # Adiciona última página
    if current_page:
        pages.append(current_page.strip())
    
    return pages if pages else [text]


def init_ui_system(width, height, game_clock):
    global PROPSYS, GAME_CLOCK, categories, glock, primary_color, background_color, secondary_color, user_interface
    PROPSYS = ProportionalSystem(width, height)
    GAME_CLOCK = game_clock
    
    # Initialize globals that depend on config
    categories[:] = list(DICT['contentvals'].keys())
    glock = Glock()
    primary_color = DEFS['pri']
    background_color = DEFS['bg']
    secondary_color = DEFS["sec"]
    
    # Define Interface do Usuário
    user_interface.update({
        "background": UElement(
            x_percent=0,
            y_percent=0,
            width_percent=1,
            height_percent=1,
            color=background_color,
            inverted_colors=True
        ),
        "top_bar": UElement(
            x_percent=0.125,
            y_percent=0.0625,
            width_percent=0.75,
            height_percent=0.125,
            color=primary_color,
            subelements={
                'nav_prev':{
                    'width_percent':0.2,
                    'text':"<<",
                    'clickable':True,
                    'background':False,
                },
                'title_area': {
                    'x_percent':0.2,
                    'width_percent':0.6,
                    'subelements':{
                        "main_title": {
                            'text':"!header",
                            'font_size_percent':0.08,
                            'inverted_colors':True,
                            'color':(255,255,255),
                        },
                    }
                },
                "nav_next": {
                    'x_percent':0.8,
                    'width_percent':0.2,
                    'text':">>",
                    'clickable':True,
                    'background':False,
                }
            }
        ),
        "content_panel": UElement(
            x_percent=0.125,
            y_percent=0.175,
            width_percent=0.75,
            height_percent=0.675,
            background=False,
            subelements={
            }
        ),
        "bottom_bar": UElement(
            x_percent=0.125,
            y_percent=0.85,
            width_percent=0.75,
            height_percent=0.125,
            color=primary_color,
            subelements={
                "time_display": {
                    'width_percent':0.33,
                    'font_size_percent':0.04,
                    'text':"!time_24hr",
                },
                "date_display": {
                    'x_percent':0.33,
                    'width_percent':0.33,
                    'font_size_percent':0.0425,
                    'text':"!short_date",
                    'background':False,
                },
                "weekday_display": {
                    'x_percent':0.67,
                    'width_percent':0.33,
                    'font_size_percent':0.04,
                    'text':"!week_day",
                },
            }
        ),
    })
    
    build_ui()

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

def apply_gradient_effect(surface, width, height, base_color, intensity=0.5, opacity=150, border_radius=30):
    """
    Aplica efeito de gradiente vertical arredondado em uma superfície
    
    Args:
        surface: Superfície pygame onde aplicar o gradiente
        width: Largura da área de gradiente
        height: Altura da área de gradiente
        base_color: Cor base do elemento
        intensity: Intensidade do escurecimento (0.0-1.0, padrão 0.5 = 50%)
        opacity: Opacidade máxima do gradiente (0-255, padrão 150)
        border_radius: Raio dos cantos arredondados
    
    Returns:
        Superfície com efeito de gradiente aplicado
    """
    if width < 10 or height < 10:
        return surface
    
    # Cria superfície para o gradiente
    gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    r, g, b = base_color[:3]
    
    for i in range(height):
        # Gradiente de cima para baixo - escurece progressivamente
        progress = i / height
        # Escurece a cor base
        dark_r = int(r * (1 - progress * intensity))
        dark_g = int(g * (1 - progress * intensity))
        dark_b = int(b * (1 - progress * intensity))
        alpha = int(opacity * progress)  # Aumenta opacidade conforme desce
        
        pygame.draw.line(gradient_surface, (dark_r, dark_g, dark_b, alpha), 
                       (0, i), (width, i))
    
    # Aplica máscara arredondada ao gradiente
    gradient_mask = pygame.Surface((width, height), pygame.SRCALPHA)
    mask_rect = pygame.Rect(0, 0, width, height)
    pygame.draw.rect(gradient_mask, (255, 255, 255, 255), mask_rect, border_radius=border_radius)
    gradient_surface.blit(gradient_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    
    # Aplica gradiente na superfície principal
    surface.blit(gradient_surface, (0, 0))
    
    return surface

def apply_shine_effect(surface, width, height, intensity=40, shine_percent=0.3, border_radius=30, offset_y=5, base_color=(255, 255, 255)):
    """
    Aplica efeito de brilho arredondado em uma superfície
    
    Args:
        surface: Superfície pygame onde aplicar o brilho
        width: Largura da área de brilho
        height: Altura da área de brilho
        intensity: Intensidade do brilho (0-255)
        shine_percent: Porcentagem da altura para o brilho (0.0-1.0)
        border_radius: Raio dos cantos arredondados
        offset_y: Deslocamento vertical do brilho
        base_color: Cor base do elemento para adaptar o brilho
    
    Returns:
        Superfície com efeito de brilho aplicado
    """
    if width < 20 or height < 10:
        return surface
    
    shine_height = int(height * shine_percent)
    if shine_height <= 0:
        return surface
    
    # Calcula cor de brilho adaptativa baseada na cor base
    r, g, b = base_color[:3]
    brightness = (r + g + b) / 3
    
    # Cria superfície para o brilho
    shine_surface = pygame.Surface((width, shine_height), pygame.SRCALPHA)
    
    if brightness < 128:  # Cor escura - usa brilho clarificado
        # Para cores escuras, desenha gradiente da cor clarificada
        for i in range(shine_height):
            # Gradiente que diminui conforme desce
            progress = i / shine_height
            alpha = int(intensity * 0.5 * (1 - progress))  # Intensidade reduzida
            
            # Clarifica a cor base
            shine_r = min(255, int(r * 2.5))
            shine_g = min(255, int(g * 2.5))
            shine_b = min(255, int(b * 2.5))
            
            # Desenha linha do gradiente
            pygame.draw.line(shine_surface, (shine_r, shine_g, shine_b, alpha), 
                           (0, i), (width, i))
    else:  # Cor clara - usa escurecimento sutil
        # Para cores claras, desenha gradiente escuro para criar profundidade
        for i in range(shine_height):
            progress = i / shine_height
            # Escurecimento sutil que diminui conforme desce
            alpha = int(intensity * 0.3 * (1 - progress))  # Intensidade mais baixa
            
            # Usa preto para escurecer
            pygame.draw.line(shine_surface, (0, 0, 0, alpha), 
                           (0, i), (width, i))
    
    # Aplica máscara arredondada
    mask = pygame.Surface((width, shine_height), pygame.SRCALPHA)
    mask_rect = pygame.Rect(0, 0, width, shine_height * 2)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask_rect, border_radius=border_radius)
    shine_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    
    # Desenha o brilho na superfície principal
    surface.blit(shine_surface, (0, offset_y))
    
    return surface



class UElement:
    def __init__(self, x_percent=0, y_percent=0, width_percent=1, height_percent=1, 
                 text='', color=(255,255,255), clickable=False, font_size_percent=0.1, 
                 text_align='center', outline_size=5, subelements=None, parent=None,inverted_colors=False,background=True,visible=True,name=None):
        """
        Botão com coordenadas proporcionais
        
        Args:
            x_percent, y_percent: Posição RELATIVA ao pai em porcentagem (0.0 a 1.0)
            width_percent, height_percent: Tamanho RELATIVO ao pai em porcentagem (0.0 a 1.0)
        """  
        self.parent = parent
        
        # Calcula coordenadas ABSOLUTAS baseadas no pai
        parentvals = {
            'x_percent': parent.x_percent if parent else 0,
            'y_percent': parent.y_percent if parent else 0,  
            'width_percent': parent.width_percent if parent else 1,
            'height_percent': parent.height_percent if parent else 1
        }
        self.x_percent = parentvals['x_percent'] + x_percent * parentvals['width_percent']
        self.y_percent = parentvals['y_percent'] + y_percent * parentvals['height_percent']
        self.width_percent = parentvals['width_percent'] * width_percent
        self.height_percent = parentvals['height_percent'] * height_percent
        
        if PROPSYS is None:
            raise RuntimeError("UI System not initialized. Call init_ui_system() first.")

        x_px = PROPSYS.percent_to_px_x(self.x_percent)  # Use self.x_percent!
        y_px = PROPSYS.percent_to_px_y(self.y_percent)  # Use self.y_percent!
        width_px = PROPSYS.percent_to_px_x(self.width_percent)  # Use self.width_percent!
        height_px = PROPSYS.percent_to_px_y(self.height_percent)  # Use self.height_percent!
        self.visible=visible
        self.rect = pygame.Rect(x_px, y_px, width_px, height_px)
        self.text = text
        self.name = name if name else text
        self.color = color
        self.clickable = clickable
        self.hovering = False
        self.outline_size = outline_size
        self.inverted_colors = inverted_colors
        self.background = background
        # Tamanho da fonte proporcional
        font_size = int(PROPSYS.percent_to_px_y(font_size_percent))
        self.font = pygame.font.Font("assets/fonts/bmspace.ttf", font_size)
        self.text_align = text_align
        self.text_surface = self._render_text_wrapped(text, color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
        if text_align == 'left':
            self.text_rect.left = self.rect.left *1.1
        elif text_align == 'right':
            self.text_rect.right = self.rect.right * 0.9
            
        self.font_size_percent = font_size_percent
        
        # Processa subelementos
        self.subelements = {}
        if subelements is not None:
            for subelement_key, subelement_dict in subelements.items():
                self.add_subelement(subelement_key, subelement_dict)

    def _render_text_wrapped(self, text, color):
        """Renderiza texto com quebra de linha automática se for muito largo"""
        words = str(text).split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.font.render(test_line, True, color)
            
            if test_surface.get_width() <= self.rect.width * 0.9:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        if not lines:
            return self.font.render('', True, color)
        
        # Renderiza múltiplas linhas
        line_height = self.font.get_height()
        total_height = line_height * len(lines)
        surface = pygame.Surface((self.rect.width, total_height), pygame.SRCALPHA)
        
        for i, line in enumerate(lines):
            line_surface = self.font.render(line, True, color)
            y_offset = i * line_height
            
            if self.text_align == 'left':
                surface.blit(line_surface, (0, y_offset))
            elif self.text_align == 'right':
                surface.blit(line_surface, (self.rect.width - line_surface.get_width(), y_offset))
            else:  # center
                surface.blit(line_surface, ((self.rect.width - line_surface.get_width()) // 2, y_offset))
        
        return surface

    def add_subelement(self, subelement_key, subelement_dict):
        self.subelements[subelement_key] = UElement(
            x_percent=subelement_dict.get('x_percent', 0),
            y_percent=subelement_dict.get('y_percent', 0),
            width_percent=subelement_dict.get('width_percent', 1),
            height_percent=subelement_dict.get('height_percent', 1),
            font_size_percent=subelement_dict.get('font_size_percent', 0.1),
            text=subelement_dict.get('text', ''),
            name=subelement_dict.get('name', None) if 'name' in subelement_dict else subelement_key,
            text_align=subelement_dict.get('text_align', 'center'),
            color=subelement_dict.get('color', (255,255,255)),
            clickable=subelement_dict.get('clickable', False),
            outline_size=subelement_dict.get('outline_size', 5),
            parent=self,
            inverted_colors=subelement_dict.get('inverted_colors', False),
            subelements=subelement_dict.get('subelements', None),
            background=subelement_dict.get('background', True),
            visible=subelement_dict.get('visible', True)
        )

    def draw(self,screen):
        if not self.visible:
            return
        # Parse text for variables
        txt = self.text
        if '!' in self.text:
            words = self.text.split(' ')
            new_words = []
            for word in words:
                if '!' in word:
                    # Lida com casos como "Rain: !weather_rain %" onde ! está dentro
                    # Precisamos extrair o nome da variável. Assumindo formato simples !var
                    # ou !var_name
                    
                    # Abordagem simples: se palavra começa com !, tenta substituir
                    # Se contém !, divide por ! e substitui a parte depois
                    
                    prefix = ""
                    suffix = ""
                    command = word
                    
                    if '!' in word:
                        parts = word.split('!')
                        prefix = parts[0]
                        command = parts[1]
                        # Lida com pontuação potencial após comando?
                        # Por enquanto assume separação limpa ou sufixo simples
                    
                    val = "N/A"
                    if command == 'header':
                        vars=getVars('content_index')
                        if vars < len(categories):
                            val=categories[vars]
                        else:
                            val="Error"
                    elif command=="tv":
                        if TV:
                            TV.draw()
                        val = "" # Don't print anything for tv command
                    elif command.startswith("SPRITE_"):
                        # Renderização genérica de sprite: SPRITE_<sprite_key>
                        import graphics
                        sprite_key = command[7:]  # Remove prefixo "SPRITE_"
                        # Obtém o sprite
                        sprite_data = graphics.SPRITE_LOADER.get_sprite(sprite_key)
                        if sprite_data:
                            sprite = sprite_data["sprite"]
                            # Escala sprite para caber na altura do botão, aumenta tamanho se hovering
                            hover_scale = 1.2 if self.hovering else 1.0
                            scale_factor = (self.rect.height / sprite.get_height()) * hover_scale
                            scaled_width = int(sprite.get_width() * scale_factor)
                            scaled_height = int(sprite.get_height() * scale_factor)
                            scaled_sprite = pygame.transform.scale(sprite, (scaled_width, scaled_height))
                            # Centraliza o sprite no retângulo do botão
                            sprite_rect = scaled_sprite.get_rect(center=self.rect.center)
                            screen.blit(scaled_sprite, sprite_rect)
                        val = ""  # Não imprime texto
                    elif command=="music_display":
                        if GAME_CLOCK.player.metadata.get('art'):
                            img=pygame.image.load(io.BytesIO(GAME_CLOCK.player.metadata.get('art', b"")))
                            
                            # Escala a imagem
                            img_size = self.rect.height
                            scaled_img = pygame.transform.scale(img, (img_size, img_size))
                            
                            # Aplica transparência
                            scaled_img.set_alpha(128)
                            
                            # Desenha na tela
                            rect = scaled_img.get_rect(center=self.rect.center)
                            screen.blit(scaled_img, rect)
                        val = "" 
                    elif command=="music_progress":
                        progress = glock.player.get_progress()
                        # Atualiza a largura percentual
                        self.width_percent = self.parent.width_percent * (progress / 100.0) if self.parent else (progress / 100.0)
                        # Recalcula o rect com a nova largura
                        x_px = PROPSYS.percent_to_px_x(self.x_percent)
                        y_px = PROPSYS.percent_to_px_y(self.y_percent)
                        width_px = PROPSYS.percent_to_px_x(self.width_percent)
                        height_px = PROPSYS.percent_to_px_y(self.height_percent)
                        self.rect = pygame.Rect(x_px, y_px, width_px, height_px)
                        val = ""
                    elif command=="map_render":
                        if MAP_SYSTEM:
                            MAP_SYSTEM.set_content_area(self.rect)
                            # Get location from game clock if available, otherwise default
                            lat = 42.355
                            lon = -71.065
                            if GAME_CLOCK and 'map_lat' in GAME_CLOCK.info:
                                 lat = GAME_CLOCK.info['map_lat']
                                 lon = GAME_CLOCK.info['map_lon']
                            map_surf, source = MAP_SYSTEM.get_static_map(lat, lon)
                            if map_surf:
                                screen.blit(map_surf, self.rect)
                        val = "" # Não imprime nada para comando de mapa
                    elif command.startswith("toggle_"):
                        # Suporte para variáveis de toggle: toggle_<setting_name>
                        import config
                        setting_name = command[7:]  # Remove prefixo "toggle_"
                        val = config.get_toggle_display(setting_name)
                    elif command == "chat_input":
                        # Exibe o texto digitado pelo usuário com cursor piscante
                        global chat_cursor_timer, chat_cursor_visible
                        current_time = pygame.time.get_ticks()
                        
                        # Atualiza cursor a cada 500ms (pisca a cada meio segundo)
                        if current_time - chat_cursor_timer >= 500:
                            chat_cursor_timer = current_time
                            chat_cursor_visible = not chat_cursor_visible
                        
                        # Mostra cursor "I" apenas se campo estiver ativo
                        if chat_input_active and chat_cursor_visible:
                            val = chat_input + " I"  # Cursor "I" com espaço
                        else:
                            val = chat_input
                    elif command == "teevee_response":
                        # Exibe a resposta do TeeVee ou mensagem de espera
                        if waiting_for_response:
                            val = "Pensando..."
                        else:
                            val = chat_response if chat_response else ""
                    elif command == "page_indicator":
                        # Exibe indicador de página (ex: <1/3>)
                        if response_pages and len(response_pages) > 1:
                            val = f"<{current_page + 1}/{len(response_pages)}>"
                        else:
                            val = ""
                    elif command == "page_prev_arrow":
                        # Exibe seta anterior apenas se houver múltiplas páginas
                        if response_pages and len(response_pages) > 1:
                            val = "<"
                        else:
                            val = ""
                    elif command == "page_next_arrow":
                        # Exibe seta próxima apenas se houver múltiplas páginas
                        if response_pages and len(response_pages) > 1:
                            val = ">"
                        else:
                            val = ""
                    elif GAME_CLOCK and (command in GAME_CLOCK.vals):
                        val=GAME_CLOCK.vals[command]
                    elif GAME_CLOCK and (command in GAME_CLOCK.info):
                        val=str(GAME_CLOCK.info[command])
                    elif GAME_CLOCK and (command in GAME_CLOCK.player.metadata):
                        val=str(GAME_CLOCK.player.metadata[command])
                    if val != "":
                         new_words.append(prefix + str(val) + suffix)
                else:
                    new_words.append(word)
            
            if any(w != "" for w in new_words):
                txt = " ".join(new_words)
            else:
                txt = "" # Se todas as substituições resultaram em strings vazias (como map_render), mantém vazio
            self.update_font(newtext=txt)
            
        """Desenha o botão na superfície"""
        text_surface= self.text_surface
        if self.background:
            if self.inverted_colors:
                # Cria superfície temporária para efeitos
                temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                
                # Desenha retângulo base com cantos arredondados
                temp_rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
                pygame.draw.rect(temp_surface, self.color, temp_rect, border_radius=30)
                
                # Aplica gradiente usando função reutilizável
                apply_gradient_effect(temp_surface, self.rect.width, self.rect.height, 
                                    self.color, intensity=0.5, opacity=150, border_radius=30)
                
                if self.rect.width < 20:
                    return
                # Aplica brilho usando função reutilizável com cor adaptativa
                apply_shine_effect(temp_surface, self.rect.width, self.rect.height, 
                                 intensity=40, shine_percent=0.3, border_radius=30, offset_y=5, base_color=self.color)
                
                # Adiciona borda interna sutil para definição
                inner_rect = pygame.Rect(2, 2, self.rect.width - 4, self.rect.height - 4)
                pygame.draw.rect(temp_surface, (*self.color[:3], 100), inner_rect, 1, border_radius=28)
                
                # Desenha na tela
                screen.blit(temp_surface, self.rect.topleft)
            else:
                # Cria superfície temporária para efeitos
                temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                
                # Desenha borda externa com brilho
                temp_rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
                
                # Borda principal
                pygame.draw.rect(temp_surface, self.color, temp_rect, self.outline_size, border_radius=30)
                
                # Aplica brilho usando função reutilizável com cor adaptativa
                if self.rect.width > self.outline_size * 2:
                    # Cria superfície temporária para o brilho interno
                    shine_width = self.rect.width - self.outline_size * 2
                    shine_height_total = self.rect.height - self.outline_size * 2
                    inner_shine_surface = pygame.Surface((shine_width, shine_height_total), pygame.SRCALPHA)
                    
                    apply_shine_effect(inner_shine_surface, shine_width, shine_height_total,
                                     intensity=60, shine_percent=0.15, border_radius=25, offset_y=0, base_color=self.color)
                    
                    temp_surface.blit(inner_shine_surface, (self.outline_size, self.outline_size))
                
                # Adiciona destaque na borda superior (highlight)
                highlight_thickness = max(1, self.outline_size // 2)
                highlight_rect = pygame.Rect(self.outline_size, self.outline_size,
                                            self.rect.width - self.outline_size * 2,
                                            self.rect.height - self.outline_size * 2)
                
                # Cor de destaque (mais clara)
                highlight_color = tuple(min(255, c + 40) for c in self.color[:3])
                pygame.draw.rect(temp_surface, (*highlight_color, 80), highlight_rect, 
                               highlight_thickness, border_radius=25)
                
                # Desenha na tela
                screen.blit(temp_surface, self.rect.topleft)
        screen.blit(text_surface, self.text_rect)
        for subelement_key in self.subelements:
            subelement = self.subelements[subelement_key]
            subelement.draw(screen)
    
    def update_font(self, scale=1,newtext=None):
        # Atualiza fonte
        font_size = int(PROPSYS.percent_to_px_y(self.font_size_percent*scale))
        self.font = pygame.font.Font("assets/fonts/bmspace.ttf", font_size)
        text=self.text if newtext is None else newtext
        color=self.color if not self.inverted_colors else DEFS['bg'] 
        self.text_surface = self._render_text_wrapped(str(text), color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        if self.text_align == 'left':
            self.text_rect.left = self.rect.left *1.1
        elif self.text_align == 'right':
            self.text_rect.right = self.rect.right * 0.9
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
                glock.player.play_sound('click')
                return True
        return False
    
    def get_percent_position(self):
        """Retorna a posição atual em porcentagem"""
        return (self.x_percent, self.y_percent)
    
    def get_percent_size(self):
        """Retorna o tamanho atual em porcentagem"""    
        return (self.width_percent, self.height_percent)

def searchElement(element,key):
    if element.subelements.get(key):
        return element.subelements.get(key)
    else:
        for subelement_key in element.subelements:
            subelement = element.subelements[subelement_key]
            result = searchElement(subelement, key)
            if result:
                return result
    return None

def generate_calendar_subelements():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    
    # Obtém número de dias no mês e dia inicial
    num_days = calendar.monthrange(year, month)[1]
    
    calendar_subs = {}
    
    # Layout de grade: 7 colunas (Seg-Dom), 5-6 linhas
    cols = 7
    rows = 6
    
    cell_width = 1.0 / cols
    cell_height = 1.0 / rows
    
    # Posição inicial (offset para primeiro dia do mês)
    # monthrange retorna (weekday, days). weekday é 0-6 (Seg-Dom)
    # Queremos Domingo como 0, então deslocamos +1 e mod 7
    # Seg(0)->1, Ter(1)->2, ..., Sáb(5)->6, Dom(6)->0
    start_day = (calendar.monthrange(year, month)[0] + 1) % 7
    
    current_row = 0
    current_col = start_day
    
    for day in range(1, num_days + 1):
        key = f"CALENDAR_DAY{day}"
        
        calendar_subs[key] = {
            "text": str(day),
            "x_percent": current_col * cell_width,
            "y_percent": current_row * cell_height,
            "width_percent": cell_width,
            "height_percent": cell_height,
            "font_size_percent": 0.03,
            "background": True if day == now.day else False,
            "color": primary_color
        }
        
        current_col += 1
        if current_col >= cols:
            current_col = 0
            current_row += 1
            
    return calendar_subs

def build_ui():
    vars = getVars('content_index')
    for i, (menu, vals) in enumerate(DICT['contentvals'].items()): 
        frame={
            'visible': i==vars,
            'background':True,
            'subelements':{},
        }
        
        # Cópia profunda de vals para evitar modificar DICT original
        vals_copy = copy.deepcopy(vals)
        
        # Injeta dias do calendário se for painel de clima
        if 'format' in vals_copy and vals_copy['format'] == 'weather':
            # Precisamos encontrar CALENDAR_FRAME na estrutura e populá-lo
            # A estrutura está em DICT['format']['weather']
            # Mas aqui estamos iterando sobre contentvals.
            # O 'vals' aqui é apenas {'format': 'weather'}
            
            # Precisamos modificar o formato carregado de DICT['format']['weather']
            # Mas não podemos modificar DICT diretamente ou persistirá/duplicará em re-renders se fosséssemos re-renderizar
            # Porém, build_ui é chamado uma vez.
            
            # Vamos obter o formato de clima
            weather_format = copy.deepcopy(DICT['format']['weather'])
            
            # Encontra CALENDAR_FRAME
            if 'subelements' in weather_format:
                if 'WEATHER_DISPLAY' in weather_format['subelements']:
                    if 'subelements' in weather_format['subelements']['WEATHER_DISPLAY']:
                        if 'CALENDAR_FRAME' in weather_format['subelements']['WEATHER_DISPLAY']['subelements']:
                            calendar_frame = weather_format['subelements']['WEATHER_DISPLAY']['subelements']['CALENDAR_FRAME']
                            calendar_frame['subelements'] = generate_calendar_subelements()
            
            # Agora usa este formato modificado para este item de menu
            # Precisamos construir manualmente o conteúdo do frame porque o loop abaixo espera pares chave-valor
            # que mapeiam para subelementos.
            
            # Na verdade, o loop abaixo itera sobre chaves em 'vals'.
            # Para WEATHER, vals é {"format": "weather"}
            # O loop vê key="format", val="weather"
            # Verifica se 'format' em name (sim) e DICT['format'][val] existe (sim)
            # Então define format=DICT['format'][val]
            
            # Então precisamos interceptar este caso específico no loop
            pass

        enums=list(enumerate(vals.items()))
        for j, (name, val) in enums:
            format={}
            
            if 'format' in name and DICT['format'][val]:
                if val == 'weather':
                 # Tratamento especial para clima para injetar calendário
                     format = copy.deepcopy(DICT['format'][val])
                     # Injeta calendário
                     try:
                        format['subelements']['WEATHER_DISPLAY']['subelements']['CALENDAR_FRAME']['subelements'] = generate_calendar_subelements()
                     except KeyError:
                         print("Could not inject calendar: structure mismatch")
                else:
                    format=DICT['format'][val]
            else:
                format = {
                    'text': name + " : ",
                    'y_percent': j * 0.33,
                    'height_percent': 0.33,
                    'font_size_percent': 0.05,
                    'text_align': 'left',
                    'color': primary_color,
                    'subelements': {
                        name + "value": {
                            'x_percent': 0.665,
                            'width_percent': 0.33,
                            'text': val,
                            'color': secondary_color,
                            'inverted_colors': True,
                            'font_size_percent': 0.05,
                        }
                    }
                }
            frame['subelements'][name] = format 
        user_interface['content_panel'].add_subelement(menu, frame)

def get_all_clickable(element):
    buttons = []
    if element.clickable:
        buttons.append(element)
    for subelement_key in element.subelements:
        subelement = element.subelements[subelement_key]
        if subelement.visible:
            buttons.extend(get_all_clickable(subelement))
    return buttons

def clickable_elements():
    buttons=[]
    
    for element_key in user_interface:
        element = user_interface[element_key]
        buttons.extend(get_all_clickable(element))
    return buttons

def render_ui(screen):
    for element_key in user_interface:
        element = user_interface[element_key]   
        element.draw(screen)
    return user_interface