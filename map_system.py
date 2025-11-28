import math
import pygame
import requests
from io import BytesIO
import threading
from config import DEFS

# Configurações do mapa (Hardcoded defaults since config.ini is missing)
MAP_CONFIG = {
    'min_zoom': 2,
    'max_zoom': 18,
    'initial_zoom': 12,
    'tiles_wide': 3,
    'tiles_high': 3,
    'max_offset': 10.0
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
                # print(f"📡 Baixando tile: {url}")  # Debug removed to reduce clutter
                response = requests.get(url, timeout=3, headers={
                    'User-Agent': 'PipBoy-3000-MKIV/1.0 (Educational Project)'
                })
                
                if response.status_code == 200:
                    image_file = BytesIO(response.content)
                    tile_surface = pygame.image.load(image_file).convert()
                    
                    green_overlay = pygame.Surface(tile_surface.get_size(), pygame.SRCALPHA)
                    green_overlay.fill((255, 255, 255, 80))
                    tile_surface.blit(green_overlay, (0, 0))
                    self.cache[cache_key] = tile_surface
                    return tile_surface
                    
            except Exception as e:
                print(f"❌ Erro no tile {x},{y}: {e}")
                continue
        return None

class MapManager:
    def __init__(self, game_clock, content_area_rect=None):
        self.robust_map = RobustMap()
        self.game_clock = game_clock
        
        self.current_zoom = MAP_CONFIG['initial_zoom']
        self.tiles_wide = MAP_CONFIG['tiles_wide']
        self.tiles_high = MAP_CONFIG['tiles_high']
        
        self.content_area = content_area_rect
        
        self.current_map_surface = None
        self.current_map_source = "LOADING..."
        self.is_loading = False
        self.loading_thread = None
        
        # Optimization: Track last rendered location
        self.last_rendered_lat = None
        self.last_rendered_lon = None
        self.last_rendered_zoom = None

    def set_content_area(self, content_area_rect):
        """Define a área de conteúdo para dimensionamento do mapa"""
        self.content_area = content_area_rect

    def zoom_in(self):
        if self.current_zoom < MAP_CONFIG['max_zoom']:
            self.current_zoom += 1
            
    def zoom_out(self):
        if self.current_zoom > MAP_CONFIG['min_zoom']:
            self.current_zoom -= 1
        
    def lat_lon_to_tile(self, lat, lon, zoom):
        """Converte latitude/longitude para coordenadas de tile"""
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        x_tile = int((lon + 180.0) / 360.0 * n)
        y_tile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return x_tile, y_tile
    
    def get_static_map(self, lat, lon):
        """Interface otimizada - não bloqueante"""
        
        # Check if we need to reload
        should_reload = False
        
        if self.current_map_surface is None:
            should_reload = True
        elif self.last_rendered_lat is None or self.last_rendered_lon is None:
            should_reload = True
        elif self.last_rendered_zoom != self.current_zoom:
            should_reload = True
        else:
            # Check for significant location change (approx 11 meters)
            lat_diff = abs(lat - self.last_rendered_lat)
            lon_diff = abs(lon - self.last_rendered_lon)
            if lat_diff > 0.0001 or lon_diff > 0.0001:
                should_reload = True
        
        if should_reload and not self.is_loading:
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
            
            center_x, center_y = self.lat_lon_to_tile(lat, lon, self.current_zoom)
            
            start_x = int(center_x - self.tiles_wide // 2)
            start_y = int(center_y - self.tiles_high // 2)
            
            tile_size = 256
            map_width = self.tiles_wide * tile_size
            map_height = self.tiles_high * tile_size
            
            new_map_surface = pygame.Surface((map_width, map_height))
            new_map_surface.fill((0, 15, 0))
            
            tiles_loaded = 0
            for y in range(self.tiles_high):
                for x in range(self.tiles_wide):
                    tile_x = start_x + x
                    tile_y = start_y + y
                    
                    max_tile = 2 ** self.current_zoom - 1
                    if 0 <= tile_x <= max_tile and 0 <= tile_y <= max_tile:
                        tile_surface = self.robust_map.get_tile(tile_x, tile_y, self.current_zoom)
                        if tile_surface:
                            new_map_surface.blit(tile_surface, (x * tile_size, y * tile_size))
                            tiles_loaded += 1
            
            if self.content_area:
                new_map_surface = pygame.transform.smoothscale(new_map_surface, (self.content_area.width, self.content_area.height))
            
            # Apply rounded corners
            new_map_surface = self._apply_round_corners(new_map_surface, 20)
            
            self.current_map_surface = new_map_surface
            self.current_map_source = f"REAL MAP ({tiles_loaded}/{self.tiles_wide * self.tiles_high} tiles)"
            
            # Update last rendered state
            self.last_rendered_lat = lat
            self.last_rendered_lon = lon
            self.last_rendered_zoom = self.current_zoom
            
            print(f"✅ Mapa carregado: {tiles_loaded} tiles")
            
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
        
        if self.content_area:
            width = self.content_area.width
            height = self.content_area.height
        
        fallback = pygame.Surface((width, height))
        bg_color = DEFS.get('bg', (0, 0, 0))
        accent_color = DEFS.get('sec', (0, 255, 0))
        text_color = DEFS.get('pri', (255, 255, 255))
        
        fallback.fill(bg_color)
        
        tile_size = width // self.tiles_wide
        for i in range(1, self.tiles_wide):
            x = i * tile_size
            pygame.draw.line(fallback, accent_color, (x, 0), (x, height), 1)
        for i in range(1, self.tiles_high):
            y = i * tile_size
            pygame.draw.line(fallback, accent_color, (0, y), (width, y), 1)
        
        try:
            font = pygame.font.Font(None, 36)
            text = font.render("MAP DATA UNAVAILABLE", True, text_color)
            text_rect = text.get_rect(center=(width//2, height//2))
            fallback.blit(text, text_rect)
        except:
            pass
            
        # Apply rounded corners
        fallback = self._apply_round_corners(fallback, 20)
        
        return fallback

    def _apply_round_corners(self, surface, radius):
        """Applies rounded corners to a surface"""
        rect = surface.get_rect()
        mask = pygame.Surface(rect.size, pygame.SRCALPHA)
        
        # Draw rounded rectangle on mask
        pygame.draw.rect(mask, (255, 255, 255), rect, border_radius=radius)
        
        # Create a new surface with alpha channel
        new_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        new_surface.blit(surface, (0, 0))
        
        # Apply mask
        new_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        
        return new_surface

class RealMap:
    def __init__(self, game_clock, content_area_rect=None):
        self.map_manager = MapManager(game_clock, content_area_rect)
        
    def set_content_area(self, content_area_rect):
        """Define a área de conteúdo para o mapa"""
        self.map_manager.set_content_area(content_area_rect)
        
    def get_static_map(self, lat, lon):
        return self.map_manager.get_static_map(lat, lon)