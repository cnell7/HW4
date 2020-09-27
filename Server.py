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
rcpts = []
mailboxs = []
datas = []

#############################################################
##############            MAIL FROM            ##############
#############################################################


def mail_from_cmd(string):
    #   checks MAIL FROM: command
    string = check_mail_from(string)
    #    <nullspace>
    string = nullspace(string)
    #   <reverse-path>
    string = reverse_path(string)
    if(not(string)):
        return False
    #    <nullspace>
    string = nullspace(string)
    if(not(string)):
        return False
    #   <CLRF>
    return CRLF(string)


def check_mail_from(string):
    mailString = "MAIL"
    fromString = "FROM:"
    # MAIL
    mail = string[0:4]
    if(not(mailString == mail)):
        return False
    string = string[4:]
    #    <whitespace>
    if(SP(string) == False):
        return False
    string = whitespace(string)
    #   "FROM:"
    if(not(fromString == string[0:5])):
        return False
    string = string[5:]
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


def reverse_path(string):
    #  <path>
    return path(string)


def path(string):
    # "<"
    if(string[0] != '<'):
        return False
    #  <mailbox>
    string = mailbox(string[1:])
    if(string == False):
        return False
    #  ">"
    if(string[0] != '>'):
        return False
    return string[1:]


def mailbox(string):
    #  <local-part>
    copy = string
    string = local_part(string)
    if(string == False or (copy[0] == string[0])):
        return False
    #  "@"
    if(string[0] != '@'):
        return False
    #  <domain>
    string = domain(string[1:])
    if(string == False):
        return False
    return string


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
    elif():
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


#############################################################
##############            RCPT TO              ##############
#############################################################

#   Makes sure the RCPT TO: syntax is all corect
def rcpt_to(string):
    #   checks RCPT TO: command
    string = check_rcpt_to(string)
    #   <nullspace>
    string = nullspace(string)
    #   <forward-path>
    string = forward_path(string)
    if(not(string)):
        return False
    #   <nullspace>
    string = nullspace(string)
    #   <CRLF>
    return CRLF(string)

#   Makes sure the 'RCPT TO:' command has been typed correctly


def check_rcpt_to(string):
    rcptString = "RCPT"
    toString = "TO:"
    #   "RCPT"
    if(not(rcptString == string[0:4])):
        return False
    string = string[4:]
    #    <whitespace>
    if(SP(string) == False):
        return False
    string = whitespace(string)
    #   "TO:"
    if(not(toString == string[0:3])):
        return False
    string = string[3:]
    return string


def forward_path(string):
    return path(string)

#############################################################
##############              DATA               ##############
#############################################################


#   Takes line of input and appends to list of RCPT TO: files
def data(string):
    if(string == ".\n"):
        return -2
    datas.append(string)
    return -1


#   Makes sure the 'DATA' command has been typed correctly


def check_data(string):
    if(string[0:4] != "DATA"):
        return False
    string = string[4:]
    #   <nullspace>
    string = nullspace(string)
    #   <CRLF>
    return CRLF(string)


#   Gets the mailbox of the RCPT TO: to make a file name
def getMailbox(string):
    count = 0
    while(string[count] != '<'):
        count += 1
    count += 1
    string = string[count:]
    count = 0
    while(string[count] != '>'):
        count += 1
    return string[:count]

#   Makes a "From: " string ending in the mailbox


def from_(string):
    return "From: <" + getMailbox(string) + ">"

#   Makes a "To: " string ending in the mailbox


def to(string):
    return "To: <" + getMailbox(string) + ">"


#   Gets the domain of an address so that it can be used to create a file in the forward directory (called by writeData)


def getDomain(string):
    position = 0
    while string[position] != '@':
        position += 1
    return string[position+1:]


#   After full correct input, we will write all From, To and Data messages
#       to all RCPT TO: files


def writeData(connectionSocket):
    already = []
    for entry in rcpts:
        fileName = getDomain(entry)
        if not(fileName in already):
            already.append(fileName)
    for r in already:
        f = open("forward/"+r, "a+")
        for d in datas:
            f.write(d)
        f.close()
    ok250(0, connectionSocket)
    return 0

#   500 Syntax error


def error500(string, connectionSocket):
    message = "500 Syntax error: command unrecognized"
    connectionSocket.send(message.encode())
    return False

#   501 Syntax error


def error501(string, connectionSocket):
    message = "501 Syntax error in parameters or arguments"
    connectionSocket.send(message.encode())
    return False

#   503 Bad sequence


def error503(string, connectionSocket):
    message = "503 Bad sequence of commands"
    connectionSocket.send(message.encode())
    return False

#   250 OK


def ok250(count, connectionSocket):
    message = "250 OK"
    try:
        connectionSocket.send(message.encode())
    except OSError:
        print("ERROR sending OK message")
        return False
    count += 1
    return count


#   HELO message parse


