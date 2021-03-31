# importing required libraries
import socket, sys, time

# Creating socket and recieving the hostname
new_socket = socket.socket()
hostname = socket.gethostname() # gets IP of other user
socket_ip = socket.gethostbyname(hostname)
port = 8080    # Default-free port on most machines

# Binding host and port
new_socket.bind((hostname,port))
print("ip: ", socket_ip)

# Listening for connections
name = input("enter username: ")
new_socket.listen()

# Accepting incoming connections
conn, add, = new_socket.accept()
print("Recieved communication from ", add[0])

# storting incoming connection data
client = (conn.recv(1024)).decode()
print(client, " has connected")
conn.send(name.encode())

# delivering packets/messages
while True:
    message = input("You: ")
    conn.send(message.encode())
    message = conn.recv(1024)
    message = message.decode()
    print(client, ":", message)

