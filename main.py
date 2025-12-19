import pygame
import sys
import os
import config
import graphics
import ui
import game_clock
import map_system

# Inicialização
pygame.init()

# Carrega Configuração
DEFS, DICT = config.load_config()

# Configura Tela
SCREEN = pygame.display.set_mode((int(DEFS['width']), int(DEFS['height'])))
if DEFS['fullscreen']:
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption("Euphemeris")

# Carrega Assets
SHEET = pygame.image.load("assets/spritesheet.png").convert_alpha()
OVERLAY_IMAGE = pygame.image.load("assets/overlay.png").convert_alpha()

# Inicializa Sistemas
GAME_CLOCK = game_clock.Glock()
ui.init_ui_system(DEFS['width'], DEFS['height'], GAME_CLOCK)
MAP_SYSTEM = map_system.RealMap(GAME_CLOCK)
ui.set_map_system(MAP_SYSTEM)
SPRITE_LOADER = graphics.init_graphics(SCREEN, SHEET, ui.PROPSYS, GAME_CLOCK)

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
                    
                    # Divide nome do botão
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
                            
                    elif parts[0] == "config":
                        # Handler para botões de configuração
                        setting_name = parts[1]  # fullscreen, crt, scanlines, distortion, overlay
                        config.toggle_setting(setting_name)
                        # Recarrega DEFS (config.load_config() já atualiza config.DEFS)
                        # Atualiza a tela se necessário
                        if setting_name == "fullscreen":
                            if config.DEFS['fullscreen']:
                                SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            else:
                                SCREEN = pygame.display.set_mode((int(config.DEFS['width']), int(config.DEFS['height'])))
                                
                    elif parts[0] == "chat":
                        if parts[1] == "send":
                            # Envia mensagem para Ollama processar
                            if ui.chat_input.strip():
                                # Remove resposta antiga se existir
                                if os.path.exists('response.txt'):
                                    os.remove('response.txt')
                                
                                # Escreve input para arquivo
                                with open('input.txt', 'w', encoding='utf-8') as f:
                                    f.write(ui.chat_input)
                                
                                ui.chat_input = ""
                                ui.waiting_for_response = True
                        elif parts[1] == "input":
                            # Ativa o campo de input
                            ui.chat_input_active = True
                            
                    elif parts[0] == "response":
                        # Navegação entre páginas da resposta
                        if parts[1] == "prev" and ui.current_page > 0:
                            ui.current_page -= 1
                            ui.chat_response = ui.response_pages[ui.current_page]
                            TV.start_talking(ui.chat_response)
                        elif parts[1] == "next" and ui.current_page < len(ui.response_pages) - 1:
                            ui.current_page += 1
                            ui.chat_response = ui.response_pages[ui.current_page]
                            TV.start_talking(ui.chat_response)
                    print(f"Clicou no botão: {button.name}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif ui.chat_input_active:
                # Captura texto quando campo está ativo
                if event.key == pygame.K_RETURN:
                    # Enter envia mensagem
                    if ui.chat_input.strip():
                        # Remove resposta antiga se existir
                        if os.path.exists('response.txt'):
                            os.remove('response.txt')
                        
                        # Escreve input para arquivo
                        with open('input.txt', 'w', encoding='utf-8') as f:
                            f.write(ui.chat_input)
                        
                        ui.chat_input = ""
                        ui.waiting_for_response = True
                    ui.chat_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    ui.chat_input = ui.chat_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    ui.chat_input_active = False
        elif event.type == pygame.TEXTINPUT and ui.chat_input_active:
            # Adiciona caractere digitado
            ui.chat_input += event.text
    
    # Verifica se há resposta do Ollama
    if ui.waiting_for_response and os.path.exists('response.txt'):
        try:
            with open('response.txt', 'r', encoding='utf-8') as f:
                full_response = f.read().strip()
            
            # Divide resposta em páginas
            ui.response_pages = ui.split_response_into_pages(full_response, ui.max_chars_per_page)
            ui.current_page = 0
            ui.chat_response = ui.response_pages[0] if ui.response_pages else ""
            
            # Inicia animação de fala
            TV.start_talking(ui.chat_response)
            
            # Remove arquivo de resposta
            os.remove('response.txt')
            ui.waiting_for_response = False
        except Exception as e:
            print(f"Erro ao ler resposta: {e}")
    
    # Limpa a tela
    SCREEN.fill(DEFS['bg'])
    
    userint = ui.render_ui(SCREEN)   
    GAME_CLOCK.update()
    TV.update()  # Atualiza animação de fala do TeeVee
    # Desenha a TV    
    if DEFS['crt']:
            SCREEN.blit(crt, (0, 0))    
    # Escala overlay (convertendo para int por segurança)
    if DEFS['overlay']:   
        OVERLAY_SCALED = pygame.transform.scale(OVERLAY_IMAGE, (int(DEFS['width']), int(DEFS['height'])))
        SCREEN.blit(OVERLAY_SCALED, (0, 0))
    # Aplica barrel distortion (efeito CRT final)
    if DEFS['distortion']:
        distorted_screen = graphics.apply_barrel_distortion(SCREEN, distortion_strength=0.05)
        SCREEN.blit(distorted_screen, (0, 0))
    if DEFS['scanlines']:
        scanlines = graphics.apply_scanlines(SCREEN, SCREEN.get_rect(), 2, 40, pygame.time.get_ticks() / 50)
        SCREEN.blit(scanlines, (0, 0))
    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()