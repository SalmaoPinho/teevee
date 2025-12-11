"""
Demonstração de Barrel Distortion (Distorção de Barril)
Simula a curvatura de monitores CRT antigos aplicada à tela toda
"""

import pygame
import math
import numpy as np

pygame.init()

# Configurações
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Barrel Distortion - Efeito CRT")
clock = pygame.time.Clock()

# Cores
BG_COLOR = (20, 20, 30)
PRIMARY = (100, 150, 255)
SECONDARY = (255, 100, 150)
ACCENT = (100, 255, 150)

def apply_barrel_distortion(source_surface, distortion_strength=0.2):
    """
    Aplica distorção de barril a uma superfície
    Args:
        source_surface: Superfície original
        distortion_strength: Força da distorção (0.0 = sem distorção, 0.5 = muito curvado)
    
    Returns:
        Nova superfície com distorção aplicada
    """
    width, height = source_surface.get_size()
    distorted = pygame.Surface((width, height))
    distorted.fill((0, 0, 0))
    
    # Centro da tela
    center_x = width / 2
    center_y = height / 2
    
    # Raio máximo (diagonal)
    max_radius = math.sqrt(center_x**2 + center_y**2)
    
    # Para cada pixel na superfície de destino
    for y in range(height):
        for x in range(width):
            # Calcula distância do centro (normalizada)
            dx = (x - center_x) / center_x
            dy = (y - center_y) / center_y
            distance = math.sqrt(dx**2 + dy**2)
            
            # Aplica distorção de barril
            # Fórmula: r' = r * (1 + k * r^2)
            # onde k é a força da distorção
            distortion_factor = 1 + distortion_strength * (distance ** 2)
            
            # Calcula nova posição
            new_dx = dx * distortion_factor
            new_dy = dy * distortion_factor
            
            # Converte de volta para coordenadas de pixel
            source_x = int(center_x + new_dx * center_x)
            source_y = int(center_y + new_dy * center_y)
            
            # Verifica se está dentro dos limites
            if 0 <= source_x < width and 0 <= source_y < height:
                color = source_surface.get_at((source_x, source_y))
                distorted.set_at((x, y), color)
    
    return distorted

def draw_test_pattern(surface):
    """Desenha um padrão de teste para visualizar a distorção"""
    width, height = surface.get_size()
    
    # Fundo
    surface.fill(BG_COLOR)
    
    # Grade
    grid_spacing = 50
    for x in range(0, width, grid_spacing):
        pygame.draw.line(surface, (50, 50, 70), (x, 0), (x, height), 1)
    for y in range(0, height, grid_spacing):
        pygame.draw.line(surface, (50, 50, 70), (0, y), (width, y), 1)
    
    # Círculos concêntricos
    center_x, center_y = width // 2, height // 2
    for radius in range(50, min(width, height) // 2, 50):
        pygame.draw.circle(surface, (70, 70, 90), (center_x, center_y), radius, 2)
    
    # Retângulos coloridos
    rect_size = 100
    margin = 150
    
    # Cantos
    pygame.draw.rect(surface, PRIMARY, (margin, margin, rect_size, rect_size), border_radius=15)
    pygame.draw.rect(surface, SECONDARY, (width - margin - rect_size, margin, rect_size, rect_size), border_radius=15)
    pygame.draw.rect(surface, ACCENT, (margin, height - margin - rect_size, rect_size, rect_size), border_radius=15)
    pygame.draw.rect(surface, PRIMARY, (width - margin - rect_size, height - margin - rect_size, rect_size, rect_size), border_radius=15)
    
    # Centro
    pygame.draw.rect(surface, SECONDARY, (center_x - rect_size // 2, center_y - rect_size // 2, rect_size, rect_size), border_radius=15)
    
    # Texto
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    
    title = font_large.render("BARREL DISTORTION", True, (255, 255, 255))
    surface.blit(title, (center_x - title.get_width() // 2, 50))
    
    subtitle = font_small.render("Efeito CRT Simulado", True, (200, 200, 200))
    surface.blit(subtitle, (center_x - subtitle.get_width() // 2, 130))

# Cria superfície de teste
test_surface = pygame.Surface((WIDTH, HEIGHT))

# Variáveis de controle
distortion_strength = 0.15
show_original = False
auto_animate = True
animation_time = 0

# Loop principal
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                show_original = not show_original
            elif event.key == pygame.K_a:
                auto_animate = not auto_animate
            elif event.key == pygame.K_UP:
                distortion_strength = min(0.5, distortion_strength + 0.02)
            elif event.key == pygame.K_DOWN:
                distortion_strength = max(0.0, distortion_strength - 0.02)
            elif event.key == pygame.K_r:
                distortion_strength = 0.15
    
    # Atualiza animação
    if auto_animate:
        animation_time += clock.get_time() / 1000.0
        distortion_strength = 0.15 + 0.1 * math.sin(animation_time)
    
    # Desenha padrão de teste
    draw_test_pattern(test_surface)
    
    # Aplica distorção ou mostra original
    if show_original:
        screen.blit(test_surface, (0, 0))
    else:
        distorted = apply_barrel_distortion(test_surface, distortion_strength)
        screen.blit(distorted, (0, 0))
    
    # UI de controle
    font_ui = pygame.font.Font(None, 24)
    
    controls = [
        f"Distorção: {distortion_strength:.2f}",
        f"ESPAÇO: {'Original' if show_original else 'Distorcido'}",
        f"A: Animação {'ON' if auto_animate else 'OFF'}",
        "↑/↓: Ajustar distorção",
        "R: Reset",
        "ESC: Sair"
    ]
    
    y_offset = HEIGHT - 150
    for i, text in enumerate(controls):
        label = font_ui.render(text, True, (200, 200, 200))
        # Fundo semi-transparente
        bg_rect = pygame.Rect(10, y_offset + i * 25 - 2, label.get_width() + 10, 22)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 180))
        screen.blit(bg_surface, bg_rect.topleft)
        screen.blit(label, (15, y_offset + i * 25))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
