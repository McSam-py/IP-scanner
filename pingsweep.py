import re
import sys
import os
import socket
import datetime
import subprocess
import threading

hosts_up = 0
hosts_down = 0

#Function to find the ip address of the user.
def get_host_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8",80))
	return s.getsockname()[0]

#Fucntion to check whether an IP is alive.
def check_ip(IP):
	global hosts_up
	global hosts_down
	try:
		if  subprocess.call(["ping", IP],stdout=subprocess.PIPE) == 0: #This command peforms a ping request on the IP.
			hosts_up = hosts_up + 1 #Counter for the number of live hosts
			print(date_and_time + " [+] {}: host is up.".format(IP) + " Number: " + str(hosts_up)) 
		else:
			hosts_down = hosts_down + 1 #Counter for the number hosts down
			pass
			
	except OSError:
		print(date_and_time+" [*] Unreachable Netowrk.")

	except KeyboardInterrupt:
		print("[+] Cancelled!")
		sys.exit()

def main_program():
	global date_and_time
	try:
		net = str(sys.argv[1]) #Takes the argument from the user.

		if net =="-h": 
			print("   Help\n-----------\nUsage: python pingsweep.py <IP address or range>\nEg: python pingsweep.py 127.0.0.1\nEg: python pingsweep.py 127.0.0.1/24") #Displays a help list.
			sys.exit()

		else:
			pass

	except IndexError: #This exception handles a case where the user provides no argumnets.
		net1 = (get_host_ip()).split(".")[:3]
		net = ".".join(net1) + ".0/24"



	date_and_time = str(datetime.datetime.now()) #show date and time.
	print(date_and_time + " [+] Scan started.") 


	try:
		if re.search('/',net): #Searches for '/' in the argument provided by the user. 
			if int(net.split("/")[1]) > 24: #This condition checks whether the argument give by the user is out of range.
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


		elif int(net.split(".")[-1]) > 255: #This condition checks whether the argument give by the user is out of range.
			print(date_and_time + " [-] {}: is not in your IP range.".format(net))


		else:
			check_ip(net)

	except ValueError:
		check_ip(net)

if __name__ == '__main__':
	main_program()
