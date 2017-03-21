#client file, run on classsroom.cs.edu

import socket
import sys
import string
import os

def pathParser(s, l):  



          ##########################  beginning SMTP protocol input parsing #################################

  if s[0]==' ' or s[0]=='@' or s[0]=='<' or s[0]=='>' or s[0]=='(' or s[0]==')' or s[0]=='[' or s[0]==']' or s[0]=='\\' or s[0]=='.' or s[0]==',' or s[0]==';' or s[0]==':' or s[0]=='\"':      
    errorSmtpSyntax()
    return 0          



#check the mailbox

  atCheck = s.find('@')   
  if atCheck == -1:     #locates the @ char, and makes sure it's not missing.
    errorSmtpSyntax()
    return 0

  localpartChecker = list(s) 

  for i in localpartChecker:    #Makes sure mailbox is not a special char or a space
    if i == '@':
      break
    if i==' ' or i=='<' or i=='>' or i=='(' or i==')' or i=='[' or i==']' or i=='\\' or i=='.' or i==',' or i==';' or i==':' or i=='\"':
      errorSmtpSyntax()
      return 0
      break

#check the domain

  preAt, postAtStr = s.split('@', 1)    #postAtStr string is everything after the '@' character.

  if postAtStr[0] not in string.ascii_letters:    #Checks very first domain char
    errorSmtpSyntax()
    return 0


  postAtL = list(postAtStr)       #postAtL is the list version of postAtStr
  for j in range( 0, len(postAtL) ):
    if postAtL[j] == '>' or postAtL[j] == ' ':
      break
    if (postAtL[j-1] == '.') and postAtL[j] not in string.ascii_letters:    #Checks the char directly after any '.'
      errorSmtpSyntax()
      return 0
      break


#check the final part of the path

  if ' ' in s:
    prePathClose, postPath = s.split(' ', 1)    #postPaths is everything after the '>' character.
    postPathL = list(postPath)
 
    for b in postPathL:
      if b != '\r' and b != '\n' and b != '\t' and b != ' ':
        errorSmtpSyntax()
        return 0    

          #################################  ENDof SMTP protocol input parsing #################################

  return 1








          ##########################  beginning small helper methods #################################

def errorSmtpSyntax(): 
  print 'Syntax error...your input does not conform to SMTP protocol.  Try again.'
  return

def endOfTxtChecker(s):
  if s == '.\n':
    return 1
  return 0

def responseHandler250(s):
  if s[:3] != '250':
    print 'message from server does not conform to SMTP protocol; 250 was expected.  connection will be closed.'
    return 1

def responseHandler354(s):
  if s[:3] != '354':
    print'message from server does not conform to SMTP protocol; 354 was expected.  connection will be closed.'
    return 1

          ##########################  END small helper methods #################################









def main():

#accepts the hostname of the server 
#(snapper, for testing purposes)
  hostName = sys.argv[1]

#accepts the port # (should be same as parameter for server program)
#(16468, for testing purposes)
  portNum = int( sys.argv[2] )
    
  try:
    while 1:                
 
#prepare variables     
      paths = []
      stateCheckerMF = 0
      stateCheckerRC = 0  
      stillTakingText = 1


      while stateCheckerMF == 0:        #MAIL FROM parse:

        print 'From:'

        inVarMF = raw_input()    
        inListMF = list(inVarMF)


        if pathParser(inVarMF, inListMF) == 1:
          stateCheckerMF = 1

#accept input: RCPT TO

      while stateCheckerRC == 0:
        print 'To:'
        
        rcptPaths = []

        inVarRC = raw_input()     

        initialRcptPaths = inVarRC.split(',')

        numberOfRcptPaths = len(initialRcptPaths)
        numberOfCorrectRcptPaths = 0

        for o in initialRcptPaths:
          while(1):
            if o[0] == ' ':
              o = o.replace(' ', '', 1)
            elif o[0] == '\t':
              o = o.replace('\t', '', 1)
            else:
              break
          # o = o.replace(' ', '')
          # o = o.replace('\t', '')
          inListRC = list(o)
          if pathParser(o, inListRC) == 1:
            rcptPaths.append(o)
            numberOfCorrectRcptPaths += 1
        if numberOfCorrectRcptPaths == numberOfRcptPaths:
          stateCheckerRC = 1


      print 'so now the list of paths is:'
      print rcptPaths

