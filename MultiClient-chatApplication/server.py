import threading
import socket

# localhost
host = '127.0.0.1'  
# port
port = 6789

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind server to localhost on port 6789
server.bind((host, port)) 
# listening, waiting for incoming connection
server.listen() 

clients = []
nicknames = []

# sends msg to all the client that connets to the server
def broadCast(message):
    for client in clients:
        client.send(message)
    
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadCast(message)
        except:
            index = clients.index(client)
            # wholeft = clients[index]
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadCast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        # client and address of the client
        client, address = server.accept()
        print(f'connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadCast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
receive()