#This program will parse string commands and determine if they're valid SMTP commands.
#validates the 'MAIL FROM', 'RCPT TO', and 'DATA' commands.

import sys
import string


def mFParser(s, l):  #s is the input string, l is the full input list.  l not currently used!!!


        #################################  Beginning of MAIL FROM #############################


  colonCheck = s.find(':', 1)   
  if colonCheck == -1:      #locates the colon string, and makes sure it's not missing.
    error500()
    return 0

  mailFromStr, rvsPathStr = s.split( s[colonCheck], 1 )   #Splits the input string at the colon.



  mailStr = mailFromStr[:5]     #seperates off the 'mail' str, and checks it  #WHY IS THIS 4???
  if mailStr != 'MAIL ':
    error500()
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
    if x != ' ':        #this block checks that what's between 'mail' and 'from' is indeed blank space, and not chars.
      error500()
      return 0
      break




          #################################  Beginning of Path #################################

  pathL = list(rvsPathStr)    

  for y in pathL:
    if y == '<':    #this block checks the first path error
      break
    if y != ' ':
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
  if postPath != '\r\n':
    error501()
    return 0

          #################################  End of all parsing #################################

  return 1



def rCParser(s, l):     #Parses the RCPT-TO string.


  colonCheck = s.find(':', 1)   
  if colonCheck == -1:      #locates the colon string, and makes sure it's not missing.
    error500()
    return 0

  rcptToStr, forwardPathStr = s.split( s[colonCheck], 1 )   #Splits the input string at the colon.


  rcptStr = rcptToStr[:5]     #seperates off the 'RCPT' str, and checks it  
  if rcptStr != 'RCPT ':
    error500()
    return 0

  toStr = rcptToStr[-2:]        #seperates off the 'TO' str, and checks it
  if fromStr != 'TO':
    error500()
    return 0

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

  try:
    while 1:                #accept input, parse it, and provide output in a loop.
      
      inVarMF = raw_input() + '\r\n'    #mail from parser call
      inListMF = list(inVarMF)
      print inVarMF[0:inVarMF.index('\r')]
      if mFParser(inVarMF, inListMF) == 1:
        print '250 OK'

     inVarRC = raw_input() + '\r\n'     #rcpt-to parser call
      inListRC = list(inVarRC)
      print inVarRC[0:inVarRC.index('\r')]
      if rCParser(inVarRC, inListRC) == 1:
        print '250 OK'
  except EOFError:
    pass

if __name__ == '__main__':
    main()






