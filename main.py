import pygame
import sys
import config
import graphics
import ui
import game_clock
import map_system

# Inicialização
pygame.init()

# Load Config
DEFS, DICT = config.load_config()

# Setup Screen
SCREEN = pygame.display.set_mode((int(DEFS['width']), int(DEFS['height'])))
if DEFS['fullscreen']:
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption("Euphemeris")

# Load Assets
SHEET = pygame.image.load("assets/spritesheet.png").convert_alpha()
OVERLAY_IMAGE = pygame.image.load("assets/overlay.png").convert_alpha()

# Init Systems
GAME_CLOCK = game_clock.Glock()
ui.init_ui_system(DEFS['width'], DEFS['height'], GAME_CLOCK)
MAP_SYSTEM = map_system.RealMap(GAME_CLOCK)
ui.set_map_system(MAP_SYSTEM)
SPRITE_LOADER = graphics.init_graphics(SCREEN, SHEET, ui.PROPSYS)

clock = pygame.time.Clock()
global TV
TV = graphics.TeeVee()
ui.set_tv(TV)

crt = graphics.apply_crt_effect()
buttons = ui.clickable_elements()

running = True
content_index = config.getVars('content_index')
categories = list(DICT['contentvals'].keys())

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
                    
                    #divide button name
                    parts = button.name.split("_")
                    if parts[0] == "nav":
                        if parts[1] == "next":
                            content_index = (content_index + 1) % len(categories)
                        else:
                            content_index = (content_index - 1) % len(categories)
                        config.setVars('content_index', content_index)
                        element = ui.searchElement(ui.user_interface['content_panel'], categories[content_index])
                        for name, sibling in element.parent.subelements.items():
                            sibling.visible = False
                        element.visible = True
                        buttons = ui.clickable_elements()
                        
                    elif parts[0] == "music":
                        if parts[1] == "pause":
                            if GAME_CLOCK.player.is_playing:
                                GAME_CLOCK.player.pause()
                                button.text="!SPRITE_play"
                            else:
                                GAME_CLOCK.player.play()
                                button.text="!SPRITE_pause"
                        elif parts[1] == "next":
                            GAME_CLOCK.player.skip_music(dir=1)
                        elif parts[1] == "prev":
                            GAME_CLOCK.player.skip_music(dir=-1)
                        elif parts[1] == "queue":
                            GAME_CLOCK.player.randomize_queue()
                            
                    elif parts[0] == "zoom":
                        if parts[1] == "in":
                            MAP_SYSTEM.map_manager.zoom_in()
                        else:
                            MAP_SYSTEM.map_manager.zoom_out()
                        config.setVars('zoom', MAP_SYSTEM.map_manager.current_zoom)
                        
                    elif parts[0] == "volume":
                        if parts[1] == "up":
                            GAME_CLOCK.player.volume_change(1)
                        else:
                            GAME_CLOCK.player.volume_change(-1)
                    print(f"Clicou no botão: {button.name}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Limpa a tela
    SCREEN.fill(DEFS['bg'])
    
    # Desenha a TV    
    userint = ui.render_ui(SCREEN)    
    SCREEN.blit(crt, (0, 0))
    
    # Scale overlay (casting to int to be safe)
    OVERLAY_SCALED = pygame.transform.scale(OVERLAY_IMAGE, (int(DEFS['width']), int(DEFS['height'])))
    SCREEN.blit(OVERLAY_SCALED, (0, 0))
    
    GAME_CLOCK.update()
    
    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()