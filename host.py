"""Custom topology example
Two directly connected switches plus a host for each switch:
   host --- switch --- switch --- host
Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""
from mininet.cli  import CLI
from mininet.node import OVSController,OVSKernelSwitch,Controller,RemoteController
from mininet.topo import Topo
from mininet.net  import Mininet
from mininet.log  import setLogLevel
from mininet.util import dumpNodeConnections
from scapy 	  import *  

#controller 
CONTROLLER_IP = "192.168.1.2"


class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."
       # net = Mininet(controller=Controller, switch=OVSSwitch)
        # Add hosts and switches
        webserver = self.addHost( 'webserver' )
        webclient1 = self.addHost('webclient1')
        webclient2 = self.addHost('webclient2')
        hacker = self.addNode('hacker')

        trafficG1 = self.addHost( 'trafficG1' )
        trafficG2 = self.addHost( 'trafficG2' )

        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
	ovsk = self.addSwitch('openflow',dpid="3",cls=OVSKernelSwitch)

        # Add links
        #s2 network 
        self.addLink( webserver, s2 )
        self.addLink( trafficG1, s2 )
        self.addLink( trafficG2, s2 )
        self.addLink(ovsk,s3)
        self.addLink(ovsk,s2)
        #s3 network
        self.addLink(webclient1,s3)
        self.addLink(webclient2,s3)
        self.addLink(hacker,s3)
        
def  simpleTest():
	"Test the topologie"
	topo = MyTopo()
	net = Mininet(topo=topo,controller=lambda name: RemoteController( name, ip='192.168.1.2' ),autoStaticArp=True)
        #Controller configuration TODO
        #net.addController(controller=CONTROLLER_IP,port=6633)
	net.start()
	print "==============> Web Traffic <=========="
        webserver = net.get('webserver')
	webclient1 = net.get('webclient1')
	webclient2 = net.get('webclient2')
	deb = webserver.cmd("python -m CGIHTTPServer 9000 &")
	print "the web server is lunched his PID : %s" % deb
	webclient1.sendCmd('curl -I http://%s:9000/?[1-10]' % webserver.IP())
	webclient2.sendCmd('curl -I http://%s:9000/?[1-10]' % webserver.IP())
	print "================>Traffic Generation<================"
	tg1 =  net.get('trafficG1')
	tg2 = net.get('trafficG2')
	tg1.sendCmd('python tg.py &')
	tg2.sendCmd('python tg.py &')
	
	

	CLI(net)
if __name__ == '__main__':
	
	simpleTest()

topos = { 'mytopo': ( lambda: MyTopo() ) }
 
