#server file, run on snapper.cs.edu

import socket
import sys
import string
import os


def mFParser(s, l):  


        #################################  Beginning of MAIL FROM #############################


  colonCheck = s.find(':', 1)   
  if colonCheck == -1:      #locates the colon string, and makes sure it's not missing.
    return 500

  mailFromStr, rvsPathStr = s.split( s[colonCheck], 1 )   #Splits the input string at the colon.



  mailStr = mailFromStr[:5]     #seperates off the 'mail' str, and checks it  
  if mailStr != 'MAIL ':
    return 500

  fromStr = mailFromStr[-4:]        #seperates off the 'from' str, and checks it
  if fromStr != 'FROM':
    return 500




  afterMailStr = mailFromStr[4:] #creates a string that's everything after 'MAIL'
  blankSpaceL = list(afterMailStr)  #creates a list from the String in previous line

  for x in blankSpaceL: 
    if x == 'F':  
      break
    if x != ' ' and x != '\t':        #this block checks that what's between 'mail' and 'from' is indeed blank space, and not chars.
      return 500
      break

  pathListMF = list(rvsPathStr) 
   
  return pathParser(rvsPathStr, pathListMF) 






def rCParser(s, l):     #Parses the RCPT-TO string.


        #################################  Beginning of RCPT-TO #############################



  colonCheck = s.find(':', 1)   
  if colonCheck == -1:      #locates the colon string, and makes sure it's not missing.
    return 500

  rcptToStr, forwardPathStr = s.split( s[colonCheck], 1 )   #Splits the input string at the colon.


  rcptStr = rcptToStr[:5]     #seperates off the 'RCPT' str, and checks it  
  if rcptStr != 'RCPT ':
    return 500

  toStr = rcptToStr[-2:]        #seperates off the 'TO' str, and checks it
  if toStr != 'TO':
    return 500


  afterRcptStr = rcptToStr[4:] #creates a string that's everything after 'RCPT'
  blankSpaceL2 = list(afterRcptStr)  

  for x in blankSpaceL2: 
    if x == 'T':  
      break
    if x != ' ' and x != '\t':        #this block checks that what's between 'mail' and 'from' is indeed blank space, and not chars.
      return 500
      break

  pathListRc = list(forwardPathStr) 

  return pathParser(forwardPathStr, pathListRc)  











def pathParser(s, l):    #This multipurpose path parser is for use in both MAIL FROM and RCPT TO.


          #################################  Beginning of Path #################################

  pathL = l    

  for y in pathL:
    if y == '<':    #this block checks the first path error
      break
    if y != ' ' and y != '\t':
      return 501
      break




          ##########################  Beginning of local-part #################################

  preBrack, z = s.split('<', 1)  #Makes sure mailbox is not a special char or a space
  if z[0]==' ' or z[0]=='@' or z[0]=='<' or z[0]=='>' or z[0]=='(' or z[0]==')' or z[0]=='[' or z[0]==']' or z[0]=='\\' or z[0]=='.' or z[0]==',' or z[0]==';' or z[0]==':' or z[0]=='\"':      
    return 501         



          #################################  mailbox #################################
  

  atCheck = s.find('@')   
  if atCheck == -1:     #locates the @ char, and makes sure it's not missing.
    return 501

  localpartChecker = list(z)  #Creates a list out of z

  for i in localpartChecker:    #Makes sure mailbox is not a special char or a space
    if i == '@':
      break
    if i==' ' or i=='<' or i=='>' or i=='(' or i==')' or i=='[' or i==']' or i=='\\' or i=='.' or i==',' or i==';' or i==':' or i=='\"':
      return 501
      break

          #################################  domain #################################

  preAt, postAtStr = s.split('@', 1)    #postAtStr string is everything after the '@' character.

  if postAtStr[0] not in string.ascii_letters:    #Checks very first domain char
    return 501


  postAtL = list(postAtStr)       #postAtL is the list version of postAtStr
  for j in range( 0, len(postAtL) ):
    if postAtL[j] == '>' or postAtL[j] == ' ':
      break
    if (postAtL[j-1] == '.') and postAtL[j] not in string.ascii_letters:    #Checks the char directly after any '.'
      return 501
      break
    if postAtL[j].isdigit() == 0 and postAtL[j] != '.' and postAtL[j] not in string.ascii_letters:  #checks whole domain or wierd chars
      return 501
      break


          #################################  End of Path #################################
  
  endPathChck = s.find('>', 1)    
  if endPathChck == -1:     #locates the '>' character, and makes sure it's not missing.
    return 501

  for t in postAtL:

    if  t == '>':   #this block checks the second path error
      break
    if t == ' ':
      return 501
      break

          #################################  final part of "rcpt-to-cmd" #################################

  prePathClose, postPath = s.split('>', 1)    #postPaths is everything after the '>' character.
  postPathL = list(postPath)
 
  for b in postPathL:
    if b != '\r' and b != '\n' and b != '\t' and b != ' ':
      return 501    

          #################################  End of RCPT-TO parsing #################################

  return 1




