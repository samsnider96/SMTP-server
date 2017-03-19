#server file, run on snapper.cs.edu

import socket
import sys
import string
import os




def socketConnector(pN):
  #create "welcoming socket".  pN is the port number

  clientName = 'classroom.cs.unc.edu'
  greetingMssg = '220 greetings from snapper.cs.edu'

  serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  serverSock.bind( ('', pN) ) #create the TCP welcoming socket
  serverSock.listen(1)  #start listening for incoming requests

  while True:   #(servers are 'always running')
    connectionSock, addr = serverSock.accept() #creates a new socket when a request comes in
    connectionSock.send( greetingMssg.encode() )
    heloMssg = connectionSock.recv(1024)  #recieve the helo message
#    print( heloResponse.decode() )  #this is for testing
    helloResponse = '250 ' + helloMssg.decode() + 'pleased to meet you.'
    connectionSock.send( helloResponse.encode() )
    connectionSock.close()

    #old code:
#  welcomeSock.connect( (clientName, pN) )
#  welcomeSock.send( greetingMssg.encode() )
#  heloResponse = welcomeSock.recv(1024)
#  print( heloResponse.decode() )
#  welcomeSock.close()


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
