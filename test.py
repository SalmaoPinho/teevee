import pygame
import sys
from datetime import datetime
from utilities import ProportionalSystem, Button

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Simples Proporcional")

# Sistema proporcional global
PROPSYS = ProportionalSystem(WIDTH, HEIGHT)
import utilities as _utilities
_utilities.PROPSYS = PROPSYS

# Carregar imagem de overlay
try:
    OVERLAY_IMAGE = pygame.image.load("overlay.png").convert_alpha()
    # Redimensionar para caber na tela se necessário
    OVERLAY_IMAGE = pygame.transform.scale(OVERLAY_IMAGE, (WIDTH, HEIGHT))

except:
    print("Erro ao carregar overlay.png, usando fallback")
    # Fallback: criar uma imagem simples com bordas
    OVERLAY_IMAGE = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # Desenhar bordas na imagem de fallback


# Cores (mais transparentes para combinar com overlay)
COLORS = {
    'background': (25, 25, 40, 200),  # Adicionado alpha
    'highlight': (255, 215, 0),
    'text': (240, 240, 240),
    'accent': (65, 105, 225, 150),  # Mais transparente
    'button_normal': (80, 80, 120, 180),
    'button_hover': (100, 100, 160, 220)
}

# Fontes
font_large = pygame.font.SysFont('assets/fonts/bmspace.ttf', 32, bold=True)
font_medium = pygame.font.SysFont('assets/fonts/bmspace.ttf', 24)
font_small = pygame.font.SysFont('assets/fonts/bmspace.ttf', 18)

# Dados do menu
menus = {
    'inicio': ["Novo Jogo", "Carregar", "Opções", "Sair"],
    'config': ["Áudio", "Vídeo", "Controles", "Voltar"],
    'perfil': ["Ver Perfil", "Editar", "Estatísticas", "Voltar"],
    'ajuda': ["Tutorial", "Controles", "Sobre", "Voltar"]
}

current_menu = 'inicio'
current_index = 0

