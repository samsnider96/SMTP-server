#client file, run on snapper.cs.edu

import socket
import sys
import string
import os






def socketConnector(h, p):

  heloMssg = 'HELO' #...I need to change this later on but will leave it for now.

  clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  clientSock.connect( (h,p) ) 
  greetingMssg = clientSock.recv(1024)
  print( greetingMssg.decode() )
  #if greeting message is propper, ...
  clientSock.send( heloMssg.encode() )
  clientSock.close()



def main():

#accepts the hostname of the server 
#(classroom, for testing purposes)
  hostName = sys.argv[1]

#accepts the port # (should be same as parameter for server program)
#(16468, for testing purposes)
  portNum = int( sys.argv[2] )
    

  socketConnector(hostName, portNum)

if __name__ == '__main__':
    main()