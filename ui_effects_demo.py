"""
Demonstração de Efeitos Visuais para UI
Vários tipos de efeitos que podem ser aplicados para detalhar interfaces
"""

import pygame
import math

pygame.init()

# Configurações
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demonstração de Efeitos de UI")
clock = pygame.time.Clock()

# Cores
BG_COLOR = (20, 20, 30)
PRIMARY = (100, 150, 255)
SECONDARY = (255, 100, 150)
ACCENT = (100, 255, 150)

# ==================== EFEITOS ====================

def apply_inner_shadow(surface, rect, intensity=30, offset=5):
    """Sombra interna - cria profundidade"""
    shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Sombra superior
    for i in range(offset):
        alpha = int(intensity * (1 - i / offset))
        pygame.draw.line(shadow, (0, 0, 0, alpha), (0, i), (rect.width, i))
    
    # Sombra esquerda
    for i in range(offset):
        alpha = int(intensity * (1 - i / offset))
        pygame.draw.line(shadow, (0, 0, 0, alpha), (i, 0), (i, rect.height))
    
    surface.blit(shadow, (0, 0))
    return surface

def apply_outer_glow(surface, rect, color, intensity=50, size=10):
    """Brilho externo - destaque e atenção"""
    glow = pygame.Surface((rect.width + size*2, rect.height + size*2), pygame.SRCALPHA)
    
    for i in range(size):
        alpha = int(intensity * (1 - i / size))
        inflate = i * 2
        glow_rect = pygame.Rect(size - i, size - i, 
                                rect.width + inflate, rect.height + inflate)
        pygame.draw.rect(glow, (*color, alpha), glow_rect, border_radius=20)
    
    return glow

def apply_gradient_overlay(surface, rect, start_color, end_color, vertical=True):
    """Gradiente - transição suave de cores"""
    gradient = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    if vertical:
        for i in range(rect.height):
            ratio = i / rect.height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            pygame.draw.line(gradient, (r, g, b, 100), (0, i), (rect.width, i))
    else:
        for i in range(rect.width):
            ratio = i / rect.width
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            pygame.draw.line(gradient, (r, g, b, 100), (i, 0), (i, rect.height))
    
    surface.blit(gradient, (0, 0))
    return surface