#accept input: subject
      print 'Subject:'
      inVarSubject = raw_input()

#accept input: message body
      print 'Message:'

      allText = ''

      while stillTakingText == 1:   #text input loop:
            
        inVarTxt = raw_input() + '\n' 

        if endOfTxtChecker(inVarTxt) == 0:
          allText += inVarTxt

        if endOfTxtChecker(inVarTxt) == 1:
          stillTakingText = 0


#prepare variables to send through the socket

  #handshaking variables
      hostNameOfClient = socket.gethostname()
      heloMssg = 'HELO ' + hostNameOfClient + '\n' #...I tHINK need to change this later on but will leave it for now.

  #header variables
      fromAddressForHeader = 'MAIL FROM: ' + '<' + inVarMF + '>' + '\n'

      rcptAddressesForHeader = []
      for j in rcptPaths:
        j = 'RCPT TO: ' + '<' + j + '>'
        rcptAddressesForHeader.append(j)

      data = 'DATA'

  #body variables
      fromAddressForBody = 'From: ' + '<' + inVarMF + '>' + '\n'
      rcptAddressesForBody = rcptPaths[:]
      allRcpts = ''
      for k in rcptAddressesForBody:
        k = 'To: ' + '<' + k + '>' + '\n'
        allRcpts  = allRcpts + k
      subjectLine = 'Subject: ' + inVarSubject + '\n\n'
      mssgBody = fromAddressForBody + allRcpts + subjectLine + allText

      quit = 'QUIT\n'

#create the client socket, connect to the server
      clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
      clientSock.connect( (hostName, portNum) )  

#handshaking
      greetingMssg = clientSock.recv(1024)   #recieve the greeting message from server
#      print greetingMssg.decode()  #this is for testing
      clientSock.send( heloMssg.encode() ) #send the initial HELO message
      heloResponse = clientSock.recv(1024)  #recieve the HELO response message
#      print heloResponse #this is for testing



#send the header of the email through the socket
  #FROM part
      clientSock.send( fromAddressForHeader.encode() )
      response1 = clientSock.recv(1024)
  #error handling
      if responseHandler250( response1.decode() ) == True:
        clientSock.close()
        sys.exit()
      print 'done sending from addresses'


  #RCPT part
      for i in rcptAddressesForHeader:
        clientSock.send( i.encode() )
        response2 = clientSock.recv(1024)
  #error handling
        if responseHandler250( response2.decode() ) == True and responseHandler354( response3.decode() ) == True:
          clientSock.close()
          sys.exit()
  #354 recieved, need to start in on data part
        if responseHandler250( response2.decode() ) == True and responseHandler354( response3.decode() ) == False:
          break
         
      print 'done sending rcpt addresses'


      clientSock.send( data.encode() )
      print 'data command sent'
      response3 = clientSock.recv(1024)
  #error handling
      if responseHandler354( response3.decode() ) == True:
        clientSock.close()
        sys.exit()

      print '354 recieved'

        


#send the body of the email through the socket
      clientSock.send( mssgBody.encode() )
      print 'message body sent'

      response4 = clientSock.recv(1024)
      print '250 from mesage body recieved'

  #error handling
      if responseHandler250( response4.decode() ) == True:
        clientSock.close()
        sys.exit()


      clientSock.send( quit.encode() )
      print 'quit sent'

#job is done.  Close socket and exit program.
      clientSock.close()
      print 'connection closed'
      sys.exit()

  except EOFError:
    sys.exit()



if __name__ == '__main__':
    main()


