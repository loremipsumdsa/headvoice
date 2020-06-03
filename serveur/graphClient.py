import socket
from threading import Thread
import sys
import time
from tkinter import *
#from ScrolledText import ScrolledText

host="localhost"
port=1281

class ScrolledText(Text):
    def __init__(self, master=None, **kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)

        kw.update({'yscrollcommand': self.vbar.set})
        Text.__init__(self, self.frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))



class ThEmission(Thread):
	def __init__(self,connexion):
		Thread.__init__(self)
		self.connexion=connexion
		self.turn=True
		self.sendL=[]

	def run(self):
		while self.turn:
			for msg in self.sendL:
				self.connexion.send(msg.encode())
				self.sendL.remove(msg)

	def send(self,msg):
		self.sendL.append(msg)

	def stop(self):
		self.turn=False

class ThReception(Thread):
	def __init__(self,connexion):
		Thread.__init__(self)
		self.connexion=connexion
		self.turn=True

	def run(self):
		while self.turn:
			msgToPrint=self.connexion.recv(1024).decode()
			scrolledText.insert(END, msgToPrint + "\n")

	def stop(self):
		self.turn=False

def send():
	thE.send(entry.get())
	print(entry.get())


global scrolledText
global entry
global button
global thE
global thR


fenetre=Tk()
scrolledText=ScrolledText(fenetre,width=30,height=15)
scrolledText.pack()
entry=Entry(fenetre, text=" ")
entry.pack()
button=Button(fenetre,text="Send", command=send)
button.pack()


connexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	connexion.connect((host,port))
except socket.error:
	print("connexion fail")

print("connexion ok")

thE=ThEmission(connexion)
thR=ThReception(connexion)
thE.start()
thR.start()

fenetre.mainloop()
thE.stop()
thR.stop()
connexion.close()