def heloParse(string, connectionSocket):
    #   HELO <whitespace> <domain> <nullspace> <CRLF>
    iString = string
    if(not(string[:4] == 'HELO')):
        return error500(iString, connectionSocket)
    string = string[4:]
    copy = string
    string = whitespace(string)
    if(copy[0] == string[0]):
        return error501(iString, connectionSocket)
    findDomain = string
    string = domain(string)
    if(not(string)):
        return error501(iString, connectionSocket)
    findDomain = findDomain[:len(findDomain)-len(string)]
    string = nullspace(string)
    string = CRLF(string)
    if(not(string)):
        return error501(iString, connectionSocket)
    return findDomain


def quitParse(string, connectionSocket):
    #   <QUIT> ::= “QUIT” <nullspace> <CRLF>
    if(not(string[0:4] == 'QUIT')):
        return error500(string, connectionSocket)
    string = string[4:]
    string = nullspace(string)
    string = CRLF(string)
    if(not(string)):
        return error501(string, connectionSocket)
    return True


#   Selects the correct command to call and throws error if needed


def call_command(string, count, connectionSocket):
    passCommand = False
    #   DATA (store input, then write)
    if(count == -1):
        copy = data(string)
        if(copy == -2):
            acceptedString = "250 Message accepted for delivery"
            try:
                connectionSocket.send(acceptedString.encode())
            except OSError:
                print("ERROR sending 250 message")
                return False

            try:
                quit_ = connectionSocket.recv(1024).decode()
            except OSError:
                print("ERROR recv quit message")
                return False

            if(check_mail_from(quit_) != False):
                writeData(connectionSocket)
                return call_command(quit_)
            quit_ = quitParse(quit_, connectionSocket)
            if not(quit_):
                print("ERROR no or incorrect QUIT message")
                return False
            writeData(connectionSocket)
            return "Done"
        return copy
    #   MAIL FROM:
    elif(check_mail_from(string) != False):
        if(count != 0):
            return error503(string, connectionSocket)
        passCommand = mail_from_cmd(string)
        if(passCommand != False):
            mailboxs.append(from_(string))
            if(passCommand != True):
                count = ok250(count, connectionSocket)
                return call_command(passCommand, count, connectionSocket)
            return ok250(count, connectionSocket)
        return error501(string, connectionSocket)
    #   RCPT TO:
    elif(check_rcpt_to(string) != False):
        if(count < 1):
            return error503(string, connectionSocket)
        passCommand = rcpt_to(string)
        if(passCommand != False):
            rcpts.append(getMailbox(string))
            mailboxs.append(to(string))
            if(passCommand != True):
                count = ok250(count, connectionSocket)
                return call_command(passCommand, count, connectionSocket)
            return ok250(count, connectionSocket)
        return error501(string, connectionSocket)
    #   DATA
    elif(check_data(string) != False):
        passCommand = check_data(string)
        if(count < 2):
            return error503(string, connectionSocket)
        mailStart = "354 Start mail input; end with <CRLF>.<CRLF>"
        try:
            connectionSocket.send(mailStart.encode())
        except OSError:
            print("ERROR sending 354 message")
            return False
        count = -1
        if(passCommand != True):
            return call_command(passCommand, count, connectionSocket)
        return count
    #   Unrecognized command
    else:
        return error500(string, connectionSocket)


def acceptingMessages(connectionSocket):
    count = 0
    takingMessages = True
    datas.clear()
    mailboxs.clear()
    rcpts.clear()

    greeting = "220 comp431fa20.cs.unc.edu\n"
    try:
        connectionSocket.send(greeting.encode())
    except OSError:
        print("ERROR sending 220 message")
        return False

    try:
        heloMessage = connectionSocket.recv(1024).decode()
    except OSError:
        print("ERROR recv HELO message")
        return False
    test = heloParse(heloMessage, connectionSocket)
    if not(test):
        print("ERROR HELO message incorrect")
        return False

    heloResponse = "250 Hello" + \
        heloMessage[4:len(heloMessage)-1]+" pleased to meet you\n"
    try:
        connectionSocket.send(heloResponse.encode())
    except OSError:
        print("ERROR sending 250 hello message")
        return False

    while takingMessages:
        try:
            line = connectionSocket.recv(1024).decode()
        except OSError:
            print("ERROR recv state machine message")
            return False

        count = call_command(line, count, connectionSocket)
        if(count == "Done"):
            takingMessages = False
        elif(not(count) or count == 0):  # False = start over from MAIL FROM command
            print("ERROR encountered during SMTP command parse")
            datas.clear()
            mailboxs.clear()
            rcpts.clear()
            count = 0

    if(count != "Done"):
        print("ERROR incomplete data input")
        return error501("Incomplete data input", connectionSocket)

    closeMessage = "221 comp431fa20.cs.unc.edu closing connection\n"
    try:
        connectionSocket.send(closeMessage.encode())
    except OSError:
        print("ERROR sending 221 message")
        return False
    return True


def main():
    #   Make welcome socket and set port number from command line
    try:
        serverPort = int(sys.argv[1])
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(('', serverPort))
        # Server begins listening for incoming TCP requests
        serverSocket.listen(1)
    except OSError:
        print("ERROR creating socket")
        return False
    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
        except OSError:
            print("ERROR accepting socket")
            return False

        acceptingMessages(connectionSocket)

        try:
            connectionSocket.close()  # Close connection to this client
        except OSError:
            print("ERROR accepting socket")
            return False


main()
