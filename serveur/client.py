import socket
from threading import Thread
import sys
import time

host="localhost"
port=1281

class ThEmission(Thread):
	def __init__(self,connexion):
		Thread.__init__(self)
		self.connexion=connexion
		self.turn=True
	def run(self):
		msg=input('>')
		self.connexion.send(msg.encode())

class ThReception(Thread):
	def __init__(self,connexion):
		Thread.__init__(self)
		self.connexion=connexion
		self.turn=True

	def run(self):
		msg=self.connexion.recv(1024)
		print(msg.decode())



connexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	connexion.connect((host,port))
except socket.error:
	print("connexion fail")

print("connexion ok")




while 1:
	thE=ThEmission(connexion)
	thE.start()
	thR=ThReception(connexion)
	thR.start()
