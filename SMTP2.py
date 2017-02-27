#does "MAIL FROM:', 'QUIT', etc need to go to standard error instead of output??
#Should printing 'DATA' be conditional?

#Can I assume that the server will respond with only valid response numbers?  For example, what if 
#the program respons with 'hello'....should my program quit?  Or just chill?
#Or, what happens if I type '354' when it expects a '250'?


#seperate at the space, then check if space exists, and check to left of space.

import sys
import string
import os

def messageParser(s):

    #################################  first line #################################


  line1, afterLine1 = s.split( '\r\n', 1 )   #seprates the first line of fwFile

  uselessString1, tempString1 = line1.split( '<', 1 )   
  fromAddress, uselessString2 = tempString1.split( '>', 1 )


  print('MAIL FROM: <' + fromAddress + '>')


  response1 = raw_input()                   #wait for response from server, then handle it in next line
  responseHandler250(response1)


    #################################  second line #################################



  nextFromLocation = afterLine1.find("From:")  #find the next from token, meaning, the next message.
  
  afterLastRCPT = RCPTParser(afterLine1, nextFromLocation) #Call RCPTParser, a recursive function that will 
                                                            #handle the rest of RCPT parsing.

    #################################  DATA section #################################

  print('DATA')

  response3 = raw_input()                   #wait for response from server, then handle it in next line
  responseHandler354(response3)


  if nextFromLocation == -1:
    print afterLastRCPT
    print('.')

    response4 = raw_input()                   #wait for response from server, then handle it in next line
    responseHandler250(response4)
    
    print("QUIT")
    sys.exit()

  else:
#    print afterLastRCPT
    messageToPrint, nextMessage = afterLastRCPT.split("From:", 1)  #Locate beginning of next message
    print(messageToPrint + '.')
 #   print('.')
    response4 = raw_input()                   #wait for response from server, then handle it in next line
    responseHandler250(response4)
    messageParser(nextMessage)          #Recursion that begins next message in the file.


  return



def responseHandler250(s):
#echo to standard error
  print >> sys.stderr, s

#split the string at the first space
  sList = s.split()

#check if an acceptable response was returned
  if sList[0] != '250':
    print("QUIT")
    sys.exit()



def responseHandler354(s):
#echo to standard error
  print >> sys.stderr, s

#split the string at the first space
  sList = s.split()

#check if an acceptable response was returned
  if sList[0] != '354':
    print("QUIT")
    sys.exit()




def RCPTParser(s, nFL): #parameters: "s" is a string starting at the current line of RCPT 
                          #parsing, and "nFL" (nextFromLine) is the integer location of 
                          #the beginning of the next message in "s".

  RCPTLine, afterRCPTLine = s.split( '\r\n', 1 ) #Splits off current RCPT line, for recursion purposes.

  uselessString3, tempString2 = RCPTLine.split( '<', 1 )   
  rcptAddress, uselessString4 = tempString2.split( '>', 1 )  #seperates the receipt address from 
                                                                #brackets, stores it in "rcptAddress"


  print('RCPT TO: <' + rcptAddress + '>')

  response2 = raw_input()                   #wait for response from server, then handle it in next line
  responseHandler250(response2)

  nextRCPTLocation = afterRCPTLine.find("To:")  #find the next to token


  if nextRCPTLocation != -1 and nFL != -1 and nextRCPTLocation < nFL: #if there's another RCPT in the same message,
                                                                        #AND there's more messages in the file.
    nextFromLocation = afterRCPTLine.find("From:")  #reset the nFL parameter; its location has changed now.                                     
    return RCPTParser(afterRCPTLine, nextFromLocation)

  elif nFL == -1 and nextRCPTLocation != -1:    #if there's another RCPT in the same message,
                                                  #AND there's only one message in the file
    nextFromLocation = afterRCPTLine.find("From:")  #reset the nFL parameter; its location has changed now.                                     
    return RCPTParser(afterRCPTLine, nextFromLocation)

  else:
    return afterRCPTLine   #Return a string with everything in the message after the last RCPT Line


def main():



  f = open(sys.argv[1],"r")
  fwFile = f.read()
  f.close()             #fwFile is the entire forward file.

  messageParser(fwFile)

#      except EOFError:
 #       print("QUIT")
 #       sys.exit()




if __name__ == '__main__':
  main()

