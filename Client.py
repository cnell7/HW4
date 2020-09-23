#   SMTP "MAIL FROM" message checker
#   Author: Christian Nell
#   Onyen: cnell
#   PID: 7302-29326
#   Date: 8/11/20
#   Purpose: To check a Simple Mail Transfer Protocol "MAIL FROM" message
#               and make sure it is following the correct syntax. This
#               message tells the mail server which person is trying to
#               email a message.
#
#   UNC Honor Pledge: I certify that no unauthorized assistance has been received or
#       given in the completion of this work
#       Signature: _Christian Nell__
import sys
import shutil
mailFrom = ""
rcptTo = []
data = []


def whitespace(string):
    #   <SP> | <SP> <whitespace>
    if(SP(string) == False):
        return string
    string = SP(string)
    return whitespace(string)


def SP(string):
    #   the space or tab char
    if(string[0] == ' ' or string[0] == '\t'):
        return string[1:]
    elif(string[0] == '\\'):
        if(string[1] == 't'):
            return string[2:]
    return False


def CRLF(string):
    #    the newline character
    if(string[0] == '\n'):
        string = string[1:]
        if(len(string) == 0):
            return True
        return string[1:]
    if(string[0] == '\\'):
        if(string[1] == 'n'):
            return string[2:]
    return False


def fromParse(string):
    #   Checkes for "From: " and a mailbox in a forward file
    if(string[0:5] != "From:"):
        return False
    string = string[6:]
    mailFrom = string
    return string


def toParse(string):
    #   Checkes for "To: " and a mailbox in a forward file
    if(string[0:3] != "To:"):
        return False
    string = string[4:]
    rcptTo.append(string)
    return string


def dataParse(string):
    #   Checks for Data in the forward file
    sys.stdout.write(string)
    data.append(string)
    return True


def responseCodeChecker(state):
    #   Checks the server's response
    #    <resp-number>
    temp = sys.stdin.readline()
    copy = temp[3:]
    sys.stderr.write(temp)
    code = temp[0:3]
    if(not(code == "250" or code == "354" or code == "500" or code == "501")):
        return False
    if(state == 0 or state == 1):
        if(code != "250"):
            return False
    elif(state == 2):
        if(code != "354"):
            return False
    #   <whitespace>
    if(copy[0] == whitespace(copy)[0]):
        return False
    copy = whitespace(copy)
    if(not(copy[1:])):
        return False
    #   <arbitrary-text> <CRLF>
    return True


def call_command(string, state):
    #   Checks to make sure file has correct From:, To: and Data parameters then logs to standard out
    isTrue = False
    if(state == 0):  # State 0 = From:
        string = fromParse(string)
        sys.stdout.write("MAIL FROM: " + string)
        if(not(responseCodeChecker(0))):
            return -1
        return 1
    elif(state == 1):  # State 1 = To:
        isTrue = toParse(string)
        if(isTrue == False):  # Move to state 2
            sys.stdout.write("DATA\n")
            if(not(responseCodeChecker(2))):
                return -1
            return call_command(string, 2)
        string = toParse(string)
        sys.stdout.write("RCPT TO: " + string)
        if(not(responseCodeChecker(1))):
            return -1
        return 1
    elif(state == 2):  # State 2 = Data
        isTrue = fromParse(string)
        if(isTrue):  # Move back to state 0
            sys.stdout.write(".\n")
            if(not(responseCodeChecker(0))):
                return -1
            return call_command(string, 0)
        dataParse(string)
        return 2
    return False


def main():
    #   Iterates through the lines in a forward file to process client-side
    state = 0
    with open(sys.argv[1], 'r') as my_file:
        for line in my_file:
            if(state == 0):
                rcptTo.clear()
                data.clear()
            state = call_command(line, state)
            if(state == -1):
                break
    if(state == 1):
        sys.stdout.write("DATA\n")
        if(not(responseCodeChecker(2))):
            state == 0

    if(not(state == -1)):  # End of file
        sys.stdout.write(".\n")
        responseCodeChecker(0)

    sys.stdout.write("QUIT\n")
    return False


main()
