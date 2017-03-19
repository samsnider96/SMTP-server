#client file, run on classsroom.cs.edu

import socket
import sys
import string
import os

def pathParser(s, l):  



          ##########################  Beginning of local-part #################################

  if s[0]==' ' or s[0]=='@' or s[0]=='<' or s[0]=='>' or s[0]=='(' or s[0]==')' or s[0]=='[' or s[0]==']' or s[0]=='\\' or s[0]=='.' or s[0]==',' or s[0]==';' or s[0]==':' or s[0]=='\"':      
    error501()
    return 0          



          #################################  mailbox #################################
  

  atCheck = s.find('@')   
  if atCheck == -1:     #locates the @ char, and makes sure it's not missing.
    print '1'
    error501()
    return 0

  localpartChecker = list(s) 

  for i in localpartChecker:    #Makes sure mailbox is not a special char or a space
    if i == '@':
      break
    if i==' ' or i=='<' or i=='>' or i=='(' or i==')' or i=='[' or i==']' or i=='\\' or i=='.' or i==',' or i==';' or i==':' or i=='\"':
      print '2'
      error501()
      return 0
      break

          #################################  domain #################################

  preAt, postAtStr = s.split('@', 1)    #postAtStr string is everything after the '@' character.

  if postAtStr[0] not in string.ascii_letters:    #Checks very first domain char
    print '3'
    error501()
    return 0


  postAtL = list(postAtStr)       #postAtL is the list version of postAtStr
  for j in range( 0, len(postAtL) ):
    if postAtL[j] == '>' or postAtL[j] == ' ':
      break
    if (postAtL[j-1] == '.') and postAtL[j] not in string.ascii_letters:    #Checks the char directly after any '.'
      print '4'
      error501()
      return 0
      break
#    if postAtL[j].isdigit() == 0 and postAtL[j] != '.' and postAtL[j] not in string.ascii_letters:  #checks whole domain for wierd chars
 #     print '4.5'
#      error501()
 #     return 0
 #     break


          #################################  final part of "path" #################################

  if ' ' in s:
    prePathClose, postPath = s.split(' ', 1)    #postPaths is everything after the '>' character.
    postPathL = list(postPath)
 
    for b in postPathL:
      if b != '\r' and b != '\n' and b != '\t' and b != ' ':
        print '5'
        error501()
        return 0    

          #################################  End of RCPT-TO parsing #################################

  return 1

def error500(): 
  print 'Syntax error: command unrecognized'
  return

def error501(): 
  print 'Syntax error in parameters or arguments'
  return

def error503(): 
  print 'Bad sequence of commands'
  return

def endOfTxtChecker(s):

  if s == '.\r':
    return 1

  return 0

#def greeetingMssgChecker(s): #checks if the greeting message is legit


# def socketConnector(h, p): #arguments: host name and port numberd

#   heloMssg = 'HELO\r' #...I tHINK need to change this later on but will leave it for now.

#   clientSock = socket(AF_INET, SOCK_STREAM)  #create the socket

#   clientSock.connect( (h,p) )         #connect to the server
#   greetingMssg = clientSock.recv(1024)   #recieve the greeting message

#   clientSock.send( heloMssg.encode() )
#   clientsock.recv(1024)  #recieve the hello response message
#   clientSock.close()



def main():

#accepts the hostname of the server 
#(snapper, for testing purposes)
  hostName = sys.argv[1]

#accepts the port # (should be same as parameter for server program)
#(16468, for testing purposes)
  portNum = int( sys.argv[2] )
    
  try:
    while 1:                #accept input, parse it, and provide output in a loop.
      
      paths = []
      rcptPaths = []

                              #set state machine variables:
      stateCheckerMF = 0
      stateCheckerRC = 0
      oneOrMoreRC = 0  #checks if there's been one or more valid RCPT TO commands
      stillTakingText = 1


      while stateCheckerMF == 0:        #MAIL FROM parse:

        print 'From:'

        inVarMF = raw_input() + '\r'    
        inListMF = list(inVarMF)


        if pathParser(inVarMF, inListMF) == 1:
          stateCheckerMF = 1


        print 'To:'

        inVarRC = raw_input() + '\r'     

        rcptPaths = inVarRC.split(',')

#        inListRC = list(inVarRC)

        for o in rcptPaths:
          o = o.strip()
          inListRC = list(o)
          pathParser(o, inListRC)    #needa add functionality for multiple recipients

        print rcptPaths


      print 'Subject:'
      inVarSubject = raw_input() + '\r'

      print 'Message:'

      allText = ''

      while stillTakingText == 1:   #text input loop:
            
        inVarTxt = raw_input() + '\r'  


        if endOfTxtChecker(inVarTxt) == 0:
          allText += inVarTxt

        if endOfTxtChecker(inVarTxt) == 1:
          stillTakingText = 0


      startMF = inVarMF.find('<', 1) + 1
      endMF = inVarMF.find('>', 1)


#prepare variables to send through the socket
      heloMssg = 'HELO\r' #...I tHINK need to change this later on but will leave it for now.
      fromAddressForHeader = 'MAIL FROM: ' + '<' + inVarMF + '>' + '\r'
      rcptAddressesForHeader = rcptPaths[:]
      for j in rcptAddressesForHeader:
        j = 'RCPT TO: ' + '<' + j + '>' + '\r'
      data = 'DATA'
      fromAddressForLaterInHeader = 'From: ' + '<' + inVarMF + '>' + '\r'
      rcptAddressesForLaterInHeader = rcptPaths[:]
      for k in rcptAddressesForLaterInHeader:
        k = 'To: ' + '<' + k + '>' + '\r'
      subjectLine = 'Subject: ' + inVarSubject + '\r\r'
      quit = 'QUIT'


#create the client socket, connect to the server
      clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
      clientSock.connect( (hostName, portNum) )  

#handshaking
      greetingMssg = clientSock.recv(1024)   #recieve the greeting message from server
      clientSock.send( heloMssg.encode() ) #send the initial HELO message
      clientsock.recv(1024)  #recieve the HELO response message

#send the email through the socket
      clientSock.send( fromAddressForHeader.edncode() )
      for i in rcptPathsForHeader:
        clientSock.send( i.encode() )
      clientSock.send( data.encode() )
      clientSock.send( fromAddressForLaterInHeader.encode() )
      for y in rcptPathsForLaterInHeader:
        clientSock.send( y.encode() )
      clientSock.send( subjectLine.encode() )
      clientSock.send( allText.encode() )
      clientSock.send( quit.encode() )




      clientSock.close()

  except EOFError:
    sys.exit()



if __name__ == '__main__':
    main()


