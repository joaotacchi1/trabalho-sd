import time
import socket
import ntplib
from datetime import datetime
import random

NTP_SERVER = "pool.ntp.org"

class NTPServer:
    def __init__(self, host='0.0.0.0', port=1234):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.ntp_client = ntplib.NTPClient()
        
    def get_ntp_time(self):  # Obtém a hora real de um servidor NTP
        try:
            response = self.ntp_client.request(NTP_SERVER, version=3)
            print(f"Horário NTP: {datetime.fromtimestamp(response.tx_time)}")
            return response.tx_time
        except Exception as e:
            print(f"Erro ao conectar ao NTP: {e}")
            return time.time()

    def run(self):
        print(f"Servidor NTP rodando em {self.host}:{self.port}.")
        while True:
            data, addr = self.sock.recvfrom(1024)
            if data.decode() == "REQUEST_TIME":
                # Simula atraso de rede (entre 0.1 e 0.5 segundos)
                delay = random.uniform(0.1, 0.5)
                current_time = self.get_ntp_time()
                # Adiciona o atraso estimado ao tempo enviado
                send_time = current_time + (delay / 2)
                self.sock.sendto(str(send_time).encode(), addr)
                print(f"Enviado tempo {datetime.fromtimestamp(send_time)} para {addr} com delay {delay:.3f}s")

if __name__ == "__main__":
    server = NTPServer(host="192.168.11.143") # Mudar ip para ip da máquina do servidor
    server.run()