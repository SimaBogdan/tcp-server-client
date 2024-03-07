import socket
import random
import queue
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 12345))

clients = [] #clientii sunt salvati intr-o lista deoarece cum avem o conexiune mai stabila mi s-a parut mai usor decat un dictionar in acest caz
client_queue = queue.Queue()

server.listen(5)
print("THE SERVER NEEDS BLOOD") #the server is a bit hungry

#aceasta functie compara statusurile jucatoriilor si ajuta pentru aflarea castigatorului
def compare_stats(client1, stats1, client2, stats2):

    points1 = 0
    points2 = 0

    for stat in stats1:
        if stats1[stat] > stats2[stat]:
            points1 += 1
        elif stats2[stat] > stats1[stat]:
            points2 += 1

    if points1 > points2:
        return f'{client1} wins!'
    elif points2 > points1:
        return f'{client2} wins!'
    else:
        return "It's a tie :("

#aceasta functie ne permite sa gestionam mai multi clienti in acest server print threading
def client_handler(client_socket):

    while True:
        data = client_socket.recv(1024) #colectam datele din client

        message = data.decode('utf-8')

        if message.startswith('CONNECT'):

            _, client_name = message.split()

            stats = {
                'Strength': random.randint(1, 10),
                'Speed': random.randint(1, 10),
                'Durability': random.randint(1, 10),
                'IQ': random.randint(1, 10)
            }

            clients.append((client_name, stats, client_socket)) #formam jucatorul
            client_queue.put(client_name)

            client_stats = ', '.join(f'{stat}: {value}' for stat, value in stats.items())
            client_socket.send(client_stats.encode('utf-8')) #trimitem inapoi clientului statusurile lui

            if len(clients) >= 2:
                client1 = client_queue.get()
                client2 = client_queue.get()

                client1_stats = next(stats for name, stats, socket in clients if name == client1)
                client2_stats = next(stats for name, stats, socket in clients if name == client2)

                winner = compare_stats(client1, client1_stats, client2, client2_stats) #winner winner chicken dinner

                for _, _, socket in clients:
                    socket.send(f'{winner}\n'.encode('utf-8')) #trimitem rezultatele clientilor

    #clients.remove((client_name, stats, client_socket))
    client_socket.close()

while True:

    client_socket, client_address = server.accept() #acceptam conexiunea cu clientul
    print(f"Client has joined the fight {client_address}")
    client_thread = threading.Thread(target=client_handler, args=(client_socket,)) #se creaza un nou thread pentru fiecare client nou si pentru izolarea fiecarui client
    client_thread.start()
