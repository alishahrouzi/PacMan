import pygame
import time 
import zmq
from enum import Enum

class GameState(Enum):
    RUNNING = 1
    PAUSED = 2
    GAMEOVER = 2 
    
class GameManager:
    def __init__(self):
        pygame.init()
        self.state = GameState.RUNNING
        self.clock = pygame.time.Clock()
        self.tick_rate = 30
        self.context = zmq.Context()
        
        
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:5555")
        
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect("tcp://localhost:5556")
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
        
        
    def start_game(self):
        print("Game Started!")
        while self.state != GameState.GAMEOVER:
            self.handle_events()
            self.update_game_state()
            self.send_updates()
            self.clock.tick(self.tick_rate)
    
    def handle_events(self):
        try:
            while True:
                message = self.subscriber.recv_string(flags=zmq.NOBLOCK)
                self.process_message(message)
        except zmq.Again:
            pass
    
    def process_message(self,message):
        if message == "PAUSE":
            self.state = GameState.PAUSED
        elif message == "RESUME":
            self.state = GameState.RUNNING
        elif message == "GAME_OVER":
            self.state = GameState.GAMEOVER
    
    def update_game_state(self):
        if self.state == GameState.RUNNING:
            print("Game is Running...")
    
    def send_updates(self):
        if self.state == GameState.RUNNING:
            self.publisher.send_string("Updates:STATE_RUNNING")
        elif self.state == GameState.PAUSED:
            self.publisher.send_string("UPDATE:STATE_PAUSED")
        elif self.state == GameState.GAMEOVER:
            self.publisher.send_string("UPDATE:STATE_GAMEOVER")
    
if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.start_game()