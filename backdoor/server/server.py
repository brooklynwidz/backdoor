import socket 
import threading
import json
import termcolor
import subprocess


ip = '192.168.1.26'
port = 5555
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((ip,port))
print(termcolor.colored("[+] Listening for client", 'green'))
server.listen(5)



mode = input("Enter Mode (shell/chat)")
if mode == 'chat':
    def communication(client):
        msg = input("[+] client:> ")
        client.send(msg.encode())
        client.recv(1024).decode

elif mode == 'shell':
    def shell(client):
        while True:
            command = input("[+]Shell:~ ")
            subprocess.getoutput(command)
    
def handle_clinet():
    client,addr = server.accept()
    threading.Thread(target=communication, args=(client,))
    threading.Thread(target=shell, args=(client,))
