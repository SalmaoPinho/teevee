# simple_sprite_loader.py
import pygame
import os

class spriteLoader:
    def __init__(self):
        self.sprites = {}
    
    def load_spritesheet(self, key, path, top_left, bottom_right, scale=1.0):
        """
        Carrega uma spritesheet e extrai uma área específica
        
        Args:
            key: Nome para identificar o sprite
            path: Caminho do arquivo da spritesheet
            top_left: (x, y) do canto superior esquerdo da área
            bottom_right: (x, y) do canto inferior direito da área
            scale: Fator de escala (opcional)
        """
        try:
            if not os.path.exists(path):
                print(f"Erro: Arquivo não encontrado - {path}")
                return None
            
            # Carrega a spritesheet completa
            sheet = pygame.image.load(path).convert_alpha()
            
            # Calcula a largura e altura da área desejada
            x1, y1 = top_left
            x2, y2 = bottom_right
            width = x2 - x1
            height = y2 - y1
            
            # Extrai a área específica
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(sheet, (0, 0), (x1, y1, width, height))
            
            # Aplica escala se necessário
            if scale != 1.0:
                new_width = int(width * scale)
                new_height = int(height * scale)
                sprite = pygame.transform.scale(sprite, (new_width, new_height))
            
            self.sprites[key] = sprite
            print(f"Sprite '{key}' carregado: {sprite.get_size()}")
            return sprite
            
        except Exception as e:
            print(f"Erro ao carregar sprite {key}: {e}")
            return None
    
    def get_sprite(self, key):
        """Retorna um sprite pela chave"""
        return self.sprites.get(key)
    
    def draw_sprite(self, surface, key, position):
        """Desenha um sprite na superfície"""
        sprite = self.get_sprite(key)
        if position=='center':
            rect = sprite.get_rect()
            position = (surface.get_width()//2 - rect.width//2, surface.get_height()//2 - rect.height//2)
        if sprite:
            surface.blit(sprite, position)
            return True
        return False