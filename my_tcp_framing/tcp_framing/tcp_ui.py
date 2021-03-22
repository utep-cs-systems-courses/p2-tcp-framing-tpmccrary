import os
import sys
import re
import tcp_framing.my_read


class UI():

    def __init__(self) -> None:
        os.write(1, "Please enter this command to send file contents: 'scp <file_name> <host_name>:<remote_file_name>'\n".encode())
        pass

    def getUserInput(self):
        userInput = tcp_framing.my_read.myReadLine()
        
        return self.tokenizeArgs(userInput)

        
        

    # Returns the list of arguments from the user input.
    def tokenizeArgs(self, input):
        # If user inputs nothing, return empty arguments.
        if input == '\n' or input == '':
            return ['']

        inputArgs = []
        arg = ''
        inQuote = False

        i = 0
        while(i < len(input)):
            # Here we go through every character in the user input to make up an argument.
            # A space is what decides the speration of arguments, however, if we are in a quote, spaces are part of the argument.

            # If we find our first quote, flag that we are in a quote, and move on to the next character.
            if input[i] == '"' and inQuote == False:
                inQuote = True
                i += 1
            # If we reach a second quote, flag that we are out of the quote, and move on to the next character.
            elif input[i] == '"' and inQuote == True:
                inQuote = False
                i += 1

            # If the character is not a space, or if we are in a
            # quote (therefore we do not care about spaces), add the character to the argument.
            if (input[i] != ' ' and input[i] != '\n') or inQuote == True:
                arg += input[i]
            # If the character is a space, we are not in a quote, and the argument is not empty,
            # add the argument to the list of arguments.
            elif (input[i] == ' ' or input[i] == '\n') and inQuote == False and arg != '':
                inputArgs.append(arg)
                arg = ''

            i += 1

        return inputArgs
