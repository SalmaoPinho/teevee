# main.py
import pygame
import sys
import utilities
screen,DEFS, SHEET, PROPSYS, SPRITE_LOADER, GAME_CLOCK = utilities.initialize()
# Inicialização
pygame.init()
import ui
OVERLAY_IMAGE = pygame.image.load("assets/overlay.png").convert_alpha()
pygame.display.set_caption("Euphemeris")
clock = pygame.time.Clock()
tv = utilities.TeeVee()
if DEFS['fullscreen']:
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
crt=utilities.apply_crt_effect()
buttons=ui.clickable_elements()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event.pos, event):
                    print(f"{button.text} clicado!")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    # Limpa a tela
    screen.fill((50, 50, 50))
    # Desenha a TV
    tv.draw()
    ui.render_ui(screen)    
    screen.blit(crt, (0, 0))
    OVERLAY_IMAGE = pygame.transform.scale(OVERLAY_IMAGE, (DEFS['width'], DEFS['height']))
    screen.blit(OVERLAY_IMAGE, (0, 0))
    GAME_CLOCK.update()
    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()