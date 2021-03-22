import os
import sys
import re
import socket
import sys
import re
import time
from tcp_framing.tcp_ui import UI
from tcp_framing.my_framing import MyFraming
from tcp_framing.my_read import myReadLine

def main():
    ui = UI()

    userArgs = ui.getUserInput()

    if userArgs[0] == "scp":
        myClient = TcpClient(userArgs)

class TcpClient():
    
    host = "localhost"
    port = 50000     # Using 50000 to connect to proxy.
    remoteFile = "remoteFile.txt"
    clientFile = ""

    
    def __init__(self, userArgs):

        if (len(userArgs) == 1):
            os.write(1, ("Incorrent input format.\n").encode())
            sys.exit(1)
        else:
            self.clientFile = userArgs[2]

        if len(userArgs) == 3:
            try:
                self.host, self.remoteFile = re.split(
                    ":", userArgs[2])
            except:
                print("Can't parse server:filename from '%s'" % userArgs[2])
                sys.exit(1)

        # Code from helloClient.py. Connects to socket.
        s = None
        for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                print("creating sock: af=%d, type=%d, proto=%d" %
                    (af, socktype, proto))
                s = socket.socket(af, socktype, proto)
            except socket.error as msg:
                print(" error: %s" % msg)
                s = None
                continue
            try:
                print(" attempting to connect to %s" % repr(sa))
                s.connect(sa)
            except socket.error as msg:
                print(" error: %s" % msg)
                s.close()
                s = None
                continue
            break

        if s is None:
            print('could not open socket')
            sys.exit(1)

        # while True:
        #     conn, addr = s.accept() # wait until incoming connection request (and accept it)
        #     if os.fork() == 0:      # child becomes server
        #         print('Connected by', addr)
        #         conn.send(b"hello")
        #         conn.send(b"world")
        #         conn.shutdown(socket.SHUT_WR)

        # s.send(self.frameMessage(self.defaultRemoteFile))

        myFraming = MyFraming(s)

        myFraming.sendMessage(self.remoteFile)

        serverMessage = myFraming.recvMessage()

        os.write(1,("Received: " + serverMessage + "\n").encode())

        if (serverMessage == "ok"):
            # Send file contents.
            fileContents = self.readFile(self.clientFile)

            myFraming.sendMessage(fileContents)

            os.write(1, ("Sent: " + self.clientFile).encode())

        s.close()


    def readFile(self, filename):
        fd = os.open(filename, os.O_RDONLY)

        inLine = myReadLine(fd)
        allLines = ""

        while inLine != "":
            allLines += inLine
            inLine = myReadLine(fd)
        
        os.close(fd)

        return allLines
    
    



if __name__ == '__main__':
    main()
