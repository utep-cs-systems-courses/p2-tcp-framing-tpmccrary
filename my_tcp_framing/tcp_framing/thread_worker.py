#! /usr/bin/env python3

import sys
import time
import os
import socket
from tcp_framing.my_framing import MyFraming
from threading import Thread, Lock

threadNum = 0
inTransfer = set()
transLock = Lock()

# Class Worker inheritance from Thread. Used to create new thread for server.
class Worker(Thread):
    def __init__(self, socketConn, address):
        global threadNum
        # Initialize thread.
        Thread.__init__(self, name="Thread-%d" % threadNum)
        # Add to number of threads we have ran. Not important but good just to see.
        threadNum += 1
        self.thisThread = threadNum
        self.socketConn = socketConn
        self.address = address

    # Overiding this method from super class.
    def run(self):
        # A plus of threds, all threads can access global variables.
        global transLock

        os.write(1, ("Starting Thread: " + str(self.thisThread) + "\n").encode())
        os.write(1, ("Thread " + str(self.thisThread) + ": Connected by " + str(self.address) + "\n").encode())
        # conn.send(b"hello")
        # conn.send(b"world")
        # data = conn.recv(1024).decode()
        
        # Make MyFraming object with socket conn. Used to send and receive messages.
        myFraming = MyFraming(self.socketConn)

        # Get filename from client.
        fileName = myFraming.recvMessage()
        os.write(1, ("Thread " + str(self.thisThread) + ": Received: " + fileName + " \n").encode())

        # Locking logic here. Locking the critical section.
        # If thread cannot aquire, it gets blocked and can go to sleep if OS allows.
        transLock.acquire()
        # Returns true if given file is available to transfer.
        canTransfer = self.canTransfer(fileName)
        # Thread releases once done with this code.
        transLock.release()

        # Here we actually check the status of the file. If its in transfer, tell client it is and dont send anything.
        if (canTransfer is False):
            sentMessage = myFraming.sendMessage("Error: File in use by another client.")
            os.write(1, ("Thread " + str(self.thisThread) + ": Sent: " + sentMessage + "\n").encode())
        # If it is not taken, create the file and write to it.
        else:

            # Put the file name in the set so other threads can check it.
            inTransfer.add(fileName)

            # Send ok to the client.
            sentMessage = myFraming.sendMessage("ok")
            os.write(1, ("Thread " + str(self.thisThread) + ": Sent: " + sentMessage + "\n").encode())

            # Get the file contents from the client.
            fileContents = myFraming.recvMessage()
            sentMessage = myFraming.sendMessage("ok")
            os.write(1, ("Thread " + str(self.thisThread) + ": Sent: " + sentMessage + "\n").encode())

            # Write it to the file.
            fd = os.open("my_tcp_framing/test/" + fileName, os.O_CREAT | os.O_WRONLY)
            os.write(fd, (fileContents).encode())
            os.close(fd)

            os.write(1, ("Thread " + str(self.thisThread) + ": Created: " + fileName + "\n").encode())
            
            # Remove filr from set as it is no longer being transfered.
            inTransfer.remove(fileName)

        # Shut down the socket.
        print("Shutting down socket on Thread " + str(self.thisThread))
        self.socketConn.shutdown(socket.SHUT_WR)
    
    # Returns true if given file is available to transfer.
    def canTransfer(self, fileName):
        global inTransfer
        if (fileName in inTransfer):
            return False
        else:
            return True



    
