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
rcpts = []
mailboxs = []
datas = []
#   Called to print out incorrect input before returning and showing ERROR -- token


def echo(string):
    if(string[0] == '\n'):
        print("")
        return False
    counter = 0
    copy = string
    while(CRLF(string) == False):
        string = string[1:]
        counter += 1
    print(copy[0:counter])
    string = string[2:]
    if(len(string) < 1):
        return True
    return string

#############################################################
##############            MAIL FROM            ##############
#############################################################


def mail_from_cmd(string):
    echo(string)
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
    echo(string)
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
    restOfString = echo(string)
    copy = string
    counter = 0
    if(string[0] == '.'):
        if(CRLF(string[1:])):
            return -2
    while(CRLF(copy) == False):
        copy = copy[1:]
        counter += 1
    datas.append(string[:counter] + '\n')
    if(restOfString == False or restOfString == True):
        return -1
    return data(restOfString)

#   Makes sure the 'DATA' command has been typed correctly


def check_data(string):
    # echo(string)
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


#   Selects the correct command to call and throws error if needed


def call_command(string, count):
    passCommand = False
    #   DATA (store input, then write)
    if(count == -1):
        copy = data(string)
        if(copy == -2):
            return writeData()
        return copy
    #   MAIL FROM:
    elif(check_mail_from(string) != False):
        if(count != 0):
            return error503(string)
        passCommand = mail_from_cmd(string)
        if(passCommand != False):
            mailboxs.append(from_(string))
            if(passCommand != True):
                count = ok250(count)
                return call_command(passCommand, count)
            return ok250(count)
        return error501(string)
    #   RCPT TO:
    elif(check_rcpt_to(string) != False):
        if(count < 1):
            return error503(string)
        passCommand = rcpt_to(string)
        if(passCommand != False):
            rcpts.append(getMailbox(string))
            mailboxs.append(to(string))
            if(passCommand != True):
                count = ok250(count)
                return call_command(passCommand, count)
            return ok250(count)
        return error501(string)
    #   DATA
    elif(check_data(string) != False):
        passCommand = check_data(string)
        if(count < 2):
            return error503(string)
        echo(string)
        print("354 Start mail input; end with <CRLF>.<CRLF>")
        count = -1
        if(passCommand != True):
            return call_command(passCommand, count)
        return count
    #   Unrecognized command
    else:
        return error500(string)

#   After full correct input, we will write all From, To and Data messages
#       to all RCPT TO: files


def writeData():
    for r in rcpts:
        f = open("forward/"+r, "a+")
        for m in mailboxs:
            f.write(m+'\n')
        for d in datas:
            f.write(d)
        f.close()
    ok250(0)
    return 0

#   500 Syntax error


def error500(string):
    echo(string)
    print("500 Syntax error: command unrecognized")
    return False

#   501 Syntax error


def error501(string):
    print("501 Syntax error in parameters or arguments")
    return False

#   503 Bad sequence


def error503(string):
    echo(string)
    print("503 Bad sequence of commands")
    return False

#   250 OK


def ok250(count):
    print("250 OK")
    count += 1
    return count


def main():
    count = 0
    #  Get line of input from terminal and check in mail_from_cmd
    for line in sys.stdin:
        count = call_command(line, count)
        if(not(count)):  # False = start over from MAIL FROM command
            datas.clear()
            mailboxs.clear()
            rcpts.clear()
            count = 0
    if(count != 0):
        error501("Incomplete data input")


main()
