#!/usr/bin/env python


import sys
import tempfile
from sys import argv
from socket import socket

class DaemonClient():

	def __init__(self, server, port, job_id):
		self.server = server
		self.port = port
		self.job_id = job_id
		self.sock = socket()
		self.sock.connect((self.server, self.port))

	def send(self, message):
		self.sock.sendall(message + "\n")
		response = self.sock.recv(1024).strip()
		return response

	def send_to_daemon(self, file_path):
		message = "file_path: " + file_path
		response = self.send(message)
		if not response.startswith("OK"):
			return True
		
		message = "job_id: " + str(self.job_id)
		response = self.send(message)
		if not response.startswith("OK"):
			return True
		else:
			return True
	

def start_transfering(job_id, args):
	daemon_client = DaemonClient("127.0.0.1", 9100, job_id)
	fout = tempfile.NamedTemporaryFile(delete=False)
	daemon_client.send(args)
	f = sys.stdin
	text = f.read()
	fout.write(text)
	response = daemon_client.send(text)
	fout.close()
	response = daemon_client.send_to_daemon(fout.name)
	if response:
		sys.stdout.write(text)

if __name__ == '__main__':
	filelog = open("/home/ozgen/filter.log", "wb+")
	jobId = int(argv[1])
	args = argv[0]+" "+argv[1]+" "+argv[2]+" "+argv[3]+" "+argv[4]+" "+argv[5] 
	filelog.write(argv[0]+" "+argv[1]+" "+argv[2]+" "+argv[3]+" "+argv[4]+" "+argv[5])
	start_transfering(jobId, args)
