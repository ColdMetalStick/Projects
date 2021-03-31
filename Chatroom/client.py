import socket, sys, time

# Creating the socket
socket_server = socket.socket()
server_host = socket.gethostname() # hostname of server is retireved at client side and stored as server_host
ip = socket.gethostbyname(server_host) # ip addres is stored in ip
port = 8080  # port must match server's port

# Connecting to server
print("Your ip:",ip)
server_host = input("Enter server IP address: ")
name = input("Enter server name: ")
socket_server.connect((server_host, port))

# Recieving packets from the server
socket_server.send(name.encode())
server_name = socket_server.recv(1024)
server_name = server_name.decode()
print(server_name, "has joined.")

while True:
    message = (socket_server.recv(1024)).decode()
    print(server_name, ":", message)
    message = input("Me : ")
    socket_server.send(message.encode())

