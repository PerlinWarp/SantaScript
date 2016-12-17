from sys import *

tokens = [] #List of tokens

#Opens the file to be interpreted
def open_file(filename):
	data = open(filename, "r").read()
	return data 

#Lex checks for keywords, and tokens 
def lex(filecontents):
	tok = ""
	state = 0
	string = ""
	filecontents = list(filecontents)
	for char in filecontents:
		tok += char #Adding every letter to token to make it make sence
		if (tok == " "):
			if (state == 0):
			##If there isnt a string null the space
				tok = ""
			else:
				tok = " " 
		elif (tok == "\n"): #If we find a new line in the code
			tok = ""
		elif (tok == "PRINT"):
			print("Found a print")
			tokens.append("PRINT")
			tok = "" ##Reset te
		elif tok == "\"": #Found a string
			if state == 0:
				state = 1
			elif state == 1:
				print("Found a string")
				tokens.append("STRING:" + string + "\"")
				string = ""
				state = 0
				tok = ""
		elif state == 1: #We found a double quote 
			string += tok
			tok = ""

	#DEBUGGING
	#print(tokens)
	return tokens
#Parser
def parse(toks):
	print(toks)
	i = 0 #Idk why he isnt using a for loop
	while (i < len(toks)):
		if(toks[i] + " " + toks[i+1][0:6] == "PRINT STRING"):
			print(toks[i+1][7:]) #Prints the 6 character onwards
			i+=2
	


def run():
	data = open_file(argv[1])
	toks = lex(data) #Gets the tokens from the lex
	#Parser runs the tokens
	parse(toks)

run()