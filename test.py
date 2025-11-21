import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Filtro CRT")

# Criar uma superfície para o fundo (simulando conteúdo)
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill((255, 255, 255))  # Fundo branco

# Adicionar alguns elementos visuais ao fundo para teste
pygame.draw.rect(background, (200, 100, 100), (100, 100, 200, 150))
pygame.draw.circle(background, (100, 200, 100), (400, 300), 80)
pygame.draw.line(background, (100, 100, 200), (50, 500), (750, 500), 5)

# Criar textura CRT
crt_texture = pygame.image.load("assets/rgb.png").convert_alpha()
#aplicar transparencia
crt_texture.set_alpha(50)
#ajustar tamanho
size=8
crt_texture = pygame.transform.scale(crt_texture, (size, size))

# Criar uma superfície para o efeito CRT
crt_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

# Aplicar a textura CRT em toda a tela
def apply_crt_effect():
    # Limpar a overlay
    crt_overlay.fill((0, 0, 0, 0))
    
    # Aplicar a textura 16x16 repetidamente em toda a tela
    for y in range(0, SCREEN_HEIGHT, size):
        for x in range(0, SCREEN_WIDTH, size):
            crt_overlay.blit(crt_texture, (x, y))

# Aplicar o efeito CRT inicial
apply_crt_effect()

# Loop principal
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Desenhar o fundo
    screen.blit(background, (0, 0))
    
    # Aplicar o efeito CRT
    screen.blit(crt_overlay, (0, 0))
    
    # Atualizar a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()