import os
import socket
import sys
import re
import time
from tcp_framing.my_framing import MyFraming
from tcp_framing.thread_worker import Worker



def main():
    myServer = TcpServer()


class TcpServer():

    # Port number server is listening on.
    defaultListenPort = 50001

    def __init__(self) -> None:
        listenAddr = ''       # Symbolic name meaning all available interfaces
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((listenAddr, self.defaultListenPort))
        s.listen(1)              # allow only one outstanding request
        # s is a factory for connected sockets

        while True:
            # wait until incoming connection request (and accept it)
            conn, addr = s.accept()  
            # Start new thread using worker class.
            Worker(conn, addr).start()
        
        

if __name__ == '__main__':
    main()