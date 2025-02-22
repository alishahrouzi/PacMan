import zmq
import pygame

class RenderingService:
    def __init__(self):
        pygame.init()
        
        self.screen_width = 500 
        self.screen_height = 300
        self.cell_size = 50
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pac-Man")
        
        self.clock = pygame.time.Clock()
        
        self.colors = {
            "background": (0,0,0),
            "wall": (0,0,255),
            "food": (255,255,0),
            "powerup": (255,0,0,),
            "pacman": (255,255,0),
            "ghost": (255,0,255),
        }
        
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect("tcp://localhost:5558")
        self.subscriber.connect("tcp://localhost:5557")
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE,"")
        
        self.map_data = []
        self.pacman_position = {"x":50 , "y":50}
        self.ghost_position = []
        self.score = 0
        
    def draw_map(self):
        for row_index , row in enumerate(self.map_data):
            for col_index , cell in enumerate(row):
                x,y  = col_index * self.cell_size , row_index * self.cell_size
                if cell == 1: 
                    pygame.draw.rect(self.screen, self.colors["wall"], (x, y, self.cell_size, self.cell_size))
                elif cell == 2:  
                    pygame.draw.circle(self.screen, self.colors["food"], (x + self.cell_size // 2, y + self.cell_size // 2), 5)
                elif cell == 3:  
                    pygame.draw.circle(self.screen, self.colors["powerup"], (x + self.cell_size // 2, y + self.cell_size // 2), 10)
                    
    def draw_pacman(self):
        x, y = self.pacman_position["x"], self.pacman_position["y"]
        pygame.draw.circle(self.screen, self.colors["pacman"], (x + self.cell_size // 2, y + self.cell_size // 2), 20)
    
    def draw_ghost(self):
          for ghost_position in self.ghost_position:
            x, y = ghost_position["x"], ghost_position["y"]
            pygame.draw.circle(self.screen, self.colors["ghost"], (x + self.cell_size // 2, y + self.cell_size // 2), 20)
    
    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
    def update_game_state(self,message):
        if "map_data" in message:
            self.map_data = message["map_data"]
        if "pacman_position" in message:
            self.pacman_position = message["pacman_position"]
        if "ghost_positions" in message:
            self.ghost_positions = message["ghost_positions"]
        if "score" in message:
            self.score = message["score"]
    
    def listen(self):
        try:
            message = self.subscriber.recv_pyobj(flags=zmq.NOBLOCK)
            self.update_game_state(message)
        except zmq.Again:
            pass
        
    def render(self):
        self.screen.fill(self.colors["background"])
        self.draw_map()
        self.draw_pacman()
        self.draw_ghost()
        self.draw_score()
        pygame.display.flip()
        
    def run(self):
        print("Rendering Service running...")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.listen() 
            self.render()  
            self.clock.tick(60)  
            
        pygame.quit()

if __name__ == "__main__":
    rendering_service = RenderingService()
    rendering_service.run()