def MFChecker(s):  #for use in the state machine in main method

  colonCheck = s.find(':', 1)   
  if colonCheck == -1:      #locates the colon string, and makes sure it's not missing.
    return 0

  mailFromStr, rvsPathStr = s.split( s[colonCheck], 1 )   #Splits the input string at the colon.

  mailStr = mailFromStr[:5]     #seperates off the 'mail' str, and checks it  
  if mailStr != 'MAIL ':
    return 0

  fromStr = mailFromStr[-4:]        #seperates off the 'from' str, and checks it
  if fromStr != 'FROM':
    return 0

  return 1


  afterMailStr = mailFromStr[4:] #creates a string that's everything after 'MAIL'
  blankSpaceL = list(afterMailStr)  #creates a list from the String in previous line

  for x in blankSpaceL: 
    if x == 'F':  
      break
    if x != ' ' and x != '\t':        #this block checks that what's between 'mail' and 'from' is indeed blank space, and not chars.
      return 0
      break



def RCChecker(s):

  colonCheck = s.find(':', 1)   
  if colonCheck == -1:      #locates the colon string, and makes sure it's not missing.
    return 0

  rcptToStr, forwardPathStr = s.split( s[colonCheck], 1 )   #Splits the input string at the colon.


  rcptStr = rcptToStr[:5]     #seperates off the 'RCPT' str, and checks it  
  if rcptStr != 'RCPT ':
    return 0

  toStr = rcptToStr[-2:]        #seperates off the 'TO' str, and checks it
  if toStr != 'TO':
    return 0


  afterRcptStr = rcptToStr[4:] #creates a string that's everything after 'RCPT'
  blankSpaceL2 = list(afterRcptStr)  

  for x in blankSpaceL2: 
    if x == 'T':  
      break
    if x != ' ' and x != '\t':        #this block checks that what's between 'mail' and 'from' is indeed blank space, and not chars.
      return 0
      break





def dataChecker(s):  #data cheker is the same as data parser, but simply doesn't print error messages.

  spaceCheck = s.find(' ', 1) 

  dataStr = s[:4]     #seperates off the 'DATA' str, and checks it  
  if dataStr != 'DATA':
    return 0

  if l[4] != ' ' and l[4] != '\t' and l[4] != '\r':
    return 0

  elif l[4] == ' ' or l[4] == '\t':
    if spaceCheck != -1:
      preSpace, postSpace = s.split(' ', 1)    #postPaths is everything after the first ' ' character.
      postSpaceList = list(postSpace)

      for i in postSpaceList:
        if i != '\r' and i != '\n' and i != '\t' and i != ' ':
          return 0 

  return 1



def main():

#accepts the port # 
#(16468, for testing purposes)
  portNum = int( sys.argv[1] )

#start listening and prepare to handshake
  greetingMssg = '220 greetings from ' + socket.gethostname()
  serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serverSock.bind( ('', portNum) ) #create the TCP welcoming socket
  serverSock.listen(1)  #start listening for incoming requests

  while True:   #(servers are 'always running')

