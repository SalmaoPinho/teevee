"""
Demonstração de Efeitos de Texto
Vários efeitos visuais aplicados em fontes e textos
"""

import pygame
import math
import os
pygame.init()

# Configurações
WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Efeitos de Texto - Demonstração")
clock = pygame.time.Clock()

# Cores
BG_COLOR = (20, 20, 30)
TEXT_COLOR = (255, 255, 255)

# Fontes
font_large = pygame.font.Font(os.path.join("assets", "fonts", "bmspace.ttf"), 72)
font_medium = pygame.font.Font(os.path.join("assets", "fonts", "bmspace.ttf"), 48)
font_small = pygame.font.Font(os.path.join("assets", "fonts", "bmspace.ttf"), 32)

# ==================== EFEITOS DE TEXTO ====================

def draw_text_with_shadow(surface, text, font, pos, color, shadow_color=(0, 0, 0), offset=(3, 3)):
    """Texto com sombra"""
    # Desenha sombra
    shadow = font.render(text, True, shadow_color)
    surface.blit(shadow, (pos[0] + offset[0], pos[1] + offset[1]))
    # Desenha texto
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)

def draw_text_with_outline(surface, text, font, pos, color, outline_color=(0, 0, 0), thickness=2):
    """Texto com contorno"""
    # Desenha contorno em todas as direções
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx != 0 or dy != 0:
                outline = font.render(text, True, outline_color)
                surface.blit(outline, (pos[0] + dx, pos[1] + dy))
    # Desenha texto principal
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)

def draw_text_with_gradient(surface, text, font, pos, color1, color2):
    """Texto com gradiente vertical"""
    text_surf = font.render(text, True, (255, 255, 255))
    width, height = text_surf.get_size()
    
    # Cria superfície com gradiente
    gradient_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(gradient_surf, (r, g, b), (0, y), (width, y))
    
    # Aplica máscara do textof
    text_surf.set_colorkey((0, 0, 0))
    gradient_surf.blit(text_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    
    surface.blit(gradient_surf, pos)

def draw_text_with_glow(surface, text, font, pos, color, glow_color, glow_size=5):
    """Texto com brilho/glow"""
    # Desenha múltiplas camadas de glow
    for i in range(glow_size, 0, -1):
        alpha = int(100 * (1 - i / glow_size))
        glow_surf = font.render(text, True, glow_color)
        glow_surf.set_alpha(alpha)
        for dx in range(-i, i + 1):
            for dy in range(-i, i + 1):
                if math.sqrt(dx**2 + dy**2) <= i:
                    surface.blit(glow_surf, (pos[0] + dx, pos[1] + dy))
    # Desenha texto principal
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)

def draw_text_3d(surface, text, font, pos, color, depth_color, depth=3):
    """Texto com efeito 3D"""
    # Desenha camadas de profundidade
    for i in range(depth, 0, -1):
        depth_surf = font.render(text, True, depth_color)
        surface.blit(depth_surf, (pos[0] + i, pos[1] + i))
    # Desenha texto principal
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)

def draw_text_embossed(surface, text, font, pos, color):
    """Texto com efeito de relevo"""
    # Sombra escura (baixo-direita)
    shadow = font.render(text, True, (50, 50, 50))
    surface.blit(shadow, (pos[0] + 2, pos[1] + 2))
    # Luz clara (cima-esquerda)
    highlight = font.render(text, True, (255, 255, 255))
    surface.blit(highlight, (pos[0] - 1, pos[1] - 1))
    # Texto principal
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)

def draw_text_neon(surface, text, font, pos, color, time):
    """Texto com efeito neon pulsante"""
    # Calcula pulsação
    pulse = math.sin(time * 3) * 0.3 + 0.7
    
    # Glow externo
    for i in range(8, 0, -1):
        alpha = int(50 * pulse * (1 - i / 8))
        glow = font.render(text, True, color)
        glow.set_alpha(alpha)
        for angle in range(0, 360, 45):
            dx = int(math.cos(math.radians(angle)) * i)
            dy = int(math.sin(math.radians(angle)) * i)
            surface.blit(glow, (pos[0] + dx, pos[1] + dy))
    
    # Texto principal com brilho
    text_surf = font.render(text, True, color)
    text_surf.set_alpha(int(255 * pulse))
    surface.blit(text_surf, pos)

