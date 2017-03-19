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


def error501(): 
  print 'Syntax error in parameters or arguments'
  return


def endOfTxtChecker(s):

  if s == '.\n':
    return 1

  return 0

def responseHandler250(s):
#split the string at the first space
  sList = s.split()

#check if an acceptable response was returned
  if sList[0] != '250':
    print("message from client does not conform to SMTP protocol.  connection closed.")
    return 1

def responseHandler354(s):
#split the string at the first space
  sList = s.split()

#check if an acceptable response was returned
  if sList[0] != '354':
    print("message from client does not conform to SMTP protocol.  connection closed.")
    return 1

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

        inVarMF = raw_input() + '\n'    
        inListMF = list(inVarMF)


        if pathParser(inVarMF, inListMF) == 1:
          stateCheckerMF = 1


        print 'To:'

        inVarRC = raw_input() + '\n'     

        rcptPaths = inVarRC.split(',')

#        inListRC = list(inVarRC)

        for o in rcptPaths:
          o = o.strip()
          inListRC = list(o)
          pathParser(o, inListRC)    #needa add functionality for multiple recipients

        print rcptPaths


      print 'Subject:'
      inVarSubject = raw_input() + '\n'

      print 'Message:'

      allText = ''

      while stillTakingText == 1:   #text input loop:
            
        inVarTxt = raw_input() + '\n'  


        if endOfTxtChecker(inVarTxt) == 0:
          allText += inVarTxt

        if endOfTxtChecker(inVarTxt) == 1:
          stillTakingText = 0


      startMF = inVarMF.find('<', 1) + 1
      endMF = inVarMF.find('>', 1)


#prepare variables to send through the socket
      heloMssg = 'HELO/n' #...I tHINK need to change this later on but will leave it for now.
      fromAddressForHeader = 'MAIL FROM: ' + '<' + inVarMF + '>' + '\n'
      rcptAddressesForHeader = rcptPaths[:]
      for j in rcptAddressesForHeader:
        j = 'RCPT TO: ' + '<' + j + '>' + '\n'
      data = 'DATA'
      fromAddressForLaterInHeader = 'From: ' + '<' + inVarMF + '>' + '\n'
      rcptAddressesForLaterInHeader = rcptPaths[:]
      for k in rcptAddressesForLaterInHeader:
        k = 'To: ' + '<' + k + '>' + '\n'
      subjectLine = 'Subject: ' + inVarSubject + '\n'
      quit = 'QUIT'


#create the client socket, connect to the server
      clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
      clientSock.connect( (hostName, portNum) )  

#handshaking
      greetingMssg = clientSock.recv(1024)   #recieve the greeting message from server
      print greetingMssg.decode()  #this is for testing
      clientSock.send( heloMssg.encode() ) #send the initial HELO message
      heloResponse = clientSock.recv(1024)  #recieve the HELO response message
      print heloResponse #this is for testing

#send the header of the email through the socket
      clientSock.send( fromAddressForHeader.encode() )
      response1 = clientSock.recv(1024)
      if responseHandler250(response1) == true:
        clientSock.close()
        continue

      for i in rcptAddressesForHeader:
        clientSock.send( i.encode() )
        response2 = clientSock.recv(1024)
        if responseHandler250(response2) == true:
          clientSock.close()
          break        #I need a double continue here, somehow....

      clientSock.send( data.encode() )
      if responseHandler354(response1) == true:
        clientSock.close()
        continue

      clientSock.send( '\n'.encode() )

#send the body of the email through the socket
      clientSock.send( fromAddressForLaterInHeader.encode() )
      for y in rcptAddressesForLaterInHeader:
        clientSock.send( y.encode() )
      clientSock.send( subjectLine.encode() )
      clientSock.send( allText.encode() )
      clientSock.send( quit.encode() )




      clientSock.close()

  except EOFError:
    sys.exit()



if __name__ == '__main__':
    main()


