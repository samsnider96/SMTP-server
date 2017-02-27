#does "MAIL FROM:', 'QUIT', etc need to go to standard error instead of output??
#Should printing 'DATA' be conditional?

#Can I assume that the server will respond with only valid response numbers?  For example, what if 
#the program respons with 'hello'....should my program quit?  Or just chill?
#Or, what happens if I type '354' when it expects a '250'?

#Do I need the while and try loops in the bottom?  Like, is there just going to be one argument?  
#I think so...

#Debug case:  when use clicks control D randomly

#Need to fix blank line that comes between message body and period when printing...only happens sometimes.


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


  line2, afterLine2 = afterLine1.split( '\r\n', 1 )   #seprates the 2nd line of fwFile

  uselessString3, tempString2 = line2.split( '<', 1 )   
  rcptAddress, uselessString4 = tempString2.split( '>', 1 )


  print('RCPT TO: <' + rcptAddress + '>')

  response2 = raw_input()                   #wait for response from server, then handle it in next line
  responseHandler250(response2)


    #################################  DATA section #################################

  print('DATA')

  response3 = raw_input()                   #wait for response from server, then handle it in next line
  responseHandler354(response3)


  temporaryNum = afterLine2.find("From:")  #Check if there's another message after this
  if temporaryNum == -1:
    print(afterLine2)
    print('.')

    response4 = raw_input()                   #wait for response from server, then handle it in next line
    responseHandler250(response4)
    
    print("QUIT")
    sys.exit()
  else:
    messageToPrint, nextMessage = afterLine2.split("From:", 1)  #Locate beginning of next message
    print(messageToPrint + '.')
 #   print('.')
    response4 = raw_input()                   #wait for response from server, then handle it in next line
    responseHandler250(response4)
    messageParser(nextMessage)          #Recursion that begins next message in the file.






  # temporaryNum = afterLine2.find("From:")  #Check if there's another message after this,quit if not
  # if temporaryNum == -1:
  #    print("QUIT")
  #    sys.exit()
  # else:
  #   uselessString5, nextMessage = afterLine2.split("From:", 1)  #Locate beginning of next message
  #   messageParser(nextMessage)                                  #use recursion to parse next message




  return

#use fromRecognizer to check for the end of the program

#  except EOFError:
 #   print("QUIT")
 #   sys.exit()




def responseHandler250(s):
#echo to standard error
  print >> sys.stderr, s

#check if an acceptable response was returned
  if s[:3] != '250':
    print("QUIT")
    sys.exit()

def responseHandler354(s):
#echo to standard error
  print >> sys.stderr, s

#check if an acceptable response was returned
  if s[:3] != '354':
    print("QUIT")
    sys.exit()




def fromRecognizer(s):

  fromStr = s[:5]        #seperates off the 'from' str, and checks it
  if fromStr == 'From:':
    return 1
  else:
    return 0


def main():


#  try:
 #   while 1:                #accept input, parse it, and provide output in a loop.

  f = open(sys.argv[1],"r")
  fwFile = f.read()
  f.close()             #fwFile is the entire forward file.

  messageParser(fwFile)

#      except EOFError:
 #       print("QUIT")
 #       sys.exit()




if __name__ == '__main__':
  main()

