# MSPTP

This is the attack implementation for the "MS-PTP: Protecting Network Timing from Byzantine Attacks" paper. The readers need to deploy a local network with three Raspberry Pi 4 nodes to launch the attack. All nodes shall install the following packets:
- UDPdump
- PTPD2
- Wireshark
- Python 3

# How to use

The ieee1588.py file contains all modified packets to launch the attack. The attack's main file is the Malinfo.py. The readers must change the IP and port numbers in this file according to their local network. The readers can modify the attack pattern by changing the attack parameters. For result visualization, the readers are referred to execute the other Python files.