#handshaking
    connectionSock, addr = serverSock.accept() #creates a new socket when a request comes in

    try:

      connectionSock.send( greetingMssg.encode() )
      heloMssg = connectionSock.recv(1024)  
      heloResponse = '250 ' + heloMssg.decode() + ' pleased to meet you.'
      connectionSock.send( heloResponse.encode() )

  #Do I need to parse the Helo message?



  #begin recieving email headers
  #begin recieving MF
      rcptAddressesForHeader = []

      temp1 = connectionSock.recv(1024)
      fromAddressForHeader = temp1.decode()

  #dataChecker and RCChecker
      if dataChecker(fromAddressForHeader) == 1 or RCChecker(fromAddressForHeader) == 1:
        print 'Bad sequence of commands recieved from client'
        connectionSock.send( '503 Bad sequence of commands'.encode() )
        connectionSock.close()
        break

  #MFParser
      inListMF = list(fromAddressForHeader)
      if mFParser(fromAddressForHeader, inListMF) == 500:
        print 'unrecognized command recieved from client'
        connectionSock.send( '500 Syntax error: command unrecognized'.encode() )
        connectionSock.close()
        break

      if mFParser(fromAddressForHeader, inListMF) == 501:
        print 'bad email address in command recieved from client'
        connectionSock.send( '501 Syntax error in parameters or arguments'.encode() )
        connectionSock.close()
        break


      connectionSock.send( '250 OK'.encode() )

      print 'done taking from address:' + fromAddressForHeader


  #begin recieving RCPT
    #first
      temp2 = connectionSock.recv(1024)
      firstToAddress = temp2.decode()


  #dataChecker, MFChecker
      if dataChecker(firstToAddress) == 1 or MFChecker(firstToAddress) == 1:
        print 'Bad sequence of commands recieved from client'
        connectionSock.send( '503 Bad sequence of commands'.encode() )
        connectionSock.close()
        break

  #rCParser
      inListRC = list(firstToAddress)
      if rCParser(firstToAddress, inListRC) == 500:
        print 'unrecognized command recieved from client'
        connectionSock.send( '500 Syntax error: command unrecognized'.encode() )
        connectionSock.close()
        break

      if rCParser(firstToAddress, inListRC) == 501:
        print 'bad email address in command recieved from client'
        connectionSock.send( '501 Syntax error in parameters or arguments'.encode() )
        connectionSock.close()
        break



     #data checker AND oneormore = false


      rcptAddressesForHeader.append( firstToAddress )
      connectionSock.send( '250 OK'.encode() )
    #after first
      while(1):
        thisAddress = connectionSock.recv(1024)
        thisAddress.decode()
        if thisAddress.strip() == 'DATA':
          break
        else:
          if MFChecker(thisAddress) == 1:
            print 'Bad sequence of commands recieved from client'
            connectionSock.send( '503 Bad sequence of commands'.encode() )
            connectionSock.close()
            break
          rcptAddressesForHeader.append(thisAddress)
          connectionSock.send( '250 OK'.encode() )

      print 'done taking to addresses:'
      print rcptAddressesForHeader


  #begin recieve message body
      connectionSock.send( '354'.encode() )

      print '354 sent'

      temp3 = connectionSock.recv(1024)
      mssgBody = temp3.decode()

      print 'done taking mssg body:' + mssgBody

      connectionSock.send( '250 OK'.encode() )
      print '250 after message body sent'


      temp4 = connectionSock.recv(1024)
      # if temp4.decode().split() == 'QUIT'
      #   connectionSock.close()

      print 'done taking quit message'


      connectionSock.close()

      print 'connection has been closed.  now to send to forward file.'

  #need to add proccessing here to establish how many domains there will be
      domains = []
      print 'the rcptAddressesForHeader array is:'
      print rcptAddressesForHeader
      for k in rcptAddressesForHeader:
        preAt, postAtStr = k.split('@', 1)    #postAtStr string is everything after the '@' character.
        targetString, uselessString = postAtStr.split('>', 1)
        domains.append(targetString)

      print 'domains added to array:'
      print domains

  #write to forward file
      for i in domains:
        f = open('forward/' + i, 'a+')
        f.write(mssgBody)
        f.close()

      print 'forward files addded'

    except:
      print 'the server encountered a socket error.'





if __name__ == '__main__':
  main()
