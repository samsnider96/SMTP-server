def dataParser(s, l):

  spaceCheck = s.find(' ', 1) 

  dataStr = s[:4]     #seperates off the 'DATA' str, and checks it  
  if dataStr != 'DATA':
    error500()
    return 0

  if l[4] != ' ' and l[4] != '\t' and l[4] != '\r':
    error500()
    return 0

  elif l[4] == ' ' or l[4] == '\t':
    if spaceCheck != -1:
      preSpace, postSpace = s.split(' ', 1)    #postPaths is everything after the first ' ' character.
      postSpaceList = list(postSpace)

      for i in postSpaceList:
        if i != '\r' and i != '\n' and i != '\t' and i != ' ':
          error500()
          return 0 

  return 1


def error500(): 

  print '500 Syntax error: command unrecognized'
  return


def main():

  inVarData = raw_input() + '\r\n'  #DATA parse:
  inListData = list(inVarData)
  if dataParser(inVarData, inListData) == 1:
    print '354 Start mail input; end with <CRLF>.<CRLF>'

if __name__ == '__main__':
    main()