import re
import sys
import os
import socket
import datetime
import subprocess
import threading

global date_and_time

hosts_up = 0
hosts_down = 0

def get_host_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8",80))
	return s.getsockname()[0]

def check_ip(IP):
	global hosts_up
	global hosts_down
	try:
		if  subprocess.call(["ping", IP],stdout=subprocess.PIPE) == 0:
			hosts_up = hosts_up + 1
			print(date_and_time + " [+] {}: host is up.".format(IP) + " Number: " + str(hosts_up)) 
			

		else:
			hosts_down = hosts_down + 1
			pass
	except OSError:
		print(date_and_time+" [*] Unreachable Netowrk.")

	except KeyboardInterrupt:
		print("[+] Cancelled!")
		sys.exit()

try:
	net = str(sys.argv[1])

	if net =="-h":
		print("   Help\n-----------\nUsage: python pingsweep.py <IP address or range>\nEg: python pingsweep.py 127.0.0.1\nEg: python pingsweep.py 127.0.0.1/24")
		sys.exit()

	else:
		pass

except IndexError:

	net1 = (get_host_ip()).split(".")[:3]
	net = ".".join(net1) + ".0/24"



date_and_time = str(datetime.datetime.now())
print(date_and_time + " [+] Scan started.")


try:
	if re.search('/',net):
		if int(net.split("/")[1]) > 24:
			print(date_and_time + " [-] {}: is not in your IP range.".format(net))

		else:
			total = int(net[-2:]) + 230
			net2 = net.split(".")[-1]
			net3 = net2.split("/")[-2]
			net4 = net.split(".")
			threads = []
			for i in range(int(net3),total):
				ip_range = f'''{".".join(net4[:3])}.{str(i)}'''
				thread = threading.Thread(target=check_ip, args=(ip_range,))
				threads.append(thread)

			for i in range(len(threads)):
				threads[i].start()


	elif int(net.split(".")[-1]) > 255:
		print(date_and_time + " [-] {}: is not in your IP range.".format(net))


	else:
		check_ip(net)

except ValueError:
	check_ip(net)