def draw_text_pixelated(surface, text, font, pos, color, pixel_size=4):
    """Texto com efeito pixelado"""
    text_surf = font.render(text, True, color)
    width, height = text_surf.get_size()
    
    # Reduz e aumenta para criar efeito pixelado
    small_surf = pygame.transform.scale(text_surf, (width // pixel_size, height // pixel_size))
    pixelated = pygame.transform.scale(small_surf, (width, height))
    
    surface.blit(pixelated, pos)

def draw_text_wavy(surface, text, font, pos, color, time, amplitude=5):
    """Texto com efeito ondulado"""
    x, y = pos
    for i, char in enumerate(text):
        char_surf = font.render(char, True, color)
        offset_y = int(math.sin(time * 2 + i * 0.5) * amplitude)
        surface.blit(char_surf, (x, y + offset_y))
        x += char_surf.get_width()

def draw_text_rainbow(surface, text, font, pos, time):
    """Texto com cores do arco-íris"""
    x, y = pos
    for i, char in enumerate(text):
        # Calcula cor do arco-íris
        hue = (time * 50 + i * 30) % 360
        # Converte HSV para RGB (simplificado)
        h = hue / 60
        c = 255
        x_val = c * (1 - abs(h % 2 - 1))
        
        if h < 1:
            r, g, b = c, x_val, 0
        elif h < 2:
            r, g, b = x_val, c, 0
        elif h < 3:
            r, g, b = 0, c, x_val
        elif h < 4:
            r, g, b = 0, x_val, c
        elif h < 5:
            r, g, b = x_val, 0, c
        else:
            r, g, b = c, 0, x_val
        
        char_surf = font.render(char, True, (int(r), int(g), int(b)))
        surface.blit(char_surf, (x, y))
        x += char_surf.get_width()

def draw_text_chromatic(surface, text, font, pos, offset=2):
    """Texto com aberração cromática"""
    # Canal vermelho
    red_surf = font.render(text, True, (255, 0, 0))
    surface.blit(red_surf, (pos[0] - offset, pos[1]))
    # Canal verde
    green_surf = font.render(text, True, (0, 255, 0))
    surface.blit(green_surf, pos)
    # Canal azul
    blue_surf = font.render(text, True, (0, 0, 255))
    surface.blit(blue_surf, (pos[0] + offset, pos[1]))

# ==================== DEMONSTRAÇÃO ====================

def draw_demo_text(y_pos, effect_name, draw_func, *args):
    """Desenha um exemplo de efeito de texto"""
    # Label do efeito
    label = font_small.render(effect_name, True, (150, 150, 150))
    screen.blit(label, (50, y_pos - 25))
    
    # Aplica efeito
    draw_func(screen, "SAMPLE TEXT", font_medium, (50, y_pos), *args)

# Loop principal
running = True
time = 0
scroll_offset = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                scroll_offset = min(scroll_offset + 30, 0)
            elif event.key == pygame.K_DOWN:
                scroll_offset -= 30
    
    screen.fill(BG_COLOR)
    time += clock.get_time() / 1000.0
    
    # Título
    title = font_large.render("Efeitos de Texto", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    
    # Grid de efeitos (com scroll)
    y = 120 + scroll_offset
    spacing = 90
    
    draw_demo_text(y, "1. Shadow (Sombra)", draw_text_with_shadow, (255, 200, 100), (50, 50, 0), (4, 4))
    y += spacing
    
    draw_demo_text(y, "2. Outline (Contorno)", draw_text_with_outline, (100, 200, 255), (0, 0, 0), 3)
    y += spacing
    
    draw_demo_text(y, "3. Gradient (Gradiente)", draw_text_with_gradient, (255, 100, 150), (100, 100, 255))
    y += spacing
    
    draw_demo_text(y, "4. Glow (Brilho)", draw_text_with_glow, (255, 255, 255), (100, 200, 255), 6)
    y += spacing
    
    draw_demo_text(y, "5. 3D Effect", draw_text_3d, (255, 200, 100), (100, 50, 0), 4)
    y += spacing
    
    draw_demo_text(y, "6. Embossed (Relevo)", draw_text_embossed, (180, 180, 180))
    y += spacing
    
    draw_demo_text(y, "7. Neon (Animado)", draw_text_neon, (0, 255, 200), time)
    y += spacing
    
    draw_demo_text(y, "8. Pixelated", draw_text_pixelated, (255, 150, 200), 3)
    y += spacing
    
    draw_demo_text(y, "9. Wavy (Ondulado)", draw_text_wavy, (200, 255, 100), time, 8)
    y += spacing
    
    draw_demo_text(y, "10. Rainbow (Arco-íris)", draw_text_rainbow, time)
    y += spacing
    
    draw_demo_text(y, "11. Chromatic Aberration", draw_text_chromatic, 3)
    y += spacing
    
    # Instruções
    instructions = font_small.render("↑/↓: Scroll | ESC: Sair | 11 Efeitos de Texto", True, (150, 150, 150))
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
