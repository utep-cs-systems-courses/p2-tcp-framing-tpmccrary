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

# TODO: Add multi-threading.
# TODO: Add threading lock. Code can be found in lecture notes named 22 mar.

def main():
    # Get user input.
    ui = UI()
    userArgs = ui.getUserInput()

    # If first arg is scp then run command.
    if userArgs[0] == "scp":
        myClient = TcpClient(userArgs)


class TcpClient():
    
    host = "localhost"
    port = 50000     # Using 50000 to connect to proxy.
    remoteFile = "remoteFile.txt"
    clientFile = ""

    
    def __init__(self, userArgs):

        # If the args is just one, its not a valid input.
        if (len(userArgs) == 1):
            os.write(1, ("Incorrent input format.\n").encode())
            sys.exit(1)
        else:
            self.clientFile = userArgs[1]

        # If the args equals 3, then get the host and remote file name.
        if len(userArgs) == 3:
            try:
                self.host, self.remoteFile = re.split(
                    ":", userArgs[2])
            except:
                print("Can't parse server:filename from '%s'" % userArgs[2])
                sys.exit(1)

        # Code from helloClient.py. Creates a socket.
        # Using host and port, tries to create. With an uspecified address family.
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

        # If socket is none.
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

        # Make MyFraming object with socket s. Used to send and receive messages.
        myFraming = MyFraming(s)

        # Send remote file name to server.
        myFraming.sendMessage(self.remoteFile)

        # Get message back from server.
        serverMessage = myFraming.recvMessage()
        os.write(1,("Received: " + serverMessage + "\n").encode())

        # If server responded with ok, send the file contents.
        if (serverMessage == "ok"):
            # Get all the file contents.
            fileContents = self.readFile(self.clientFile)

            # Send the file contents to the server.
            myFraming.sendMessage(fileContents)

            os.write(1, ("Sent: " + self.clientFile + "\n").encode())

            serverMessage = myFraming.recvMessage()
            os.write(1,("Received: " + serverMessage + "\n").encode())

        s.close()


    # Given a file name, reads all the lines and returns one string.
    def readFile(self, filename):
        fd = os.open("my_tcp_framing/test/" + filename, os.O_RDONLY)

        inLine = myReadLine(fd)
        allLines = ""

        while inLine != "":
            allLines += inLine
            inLine = myReadLine(fd)
        
        os.close(fd)

        return allLines
    
    



if __name__ == '__main__':
    main()
