import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 12345))

client_name = input("Enter your player name: ") #ce nume o sa aiba jucatorul
client.send(f'CONNECT {client_name}'.encode('utf-8')) #trimitem serverului numele

stats_data = client.recv(1024) #primim de la server statusurile jucatorului
player_stats = stats_data.decode('utf-8')
print(f'Your stats: {player_stats}') #afisam clientului ce statusuri a nimerit, poate a fost norocos

result_data = client.recv(1024) #primim rezultatele jocului
result = result_data.decode('utf-8')
print(result)

client.close()
