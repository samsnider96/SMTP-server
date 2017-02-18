#does "MAIL FROM:', 'QUIT', etc need to go to standard error instead of output??
#Should printing 'DATA' be conditional?



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

  print(afterLine2)
  print('.')

  response4 = raw_input()                   #wait for response from server, then handle it in next line
  responseHandler250(response4)





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

#def toRecognizer(s, l):

#def messageSeperator(s):
 # if 'From:' in s:


  #else return


def main():


  try:
    while 1:                #accept input, parse it, and provide output in a loop.

      f = open(sys.argv[1],"r")
      fwFile = f.read()
      f.close()             #fwFile is the entire forward file.

      messageParser(fwFile)

  except EOFError:
    print("QUIT")
    sys.exit()




if __name__ == '__main__':
  main()

