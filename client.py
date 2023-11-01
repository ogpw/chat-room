import socket
import threading
from queue import Queue
from tkinter import *

##This version of the client does not use OOP IT WORKS
##TODO: send a username/alias to server to be shown instead of IP

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
queue = Queue()

def error(err):
	errorWin = Tk()
	errorWin.title("Error")
	errorText = Label(master=errorWin, text=err)
	errorText.grid(row=0,column=0,padx=20,pady=20)
	okButton = Button(master=errorWin, text="OK", command=errorWin.destroy)
	okButton.grid(row=1,column=0,padx=20,pady=20)
	while errorWin:
		errorWin.update()

def listen():
	while True:
		serverMessage = server.recv(2048)
		if serverMessage:
			queue.put(serverMessage.decode())

def connServer():
	global server
	try:
		IP = ipEntry.get()
		PORT = int(portEntry.get())
	except ValueError:
		error("Invalid IP or port...")
	ipEntry.delete(0,END)
	portEntry.delete(0,END)

	print(IP,PORT)

	server = socket.create_connection((IP,PORT))
	server.send(unEntry.get().encode())
	unEntry.delete(0,END)
	threading.Thread(target=listen).start()

def send():
	message = msgEntry.get()
	msgEntry.delete(0,END)
	message = message.encode()
	server.send(message)
##Pipeline error sometimes, socket connection isn't made or something, something wrong with the recv I think
mainWin = Tk()
mainWin.title("Chat Client")

chatFeed = Text(master=mainWin)
chatFeed.grid(row=0,rowspan=4,column=0,padx=5,pady=5)

msgEntry = Entry(master=mainWin,width=60)
msgEntry.grid(row=4,column=0,padx=5,pady=5)

ipLabel = Label(master=mainWin,text="IP:")
ipLabel.grid(row=0,column=1)
ipEntry = Entry(master=mainWin)
ipEntry.grid(row=0,column=2,padx=5,pady=5)

portLabel = Label(master=mainWin,text="Port:")
portLabel.grid(row=1,column=1)
portEntry = Entry(master=mainWin)
portEntry.grid(row=1,column=2,padx=5,pady=5)

unLabel = Label(master=mainWin,text="Username:")
unLabel.grid(row=2,column=1)
unEntry = Entry(master=mainWin)
unEntry.grid(row=2,column=2)

connButton = Button(master=mainWin,text="Connect",command=connServer)
connButton.grid(row=3,column=1,columnspan=2,padx=5,pady=5)
connection_made = False

sendButton = Button(master=mainWin,text="Send",command=send)
sendButton.grid(row=4,column=1,columnspan=2,padx=5,pady=5)

def exit_program():
	mainWin.destroy()
	quit()

mainWin.protocol("WM_DELETE_WINDOW", exit_program)

while mainWin:
	if not queue.empty():
		chatFeed.insert(END, queue.get())
		chatFeed.insert(END, "\n")
	mainWin.update()

server.close()
quit()
