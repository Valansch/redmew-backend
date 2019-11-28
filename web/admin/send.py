#!/usr/bin/env python3
import sys
from socket import socket, AF_INET, SOCK_DGRAM

if len(sys.argv) > 2:

        mySocket = socket( AF_INET, SOCK_DGRAM )

        PORT_NUMBER = int(sys.argv[2])
        SIZE = 1024
        mySocket.sendto( bytes(sys.argv[1], 'UTF-8') , ('127.0.0.1', PORT_NUMBER) )

