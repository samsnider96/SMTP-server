#server file, run on snapper.cs.edu

import socket
import sys
import string
import os


def main():

#accepts the port # 
#(16468, for testing purposes)
  portNum = int( sys.argv[1] )

#start listening and prepare to handshake
  greetingMssg = '220 greetings from ' + socket.gethostname()
  serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serverSock.bind( ('', portNum) ) #create the TCP welcoming socket
  serverSock.listen(1)  #start listening for incoming requests

  while True:   #(servers are 'always running')

#handshaking
    connectionSock, addr = serverSock.accept() #creates a new socket when a request comes in

    try:
      connectionSock.send( greetingMssg.encode() )
      heloMssg = connectionSock.recv(1024)  
      heloResponse = '250 ' + heloMssg.decode() + ' pleased to meet you.'
      connectionSock.send( heloResponse.encode() )

  #Do I need to parse the Helo message?



  #begin recieving email headers
      rcptAddressesForHeader = []

      temp1 = connectionSock.recv(1024)
      fromAddressForHeader = temp1.decode()
      connectionSock.send( '250 OK'.encode() )

      temp2 = connectionSock.recv(1024)
      rcptAddressesForHeader.append( temp2.decode() )
      connectionSock.send( '250 OK'.encode() )

      print 'done taking from address:' + fromAddressForHeader

  #NEED TO TEST capability to accept other rcpt addresses
      
      while(1):
        thisAddress = connectionSock.recv(1024)
        thisAddress.decode()
        if thisAddress.strip() == 'DATA':
          break
        else:
          rcptAddressesForHeader.append(thisAddress)
          connectionSock.send( '250 OK'.encode() )

      print 'done taking to addresses:'
      print rcptAddressesForHeader


  #recieve message body
      connectionSock.send( '354'.encode() )

      print '354 sent'

      temp3 = connectionSock.recv(1024)
      mssgBody = temp3.decode()

      print 'done taking mssg body:' + mssgBody

      connectionSock.send( '250 OK'.encode() )
      print '250 after message body sent'


      temp4 = connectionSock.recv(1024)
      # if temp4.decode().split() == 'QUIT'
      #   connectionSock.close()

      print 'done taking quit message'


      connectionSock.close()

      print 'connection has been closed.  now to send to forward file.'

  #need to add proccessing here to establish how many domains there will be
      domains = []
      print 'the rcptAddressesForHeader array is:'
      print rcptAddressesForHeader
      for k in rcptAddressesForHeader:
        preAt, postAtStr = k.split('@', 1)    #postAtStr string is everything after the '@' character.
        targetString, uselessString = postAtStr.split('>', 1)
        domains.append(targetString)

      print 'domains added to array:'
      print domains

  #write to forward file
      for i in domains:
        f = open('forward/' + i, 'a+')

        f.write(mssgBody)
        f.close()

      print 'forward files addded'
    except:
      print 'the server encountered a socket error.'





if __name__ == '__main__':
  main()
