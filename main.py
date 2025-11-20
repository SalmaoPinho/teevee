# main.py
import pygame
import sys
import utilities
# Inicialização
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Carregador Simples de Sprites")
clock = pygame.time.Clock()

# Cria o carregador
sprite_loader = utilities.spriteLoader()

# Carrega sprites da mesma spritesheet
# Supondo uma spritesheet com vários personagens
sprite_loader.load_spritesheet(
    key="player",
    path="assets/spritesheet.png",
    top_left=(0, 0),      # Canto superior esquerdo do player
    bottom_right=(42, 62), # Canto inferior direito do player
    scale=5
)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Limpa a tela
    screen.fill((50, 50, 50))
    
    # Desenha os sprites
    sprite_loader.draw_sprite(screen, "player", 'center')
    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()