def apply_noise_texture(surface, rect, intensity=20):
    """Textura de ruído - adiciona grão e textura"""
    import random
    noise = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    for _ in range(rect.width * rect.height // 10):  # Densidade do ruído
        x = random.randint(0, rect.width - 1)
        y = random.randint(0, rect.height - 1)
        alpha = random.randint(0, intensity)
        noise.set_at((x, y), (255, 255, 255, alpha))
    
    surface.blit(noise, (0, 0))
    return surface

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

def apply_border_highlight(surface, rect, color, thickness=2, intensity=100):
    """Destaque de borda - define limites"""
    # Borda superior e esquerda (mais clara)
    pygame.draw.line(surface, (*color, intensity), (0, 0), (rect.width, 0), thickness)
    pygame.draw.line(surface, (*color, intensity), (0, 0), (0, rect.height), thickness)
    
    # Borda inferior e direita (mais escura)
    dark = tuple(max(0, c - 50) for c in color)
    pygame.draw.line(surface, (*dark, intensity), (0, rect.height-1), (rect.width, rect.height-1), thickness)
    pygame.draw.line(surface, (*dark, intensity), (rect.width-1, 0), (rect.width-1, rect.height), thickness)
    
    return surface

def apply_glass_effect(surface, rect, blur_amount=5):
    """Efeito de vidro - glassmorphism"""
    glass = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Fundo semi-transparente
    glass.fill((255, 255, 255, 30))
    
    # Brilho no topo
    for i in range(rect.height // 3):
        alpha = int(40 * (1 - i / (rect.height // 3)))
        pygame.draw.line(glass, (255, 255, 255, alpha), (0, i), (rect.width, i))
    
    # Borda sutil
    pygame.draw.rect(glass, (255, 255, 255, 50), (0, 0, rect.width, rect.height), 1, border_radius=15)
    
    surface.blit(glass, (0, 0))
    return surface

def apply_emboss(surface, rect, depth=3):
    """Efeito de relevo - aparência 3D"""
    emboss = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Luz superior esquerda
    for i in range(depth):
        alpha = int(50 * (1 - i / depth))
        pygame.draw.line(emboss, (255, 255, 255, alpha), (i, i), (rect.width - i, i))
        pygame.draw.line(emboss, (255, 255, 255, alpha), (i, i), (i, rect.height - i))
    
    # Sombra inferior direita
    for i in range(depth):
        alpha = int(50 * (1 - i / depth))
        pygame.draw.line(emboss, (0, 0, 0, alpha), (i, rect.height - i - 1), (rect.width - i, rect.height - i - 1))
        pygame.draw.line(emboss, (0, 0, 0, alpha), (rect.width - i - 1, i), (rect.width - i - 1, rect.height - i))
    
    surface.blit(emboss, (0, 0))
    return surface

def apply_pulse_animation(surface, rect, time, speed=2, intensity=30):
    """Animação de pulso - chama atenção"""
    pulse = math.sin(time * speed) * 0.5 + 0.5  # 0 a 1
    alpha = int(intensity * pulse)
    
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, alpha))
    surface.blit(overlay, (0, 0))
    
    return surface

def apply_dot_pattern(surface, rect, spacing=8, dot_size=2, intensity=20):
    """Padrão de pontos - textura sutil"""
    dots = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    for y in range(0, rect.height, spacing):
        for x in range(0, rect.width, spacing):
            pygame.draw.circle(dots, (255, 255, 255, intensity), (x, y), dot_size)
    
    surface.blit(dots, (0, 0))
    return surface

def apply_radial_gradient(surface, rect, center_color, edge_color):
    """Gradiente radial - do centro para as bordas"""
    gradient = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    center_x, center_y = rect.width // 2, rect.height // 2
    max_radius = math.sqrt(center_x**2 + center_y**2)
    
    for y in range(rect.height):
        for x in range(rect.width):
            distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            ratio = min(distance / max_radius, 1.0)
            
            r = int(center_color[0] * (1 - ratio) + edge_color[0] * ratio)
            g = int(center_color[1] * (1 - ratio) + edge_color[1] * ratio)
            b = int(center_color[2] * (1 - ratio) + edge_color[2] * ratio)
            
            gradient.set_at((x, y), (r, g, b, 100))
    
    surface.blit(gradient, (0, 0))
    return surface

def apply_vignette(surface, rect, intensity=80):
    """Vignette - escurece as bordas"""
    vignette = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    center_x, center_y = rect.width // 2, rect.height // 2
    max_radius = math.sqrt(center_x**2 + center_y**2)
    
    for y in range(rect.height):
        for x in range(rect.width):
            distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            ratio = distance / max_radius
            alpha = int(intensity * ratio * ratio)  # Quadrático para suavidade
            
            vignette.set_at((x, y), (0, 0, 0, alpha))
    
    surface.blit(vignette, (0, 0))
    return surface

def apply_diagonal_stripes(surface, rect, spacing=10, intensity=30):
    """Listras diagonais - padrão geométrico"""
    stripes = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    for i in range(-rect.height, rect.width + rect.height, spacing):
        points = [
            (i, 0),
            (i + spacing // 2, 0),
            (i + spacing // 2 - rect.height, rect.height),
            (i - rect.height, rect.height)
        ]
        pygame.draw.polygon(stripes, (255, 255, 255, intensity), points)
    
    surface.blit(stripes, (0, 0))
    return surface

def apply_corner_highlights(surface, rect, size=20, intensity=100):
    """Destaques nos cantos - ênfase visual"""
    highlights = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Canto superior esquerdo
    for i in range(size):
        alpha = int(intensity * (1 - i / size))
        pygame.draw.line(highlights, (255, 255, 255, alpha), (0, i), (size - i, i))
        pygame.draw.line(highlights, (255, 255, 255, alpha), (i, 0), (i, size - i))
    
    # Canto inferior direito (sombra)
    for i in range(size):
        alpha = int(intensity * (1 - i / size))
        y = rect.height - 1 - i
        x = rect.width - 1 - i
        pygame.draw.line(highlights, (0, 0, 0, alpha), (x - size + i, y), (x, y))
        pygame.draw.line(highlights, (0, 0, 0, alpha), (x, y - size + i), (x, y))
    
    surface.blit(highlights, (0, 0))
    return surface

def apply_color_overlay(surface, rect, overlay_color, intensity=50):
    """Sobreposição de cor - tint colorido"""
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    overlay.fill((*overlay_color, intensity))
    surface.blit(overlay, (0, 0))
    return surface

def apply_grid_pattern(surface, rect, grid_size=20, line_width=1, intensity=40):
    """Padrão de grade - estrutura geométrica"""
    grid = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Linhas verticais
    for x in range(0, rect.width, grid_size):
        pygame.draw.line(grid, (255, 255, 255, intensity), (x, 0), (x, rect.height), line_width)
    
    # Linhas horizontais
    for y in range(0, rect.height, grid_size):
        pygame.draw.line(grid, (255, 255, 255, intensity), (0, y), (rect.width, y), line_width)
    
    surface.blit(grid, (0, 0))
    return surface

# ==================== DEMONSTRAÇÃO ====================

def draw_demo_box(x, y, width, height, color, effect_name, effect_func, *args):
    """Desenha uma caixa de demonstração com efeito aplicado"""
    # Superfície base
    box = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(box, color, (0, 0, width, height), border_radius=15)
    
    # Aplica efeito
    rect = pygame.Rect(0, 0, width, height)
    effect_func(box, rect, *args)
    
    # Aplica máscara arredondada final para garantir cantos redondos
    mask = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, width, height), border_radius=15)
    box.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    
    # Desenha na tela
    screen.blit(box, (x, y))
    
    # Label
    font = pygame.font.Font(None, 20)
    label = font.render(effect_name, True, (200, 200, 200))
    screen.blit(label, (x + 5, y + height + 5))

# Loop principal
running = True
time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill(BG_COLOR)
    time += clock.get_time() / 1000.0
    
    # Título
    font_title = pygame.font.Font(None, 48)
    title = font_title.render("Efeitos de UI - Demonstração", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    
    # Grid de efeitos
    box_w, box_h = 180, 120
    margin = 20
    start_x, start_y = 50, 100
    
    # Linha 1
    draw_demo_box(start_x, start_y, box_w, box_h, PRIMARY, 
                  "Inner Shadow", apply_inner_shadow, 30, 5)
    
    draw_demo_box(start_x + (box_w + margin), start_y, box_w, box_h, SECONDARY, 
                  "Gradient Overlay", apply_gradient_overlay, (255, 100, 100), (100, 100, 255))
    
    draw_demo_box(start_x + (box_w + margin) * 2, start_y, box_w, box_h, ACCENT, 
                  "Noise Texture", apply_noise_texture, 25)
    
    draw_demo_box(start_x + (box_w + margin) * 3, start_y, box_w, box_h, PRIMARY, 
                  "Scanlines", apply_scanlines, 3, 20, time * 20)
    
    draw_demo_box(start_x + (box_w + margin) * 4, start_y, box_w, box_h, SECONDARY, 
                  "Border Highlight", apply_border_highlight, (255, 255, 100), 3, 150)
    
    # Linha 2
    draw_demo_box(start_x, start_y + box_h + margin + 30, box_w, box_h, ACCENT, 
                  "Glass Effect", apply_glass_effect, 5)
    
    draw_demo_box(start_x + (box_w + margin), start_y + box_h + margin + 30, box_w, box_h, PRIMARY, 
                  "Emboss", apply_emboss, 4)
    
    draw_demo_box(start_x + (box_w + margin) * 2, start_y + box_h + margin + 30, box_w, box_h, SECONDARY, 
                  "Pulse Animation", apply_pulse_animation, time, 2, 40)
    
    draw_demo_box(start_x + (box_w + margin) * 3, start_y + box_h + margin + 30, box_w, box_h, ACCENT, 
                  "Dot Pattern", apply_dot_pattern, 6, 1, 30)
    
    # Outer Glow (precisa ser desenhado diferente)
    glow_x = start_x + (box_w + margin) * 4
    glow_y = start_y + box_h + margin + 30
    glow_rect = pygame.Rect(0, 0, box_w, box_h)
    glow_surface = apply_outer_glow(pygame.Surface((box_w, box_h), pygame.SRCALPHA), 
                                     glow_rect, PRIMARY, 80, 15)
    screen.blit(glow_surface, (glow_x - 15, glow_y - 15))
    box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    pygame.draw.rect(box, PRIMARY, (0, 0, box_w, box_h), border_radius=15)
    screen.blit(box, (glow_x, glow_y))
    font = pygame.font.Font(None, 20)
    label = font.render("Outer Glow", True, (200, 200, 200))
    screen.blit(label, (glow_x + 5, glow_y + box_h + 5))
    
    # Linha 3 - Novos efeitos
    draw_demo_box(start_x, start_y + (box_h + margin + 30) * 2, box_w, box_h, PRIMARY, 
                  "Radial Gradient", apply_radial_gradient, (255, 200, 100), (100, 100, 255))
    
    draw_demo_box(start_x + (box_w + margin), start_y + (box_h + margin + 30) * 2, box_w, box_h, SECONDARY, 
                  "Vignette", apply_vignette, 100)
    
    draw_demo_box(start_x + (box_w + margin) * 2, start_y + (box_h + margin + 30) * 2, box_w, box_h, ACCENT, 
                  "Diagonal Stripes", apply_diagonal_stripes, 8, 40)
    
    draw_demo_box(start_x + (box_w + margin) * 3, start_y + (box_h + margin + 30) * 2, box_w, box_h, PRIMARY, 
                  "Corner Highlights", apply_corner_highlights, 25, 120)
    
    draw_demo_box(start_x + (box_w + margin) * 4, start_y + (box_h + margin + 30) * 2, box_w, box_h, SECONDARY, 
                  "Color Overlay", apply_color_overlay, (100, 255, 100), 70)
    
    # Linha 4 - Mais efeitos
    draw_demo_box(start_x, start_y + (box_h + margin + 30) * 3, box_w, box_h, ACCENT, 
                  "Grid Pattern", apply_grid_pattern, 15, 2, 50)
    
    # Instruções
    font_small = pygame.font.Font(None, 24)
    instructions = font_small.render("Pressione ESC para sair | 16 Efeitos Visuais", True, (150, 150, 150))
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
