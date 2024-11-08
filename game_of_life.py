import pygame
import numpy as np
import sys

class GameOfLife:
    def __init__(self, width=800, height=600, cell_size=10):
        pygame.init()
        
        self.width = width
        self.height = height + 100  
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Juego de la Vida - Conway')

        self.bg_color = (10, 10, 10)
        self.grid_color = (40, 40, 40)
        self.alive_color = (0, 255, 255)  #
        self.dead_color = (40, 40, 40)
        self.button_color = (60, 60, 60)
        self.button_hover_color = (80, 80, 80)
        self.button_text_color = (255, 255, 255)
        
        self.nx = width // cell_size
        self.ny = height // cell_size
        self.state = np.zeros((self.nx, self.ny))
        
        self.paused = True
        self.running = True
        self.generation = 0
        self.update_interval = 100
        self.last_update = pygame.time.get_ticks()
        
        # Configuración de botones
        self.font = pygame.font.Font(None, 36)
        self.buttons = [
            {'text': 'Iniciar/Pausar', 'rect': pygame.Rect(width - 180, 20, 150, 40)},
            {'text': 'Reiniciar', 'rect': pygame.Rect(width - 180, 70, 150, 40)},
            {'text': 'Velocidad +', 'rect': pygame.Rect(width - 180, 120, 150, 40)},
            {'text': 'Velocidad -', 'rect': pygame.Rect(width - 180, 170, 150, 40)},
            {'text': 'Blinker', 'rect': pygame.Rect(width - 180, 220, 150, 40)},
            {'text': 'Toad', 'rect': pygame.Rect(width - 180, 270, 150, 40)},
            {'text': 'Pulsar', 'rect': pygame.Rect(width - 180, 320, 150, 40)}  
        ]
        
    def draw_button(self, button, mouse_pos):
        hover = button['rect'].collidepoint(mouse_pos)
        color = self.button_hover_color if hover else self.button_color
        
        pygame.draw.rect(self.screen, color, button['rect'], border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 100), button['rect'], 2, border_radius=5)
        
        text = self.font.render(button['text'], True, self.button_text_color)
        text_rect = text.get_rect(center=button['rect'].center)
        self.screen.blit(text, text_rect)

    def count_neighbors(self, x, y):
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nx = (x + i) % self.nx
                ny = (y + j) % self.ny
                total += self.state[nx, ny]
        return total

    def update_state(self):
        new_state = np.zeros((self.nx, self.ny))
        for x in range(self.nx):
            for y in range(self.ny):
                neighbors = self.count_neighbors(x, y)
                if self.state[x, y] == 1:
                    if neighbors == 2 or neighbors == 3:
                        new_state[x, y] = 1
                else:
                    if neighbors == 3:
                        new_state[x, y] = 1
        self.state = new_state
        self.generation += 1

    def draw_grid(self):
        self.screen.fill(self.bg_color)
        
        for x in range(self.nx):
            for y in range(self.ny):
                color = self.alive_color if self.state[x, y] == 1 else self.dead_color
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                                 self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(self.screen, color, rect)
        
        status = f"Generación: {self.generation}"
        text = self.font.render(status, True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            self.draw_button(button, mouse_pos)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_pos = event.pos
                    for i, button in enumerate(self.buttons):
                        if button['rect'].collidepoint(mouse_pos):
                            if i == 0:  
                                self.paused = not self.paused
                            elif i == 1:  
                                self.state.fill(0)
                                self.generation = 0
                                self.paused = True
                            elif i == 2:  
                                self.update_interval = max(50, self.update_interval - 50)
                            elif i == 3:  
                                self.update_interval = min(500, self.update_interval + 50)
                            elif i == 4:  
                                self.add_blinker(60, 40)
                            elif i == 5:  
                                self.add_toad(20, 20)
                            elif i == 6:  
                                self.add_pulsar(30, 50) 
                            return
                    
                  
                    x = event.pos[0] // self.cell_size
                    y = event.pos[1] // self.cell_size
                    if y < self.ny:  
                        self.state[x, y] = not self.state[x, y]
            
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  
                    x = event.pos[0] // self.cell_size
                    y = event.pos[1] // self.cell_size
                    if y < self.ny:  
                        self.state[x, y] = 1

    def add_blinker(self, x, y):
        for i in range(3):
            self.state[x + i, y] = 1  

    def add_toad(self, x, y):
        self.state[x, y] = 1
        self.state[x + 1, y] = 1
        self.state[x + 2, y] = 1
        self.state[x + 1, y - 1] = 1
        self.state[x + 2, y - 1] = 1
        self.state[x + 3, y - 1] = 1

    def add_pulsar(self, x, y):
        pulsar_pattern = [
            (1, 4), (2, 4), (3, 4), (1, 5), (3, 5), (1, 6), (2, 6), (3, 6),
            (1, 8), (2, 8), (3, 8), (1, 9), (3, 9), (1, 10), (2, 10), (3, 10)
        ]
        for dx, dy in pulsar_pattern:
            if 0 <= x + dx < self.nx and 0 <= y + dy < self.ny:
                self.state[x + dx, y + dy] = 1

    def run(self):
        while self.running:
            self.handle_events()
            if not self.paused and pygame.time.get_ticks() - self.last_update >= self.update_interval:
                self.update_state()
                self.last_update = pygame.time.get_ticks()
            self.draw_grid()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

if __name__ == '__main__':
    game = GameOfLife()
    game.run()
    pygame.quit()
    sys.exit()
