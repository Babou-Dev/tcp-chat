import socket
import threading

# données de connexion
host = '127.0.0.1'
port = 65530

# Démarrage du serveur 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# liste des clients et de leurs pseudos
clients = []
nicknames = []

# Envoyer un message à tous les clients co
def broadcast(message):
    for client in clients:
        client.send(message)

# Manipuler les messages des clients
def handle(client):
    while True:
        try:
            # Envoyer un message
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} a quitté !'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

# Fonction Recevoir message
def receive():
    while True:
        # Accepter la connexion
        client, address = server.accept()
        print("Connecté avec {}".format(str(address)))

        # demande et stockage du pseudo
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # afficher et envoyer le pseudo
        print("Votre Pseudo est {}".format(nickname))
        broadcast("{} à rejoint le chat!".format(nickname).encode('utf-8'))
        client.send('Connecté au chat!'.encode('utf-8'))

        # Commence les threads
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()