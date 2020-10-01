Server side of the SMTP is now finished and this is now the working client side. My program reads a forward-file (having the format of the file I created in Homework 2) and generates and writes to standard output the SMTP messages necessary to send the contents of the mail messages in the forward-file to a destination SMTP server. My program both generates SMTP server messages and listens for the SMTP response messages that a real server would emit in response to receiving my messages.

#This part of the SMTP server is finished and fully functional.

-----Grammar-----

<response-code_> ::= <resp-number_> <whitespace_> <arbitrary-text_> <CRLF_>

<resp_number_> ::= “250” | “354” | “500” | “501”

<arbitrary-text_> ::= any sequence of printable characters

(Some of the grammar tokens are not the same as the comments in the code. This is because github is hiding the token names inside the <>. That is also why there are extra '_'.)
