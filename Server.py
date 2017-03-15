#server file, run on classroom.cs.edu

import socket
import sys
import string
import os




def socketConnector(s):
  #create "welcoming socket"

  clientName = 'snapper.cs.unc.edu'
  greetingMssg = '220 greetings from classroom.cs.edu'

  welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


  welcomeSock.connect( (clientName, s) )
  welcomeSock.send( greetingMssg.encode() )
  heloResponse = welcomeSock.recv(1024)
  print( heloResponse.decode() )
  welcomeSock.close()
#if HELO message is propper, ...

  #then create special socket just for the client


def textParser(s):
  return


def main():

#accepts the port # 
#(16468, for testing purposes)
  portNum = int( sys.argv[1] )


  socketConnector(portNum)



if __name__ == '__main__':
  main()
