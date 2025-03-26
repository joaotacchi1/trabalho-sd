import socket
import time
from datetime import datetime
import random
import threading

class NTPClient:
    def __init__(self, client_id, server_ip='192.168.11.143', server_port=1234):
        self.client_id = client_id
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.local_time = time.time() + random.uniform(-1000, 1000) # Variação de -1000 a 1000 segundos de diferença
        self.drift_rate = random.uniform(-0.01, 0.01) # Simula variação nas imperfeições como hardware, variações de temperatura, etc.
        self.ip = f"192.168.11.{103}"  # IP único para Cliente 2
        
    def update_local_time(self):
        while True:
            time.sleep(1)
            self.local_time += 1 + self.drift_rate

    def sync_with_server(self):
        while True:
            start_time = time.time()
            self.sock.sendto("REQUEST_TIME".encode(), (self.server_ip, self.server_port))
            data, _ = self.sock.recvfrom(1024)
            receive_time = time.time()
            
            rtt = receive_time - start_time
            network_delay = rtt / 2
            server_time = float(data.decode())
            adjusted_server_time = server_time + network_delay
            
            time_diff = adjusted_server_time - self.local_time
            if abs(time_diff) > 0.1:
                adjustment = time_diff / 10
                self.local_time += adjustment
                print(f"Cliente {self.client_id} ({self.ip}): "
                      f"Ajustado em {adjustment:.3f}s. "
                      f"Hora local ajustada: {datetime.fromtimestamp(self.local_time)}, "
                      f"Diff: {time_diff:.3f}s, RTT: {rtt:.3f}s")
            
            time.sleep(5)

    def run(self):
        drift_thread = threading.Thread(target=self.update_local_time, daemon=True)
        drift_thread.start()
        print(f"Cliente {self.client_id} ({self.ip}) iniciado com hora inicial (sem ajustes): "
              f"{datetime.fromtimestamp(self.local_time)}")
        self.sync_with_server()

if __name__ == "__main__":
    client = NTPClient(client_id=3)
    client.run()