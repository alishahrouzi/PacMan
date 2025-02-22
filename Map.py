import zmq

class MapService:
    def __init__(self):
        self.map_data = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 2, 0, 0, 0, 2, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 3, 0, 0, 1],
            [1, 2, 0, 0, 0, 2, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]
        
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:5557")
        
        self.subcriber = self.context.socket(zmq.SUB)
        self.subcriber.connect("tcp://localhost:5556")
        self.subcriber.setsockopt_string(zmq.SUBSCRIBE,"")
        
    def check_collision(self,position):
        x,y = position["x"],position["y"]
        grid_x,grid_y = x // 50 , y // 50
        if self.map_data.get[grid_y][grid_x] == 1 :
            return True
        return False
    
    def check_food(self,position):
        x, y = position["x"], position["y"]
        grid_x , grid_y = x // 50 , y // 50
        if self.map_data[grid_y][grid_x] in [2,3]:
            self.map_data[grid_y][grid_x] = 0
            return True
        return False
    
    def process_message(self,message):
        if "pacman_position" in message:
            position = message["pacman_position"]
            
            if self.check_collision(position):
                self.publisher.send_pyobj({"collision":True})
            else: self.publisher.send_pyobj({"collision":False})
            
            if self.check_food(position):
                self.publisher.send_pyobj({"food_eaten":True})
            else: self.publisher.send_pyobj({"food_eaten":False})
            
    def listen(self):
        while True:
            try:
                message = self.subcriber.recv_pyobj(flags = zmq.NOBLOCK)
                self.process_message(message)
            except zmq.Again:
                pass
            
    def run(self):
        print("Map Service Running...")
        while True:
            self.listen()
    
    
if __name__ == "__main__":
    map_service = MapService()
    map_service.run()