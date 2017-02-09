#This program will parse string commands and determine if they're valid SMTP commands.
#validates the 'MAIL FROM', 'RCPT TO', and 'DATA' commands.

import sys
import string
import os


def mFParser(s, l):  


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

  pathListMF = list(rvsPathStr) 
   
  return pathParser(rvsPathStr, pathListMF) 






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

  pathListRc = list(forwardPathStr) 

  return pathParser(forwardPathStr, pathListRc)  











def pathParser(s, l):    #This multipurpose path parser is for use in MAIL FROM and RCPT TO.


          #################################  Beginning of Path #################################

  pathL = l    

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
  postPathL = list(postPath)
 
  for b in postPathL:
    if b != '\r' and b != '\n' and b != '\t' and b != ' ':
      error501()
      return 0    

          #################################  End of RCPT-TO parsing #################################

  return 1






def endOfTxtChecker(s):

  if s == '.\r\n':
    return 1

  return 0

def MFChecker(s, l):  #for use in the state machine in main method

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


def RCChecker(s, l):

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





def dataChecker(s, l):  #data cheker is the same as data parser, but simply doesn't print error messages.

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


def dataParser(s, l):

  spaceCheck = s.find(' ', 1) 

  dataStr = s[:4]     #seperates off the 'DATA' str, and checks it  
  if dataStr != 'DATA':
    error500()
    return 0

  if l[4] != ' ' and l[4] != '\t' and l[4] != '\r':
    error500()
    return 0

  elif l[4] == ' ' or l[4] == '\t':
    if spaceCheck != -1:
      preSpace, postSpace = s.split(' ', 1)    #postPaths is everything after the first ' ' character.
      postSpaceList = list(postSpace)

      for i in postSpaceList:
        if i != '\r' and i != '\n' and i != '\t' and i != ' ':
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



#try switching order of these 2
  try:
    while 1:                #accept input, parse it, and provide output in a loop.
      
      paths = []

                              #set state machine variables:
      stateCheckerMF = 0
      stateCheckerRC = 0
      oneOrMoreRC = 0  #checks if there's been one or more valid RCPT TO commands
      stillTakingText = 1


      while stateCheckerMF == 0:        #MAIL FROM parse:

        inVarMF = raw_input() + '\r\n'    
        inListMF = list(inVarMF)

        print inVarMF[0:inVarMF.index('\r')]


        if dataChecker(inVarMF, inListMF) == 1: #Tried data command out of order
          error503()            
          continue

        if RCChecker(inVarMF, inListMF) == 1: #tried RCPT TO command out of order
          error503()
          continue 


        if mFParser(inVarMF, inListMF) == 1:
          print '250 OK'
          stateCheckerMF = 1


      while stateCheckerRC == 0:      #RCPT TO parse:


        inVarRC = raw_input() + '\r\n'     
        inListRC = list(inVarRC)

        print inVarRC[0:inVarRC.index('\r')]


        if dataChecker(inVarRC, inListRC) == 1 and oneOrMoreRC == 0: #Tried data command out of order
          error503()
          continue

        if MFChecker(inVarRC, inListRC) == 1:            #tried data command out of order                 
          error503() 
          continue

        if dataChecker(inVarRC, inListRC) == 1 and oneOrMoreRC == 1:  #tried data command in proper order
          print '354 Start mail input; end with <CRLF>.<CRLF>'
          stateCheckerRC = 1
          break 
                       

        if rCParser(inVarRC, inListRC) == 1:
          
          temp1, temp2 = inVarRC.split('<', 1) 
          targetString, temp3 = temp2.split('>', 1) 

          paths.append(targetString)

          oneOrMoreRC = 1     #setting this variable means that >=1 valid RCPT TO command has been read.

          print '250 OK'





      allText = ''

      while stillTakingText == 1:   #text input loop:
            
        inVarTxt = raw_input() + '\r\n'  

        print inVarTxt[0:inVarTxt.index('\r')]

        if endOfTxtChecker(inVarTxt) == 0:
          allText += inVarTxt

        if endOfTxtChecker(inVarTxt) == 1:
          stillTakingText = 0
          print '250 OK'


      startMF = inVarMF.find('<', 1) + 1
      endMF = inVarMF.find('>', 1)

      for i in paths:
        f = open('forward/' + i, 'a+')
        f.write('From: ' + '<' + inVarMF[startMF:endMF] + '>' + '\r\n')
        for j in paths:
          f.write('To: ' + '<' + j + '>' + '\r\n')
        f.write(allText)
        f.close()




  except EOFError:
    sys.exit()




if __name__ == '__main__':
    main()






