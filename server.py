import socket
import threading

# Configurações do servidor
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
ADDR = (SERVER_IP, SERVER_PORT)

# Lista de conexões ativas
clients = []

# Função para lidar com novos clientes
def handle_client(conn, addr):
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    while True:
        try:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            print(f"[{addr}] {data}")
            broadcast(data, conn)
        except:
            clients.remove(conn)
            conn.close()
            break

# Função para transmitir dados para todos os clientes conectados
def broadcast(data, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(data.encode("utf-8"))
            except:
                clients.remove(client)
                client.close()

# Função principal do servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[OUVINDO] Servidor está ouvindo em {SERVER_IP}:{SERVER_PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")

print("[INICIANDO] Iniciando servidor...")
start_server()
