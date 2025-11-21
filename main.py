# main.py
import pygame
import sys
import utilities

# Inicialização
pygame.init()
screen,DEFS, SHEET, PROPSYS, SPRITE_LOADER = utilities.initialize()
OVERLAY_IMAGE = pygame.image.load("overlay.png").convert_alpha()
pygame.display.set_caption("Euphemerais")
clock = pygame.time.Clock()
tv = utilities.TeeVee()
# Loop principal
Button= utilities.Button
topbar=["CONF","STATS","INFO"]
buttons = []
spacing=1/(len(topbar)+2)
for i, text in enumerate(topbar):
    button = Button(        
        x_percent=i * spacing+spacing,
        y_percent=0.0,
        width_percent=spacing,
        height_percent=0.1,
        text=text,
        color=(255,255,255),
        font_size_percent=0.05
    )
    buttons.append(button)
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
    # Limpa a tela
    screen.fill((50, 50, 50))
    # Desenha a TV
    tv.draw()
    for button in buttons:
        button.draw(screen)
    OVERLAY_IMAGE = pygame.transform.scale(OVERLAY_IMAGE, (DEFS['width'], DEFS['height']))
    screen.blit(OVERLAY_IMAGE, (0, 0))
    
    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()