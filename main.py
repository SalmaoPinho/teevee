# main.py
import pygame
import sys
import utilities

# Inicialização
pygame.init()
screen,DEFS, SHEET, PROPSYS, SPRITE_LOADER = utilities.initialize()
OVERLAY_IMAGE = pygame.image.load("assets/overlay.png").convert_alpha()
pygame.display.set_caption("Euphemerais")
clock = pygame.time.Clock()
tv = utilities.TeeVee()
# Loop principal
UElement= utilities.UElement
ui = [
    UElement(        
        x_percent=0.125,
        y_percent=0.05,
        width_percent=0.125,
        height_percent=0.125,
        text="<<",
        clickable=True,
    ),
    UElement(        
        x_percent=0.125,
        y_percent=0.05,
        width_percent=0.75,
        height_percent=0.125,
        text="MENU",
        color=(255,255,255),
        font_size_percent=0.08,
    ),
    UElement(        
        x_percent=0.75,
        y_percent=0.05,
        width_percent=0.125,
        height_percent=0.125,
        text=">>",
        clickable=True,
    ),
    UElement(        
        x_percent=0.125,
        y_percent=0.85,
        width_percent=0.75,
        height_percent=0.125,
        color=(255,255,255),
    ),
    UElement(        
        x_percent=0.125,
        y_percent=0.85,
        width_percent=0.25,
        height_percent=0.125,
        font_size_percent=0.05,
        text="12:00 PM",
        color=(255,255,255),
    ),
    UElement(        
        x_percent=0.625,
        y_percent=0.85,
        width_percent=0.25,
        height_percent=0.125,
        font_size_percent=0.05,
        color=(255,255,255),
        text="Monday",
    ),
    UElement(        
        x_percent=0.125,
        y_percent=0.175,
        width_percent=0.75,
        height_percent=0.675,
        color=(255,255,255),
    ),
    UElement(        
        x_percent=0.125,
        y_percent=0.7,
        width_percent=0.75,
        height_percent=0.125,
        font_size_percent=0.05,
        text="TEsting this is a dialog hello",
    ),
]
crt=utilities.apply_crt_effect()
buttons=[]
for element in ui:
    if element.clickable:
        buttons.append(element)
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
    for elem in ui:
        elem.draw(screen)
    screen.blit(crt, (0, 0))
    OVERLAY_IMAGE = pygame.transform.scale(OVERLAY_IMAGE, (DEFS['width'], DEFS['height']))
    screen.blit(OVERLAY_IMAGE, (0, 0))
    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()