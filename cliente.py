import socket
import time
from datetime import datetime
import random
import threading

class NTPClient:
    def __init__(self, client_id, server_ip='192.168.1.10', server_port=1234):
        self.client_id = client_id
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Simula hora inicial desalinhada (até 100 segundos de diferença)
        self.local_time = time.time() + random.uniform(-100, 100)
        self.drift_rate = random.uniform(-0.01, 0.01)  # Deriva de clock por segundo
        self.ip = f"192.168.1.{100 + client_id}"  # IP simulado
        
    def update_local_time(self):
        # Simula deriva natural do relógio
        while True:
            time.sleep(1)
            self.local_time += 1 + self.drift_rate

    def sync_with_server(self):
        while True:
            # Envia pedido de tempo ao servidor
            start_time = time.time()
            self.sock.sendto("REQUEST_TIME".encode(), (self.server_ip, self.server_port))
            
            # Recebe resposta do servidor
            data, _ = self.sock.recvfrom(1024)
            receive_time = time.time()
            
            # Calcula o RTT (Round-Trip Time) e o atraso estimado
            rtt = receive_time - start_time
            network_delay = rtt / 2
            
            # Tempo recebido do servidor
            server_time = float(data.decode())
            # Ajusta o tempo considerando o atraso de rede
            adjusted_server_time = server_time + network_delay
            
            # Diferença entre o tempo local e o tempo do servidor
            time_diff = adjusted_server_time - self.local_time
            
            # Ajuste gradual (usando o algoritmo de Cristian)
            if abs(time_diff) > 0.1:  # Só ajusta se diferença for significativa
                adjustment = time_diff / 10  # Ajuste gradual em 10 passos
                self.local_time += adjustment
                print(f"Cliente {self.client_id} ({self.ip}): "
                      f"Ajustado em {adjustment:.3f}s. "
                      f"Hora local: {datetime.fromtimestamp(self.local_time)}, "
                      f"Diff: {time_diff:.3f}s (diferença entre tempo local e tempo do servidor), "
                      f"RTT: {rtt:.3f}s")   
            
            # Aguarda intervalo periódico (ex.: 5 segundos)
            time.sleep(5)

    def run(self):
        # Inicia thread para simular deriva do relógio
        drift_thread = threading.Thread(target=self.update_local_time, daemon=True)
        drift_thread.start()
        
        # Inicia sincronização com o servidor
        print(f"Cliente {self.client_id} ({self.ip}) iniciado com hora inicial: "
              f"{datetime.fromtimestamp(self.local_time)}")
        self.sync_with_server()

if __name__ == "__main__":
    # Cria 4 clientes distintos
    clients = [NTPClient(i) for i in range(1, 5)]
    
    # Inicia cada cliente em uma thread separada
    threads = []
    for client in clients:
        t = threading.Thread(target=client.run)
        t.start()
        threads.append(t)
    
    # Mantém o programa rodando
    #for t in threads:
    #    t.join()