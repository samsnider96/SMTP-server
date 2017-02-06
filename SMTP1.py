#This program will parse string commands and determine if they're valid SMTP commands.
#validates the 'MAIL FROM', 'RCPT TO', and 'DATA' commands.

#TO DO ::::  

#FIX THE POST- '>' PARSING!!! 
      #I think i've done this with a for loop... STILL NEED TO MAKE SURE THE LAST CHARS ARE /r/n
          #Does \r\n count as one character or 2?
# FIX THE a.b.c thing from the email...................
#See if the 'MAIL ' or 'RCPT ' comparisons fuck up the tab case.  I think they would.

import sys
import string


def mFParser(s, l):  #s is the input string, l is the full input list.  l not currently used!!!


        #################################  Beginning of MAIL FROM #############################


  colonCheck = s.find(':', 1)   
  if colonCheck == -1:      #locates the colon string, and makes sure it's not missing.
    error500()
    return 0

  mailFromStr, rvsPathStr = s.split( s[colonCheck], 1 )   #Splits the input string at the colon.



  mailStr = mailFromStr[:5]     #seperates off the 'mail' str, and checks it  
  if mailStr != 'MAIL ':
    error500()              #I think this might fuck up the tab thing !!!!!
    return 0

  fromStr = mailFromStr[-4:]        #seperates off the 'from' str, and checks it
  if fromStr != 'FROM':
    error500()
    return 0




  afterMailStr = mailFromStr[4:] #creates a string that's everything after 'MAIL'
  blankSpaceL = list(afterMailStr)  #creates a list from the String in previous line

  for x in blankSpaceL: 
    if x == 'F':  
      break
    if x != ' ' and x != '\t':        #this block checks that what's between 'mail' and 'from' is indeed blank space, and not chars.
      error500()
      return 0
      break




          #################################  Beginning of Path #################################

  pathL = list(rvsPathStr)    

  for y in pathL:
    if y == '<':    #this block checks the first path error
      break
    if y != ' ' and y != '\t':
      error501()
      return 0
      break




          ##########################  Beginning of local-part #################################

  preBrack, z = s.split('<', 1)  #Makes sure mailbox is not a special char or a space
  if z[0]==' ' or z[0]=='@' or z[0]=='<' or z[0]=='>' or z[0]=='(' or z[0]==')' or z[0]=='[' or z[0]==']' or z[0]=='\\' or z[0]=='.' or z[0]==',' or z[0]==';' or z[0]==':' or z[0]=='\"':      
    error501()
    return 0          



          #################################  mailbox #################################
  

  atCheck = s.find('@')   
  if atCheck == -1:     #locates the @ char, and makes sure it's not missing.
    error501()
    return 0

  localpartChecker = list(z)  #Creates a list out of z

  for i in localpartChecker:    #Makes sure mailbox is not a special char or a space
    if i == '@':
      break
    if i==' ' or i=='<' or i=='>' or i=='(' or i==')' or i=='[' or i==']' or i=='\\' or i=='.' or i==',' or i==';' or i==':' or i=='\"':
      error501()
      return 0
      break

          #################################  domain #################################

  preAt, postAtStr = s.split('@', 1)    #postAtStr string is everything after the '@' character.

  if postAtStr[0] not in string.ascii_letters:    #Checks very first domain char
    error501()
    return 0


  postAtL = list(postAtStr)       #postAtL is the list version of postAtStr
  for j in range( 0, len(postAtL) ):
    if postAtL[j] == '>' or postAtL[j] == ' ':
      break
    if (postAtL[j-1] == '.') and postAtL[j] not in string.ascii_letters:    #Checks the char directly after any '.'
      error501()
      return 0
      break
    if postAtL[j].isdigit() == 0 and postAtL[j] != '.' and postAtL[j] not in string.ascii_letters:  #checks whole domain or wierd chars
      error501()
      return 0
      break


          #################################  End of Path #################################
  
  endPathChck = s.find('>', 1)    
  if endPathChck == -1:     #locates the '>' character, and makes sure it's not missing.
    error501()
    return 0

  for t in postAtL:

    if  t == '>':   #this block checks the second path error
      break
    if t == ' ':
      error501() 
      return 0
      break

          #################################  final part of "mail from" #################################

  prePathClose, postPath = s.split('>', 1)    #postPaths is everything after the '>' character.
  for b in postPath:
    if b != '\r\n' and b != '\t' and b != ' ':
      error501()
      return 0        #Needa make sure this isn't an endless loop!

          #################################  End of MAIL FROM parsing #################################

  return 1


















