import socket
from threading import Thread
import sys
import time

host="localhost"
port=1281
serverTurn=True

global server

class Channel(Thread):

####### THREAD DE TRAITEMENT DE msgES #########

	def __init__(self, cId):
		Thread.__init__(self)
		self.msgsToexe=[]
		self.turn=True
		self.cId=cId
	def run(self):
		while self.turn:
			try:
				print("Channel "+ str(self.cId) + " : " + self.msgsToexe[0])
				time.sleep(3)
				del self.msgsToexe[0]
			
			except IndexError:
				pass
				#print("no more msg")

	def addmsg(self,msg):
		self.msgsToexe.append(msg)

	def stop(self):
		self.turn=False



class ThClient(Thread):
	def __init__(self, connexion):
		Thread.__init__(self)
		self.connexion=connexion
		self.turn=True
		self.nom=self.getName()
		print("New client accepted")

	def run(self):
		while self.turn:
			try:
				msg=self.connexion.recv(1024).decode()
			except ConnectionResetError:
				self.turn=False
				break
			try:
				channel[int(msg[0]+msg[1])].addmsg(msg)
			except (ValueError, IndexError):
				if msg!= "emit" and msg!= "end":
					print("a msge can't be assignate (Syntaxe error)")

			if msg == "emit":
				transmitter.send("server emit")
			elif msg=="end":
				print("eteindre serveur")
				server.stop()
				
		self.connexion.close()
		connectedClient.remove(self)
		print("A client quit")

	def stop(self):
		self.turn=False
		self.connexion.close()
		connectedClient.remove(self)

class ThEmit(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.emitList=[]
		self.turn=True

	def run(self):
		while self.turn:
			for msg in self.emitList:
				print("i emit")
				for client in connectedClient:
					client.connexion.send(msg.encode())
				self.emitList.remove(msg)
	
	def send(self, msg):
		self.emitList.append(msg)
		print("New emission commanded")

	def stop(self):
		self.turn=False

class ThClientConn(Thread):
	def __init__(self, mainConnexion):
		Thread.__init__(self)
		self.turn=True
		self.mainConnexion=mainConnexion

	def run(self):
		while self.turn:
			newClient, adress = self.mainConnexion.accept()
			connectedClient.append(ThClient(newClient))
			connectedClient[-1].start()
	def stop(self):
		self.turn=False

global connectedClient
connectedClient=[]

print("--------HEADVOICE LEVEL 1 V 2.0------------- \n")
######  CREATION DES CHANNELS  #########
global channel
channel=[]

nbChannel=int(input("How many channel ? > "))
for i in range(nbChannel):
	channel.append(Channel(i))
	channel[i].start()


global transmitter
transmitter=ThEmit()
transmitter.start()

class Server ():
	def __init__(self, host, port):
		self.mainConnexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.turn=True
		self.thCC=0
	def start(self):
		try:
			self.mainConnexion.bind((host,port))
		except socket.error:
			print("connexion fail")

		self.mainConnexion.listen(5)
		print("Server ready")
		self.thCC=ThClientConn(self.mainConnexion)
		self.thCC.start()
	
	def stop(self):
		self.thCC.stop()
		for client in connectedClient:
			client.stop()
		self.mainConnexion.close()
		print("Server disconected")

		for chan in channel:
			chan.stop()

		transmitter.stop()
		input(">")

server=Server(host,port)
server.start()
