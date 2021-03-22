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
                
                # Make MyFraming object with socket conn. Used to send and receive messages.
                myFraming = MyFraming(conn)

                # Get filename from client.
                fileName = myFraming.recvMessage()
                
                os.write(1, ("Received: " + fileName + " \n").encode())

                # If file name is already take, tell client.
                if (os.path.isfile("./test/" + fileName)):
                    sentMessage = myFraming.sendMessage("Error: File already exist.")
                    os.write(1, ("Sent: " + sentMessage + "\n").encode())
                # If it is not taken, create the file and write to it.
                else:
                    # Send ok to the client.
                    sentMessage = myFraming.sendMessage("ok")
                    os.write(1, ("Sent: " + sentMessage + "\n").encode())

                    # Get the file contents from the client.
                    fileContents = myFraming.recvMessage()
                    sentMessage = myFraming.sendMessage("ok")
                    os.write(1, ("Sent: " + sentMessage + "\n").encode())

                    # Write it to the file.
                    fd = os.open("my_tcp_framing/test/" + fileName, os.O_CREAT | os.O_WRONLY)
                    os.write(fd, (fileContents).encode())
                    os.close(fd)

                    os.write(1, ("Created: " + fileName + "\n").encode())

                
                conn.shutdown(socket.SHUT_WR)
        
        

if __name__ == '__main__':
    main()