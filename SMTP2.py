#does 'QUIT' need to go to standard error instead of output??



import sys
import string
import os

def messageParser(s):

  line1, afterLine1 = s.split( '\r\n', 1 )   #seprates the first line of fwFile

  uselessString1, tempString1 = line1.split( '<', 1 )   
  fromAddress, uselessString2 = tempString1.split( '>', 1 )


  print('MAIL FROM: <' + fromAddress + '>')

  response1 = raw_input()
  responseHandler(response1)




  line2, afterLine2 = afterLine1.split( '\r\n', 1 )   #seprates the 2nd line of fwFile


def responseHandler(s)
#echo to standard error
  if s[:3] != '250' and s[:3] != '354':
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

