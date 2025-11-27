import math
import time
import urllib.request
import json
import random
import pygame
import requests
from io import BytesIO
import threading
import configparser

def load_map_config():
    """Carrega configurações do mapa do arquivo INI"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Cores
    colors = {
        'background': tuple(map(int, config.get('colors', 'background').split(','))),
        'highlight': tuple(map(int, config.get('colors', 'highlight').split(','))),
        'text': tuple(map(int, config.get('colors', 'text').split(','))),
        'accent': tuple(map(int, config.get('colors', 'accent').split(',')))
    }
    
    # Configurações do mapa
    map_config = {
        'min_zoom': config.getint('map', 'min_zoom'),
        'max_zoom': config.getint('map', 'max_zoom'),
        'initial_zoom': config.getint('map', 'initial_zoom'),
        'tiles_wide': config.getint('map', 'tiles_wide'),
        'tiles_high': config.getint('map', 'tiles_high'),
        'map_update_interval': config.getint('map', 'map_update_interval'),
        'max_offset': config.getfloat('map', 'max_offset')
    }
    
    return colors, map_config

# Carregar configurações globais
COLORS, MAP_CONFIG = load_map_config()

class SmartPipBoyMap:
    def __init__(self):
        self.location_cache = None
        self.last_location_update = 0
        
    def get_real_location(self):
        """Obtém localização real por IP"""
        current_time = time.time()
        
        if self.location_cache and current_time - self.last_location_update < 3600:
            return self.location_cache
            
        try:
            with urllib.request.urlopen('http://ipapi.co/json/', timeout=5) as response:
                data = json.loads(response.read().decode())
                
                location = {
                    'lat': data.get('latitude', 42.355),
                    'lon': data.get('longitude', -71.065),
                    'city': data.get('city', 'Unknown'),
                    'country': data.get('country_name', 'Unknown'),
                    'region': data.get('region', 'Unknown')
                }
                
                self.location_cache = location
                self.last_location_update = current_time
                return location
                
        except:
            return {
                'lat': 42.355, 
                'lon': -71.065,
                'city': 'Boston Common',
                'country': 'Commonwealth',
                'region': 'Massachusetts'
            }

class RobustMap:
    def __init__(self):
        self.cache = {}
        self.tile_servers = [
            "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "https://b.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "https://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
        ]
        
    def get_tile(self, x, y, zoom):
        """Obtém um tile individual com cache"""
        cache_key = f"{x}_{y}_{zoom}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        for server in self.tile_servers:
            try:
                url = server.format(z=zoom, x=x, y=y)
                print(f"📡 Baixando tile: {url}")  # Debug
                response = requests.get(url, timeout=3, headers={
                    'User-Agent': 'PipBoy-3000-MKIV/1.0 (Educational Project)'
                })
                
                if response.status_code == 200:
                    image_file = BytesIO(response.content)
                    tile_surface = pygame.image.load(image_file).convert()
                    
                    # Aplicar filtro verde Pip-Boy
                    green_overlay = pygame.Surface(tile_surface.get_size(), pygame.SRCALPHA)
                    green_overlay.fill((0, 100, 0, 80))
                    tile_surface.blit(green_overlay, (0, 0))
                    
                    self.cache[cache_key] = tile_surface
                    return tile_surface
                    
            except Exception as e:
                print(f"❌ Erro no tile {x},{y}: {e}")
                continue
        return None

class MapManager:
    def __init__(self, content_area_rect=None):
        self.robust_map = RobustMap()
        self.smart_map = SmartPipBoyMap()
        
        # Configurações do INI
        self.current_zoom = MAP_CONFIG['initial_zoom']
        self.min_zoom = MAP_CONFIG['min_zoom']
        self.max_zoom = MAP_CONFIG['max_zoom']
        
        # Sistema de navegação
        self.map_offset_x = 0
        self.map_offset_y = 0
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.last_offset_x = 0
        self.last_offset_y = 0
        
        self.last_map_update = 0
        self.map_update_interval = MAP_CONFIG['map_update_interval']
        
        # Configuração otimizada do INI
        self.tiles_wide = MAP_CONFIG['tiles_wide']
        self.tiles_high = MAP_CONFIG['tiles_high']
        self.max_offset = MAP_CONFIG['max_offset']
        
        # Área de conteúdo para dimensionamento
        self.content_area = content_area_rect
        
        self.current_map_surface = None
        self.current_map_source = "LOADING..."
        self.current_location = None
        self.is_loading = False
        self.loading_thread = None
        
    def set_content_area(self, content_area_rect):
        """Define a área de conteúdo para dimensionamento do mapa"""
        self.content_area = content_area_rect
        
    def lat_lon_to_tile(self, lat, lon, zoom):
        """Converte latitude/longitude para coordenadas de tile CORRETAMENTE"""
        # Fórmula correta para o sistema de tiles da web
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        
        # X (longitude) - simples
        x_tile = int((lon + 180.0) / 360.0 * n)
        
        # Y (latitude) - fórmula Mercator INVERTIDA para web tiles
        y_tile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        
        print(f"📍 Coordenadas: lat={lat}, lon={lon}")
        print(f"🗺️  Tile coordinates: x={x_tile}, y={y_tile}, zoom={zoom}")
        
        return x_tile, y_tile
    
    def get_static_map(self, lat, lon):
        """Interface otimizada - não bloqueante"""
        current_time = pygame.time.get_ticks()
        
        # Se já temos um mapa e não está na hora de atualizar, retorna o cache
        if (self.current_map_surface and 
            current_time - self.last_map_update < self.map_update_interval and
            not self.is_loading):
            return self.current_map_surface, self.current_map_source
        
        # Se não está carregando, inicia o carregamento
        if not self.is_loading and not self.loading_thread:
            self.is_loading = True
            self.current_map_source = "LOADING..."
            self.loading_thread = threading.Thread(
                target=self._load_map_async, 
                args=(lat, lon)
            )
            self.loading_thread.daemon = True
            self.loading_thread.start()
        
        return self.current_map_surface, self.current_map_source
    
    def _load_map_async(self, lat, lon):
        """Carrega o mapa em uma thread separada"""
        try:
            print(f"🔄 Carregando mapa assincronamente (zoom {self.current_zoom})...")
            
            # Calcular tile central CORRETAMENTE
            center_x, center_y = self.lat_lon_to_tile(lat, lon, self.current_zoom)
            
            # Aplicar offset de navegação
            center_x += self.map_offset_x
            center_y += self.map_offset_y
            
            # Calcular tiles necessários
            start_x = int(center_x - self.tiles_wide // 2)
            start_y = int(center_y - self.tiles_high // 2)
            
            print(f"🎯 Centro do mapa: tile({center_x}, {center_y})")
            print(f"📐 Área: tiles {start_x},{start_y} a {start_x + self.tiles_wide},{start_y + self.tiles_high}")
            
            # Criar surface para o mapa - dimensionada para a área de conteúdo
            tile_size = 256
            map_width = self.tiles_wide * tile_size
            map_height = self.tiles_high * tile_size
            
            # Se temos uma área de conteúdo, ajustar o tamanho do mapa
            if self.content_area:
                # Calcular escala para caber na área de conteúdo mantendo proporção
                content_width = self.content_area.width - 40  # Margem
                content_height = self.content_area.height - 40  # Margem
                
                scale_x = content_width / map_width
                scale_y = content_height / map_height
                scale = min(scale_x, scale_y, 1.0)  # Não aumentar além do original
                
                map_width = int(map_width * scale)
                map_height = int(map_height * scale)
                tile_size = int(256 * scale)
            
            new_map_surface = pygame.Surface((map_width, map_height))
            new_map_surface.fill((0, 15, 0))
            
            # Carregar tiles
            tiles_loaded = 0
            for y in range(self.tiles_high):
                for x in range(self.tiles_wide):
                    tile_x = start_x + x
                    tile_y = start_y + y
                    
                    # Verificar se o tile está dentro dos limites válidos
                    max_tile = 2 ** self.current_zoom - 1
                    if 0 <= tile_x <= max_tile and 0 <= tile_y <= max_tile:
                        tile_surface = self.robust_map.get_tile(tile_x, tile_y, self.current_zoom)
                        if tile_surface:
                            # Redimensionar tile se necessário
                            if self.content_area and tile_surface.get_size() != (tile_size, tile_size):
                                tile_surface = pygame.transform.scale(tile_surface, (tile_size, tile_size))
                            new_map_surface.blit(tile_surface, (x * tile_size, y * tile_size))
                            tiles_loaded += 1
                        else:
                            print(f"❌ Tile falhou: {tile_x},{tile_y}")
                    else:
                        print(f"⚠️  Tile fora dos limites: {tile_x},{tile_y}")
            
            self.current_map_surface = new_map_surface
            self.current_map_source = f"REAL MAP ({tiles_loaded}/{self.tiles_wide * self.tiles_high} tiles)"
            self.current_location = self.smart_map.get_real_location()
            self.last_map_update = pygame.time.get_ticks()
            
            print(f"✅ Mapa carregado: {tiles_loaded} tiles no zoom {self.current_zoom}")
            
        except Exception as e:
            print(f"❌ Erro no carregamento: {e}")
            self.current_map_surface = self._create_fallback_map()
            self.current_map_source = "FALLBACK MODE"
        finally:
            self.is_loading = False
            self.loading_thread = None
    
    def _create_fallback_map(self):
        """Cria um mapa de fallback rápido"""
        width = self.tiles_wide * 256
        height = self.tiles_high * 256
        
        # Ajustar tamanho para área de conteúdo
        if self.content_area:
            content_width = self.content_area.width - 40
            content_height = self.content_area.height - 40
            
            scale_x = content_width / width
            scale_y = content_height / height
            scale = min(scale_x, scale_y, 1.0)
            
            width = int(width * scale)
            height = int(height * scale)
        
        fallback = pygame.Surface((width, height))
        fallback.fill((0, 15, 0))
        
        # Grade simples
        tile_size = width // self.tiles_wide
        for i in range(1, self.tiles_wide):
            x = i * tile_size
            pygame.draw.line(fallback, COLORS['accent'], (x, 0), (x, height), 1)
        for i in range(1, self.tiles_high):
            y = i * tile_size
            pygame.draw.line(fallback, COLORS['accent'], (0, y), (width, y), 1)
        
        # Texto de fallback
        try:
            font = pygame.font.Font(None, 36)
            text = font.render("MAP DATA UNAVAILABLE", True, (255, 100, 100))
            text_rect = text.get_rect(center=(width//2, height//2))
            fallback.blit(text, text_rect)
        except:
            pass
        
        return fallback
    
    # Sistema de Navegação
    def start_drag(self, mouse_x, mouse_y):
        """Inicia o arrastar do mapa"""
        self.is_dragging = True
        self.drag_start_x = mouse_x
        self.drag_start_y = mouse_y
        self.last_offset_x = self.map_offset_x
        self.last_offset_y = self.map_offset_y
    
    def update_drag(self, mouse_x, mouse_y):
        """Atualiza a posição do mapa durante o arrasto"""
        if self.is_dragging:
            # Calcular deslocamento (invertido para movimento natural)
            dx = (self.drag_start_x - mouse_x) // 2
            dy = (self.drag_start_y - mouse_y) // 2
            
            # Atualizar offset (mais sensível)
            self.map_offset_x = self.last_offset_x + dx / 128.0
            self.map_offset_y = self.last_offset_y + dy / 128.0
            
            # Limitar o deslocamento máximo
            self.map_offset_x = max(-self.max_offset, min(self.max_offset, self.map_offset_x))
            self.map_offset_y = max(-self.max_offset, min(self.max_offset, self.map_offset_y))
    
    def end_drag(self):
        """Finaliza o arrastar e recarrega o mapa"""
        if self.is_dragging:
            self.is_dragging = False
            self.force_map_update()
    
    def reset_navigation(self):
        """Reseta a navegação para a posição original"""
        self.map_offset_x = 0
        self.map_offset_y = 0
        self.force_map_update()
    
    def zoom_in(self):
        """Aumenta o zoom"""
        if self.current_zoom < self.max_zoom:
            self.current_zoom += 1
            # Ajustar offset para manter a posição relativa
            self.map_offset_x *= 2
            self.map_offset_y *= 2
            self.force_map_update()
            print(f"🔍 Zoom IN para: {self.current_zoom}")
    
    def zoom_out(self):
        """Diminui o zoom"""
        if self.current_zoom > self.min_zoom:
            self.current_zoom -= 1
            # Ajustar offset para manter a posição relativa
            self.map_offset_x /= 2
            self.map_offset_y /= 2
            self.force_map_update()
            print(f"🔍 Zoom OUT para: {self.current_zoom}")
    
    def increase_size(self):
        if self.tiles_wide < 4:
            self.tiles_wide += 1
            self.force_map_update()
    
    def decrease_size(self):
        if self.tiles_wide > 2:
            self.tiles_wide -= 1
            self.force_map_update()
    
    def force_map_update(self):
        self.current_map_surface = None
        self.last_map_update = 0
        if self.loading_thread:
            self.loading_thread = None
        self.is_loading = False
    
    def get_zoom_level(self):
        return self.current_zoom
    
    def get_map_size(self):
        return f"{self.tiles_wide}x{self.tiles_high}"
    
    def get_navigation_status(self):
        """Retorna status da navegação"""
        if self.map_offset_x == 0 and self.map_offset_y == 0:
            return "CENTERED"
        else:
            return f"OFFSET: {self.map_offset_x:.1f}, {self.map_offset_y:.1f}"
    
    def get_current_location(self):
        if self.current_location:
            return self.current_location
        return self.smart_map.get_real_location()

class RealMap:
    def __init__(self, content_area_rect=None):
        self.map_manager = MapManager(content_area_rect)
        
    def set_content_area(self, content_area_rect):
        """Define a área de conteúdo para o mapa"""
        self.map_manager.set_content_area(content_area_rect)
        
    def get_static_map(self, lat, lon):
        return self.map_manager.get_static_map(lat, lon)