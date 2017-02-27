#This program acts as the Server side of the SMTP protocol.  For now, it will take standard input
#instead of recieving messages from the client.

import sys
import string
import os

def messageParser(s):

     #################################  start of first line #################################


  line1, afterLine1 = s.split( '\r\n', 1 )   #seperates the first line of the forward-File.

  uselessString1, tempString1 = line1.split( '<', 1 )   
  fromAddress, uselessString2 = tempString1.split( '>', 1 )  #Seperates the mailbox string from the first line.


  print('MAIL FROM: <' + fromAddress + '>')


  response1 = raw_input()                   
  responseHandler250(response1)



     #################################  start of second line #################################


  nextFromLocation = afterLine1.find("From:")  #find the next from token, meaning, the next message.
  
  afterLastRCPT = RCPTParser(afterLine1, nextFromLocation) #Call RCPTParser, a recursive function that will 
                                                            #handle the rest of RCPT parsing.


     #################################  start of DATA section #################################

  print('DATA')

  response3 = raw_input()                   
  responseHandler354(response3)

#Case 1: runs if the currently processing message is the last message in the forward file.
  if nextFromLocation == -1:
    print afterLastRCPT
    print('.')

    response4 = raw_input()                  
    responseHandler250(response4)
    
    print("QUIT")
    sys.exit()

#Case 2: runs if there are more messages to parse later on in the forward file.  It's recursive.
  else:
    messageToPrint, nextMessage = afterLastRCPT.split("From:", 1)  #Locate beginning of next message
    print(messageToPrint + '.')
    response4 = raw_input()                   
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



def RCPTParser(s, nFL): 

#parameters: "s" is a string starting at the current line of RCPT 
  #parsing, and "nFL" (nextFromLine) is the integer location of 
  #the very next "From:" string in "s".


  RCPTLine, afterRCPTLine = s.split( '\r\n', 1 ) #Splits off current RCPT line, for recursion purposes.

  uselessString3, tempString2 = RCPTLine.split( '<', 1 )   
  rcptAddress, uselessString4 = tempString2.split( '>', 1 )   #Seperates the mailbox string from the first line.                                                             

  print('RCPT TO: <' + rcptAddress + '>')


  response2 = raw_input()                   
  responseHandler250(response2)


  nextRCPTLocation = afterRCPTLine.find("To:")  #find the next "To:" token, in order to compare it to next "From:" token.

#Case 1:  if there's another RCPT in the same message, AND there's more messages in the file.
  if nextRCPTLocation != -1 and nFL != -1 and nextRCPTLocation < nFL: 
    
    nextFromLocation = afterRCPTLine.find("From:")    #reset the nFL parameter; its location has changed now.                                     
    return RCPTParser(afterRCPTLine, nextFromLocation)



#Case 2:  if there's another RCPT in the same message, AND there's only one message in the file
  elif nFL == -1 and nextRCPTLocation != -1:    
    
    nextFromLocation = afterRCPTLine.find("From:")    #reset the nFL parameter; its location has changed now.                                     
    return RCPTParser(afterRCPTLine, nextFromLocation)

#Case 3:  All RCPT-line parsing and recursion is done.
  else:
    return afterRCPTLine   #Return a string with everything in the forward file after the last RCPT Line.


def main():

  f = open(sys.argv[1],"r")    #Accept one forward file as a command line argument
  fwFile = f.read()
  f.close()             #fwFile is the entire forward file.

  messageParser(fwFile)



if __name__ == '__main__':
  main()

