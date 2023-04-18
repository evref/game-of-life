import pygame

class Game:
    def __init__(self, pixel_size, screen_width, screen_height):
        self.pixel_size = pixel_size
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.FPS_idx = 6
        self.FPS_list = [2, 5, 10, 15, 20, 30, 60, 120, 300, 600, 1200]

        self.gen_grid()
        self.state = 0

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.running = True


    def gen_grid(self):
        self.grid = [[0 for _ in range(self.screen_width // self.pixel_size)] 
                     for _ in range(self.screen_height // self.pixel_size)]
        
        self.visual_grid = [[pygame.Rect(x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size) for x in range(self.screen_width // self.pixel_size)]
                            for y in range(self.screen_height // self.pixel_size)]


    def run(self):
        while self.running:
            self.clock.tick(self.FPS_list[self.FPS_idx])

            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 1 if self.state == 0 else 0
                    self.FPS_idx = 0
                elif event.key == pygame.K_UP and self.state == 1:
                    self.FPS_idx += 1 if self.FPS_idx < len(self.FPS_list) - 1 else 0
                elif event.key == pygame.K_DOWN and self.state == 1:
                    self.FPS_idx -= 1 if self.FPS_idx > 0 else 0


    def update(self):
        if(self.state == 0):
            self.FPS_idx = 5
            self.update_draw_phase()
        elif(self.state == 1):
            print(self.FPS_list[self.FPS_idx])
            self.update_game_phase()
        

    def update_draw_phase(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()

        if (mouse_clicked[0]):
            x = mouse_pos[0] // self.pixel_size
            y = mouse_pos[1] // self.pixel_size

            self.grid[y][x] = 1
        elif (mouse_clicked[2]):
            x = mouse_pos[0] // self.pixel_size
            y = mouse_pos[1] // self.pixel_size

            self.grid[y][x] = 0


    def update_game_phase(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                neighbours = self.check_neighbours(x, y)
                
                if (neighbours < 2 or neighbours > 3) and self.grid[y][x] == 1:
                    self.grid[y][x] = 0
                elif neighbours == 3 and self.grid[y][x] == 0:
                    self.grid[y][x] = 1
                

    def draw(self):
        self.screen.fill((255, 255, 255))

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), self.visual_grid[y][x])

        pygame.display.flip()


    def check_neighbours(self, x, y):
        neighbours = 0

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue

                if i < 0 or i >= len(self.grid[0]) or j < 0 or j >= len(self.grid):
                    continue

                neighbours += self.grid[j][i]

        return neighbours