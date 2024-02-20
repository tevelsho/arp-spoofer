This Python script allows you to perform ARP spoofing, which can be used for "Man In The Middle" attacks on a network. It spoofs ARP packets to manipulate the ARP cache of the target machine, redirecting its traffic to the attacker. Created to try penetration testing :)

Modules Used

    scapy: Used for crafting and sending packets.
    argparse: Used for parsing command line arguments.
    time: Used for adding delays.
    sys: Used for printing messages and flushing output.

Usage

    Install Dependencies:
    pip install scapy

Run the Script:

    sudo python arp_spoofer.py -t <target_ip> -g <gateway_ip>

Arguments:

    -t, --target: Specify the IP address of the target machine.
    -g, --gateway: Specify the IP address of the gateway (router).

Example:

    sudo python arp_spoofer.py -t 192.168.1.10 -g 192.168.1.1
