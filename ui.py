import pygame
import os
from config import DICT, DEFS, getVars
from game_clock import Glock
from graphics import TeeVee
import datetime
import calendar
import copy

# --- UI System ---
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

def set_tv(tv_instance):
    global TV
    TV = tv_instance

def set_map_system(map_sys):
    global MAP_SYSTEM
    MAP_SYSTEM = map_sys

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
    
    # Define User Interface
    user_interface.update({
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
                    'font_size_percent':0.05,
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
                    'font_size_percent':0.05,
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
        self.text_surface = self.font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.text_align = text_align
        
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
                    # Handle cases like "Rain: !weather_rain %" where ! is inside
                    # We need to extract the variable name. Assuming simple !var format
                    # or !var_name
                    
                    # Simple approach: if word starts with !, try to replace it
                    # If it contains !, split by ! and replace the part after
                    
                    prefix = ""
                    suffix = ""
                    command = word
                    
                    if '!' in word:
                        parts = word.split('!')
                        prefix = parts[0]
                        command = parts[1]
                        # Handle potential punctuation after command?
                        # For now assume clean separation or simple suffix
                    
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
                    elif command=="play":
                        if glock.player.is_playing:
                            val = "II"
                        else:
                            val = "p"
                    elif command=="music_display":
                        img=glock.player.cover_art
                        surf=pygame.transform.scale(img, (self.rect.height, self.rect.height))
                        rect=surf.get_rect(center=self.rect.center)
                        #apply transparency
                        surf.set_alpha(128)
                        screen.blit(surf, rect)
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
                        val = "" # Don't print anything for map command
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
                txt = "" # If all replacements resulted in empty strings (like map_render), keep it empty
            self.update_font(newtext=txt)
            
        """Desenha o botão na superfície"""
        text_surface= self.text_surface
        if self.background:
            if self.inverted_colors:
                pygame.draw.rect(screen, self.color, self.rect, border_radius=30)
            else:
                pygame.draw.rect(screen, self.color, self.rect, self.outline_size, border_radius=30)
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
        self.text_surface = self.font.render(str(text), True,color)
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
    
    # Get number of days in month and start day
    num_days = calendar.monthrange(year, month)[1]
    
    calendar_subs = {}
    
    # Grid layout: 7 columns (Mon-Sun), 5-6 rows
    cols = 7
    rows = 6
    
    cell_width = 1.0 / cols
    cell_height = 1.0 / rows
    
    # Start position (offset for first day of month)
    # monthrange returns (weekday, days). weekday is 0-6 (Mon-Sun)
    # We want Sunday to be 0, so we shift by +1 and mod 7
    # Mon(0)->1, Tue(1)->2, ..., Sat(5)->6, Sun(6)->0
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
        
        # Deep copy vals to avoid modifying the original DICT
        vals_copy = copy.deepcopy(vals)
        
        # Inject calendar days if this is the weather panel
        if 'format' in vals_copy and vals_copy['format'] == 'weather':
            # We need to find the CALENDAR_FRAME in the structure and populate it
            # The structure is in DICT['format']['weather']
            # But here we are iterating over contentvals.
            # The 'vals' here is just {'format': 'weather'}
            
            # We need to modify the loaded format from DICT['format']['weather']
            # But we can't modify DICT directly or it will persist/duplicate on re-renders if we were to re-render
            # However, build_ui is called once.
            
            # Let's get the weather format
            weather_format = copy.deepcopy(DICT['format']['weather'])
            
            # Find CALENDAR_FRAME
            if 'subelements' in weather_format:
                if 'WEATHER_DISPLAY' in weather_format['subelements']:
                    if 'subelements' in weather_format['subelements']['WEATHER_DISPLAY']:
                        if 'CALENDAR_FRAME' in weather_format['subelements']['WEATHER_DISPLAY']['subelements']:
                            calendar_frame = weather_format['subelements']['WEATHER_DISPLAY']['subelements']['CALENDAR_FRAME']
                            calendar_frame['subelements'] = generate_calendar_subelements()
            
            # Now use this modified format for this menu item
            # We need to manually construct the frame content because the loop below expects key-value pairs
            # that map to subelements.
            
            # Actually, the loop below iterates over keys in 'vals'.
            # For WEATHER, vals is {"format": "weather"}
            # The loop sees key="format", val="weather"
            # It checks if 'format' in name (yes) and DICT['format'][val] exists (yes)
            # Then it sets format=DICT['format'][val]
            
            # So we need to intercept this specific case in the loop
            pass

        enums=list(enumerate(vals.items()))
        for j, (name, val) in enums:
            format={}
            
            if 'format' in name and DICT['format'][val]:
                if val == 'weather':
                     # Special handling for weather to inject calendar
                     format = copy.deepcopy(DICT['format'][val])
                     # Inject calendar
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