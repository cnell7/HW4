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


def getData():
    readingData = True
    datas = []
    while readingData:
        msg = sys.stdin.readline()
        if(msg == ".\n"):
            return datas
        datas.append(msg)
    return False


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


def greetingParse(string):
    if(string[:3] == '220'):
        return True
    return False


def ok250Parse(string):
    if(string[:3] == '250'):
        return True
    return False


def acceptingMessages(clientSocket):
    sendingMessages = True
    greeting = clientSocket.recv(1024).decode
    if(not(greetingParse(greeting))):
        return False
    heloMessage = "HELO comp431fa20b.cs.unc.edu"
    clientSocket.send(heloMessage.encode())
    ok250 = clientSocket.recv(1024).decode()
    if(not(ok250Parse(ok250))):
        return False
    while sendingMessages:
        return True


def main():
    state = 0
    serverName = sys.argv[1]
    serverPort = sys.argv[2]
    userMessageInput = createMessage()

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    acceptingMessages(clientSocket)
    clientSocket.close()

    '''
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
    '''


main()
