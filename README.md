Fully functional SMTP mail server using grammar provided from HW1-HW4 as well as what is defined below. An example of the three way handshake added this HW is shown right under this text.

220 Greeting :== 220 Random “greeting” text that includes the name of the server
HELO: == HELO <whitespace> <domain> <nullspace> <CRLF>
250 Response :== 250 Hello comp431fa20b.cs.unc.edu pleased to meet you


From Input :== From: reverse-path (with angle brackets)
To Input :== To: list of one or more forward paths (each with angle brackets)
Subject Input :== Subject: Text of the subject line formatted exactly as typed in by the user

Message Input: == Text of the message formatted exactly as typed in by the user.

Closing connection :==221 <server hostname> closing connection
  
  
Example:) Client running program on terminal == python ./Client.py comp431fa20.cs.unc.edu 17326
From:
jeffay@cs.unc.edu
To:
comp431TAs@cs.unc.edu
Subject:
How the heck are we going to grade HW4?!
Message:
TAs – How are we going to grade HW4? It’s going to require executing two programs for each
student on two separate machines and this is going to be difficult to automate!
.

(This is not shown to standard out, these messages are sent to the Server.py program via socket after 3-way handshake)
MAIL FROM: <jeffay@cs.unc.edu>
RCPT TO: <comp431TAs@cs.unc.edu>
RCPT TO: <kmp@unc.edu>
DATA
From: <jeffay@cs.unc.edu>
To: <comp431TAs@cs.unc.edu>, <kmp@unc.edu>
Subject: Test message
This is a test.
.
QUIT

(This is not shown to standard out, these messages are sent to the Client.py program via socket after-3 way handshake)
250 Ok
250 Ok
250 Ok
354 Data ready end with './.'
221 comp431fa20.cs.unc.edu closing connection
