import subprocess

services = [
    "Game Mangement.py",
    "RUN.py",
    "Map.py",
    "Score.py",
    "Rendering.py"
]

processes = []

try:
    for service in services:
        print(f"Starting {service}...")
        process = subprocess.Popen(["python",service] , stdout=subprocess.PIPE , stderr= subprocess.PIPE)
        processes.append(process)
        
        for process in processes:
            process.wait()
            
except KeyboardInterrupt:
    print("Shutting down all Services...")
    for process in processes:
        process.treminate()
