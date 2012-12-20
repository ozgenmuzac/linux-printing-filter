#!/usr/bin/env python

import socket
import cups

from threading import Thread

class SeapClient():
	def __init__(self):
		print "Seap Client initialized"
	def send_message(self, message):
		print "Sending Message: " + message
		

class DaemonAgent(Thread):
	def __init__(self, conn, addr):
		self.conn = conn
		self.claddr = addr
		self.seap_client = SeapClient()
		Thread.__init__(self)

	def run(self):
		print "Thread Started"
		inp = self.conn.recv(1024).strip()
		print inp
		while inp:
			inp_arr = inp.split()
			print inp_arr[0]
			if inp_arr[0] == "file_path:":
				self.seap_client.send_message(inp_arr[1])
				self.conn.send("OK\n")
				inp = self.conn.recv(1024).strip()
			elif inp_arr[0] == "job_id:":
				print "job_id: " + inp_arr[1]
				self.conn.send("OK\n")
				self.conn.close()
				break
			else:
				self.conn.send("OK\n")
				inp = self.conn.recv(1024).strip()
		


HOST = '127.0.0.1'
PORT = 9100
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while True:
	conn, addr = s.accept()
	print 'Connected by', addr
	
	a = DaemonAgent(conn, addr)
	a.start()
