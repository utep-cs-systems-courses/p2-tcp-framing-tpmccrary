#! /usr/bin/env python3

import sys
import time
import os
import socket
from tcp_framing.my_framing import MyFraming
from threading import Thread, enumerate

threadNum = 0

# Class Worker inheritance from Thread. Used to create new thread for server.
class Worker(Thread):
    def __init__(self, socketConn, address):
        global threadNum
        # Initialize thread.
        Thread.__init__(self, name="Thread-%d" % threadNum)
        # Add to number of threads we have ran. Not important but good just to see.
        threadNum += 1
        self.socketConn = socketConn
        self.address = address

    # Overiding this method from super class.
    def run(self):
        os.write(1, ("Starting Thread: " + str(threadNum) + "\n").encode())
        os.write(1, ("Connected by " + str(self.address) + "\n").encode())
        # conn.send(b"hello")
        # conn.send(b"world")
        # data = conn.recv(1024).decode()
        
        # Make MyFraming object with socket conn. Used to send and receive messages.
        myFraming = MyFraming(self.socketConn)

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

        
        self.socketConn.shutdown(socket.SHUT_WR)
        pass


    
