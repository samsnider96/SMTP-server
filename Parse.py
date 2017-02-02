#This program will parse a text string command and determine if it's a valid SMTP command.
#It validates the 'mail from' command.

import sys
import string


def parser(s, l):  #s is the input string, l is the full input list.  l not currently used!!!


				#################################  Beginning of MAIL FROM #############################


	colonCheck = s.find(':', 1)		
	if colonCheck == -1:			#locates the colon string, and makes sure it's not missing.
		error('mail-from-cmd')
		return 0

	mailFromStr, rvsPathStr = s.split( s[colonCheck], 1 )		#Splits the input string at the colon.



	mailStr = mailFromStr[:5]			#seperates off the 'mail' str, and checks it  #WHY IS THIS 4???
	if mailStr != 'MAIL ':
		error('mail-from-cmd')
		return 0

	fromStr = mailFromStr[-4:]  			#seperates off the 'from' str, and checks it
	if fromStr != 'FROM':
		error('mail-from-cmd')
		return 0




	afterMailStr = mailFromStr[4:] #creates a string that's everything after 'MAIL'
	blankSpaceL = list(afterMailStr)  #creates a list from the String in previous line

	for x in blankSpaceL:	
		if x == 'F':	
			break
		if x != ' ':				#this block checks that what's between 'mail' and 'from' is indeed blank space, and not chars.
			error('mail-from-cmd')
			return 0
			break




					#################################  Beginning of Path #################################

	pathL = list(rvsPathStr)		

	for y in pathL:
		if y == '<':		#this block checks the first path error
			break
		if y != ' ':
			error('path')
			return 0
			break




					##########################  Beginning of local-part #################################

	preBrack, z = s.split('<', 1)  #Makes sure mailbox is not a special char or a space
	if z[0]==' ' or z[0]=='@' or z[0]=='<' or z[0]=='>' or z[0]=='(' or z[0]==')' or z[0]=='[' or z[0]==']' or z[0]=='\\' or z[0]=='.' or z[0]==',' or z[0]==';' or z[0]==':' or z[0]=='\"':			
		error('local-part')
		return 0					



					#################################  mailbox #################################
	

	atCheck = s.find('@')		
	if atCheck == -1:			#locates the @ char, and makes sure it's not missing.
		error('mailbox')
		return 0

	localpartChecker = list(z)  #Creates a list out of z

	for i in localpartChecker:		#Makes sure mailbox is not a special char or a space
		if i == '@':
			break
		if i==' ' or i=='<' or i=='>' or i=='(' or i==')' or i=='[' or i==']' or i=='\\' or i=='.' or i==',' or i==';' or i==':' or i=='\"':
			error('mailbox')
			return 0
			break

					#################################  domain #################################

	preAt, postAtStr = s.split('@', 1)  	#postAtStr string is everything after the '@' character.

	if postAtStr[0] not in string.ascii_letters:		#Checks very first domain char
		error('domain')
		return 0


	postAtL = list(postAtStr)  			#postAtL is the list version of postAtStr
	for j in range( 0, len(postAtL) ):
		if postAtL[j] == '>' or postAtL[j] == ' ':
			break
		if (postAtL[j-1] == '.') and postAtL[j] not in string.ascii_letters:  	#Checks the char directly after any '.'
			error('domain')
			return 0
			break
		if postAtL[j].isdigit() == 0 and postAtL[j] != '.' and postAtL[j] not in string.ascii_letters:	#checks whole domain or wierd chars
			error('domain')
			return 0
			break


					#################################  End of Path #################################
	
	endPathChck = s.find('>', 1)		
	if endPathChck == -1:			#locates the '>' character, and makes sure it's not missing.
		error('path')
		return 0

	for t in postAtL:

		if  t == '>':		#this block checks the second path error
			break
		if t == ' ':
			error('path')		
			return 0
			break

					#################################  final part of "mail from" #################################

	prePathClose, postPath = s.split('>', 1)  	#postPaths is everything after the '>' character.
	if postPath != '\r\n':
		error('mail-from-cmd')
		return 0

					#################################  End of all parsing #################################

	return 1


def error(eM): #pass in an error message

    print 'ERROR -- ' + eM
    return


def main():

	try:
		while 1:								#accept input, parse it, and provide output in a loop.
			inVar = raw_input() + '\r\n'
			inList = list(inVar)
			print inVar[0:inVar.index('\r')]
			if parser(inVar, inList) == 1:
				print 'Sender ok'
	except EOFError:
		pass

if __name__ == '__main__':
    main()


