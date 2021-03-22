import os
import sys
import re
import socket
import sys
import re
import time

# Take input frome user: $scp <file_name> <host_name>:<remote_file_name>
# Use out of band signaling on remote file name: <message_length>:<message>
# Server creates file from received message.
# Server sends "ok" if everything went alright.
# Send contents of file, server writes it, and sends ok.
# Keep doing this till lenght is zero.


class MyFraming():

    def __init__(self, s) -> None:
        # Save connection.
        self.s = s
        pass
    
    # Sends given message to s (socket)
    def sendMessage(self, message):

        # Get length of message.
        mesLength = len(message)

        # Use Out-of-Band signaling with the format: <message_length>:<message>
        framedMessage = (str(mesLength) + ":" + message).encode()

        # Send the message to the given socket.
        self.s.send(framedMessage)

        return message


    # Receives a message from s (socket). Waits till whole message is recieved before returning to caller.
    def recvMessage(self):
        
        # Get initil message.
        message = self.s.recv(1024).decode()

        # If message does not have a : in it, keep trying to get it until we do.
        while ":" not in message:
            message += self.s.recv(1024).decode()

        # Split the message up.
        splitMessage = message.split(":")

        messageLen = splitMessage[0]
        message = splitMessage[1]

        # While message is not the correct length, keep requesting it from sender.
        while len(message) != int(messageLen):
            message += self.s.recv(1024).decode()
        
        return message
        

        


