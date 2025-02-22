import zmq 

class ScoringService:
    def __init__(self):
        self.score = 0
        
        self.context = zmq.Context()
        
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:5558")
        
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect("tcp://localhost:5557")
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
        
    def update_score(self, event):
        if event.get("food_eaten"):
            self.score += 10
        if event.get("powerup_eaten"):
            self.score += 50
        if event.get("ghost_defeated"):
            self.score += 200
            
    def send_score(self):
        message = {"score": self.score}
        self.publisher.send_pyobj(message)
        
    def listen(self):
        try :
            message = self.subscriber.recv_pyobj(flags=zmq.NOBLOCK)
            self.update_score(message)
        except zmq.Again:
            pass
    
    def run(self):
        print("Scoring Service running...")
        while True:
            self.listen()
            self.send_score()
            
if __name__ == "__main__":
    scoring_service = ScoringService()
    scoring_service.run()