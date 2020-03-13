from scapy.all  import *
from time import sleep
from random import *
port = RandShort()


while True:
	send(IP(dst='10.0.0.'+ str(randint(1,10)))/TCP(dport=port))
	sleep(1)
	send(IP(dst='10.0.0.'+ str(randint(1,10)))/UDP(dport=port))
	sleep(1)
	send(IP(dst='10.0.0.'+ str(randint(1,10)))/ICMP())
	sleep(1)

