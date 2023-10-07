import socket
from threading import Thread
from tkinter import *

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login") 

        self.login.resizable(width=False, height=False)#we don't want it to be resizable so we are giving it as false 
        self.login.configure(width=400, height=300)

        self.pls = Label(self.login,
					text = "Please login to continue",
					justify = CENTER,
					font = "Helvetica 14 bold")
        self.pls.place( relheight = 0.15,
                        relx = 0.2,
                        rely = 0.07)
        self.entryName = Entry(self.login,
							font = "Helvetica 14")
        

        self.submit= Button(self.login,text="Login",
                            font = "Helvetica 14 bold",
                            command=lambda:self.submitData(self.entryName.get())
                             )
        self.submit.place(relx=0.4,
                          rely=0.55)
        self.Window.mainloop()
        
    def submitData(self,name):
        self.login.destroy()
        self.name=name
        rec = Thread(target=self.receive)
        rec.start()
    
    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    print(message)
            except:
                print("An error occured!")
                client.close()
                break 


g=GUI()


def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))

receive_thread = Thread(target=receive)
receive_thread.start()
write_thread = Thread(target=write)
write_thread.start()
