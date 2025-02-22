import pygame 
import zmq

class MovmentService:
    def __init__(self):
        pygame.init()
        
        self.pacman_position = {"x":100 , "y":100}
        self.pacman_speed = 5
        
        self.ghost_position = [
            {"x":200 , "y":200},
            {"x":300 , "y":300},
        ]
        self.ghost_speed = 3
        
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:5556")
        
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect("tcp://localhost:5555")
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE,"")
        
    def process_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.pacman_position["y"] -= self.pacman_speed
        if keys[pygame.K_DOWN]:
            self.pacman_position["y"] += self.pacman_speed
        if keys[pygame.K_LEFT]:
            self.pacman_position["x"] -= self.pacman_speed
        if keys[pygame.K_RIGHT]:
            self.pacman_position["x"] += self.pacman_speed
            
    def move_ghosts(self):
        for ghost in self.ghost_position:
            ghost["x"] += self.ghost_speed * (-1 if pygame.time.get_ticks() % 2 == 0 else 1)
            ghost["y"] += self.ghost_speed * (-1 if pygame.time.get_ticks() % 3 == 0 else 1)
    
    def send_position(self):
        message = {
            "pacman_position": self.pacman_position,
            "ghost_position": self.ghost_position
        }
        self.publisher.send_pyobj(message)
        
    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            self.process_input()
            
            self.move_ghosts()
            
            self.send_position()
            
            clock.tick(30)
            
if __name__ == "__main__":
    movement_service = MovmentService()
    movement_service.run()