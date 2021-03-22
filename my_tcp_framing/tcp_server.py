import os
import sys
import re
import socket
import sys
import re
import time
from tcp_framing.my_framing import MyFraming



def main():
    myServer = TcpServer()


class TcpServer():

    defaultRemoteFile = "remoteFile.txt"
    defaultListenPort = 50001

    def __init__(self) -> None:
        listenAddr = ''       # Symbolic name meaning all available interfaces
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((listenAddr, self.defaultListenPort))
        s.listen(1)              # allow only one outstanding request
        # s is a factory for connected sockets

        while True:
            conn, addr = s.accept()  # wait until incoming connection request (and accept it)
            if os.fork() == 0:      # child becomes server
                print('Connected by', addr)
                # conn.send(b"hello")
                # conn.send(b"world")
                # data = conn.recv(1024).decode()
                myFraming = MyFraming(conn)

                fileName = myFraming.recvMessage()
                
                os.write(1, ("Received: " + fileName + " \n").encode())

                if (os.path.isfile("./test/" + fileName)):
                    sentMessage = myFraming.sendMessage("Error: File already exist.")
                    os.write(1, ("Sent: " + sentMessage).encode())
                else:
                    sentMessage = myFraming.sendMessage("ok")
                    os.write(1, ("Sent: " + sentMessage).encode())

                    fileContents = myFraming.recvMessage()

                    fd = os.open("my_tcp_framing/test/" + fileName)




                
                conn.shutdown(socket.SHUT_WR)
        
        

if __name__ == '__main__':
    main()