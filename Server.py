#server file, run on snapper.cs.edu

import socket
import sys
import string
import os

def textParser(s):
  return


def main():

#accepts the port # 
#(16468, for testing purposes)
  portNum = int( sys.argv[1] )


  clientName = 'classroom.cs.unc.edu'
  greetingMssg = '220 greetings from snapper.cs.edu'

  serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  serverSock.bind( ('', portNum) ) #create the TCP welcoming socket
  serverSock.listen(1)  #start listening for incoming requests

  while True:   #(servers are 'always running')
    connectionSock, addr = serverSock.accept() #creates a new socket when a request comes in
    connectionSock.send( greetingMssg.encode() )
    heloMssg = connectionSock.recv(1024)  #recieve the helo message
    print( heloMssg.decode() )  #this is for testing
    heloResponse = '250 ' + heloMssg.decode() + ' pleased to meet you.'
    connectionSock.send( heloResponse.encode() )

#Do I need to parse the Helo message?



#begin recieving email message
  
    rcptAddresses[]

    temp1 = connectionSock.recv(1024)
    fromAddress = temp1.decode()
    connectionSock.send( '250'.encode() )

    temp2 = connectionSock.recv(1024)
    rcptAddresses[0] = temp2.decode()
    connectionSock.send( '250'.encode() )

#NEED TO TEST capability to accept other rcpt addresses
    while(1)
      i = 1
      rcptAddresses[i] = connectionSock.recv(1024)
      rcptAddresses[i].decode()
      if rcptAddresses[i].strip() == 'DATA':
        del rcptAddresses[i]
        break
      else:
        connectionSock.send( '250'.encode() )


      connectionSock.send( '354'.encode() )



    connectionSock.close()





if __name__ == '__main__':
  main()
