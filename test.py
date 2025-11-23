import pygame
import sys
from utilities import initialize
screen,DEFS, SHEET, PROPSYS, SPRITE_LOADER = initialize()
# Inicializar Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Filtro CRT")

# Criar uma superfície para o fundo (simulando conteúdo)
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill((120,120,120))  # Fundo branco

# Adicionar alguns elementos visuais ao fundo para teste
pygame.draw.rect(background, (200, 100, 100), (100, 100, 200, 150))
pygame.draw.circle(background, (100, 200, 100), (400, 300), 80)
pygame.draw.line(background, (100, 100, 200), (50, 500), (750, 500), 5)
class TeeVee:
    def __init__(self):
        SPRITE_LOADER.create_sprite(
            key="frame",
            position=(0, 0),
            size=(22, 36),
            scale=DEFS["width"]/100
        )
        SPRITE_LOADER.create_sprite(
            key="mouths",
            position=(0, 0),
            size=(22, 36),
            scale=DEFS["width"]/100
        )
        self.emote = "happy"
        self.is_talking = False
        self.talk_frame = 0
        self.talk_speed = 0.2
        self.talk_timer = 0
        
    def start_talking(self):
        """Start the talking animation"""
        self.is_talking = True
        self.talk_frame = 0
        
    def stop_talking(self):
        """Stop the talking animation"""
        self.is_talking = False
        self.talk_frame = 0
        
    def update(self, dt):
        """Update animation frames"""
        if self.is_talking:
            self.talk_timer += dt
            if self.talk_timer >= self.talk_speed:
                self.talk_timer = 0
                self.talk_frame = (self.talk_frame + 1) % 3
    
    def draw_mouth_dialog(self):
        """Draw animated mouth for dialog with tapered design"""
        base_x, base_y = 6, 28
        max_width = 10
        
        if self.is_talking:
            # Animated talking frames with tapered design
            if self.talk_frame == 0:
                # Frame 1: Wide open (3 lines, decreasing width)
                for i in range(3):
                    width = max_width - (i * 3)  # Lose 3 pixels in width each line
                    x_offset = base_x + i  # Shift right each line
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + i), size=(width, 2))
                    # Outline
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + i - 1), size=(width, 2), color=(0,0,0))
                    
            elif self.talk_frame == 1:
                # Frame 2: Medium (3 lines, more tapered)
                for i in range(3):
                    width = max_width - (i * 4)  # Lose 4 pixels in width each line
                    x_offset = base_x + i + 1  # Shift right more
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + i), size=(width, 2))
                    # Outline
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + i - 1), size=(width, 2), color=(0,0,0))
                    
            else:
                # Frame 3: Small (3 lines, very tapered)
                for i in range(3):
                    width = max_width - (i * 5)  # Lose 5 pixels in width each line
                    x_offset = base_x + i + 2  # Shift right even more
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + i), size=(width, 2))
                    # Outline
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + i - 1), size=(width, 2), color=(0,0,0))
                    
        else:
            # Default mouth based on emotion (using tapered design)
            if self.emote == "happy":
                # Happy: upward curved (3 lines, decreasing width)
                for i in range(3):
                    width = max_width - (i * 3)  # Lose 3 pixels in width each line
                    x_offset = base_x + i
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + i), size=(width, 2))
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + i - 1), size=(width, 2), color=(0,0,0))
                    
            elif self.emote == "sad":
                # Sad: downward curved (3 lines, decreasing width)
                for i in range(3):
                    width = max_width - (i * 3)
                    x_offset = base_x + i
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + 2 - i), size=(width, 2))
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + 1 - i), size=(width, 2), color=(0,0,0))
                    
            elif self.emote == "neutral":
                # Neutral: straight (3 lines, decreasing width)
                for i in range(3):
                    width = max_width - (i * 3)
                    x_offset = base_x + i
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y + 1), size=(width, 2))
                    SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(x_offset, base_y), size=(width, 2), color=(0,0,0))
    
    def draw(self):
        # Frame
        SPRITE_LOADER.draw_sprite_centered("frame", DEFS['center_x'], DEFS['center_y'])
        
        # Eyes
        SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(6,22), size=(3,5))
        SPRITE_LOADER.draw_relative_to_sprite("frame", startpos=(13,22), size=(3,5))
        
        # Mouth with tapered dialog animation
        self.draw_mouth_dialog()
        
        return True

    def say_text(self, text, duration=2.0):
        """Make TeeVee talk for a duration"""
        self.start_talking()
        # In practice, you'd set a timer to call stop_talking after duration
# Loop principal
clock = pygame.time.Clock()
running = True

tv = TeeVee()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Desenhar o fundo
    screen.blit(background, (0, 0))    
    # In your main game loop
    # Start talking
    tv.start_talking()

    # Update every frame with delta time
    tv.update(clock.get_time() / 1000.0)  # where dt is your frame delta time

    # Draw as usual
    tv.draw()

    # Stop talking when done
    tv.stop_talking()
    # Atualizar a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()