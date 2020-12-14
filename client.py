import socket
import threading

# Choix du pseudo
nickname = input("Choisissez votre pseudo: ")

# Connexion au serveur
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 65530))

# écoute du serveur / Envoie du Pseudo
def receive():
    while True:
        try:
            # Recevoir un message du serveur
            # si 'NICK' envoyer le pseudo
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Fermer la connexion s'il y a une erreur 
            print("Une erreur est survenue!")
            client.close()
            break

# Envoyer un message au serveur
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# Start les Thread pour écouter et envoyer sur le serveur
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()