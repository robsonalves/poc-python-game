import socket
import threading
import time
import json

# Configurações do servidor
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
ADDR = (SERVER_IP, SERVER_PORT)

# Inicialização do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

clients = []
enemies = [{'x': 100, 'y': 100, 'speed': 2}]  # Exemplo de estado inicial dos inimigos

# Função para enviar dados para todos os clientes
def broadcast(data):
    for client in clients:
        client.send(data.encode('utf-8'))

# Função para lidar com clientes
def handle_client(client):
    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            if data:
                broadcast(data)
        except:
            clients.remove(client)
            client.close()
            break

# Função para aceitar conexões de clientes
def accept_clients():
    while True:
        client, addr = server.accept()
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,)).start()

# Função para atualizar o estado dos inimigos
def update_enemies():
    global enemies
    while True:
        # Atualizar a lógica dos inimigos aqui
        for enemy in enemies:
            enemy['x'] += enemy['speed']
            if enemy['x'] > 600 or enemy['x'] < 0:  # Supondo que a largura da janela seja 600
                enemy['speed'] = -enemy['speed']
        enemy_data = json.dumps(enemies)
        broadcast(enemy_data)
        time.sleep(1)  # Enviar atualizações a cada segundo

# Iniciar threads
threading.Thread(target=accept_clients).start()
threading.Thread(target=update_enemies).start()