class RoundedButton(Button):
    def __init__(self, x_percent, y_percent, width_percent, height_percent, 
                 text, color=COLORS['button_normal'], hover_color=COLORS['button_hover'], 
                 font_size_percent=0.02, corner_radius=15):
        # Remover alpha para cores do botão (pygame.draw não suporta alpha diretamente)
        color = color[:3] if len(color) == 4 else color
        hover_color = hover_color[:3] if len(hover_color) == 4 else hover_color
        
        super().__init__(x_percent, y_percent, width_percent, height_percent, 
                        text, color, font_size_percent)
        self.hover_color = hover_color
        self.corner_radius = corner_radius
        self.normal_color = color
    
    def draw(self):
        """Desenha botão com bordas arredondadas"""
        current_color = self.hover_color if self.hovering else self.normal_color
        
        # Desenha retângulo arredondado
        pygame.draw.rect(SCREEN, current_color, self.rect, 
                        border_radius=self.corner_radius)
        
        # Borda destacada
        pygame.draw.rect(SCREEN, COLORS['highlight'], self.rect, 
                        2, border_radius=self.corner_radius)
        
        SCREEN.blit(self.text_surface, self.text_rect)
    
    def update_font(self, scale=1):
        """Atualiza fonte mantendo proporções"""
        font_size = int(PROPSYS.percent_to_px_y(self.font_size_percent * scale))
        self.font = pygame.font.SysFont('Arial', font_size)
        color = COLORS['highlight'] if self.hovering else self.normal_color
        self.text_surface = self.font.render(self.text, True, color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

class ArrowButton(Button):
    def __init__(self, x_percent, y_percent, width_percent, height_percent, 
                 direction='left', color=COLORS['highlight']):
        """
        Botão de seta com direção oposta
        direction: 'left' ou 'right'
        """
        super().__init__(x_percent, y_percent, width_percent, height_percent, "", color)
        self.direction = direction
        self.color = color
    
    def draw(self, screen):
        """Desenha seta na direção oposta"""
        center_x = self.rect.centerx
        center_y = self.rect.centery
        size = min(self.rect.width, self.rect.height) * 0.3

        if self.direction == 'left':
            # Seta para DIREITA (←) - oposta ao lado
            points = [
                (center_x - size, center_y),
                (center_x + size, center_y - size),
                (center_x + size, center_y + size)
            ]
        else:
            # Seta para ESQUERDA (→) - oposta ao lado
            points = [
                (center_x + size, center_y),
                (center_x - size, center_y - size),
                (center_x - size, center_y + size)
            ]

        pygame.draw.polygon(screen, self.color, points)

def draw_background():
    """Desenha o fundo com overlay"""
    # Fundo sólido
    SCREEN.fill(COLORS['background'][:3])  # Remove alpha para fill
    
    # Aplicar overlay em toda a tela
    SCREEN.blit(OVERLAY_IMAGE, (0, 0))
    

def draw_top_bar():
    """Desenha a barra superior com setas opostas usando overlay"""
    # A barra já está na imagem de overlay, apenas desenhamos os elementos
    top_bar_rect = PROPSYS.get_rect(0, 0, 1.0, 0.1)
    
    # Botões de seta com direção oposta
    left_arrow = ArrowButton(0.02, 0.02, 0.06, 0.06, 'left')
    right_arrow = ArrowButton(0.92, 0.02, 0.06, 0.06, 'right')
    
    left_arrow.draw(SCREEN)
    right_arrow.draw(SCREEN)
    
    # Título do menu atual
    menu_titles = {
        'inicio': 'INÍCIO',
        'config': 'CONFIGURAÇÕES', 
        'perfil': 'PERFIL',
        'ajuda': 'AJUDA'
    }
    
    title_text = font_large.render(menu_titles[current_menu], True, COLORS['text'])
    title_rect = title_text.get_rect(center=(WIDTH // 2, PROPSYS.percent_to_px_y(0.05)))
    SCREEN.blit(title_text, title_rect)
    
    return left_arrow, right_arrow

def draw_center_content():
    """Desenha o conteúdo central com botões arredondados"""
    # A área central já está definida no overlay, apenas adicionamos os botões
    center_rect = PROPSYS.get_rect(0.1, 0.15, 0.8, 0.7)
    
    buttons = []
    menu_items = menus[current_menu]
    
    for i, item in enumerate(menu_items):
        btn = RoundedButton(
            0.2, 0.2 + i * 0.15,  # Posição
            0.6, 0.12,            # Tamanho  
            item,
            COLORS['button_normal'],
            COLORS['button_hover'],
            0.03,  # Tamanho da fonte
            20     # Raio das bordas
        )
        
        # Destacar item selecionado
        if i == current_index:
            btn.color = COLORS['highlight']
            btn.normal_color = COLORS['highlight']
            btn.update_font(scale=1.1)
        
        btn.draw()
        buttons.append(btn)
    
    return buttons

def draw_bottom_bar():
    """Desenha a barra inferior com data e dia da semana usando overlay"""
    # A barra já está na imagem de overlay, apenas adicionamos o texto
    bottom_bar_rect = PROPSYS.get_rect(0, 0.9, 1.0, 0.1)
    
    # Data atual
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    weekday_str = now.strftime("%A")
    
    # Traduzindo dias da semana
    weekdays_pt = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira', 
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    weekday_pt = weekdays_pt.get(weekday_str, weekday_str)
    
    # Renderizar textos
    date_text = font_small.render(date_str, True, COLORS['text'])
    weekday_text = font_small.render(weekday_pt, True, COLORS['highlight'])
    
    # Posicionar textos
    date_rect = date_text.get_rect(midleft=(
        PROPSYS.percent_to_px_x(0.02), 
        PROPSYS.percent_to_px_y(0.95)
    ))
    weekday_rect = weekday_text.get_rect(midright=(
        PROPSYS.percent_to_px_x(0.98), 
        PROPSYS.percent_to_px_y(0.95)
    ))
    
    SCREEN.blit(date_text, date_rect)
    SCREEN.blit(weekday_text, weekday_rect)

def handle_navigation():
    """Lida com a navegação do menu"""
    global current_index
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        current_index = (current_index - 1) % len(menus[current_menu])
        pygame.time.delay(150)
    
    if keys[pygame.K_DOWN]:
        current_index = (current_index + 1) % len(menus[current_menu])
        pygame.time.delay(150)
    
    if keys[pygame.K_RETURN]:
        return menus[current_menu][current_index]
    
    return None

def handle_menu_action(selected_item):
    """Lida com as ações dos menus"""
    global current_menu, current_index
    
    if selected_item == "Voltar":
        current_menu = 'inicio'
        current_index = 0
    elif selected_item == "Opções":
        current_menu = 'config'
        current_index = 0
    elif selected_item == "Perfil":
        current_menu = 'perfil' 
        current_index = 0
    elif selected_item == "Ajuda":
        current_menu = 'ajuda'
        current_index = 0
    elif selected_item == "Sair":
        return "quit"
    
    print(f"Ação: {selected_item}")
    return None

def main():
    clock = pygame.time.Clock()
    running = True
    global current_menu, current_index
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            # Verificar cliques nos botões de seta
            if event.type == pygame.MOUSEBUTTONDOWN:
                left_arrow, right_arrow = draw_top_bar()  # Para obter as áreas dos botões
                
                if left_arrow.rect.collidepoint(mouse_pos):
                    # Navegar para menu anterior
                    menu_order = ['inicio', 'config', 'perfil', 'ajuda']
                    current_idx = menu_order.index(current_menu)
                    current_menu = menu_order[(current_idx - 1) % len(menu_order)]
                    current_index = 0
                
                elif right_arrow.rect.collidepoint(mouse_pos):
                    # Navegar para próximo menu
                    menu_order = ['inicio', 'config', 'perfil', 'ajuda']
                    current_idx = menu_order.index(current_menu)
                    current_menu = menu_order[(current_idx + 1) % len(menu_order)]
                    current_index = 0
        
        # Processar navegação por teclado
        selected_item = handle_navigation()
        if selected_item:
            result = handle_menu_action(selected_item)
            if result == "quit":
                running = False
        
        # Desenhar tudo
        draw_background()  # Agora usa a imagem de overlay
        draw_top_bar()
        buttons = draw_center_content()
        draw_bottom_bar()
        
        # Verificar hover nos botões
        for button in buttons:
            button.check_hover(mouse_pos)
        # Top bar
            # Criar máscaras com bordas arredondadas para cada área
        
        # Top bar com bordas arredondadas
        top_bar_mask = pygame.Surface((WIDTH, 60), pygame.SRCALPHA)
        pygame.draw.rect(top_bar_mask, (255, 255, 255, 255), (0, 0, WIDTH, 60), border_radius=15)
        
        # Bottom bar com bordas arredondadas
        bottom_bar_mask = pygame.Surface((WIDTH, 40), pygame.SRCALPHA)
        pygame.draw.rect(bottom_bar_mask, (255, 255, 255, 255), (0, 0, WIDTH, 40), border_radius=15)
        
        # Center area com bordas arredondadas
        center_mask = pygame.Surface((WIDTH-160, HEIGHT-180), pygame.SRCALPHA)
        pygame.draw.rect(center_mask, (255, 255, 255, 255), (0, 0, WIDTH-160, HEIGHT-180), border_radius=20)
        
        top_bar_overlay = OVERLAY_IMAGE.subsurface((0, 0, WIDTH, 60)).copy()
        top_bar_overlay.blit(top_bar_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        SCREEN.blit(top_bar_overlay, (0, 0))
        
        # Bottom bar
        bottom_bar_overlay = OVERLAY_IMAGE.subsurface((0, HEIGHT-40, WIDTH, 40)).copy()
        bottom_bar_overlay.blit(bottom_bar_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        SCREEN.blit(bottom_bar_overlay, (0, HEIGHT-40))
        
        # Center area
        center_overlay = OVERLAY_IMAGE.subsurface((80, 90, WIDTH-160, HEIGHT-180)).copy()
        center_overlay.blit(center_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        SCREEN.blit(center_overlay, (80, 90))
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()