def rCParser(s, l):     #Parses the RCPT-TO string.


        #################################  Beginning of RCPT-TO #############################



  colonCheck = s.find(':', 1)   
  if colonCheck == -1:      #locates the colon string, and makes sure it's not missing.
    error500()
    return 0

  rcptToStr, forwardPathStr = s.split( s[colonCheck], 1 )   #Splits the input string at the colon.


  rcptStr = rcptToStr[:5]     #seperates off the 'RCPT' str, and checks it  
  if rcptStr != 'RCPT ':
    error500()            #I think this might fuck up the tab thing !!!!!
    return 0

  toStr = rcptToStr[-2:]        #seperates off the 'TO' str, and checks it
  if toStr != 'TO':
    error500()
    return 0


  afterRcptStr = rcptToStr[4:] #creates a string that's everything after 'RCPT'
  blankSpaceL2 = list(afterRcptStr)  

  for x in blankSpaceL2: 
    if x == 'T':  
      break
    if x != ' ' and x != '\t':        #this block checks that what's between 'mail' and 'from' is indeed blank space, and not chars.
      error500()
      return 0
      break



          #################################  Beginning of Path #################################

  pathL = list(forwardPathStr)    

  for y in pathL:
    if y == '<':    #this block checks the first path error
      break
    if y != ' ' and y != '\t':
      error501()
      return 0
      break




          ##########################  Beginning of local-part #################################

  preBrack, z = s.split('<', 1)  #Makes sure mailbox is not a special char or a space
  if z[0]==' ' or z[0]=='@' or z[0]=='<' or z[0]=='>' or z[0]=='(' or z[0]==')' or z[0]=='[' or z[0]==']' or z[0]=='\\' or z[0]=='.' or z[0]==',' or z[0]==';' or z[0]==':' or z[0]=='\"':      
    error501()
    return 0          



          #################################  mailbox #################################
  

  atCheck = s.find('@')   
  if atCheck == -1:     #locates the @ char, and makes sure it's not missing.
    error501()
    return 0

  localpartChecker = list(z)  #Creates a list out of z

  for i in localpartChecker:    #Makes sure mailbox is not a special char or a space
    if i == '@':
      break
    if i==' ' or i=='<' or i=='>' or i=='(' or i==')' or i=='[' or i==']' or i=='\\' or i=='.' or i==',' or i==';' or i==':' or i=='\"':
      error501()
      return 0
      break

          #################################  domain #################################

  preAt, postAtStr = s.split('@', 1)    #postAtStr string is everything after the '@' character.

  if postAtStr[0] not in string.ascii_letters:    #Checks very first domain char
    error501()
    return 0


  postAtL = list(postAtStr)       #postAtL is the list version of postAtStr
  for j in range( 0, len(postAtL) ):
    if postAtL[j] == '>' or postAtL[j] == ' ':
      break
    if (postAtL[j-1] == '.') and postAtL[j] not in string.ascii_letters:    #Checks the char directly after any '.'
      error501()
      return 0
      break
    if postAtL[j].isdigit() == 0 and postAtL[j] != '.' and postAtL[j] not in string.ascii_letters:  #checks whole domain or wierd chars
      error501()
      return 0
      break


          #################################  End of Path #################################
  
  endPathChck = s.find('>', 1)    
  if endPathChck == -1:     #locates the '>' character, and makes sure it's not missing.
    error501()
    return 0

  for t in postAtL:

    if  t == '>':   #this block checks the second path error
      break
    if t == ' ':
      error501() 
      return 0
      break

          #################################  final part of "rcpt-to-cmd" #################################

  prePathClose, postPath = s.split('>', 1)    #postPaths is everything after the '>' character.

  for b in postPath:
    if b != '\r\n' and b != '\t' and b != ' ':
      error501()
      return 0        #Needa make sure this isn't an endless loop!

          #################################  End of RCPT-TO parsing #################################

  return 1







def dataChecker(s, l):  #data cheker is the same as data parser, but simply doesn't print error messages.

  dataStr = s[:4]     #seperates off the 'DATA' str, and checks it  
  if mailStr != 'DATA':
    return 0

  preA, postA = s.split('A', 2)    #postPaths is everything after the second 'A' character.

  for i in postA:
    if i != '\r\n' and i != '\t' and i != ' ':
      return 0        #Needa make sure this isn't an endless loop!

  return 1


def dataParser(s, l):

  dataStr = s[:4]     #seperates off the 'DATA' str, and checks it  
  if mailStr != 'DATA':
    error500()
    return 0

  preA, postA = s.split('A', 2)    #postPaths is everything after the second 'A' character.

  for i in postA:
    if i != '\r\n' and i != '\t' and i != ' ':
      error500()
      return 0        #Needa make sure this isn't an endless loop!

  return 1





def error500(): 

    print '500 Syntax error: command unrecognized'
    return

def error501(): 

    print '501 Syntax error in parameters or arguments'
    return

def error503(): 

    print '503 Bad sequence of commands'
    return


def main():

                        #set state machine variables:
  stateCheckerMF = 0
  stateCheckerRC = 0
  oneOrMoreRc = 0  #checks if there's been one or more valid RCPT TO commands

  try:
    while 1:                #accept input, parse it, and provide output in a loop.
      

      while stateCheckerMF == 0:
        inVarMF = raw_input() + '\r\n'    #mail from parser call
        inListMF = list(inVarMF)
        print inVarMF[0:inVarMF.index('\r')]
        if mFParser(inVarMF, inListMF) == 1:
          print '250 OK'
          stateCheckerMF == 1


      while stateCheckerRC == 0:
        inVarRC = raw_input() + '\r\n'     #rcpt-to parser call
        inListRC = list(inVarRC)

        if dataChecker(inVarRC, inListRC) == 1 and oneOrMoreRc == 1    
          stateCheckerRC = 1                      
          break                                 #Checks that the state machine shouldn't move on.

        print inVarRC[0:inVarRC.index('\r')]
          if rCParser(inVarRC, inListRC) == 1:
            moreThanOneRc = 1     #setting this variable means that >=1 valid RCPT TO command has been read.
            print '250 OK'


      inVarData = raw_input() + '\r\n'
      inListData = list(inVarData)
      if dataParser(inVarData, inListData) == 1:
        print '354 Start mail input; end with <CRLF>.<CRLF>'


  except EOFError:
    pass

if __name__ == '__main__':
    main()






