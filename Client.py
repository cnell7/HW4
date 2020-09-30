#   Author: Christian Nell
#   Onyen: cnell
#   PID: 7302-29326
#   Date: 8/11/20
#   Purpose: SMTP mail client. Takes two command line arguments. Prompts user for- From:, To:, Subject:, Message:
#                  Message is terminated with "\n.\n". After correct message is input from user, socket connects
#                  to mail server. This client can handle several errors including socket errors.
#
#   UNC Honor Pledge: I certify that no unauthorized assistance has been received or
#       given in the completion of this work
#       Signature: _Christian Nell__
import sys
import shutil
import time
from socket import *


def reverse_path(string):
    #  <path>
    copy = string
    findPath = path(string)
    if(findPath == False):
        return False
    if(findPath[0] == '\n'):
        return copy[:len(copy)-len(findPath)]
    print("ERROR whitespace or too many paths after the first mail from path")
    return False


def forward_path(string):
    #  <path>
    copy = string
    findForward = path(string)
    if(findForward == False):
        return False
    return copy[:len(copy)-len(findForward)]


def path(string):
    #  <mailbox>
    string = mailbox(string)
    if(string == False):
        return False
    return string


def mailbox(string):
    #  <local-part>
    copy = string
    string = local_part(string)
    if(string == False or (copy[0] == string[0])):
        print("ERROR -- local-part")
        return False
    #  "@"
    if(string[0] != '@'):
        print("ERROR -- mailbox")
        return False
    #  <domain>
    string = domain(string[1:])
    if(string == False):
        return False
    return string


def whitespace(string):
    #   <SP> | <SP> <whitespace>
    if(SP(string) == False):
        return string[0:]
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


def nullspace(string):
    #   <null> | <whitespace>
    if(null(string[0])):
        return string
    return whitespace(string)


def null(c):
    #  no character
    if((c != ' ') or (c != '\t')):
        return False
    return True


def local_part(string):
    #   <string>
    string = string_(string)
    return string


def string_(string):
    #   <char> | <char> <string>
    if(char(string) == False):
        return string
    return string_(string[1:])


def char(string):
    #   any one of the printable ASCII characters, but not any
    #       of <special> or <SP>
    if(special(string[0]) or SP(string) or not(ord(string[0]) < 128) or CRLF(string[0])):
        return False
    return True


def domain(string):
    #   <element> | <element> "." <domain>
    string = element(string)
    if(string == False):
        print("ERROR -- domain")
        return False
    if(string[0] == '.'):
        string = domain(string[1:])
    return string


def element(string):
    #  <letter> | <name>
    if(not(letter(string[0]))):
        return False
    if(name(string) != False):
        string = name(string)
    else:
        string = string[1:]
    return string


def name(string):
    #   <letter> <let-dig-str>
    if(not(letter(string[0]))):
        return False
    return let_dig_str(string)


def letter(c):
    #   any one of the 52 alphabetic characters A through Z
    #       in upper case and a through z in lower case
    if c.isalpha():
        return True
    return False


def let_dig_str(string):
    #   <let-dig> | <let-dig> <let-dig-str>
    if(not(let_dig(string[0]))):
        return string
    return let_dig_str(string[1:])


def let_dig(c):
    #  <letter> | <digit>
    if(letter(c) or digit(c)):
        return True
    return False


def digit(c):
    #    any one of the ten digits 0 through 9
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if c in digits:
        return True
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


def special(c):
    #   special list ... shouldn't be in input
    special_list = ['<', '>', '(', ')', '[', ']',
                    '\\', '.', ',', ';', ':', '@', '"']
    if c in special_list:
        return True
    return False

#   500 Syntax error


def error500(string, clientSocket):
    message = "500 Syntax error: command unrecognized"
    clientSocket.send(message.encode())
    return False

#   501 Syntax error


def error501(string, clientSocket):
    message = "501 Syntax error in parameters or arguments"
    clientSocket.send(message.encode())
    return False

#   503 Bad sequence


def error503(string, clientSocket):
    message = "503 Bad sequence of commands"
    clientSocket.send(message.encode())
    return False

#   250 OK


def ok250(count, clientSocket):
    message = "250 OK"
    try:
        clientSocket.send(message.encode())
    except OSError:
        print("ERROR sending 250 message")
        return False
    count += 1
    return count

#   Gets a list of RCPTs from user via command line (called in createMessage) and makes sure they follow protocol


def getRCPTS(rcpt):
    searching = True
    rcptTo = []
    while rcpt:
        forward = forward_path(rcpt)
        if(not(forward)):
            return False
        rcptTo.append(forward)
        rcpt = rcpt[len(forward):]
        if(rcpt[0] == '\n'):
            return rcptTo
        if(not(rcpt[0] == ',')):
            print("ERROR missing ',' or ',' is in wrong place")
            return False
        rcpt = rcpt[1:]
        rcpt = whitespace(rcpt)
    return rcptTo


#   Gets user input from command line to create mail message send over TCP socket


def createMessages(serverName, serverPort):
    state = 0
    mailFrom = ""
    rcptTo = []
    subjectMessage = ""
    data = []
    fullMessage = []
    print("From:")
    for line in sys.stdin:
        if(state == 0):
            mailFrom = reverse_path(line)
            if(mailFrom == False):
                print("From:")
            else:
                fullMessage.append(mailFrom)
                state += 1
                print("To:")
        elif(state == 1):
            rcptTo = getRCPTS(line)
            if(rcptTo == False):
                print("To:")
            else:
                fullMessage.append(rcptTo)
                state += 1
                print("Subject:")
        elif(state == 2):
            subjectMessage = line
            fullMessage.append(subjectMessage)
            state += 1
            print("Message:")
        elif(state == 3):
            if(line == ".\n"):
                data.append(line)
                fullMessage.append(data)
                test = acceptingMessages(fullMessage, serverName, serverPort)
                if(test == False):
                    return False
                return True
            else:
                data.append(line)
    return True


