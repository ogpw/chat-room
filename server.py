import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#IP = str(input("IP: "))
PORT = int(input("PORT: "))

server.bind(("", PORT)) #binds the server to the local machine's ip and a custom port

server.listen(100) #listens for a maximum of 100 connections

list_of_clients = [] #create empty list of clients

def clientThread(conn, addr, un):
	for clients in list_of_clients: ##for every client that is connected
		clients.send((addr[0]+"/"+un+" connected.").encode()) ##send a message out that a new client has connected (this is called first as a new client thread has been created for a new client)
	while True: ##constant loop
		message = conn.recv(2048) ##server receives connection - receives data with max size of 2048 bytes
		if message: ##if there is a message
			messageOut = "<"+addr[0]+"/"+un+"> "+message.decode()
			print(messageOut)
			for clients in list_of_clients: #for every client in the list of clients
				##DISABLED FOR NOW FOR DEBUGGING if clients != conn: ##if the current client in the list is not the one sending the message
				clients.send(messageOut.encode()) ##send the message from this client to every other client ##CURRENTLY SENDS IT TO ALL CLIENTS, INCLUDING CLIENT THAT SENT IT
		else: ##if no connection is being received, client is assumed to have disconnected.
			print(addr[0]+" disconnected.") ##print that a client has disconnected in the server console
			if conn in list_of_clients:
				list_of_clients.remove(conn)
			for clients in list_of_clients: ##same code for when a client connects but instead says said client has disconnected
				clients.send((addr[0]+"/"+un+" disconnected.").encode())
			break
#	conn.send(("Welcome...").encode())
#
#	while True:
#		try:
#			message = conn.recv(2048)
#			if message:
#				print("<"+addr[0]+">"+message)
#		except:
#			continue


while True:
	connection, address = server.accept()
	username = connection.recv(2048).decode() #sets username blank for now
	print(address[0]+" connected with username: "+username) ##outputs to the console that a client has connected
	list_of_clients.append(connection) ##adds the new client to list_of_clients
	threading.Thread(target=clientThread,args=(connection,address,username)).start() ##starts a new thread

conn.close()
server.close()
