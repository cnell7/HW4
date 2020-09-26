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
    clientSocket.send(message.encode())
    count += 1
    return count

#   Gets a list of RCPTs from user via command line (called in createMessage) and makes sure they follow protocol


def getRCPTS():
    searching = True
    rcptTo = []
    rcpt = sys.stdin.readline()
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

#   Gets data from user via command line (called in createMessage)


def getData():
    readingData = True
    datas = []
    while readingData:
        msg = sys.stdin.readline()
        if(msg == ".\n"):
            return datas
        datas.append(msg)
    return False

#   Gets user input from command line to create mail message send over TCP socket


def createMessage():
    mailFrom = False
    rcptTo = False
    while(mailFrom == False):
        print("From:")
        mailFrom = sys.stdin.readline()
        mailFrom = reverse_path(mailFrom)
    while(rcptTo == False):
        print("To:")
        rcptTo = getRCPTS()

    print("Subject:")
    subjectMessage = sys.stdin.readline()
    print("Message:")
    data = getData()
    return [mailFrom, rcptTo, subjectMessage, data]

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
    toString = "To: <" + userMessageInput[0] + ">\n"
    clientSocket.send(toString.encode())

    createFromString = "From: "
    i = 0
    while i < len(userMessageInput[1]):
        if(i == len(userMessageInput[1])-1):
            createFromString = createFromString + \
                "<"+userMessageInput[1][i]+">\n"
        else:
            createFromString = createFromString + \
                "<"+userMessageInput[1][i]+">, "
        i += 1
    clientSocket.send(createFromString.encode())

    subjectString = "Subject: " + userMessageInput[2]+"\n"
    clientSocket.send(subjectString.encode())

    for entry in userMessageInput[3]:
        clientSocket.send(entry.encode())

    quitString = "QUIT\n"
    clientSocket.send(quitString.encode())
    return True

#   After user input and handshake, client begins to send messages to server in SMTP format (after done with SMTP protocol then calls sendingDataMessages)


def sendingMessages(userMessageInput, clientSocket):
    sendingMessages = True
    while sendingMessages:
        MAIL_FROM = "MAIL FROM: <" + userMessageInput[0] + ">\n"
        clientSocket.send(MAIL_FROM.encode())
        okResponse = clientSocket.recv(1024).decode()
        okResponse = ok250Parse(okResponse, clientSocket)
        if okResponse != True:
            return False
        for entry in userMessageInput[1]:
            RCPT_TO = "RCPT TO: <" + entry + ">\n"
            clientSocket.send(RCPT_TO.encode())
            okResponse = clientSocket.recv(1024).decode()
            okResponse = ok250Parse(okResponse, clientSocket)
            if okResponse != True:
                return False
        DATA = "DATA\n"
        clientSocket.send(DATA.encode())
        send354 = clientSocket.recv(1024).decode()
        send354 = send354Parse(send354, clientSocket)
        if send354 != True:
            return False
        sendingDataMessages(userMessageInput, clientSocket)

        sendingMessages = False
    return True

#   After user input, does handshake then calls sendingMessages function that sends the user's unput


def acceptingMessages(serverName, serverPort):
    userMessageInput = createMessage()
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    test = False
    while not(test):  # Gets 220 message from server and parses
        greeting = clientSocket.recv(1024).decode()
        print(greeting)
        test = greetingParse(greeting, clientSocket)
    heloMessage = "HELO comp431fa20b.cs.unc.edu\n"
    clientSocket.send(heloMessage.encode())
    print(heloMessage)
    test = False
    while not(test):  # Gets 250 message from server and parses
        ok250 = clientSocket.recv(1024).decode()
        print(ok250)
        test = ok250Parse(ok250, clientSocket)
    sendingMessages(userMessageInput, clientSocket)
    clientSocket.close()
    return True


def main():
    state = 0
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
    acceptingMessages(serverName, serverPort)


main()