#   Parses--> 220 Random “greeting” text that includes the name of the server


def greetingParse(string, clientSocket):
    if(string[:3] == '220'):
        return True
    return error500(string, clientSocket)

#   Parses--> 250 Hello <hostname> pleased to meet you


def ok250Parse(string, clientSocket):
    if(string[:3] == '250'):
        return True
    return error500(string, clientSocket)

#   After sending DATA SMTP command, makes sure server sends 354 response message


def send354Parse(string, clientSocket):
    if(string[:3] == '354'):
        return True
    return error500(string, clientSocket)

#   After confirming in sendingMessages that the user has input correct MAIL FROM and RCPT TO addresses, this function sends it to the server


def sendingDataMessages(userMessageInput, clientSocket):
    toString = "From: <" + userMessageInput[0] + ">\n"
    try:
        clientSocket.send(toString.encode())
    except OSError:
        print("ERROR sending From: message")
        return False

    createFromString = "To: "
    i = 0
    while i < len(userMessageInput[1]):
        if(i == len(userMessageInput[1])-1):
            createFromString = createFromString + \
                "<"+userMessageInput[1][i]+">\n"
        else:
            createFromString = createFromString + \
                "<"+userMessageInput[1][i]+">, "
        i += 1
    try:
        clientSocket.send(createFromString.encode())
    except OSError:
        print("ERROR sending To: message")
        return False

    subjectString = "Subject: " + userMessageInput[2]+"\n"
    try:
        clientSocket.send(subjectString.encode())
    except OSError:
        print("ERROR sending subject message")
        return False

    for entry in userMessageInput[3]:
        time.sleep(.005)
        try:
            clientSocket.send(entry.encode())
        except OSError:
            print("ERROR sending part of data message")
            return False
    try:
        okResponse = clientSocket.recv(1024).decode()
    except OSError:
        print("ERROR recv OK response")
        return False

    okResponse = ok250Parse(okResponse, clientSocket)
    if okResponse != True:
        print("ERROR with ok250 response")
        return False

    quitString = "QUIT\n"
    try:
        clientSocket.send(quitString.encode())
    except OSError:
        print("ERROR sending QUIT message")
        return False

    return True

#   After user input and handshake, client begins to send messages to server in SMTP format (after done with SMTP protocol then calls sendingDataMessages)


def sendingMessages(userMessageInput, clientSocket):
    sendingMessages = True
    while sendingMessages:
        MAIL_FROM = "MAIL FROM: <" + userMessageInput[0] + ">\n"
        try:
            clientSocket.send(MAIL_FROM.encode())
        except OSError:
            print("ERROR sending MAIL FROM: message")
            return False

        try:
            okResponse = clientSocket.recv(1024).decode()
        except OSError:
            print("ERROR recv OK response")
            return False
        okResponse = ok250Parse(okResponse, clientSocket)
        if okResponse != True:
            print("ERROR 250 not received after MAIL FROM")
            return False
        for entry in userMessageInput[1]:
            RCPT_TO = "RCPT TO: <" + entry + ">\n"
            try:
                clientSocket.send(RCPT_TO.encode())
            except OSError:
                print("ERROR sending RCPT TO: message")
                return False

            try:
                okResponse = clientSocket.recv(1024).decode()
            except OSError:
                print("ERROR recv OK response")
                return False

            okResponse = ok250Parse(okResponse, clientSocket)
            if okResponse != True:
                print("ERROR 250 not received after RCPT TO")
                return False
        DATA = "DATA\n"
        try:
            clientSocket.send(DATA.encode())
        except OSError:
            print("ERROR sending DATA message")
            return False

        try:
            send354 = clientSocket.recv(1024).decode()
        except OSError:
            print("ERROR recv 354 message")
            return False

        send354 = send354Parse(send354, clientSocket)
        if send354 != True:
            print("ERROR 354 not received after DATA")
            return False
        sendingDataMessages(userMessageInput, clientSocket)

        sendingMessages = False
    return True

#   After user input, does handshake then calls sendingMessages function that sends the user's unput


def acceptingMessages(userMessageInput, serverName, serverPort):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
    except OSError:
        print("ERROR creating socket")
        return False
    try:
        clientSocket.connect((serverName, serverPort))
    except OSError:
        print("ERROR connecting socket")
        return False
    # Gets 220 message from server and parses
    try:
        greeting = clientSocket.recv(1024).decode()
    except OSError:
        print("ERROR recv 220 message")
        return False

    test = greetingParse(greeting, clientSocket)
    if not(test):
        print("ERROR 220 message incorrect")
        return False
    heloMessage = "HELO comp431fa20b.cs.unc.edu\n"
    try:
        clientSocket.send(heloMessage.encode())
    except OSError:
        print("ERROR sending HELO message")
        return False
    # Gets 250 message from server and parses
    try:
        ok250 = clientSocket.recv(1024).decode()
    except OSError:
        print("ERROR recv 250 message")
        return False
    test = ok250Parse(ok250, clientSocket)
    if not(test):
        print("ERROR 250 message incorrect")
        return False
    sendingMessages(userMessageInput, clientSocket)
    try:
        clientSocket.close()
    except OSError:
        print("ERROR closing socket")
        return False
    return True


def main():
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
    createMessages(serverName, serverPort)


main()
