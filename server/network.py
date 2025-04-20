import socket
import threading
import json

from db import init_db, SessionLocal
from models import ReinasResult

class Server:
    def __init__(self, host='127.0.0.1', port=5000):
        # Inicializa la BD (crea tablas)
        init_db()

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
    
    def handle_client(self, conn, addr):
        print(f'🌐 Conexión desde {addr}')
        try:
            data = conn.recv(4096)
            text = data.decode()
            print(f'📨 Recibido raw: {text}')

            # Intentamos parsear JSON
            try:
                payload = json.loads(text)
            except json.JSONDecodeError as e:
                print(f'⚠️ JSON inválido: {e}')
                conn.sendall(b'NACK')
                return

            # Si es resultado de N-Reinas, guardamos
            if payload.get('juego') == 'nreinas':
                sess = SessionLocal()
                resultado = ReinasResult(
                    N=payload['N'],
                    resuelto=payload['resuelto'],
                    pasos=payload['pasos']
                )
                sess.add(resultado)
                sess.commit()
                sess.close()
                print(f'✅ Guardado en DB: N={payload["N"]}, resuelto={payload["resuelto"]}, pasos={payload["pasos"]}')
                conn.sendall(b'ACK')
            else:
                print('ℹ️ Mensaje no reconocido o juego distinto')
                conn.sendall(b'NACK')

        except Exception as e:
            print(f'⚠️ Error manejando cliente {addr}: {e}')
            conn.sendall(b'NACK')
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
            print('\n🛑 Servidor detenido')
        finally:
            self.sock.close()
