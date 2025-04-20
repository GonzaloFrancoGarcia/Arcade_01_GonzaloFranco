import socket
import threading

class Server:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
    
    def handle_client(self, conn, addr):
        print(f'🌐 Conexión entrante desde {addr}')
        try:
            data = conn.recv(1024)
            if data:
                text = data.decode()
                print(f'📨 Recibido: {text}')
                conn.sendall(b'ACK')  # confirmación sencilla
        except Exception as e:
            print(f'⚠️ Error con {addr}: {e}')
        finally:
            conn.close()
    
    def start(self):
        print(f'🚀 Servidor escuchando en {self.host}:{self.port}')
        try:
            while True:
                conn, addr = self.sock.accept()
                t = threading.Thread(target=self.handle_client, args=(conn, addr))
                t.daemon = True
                t.start()
        except KeyboardInterrupt:
            print('\n🛑 Servidor detenido por teclado')
        finally:
            self.sock.close()
