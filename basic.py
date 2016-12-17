from sys import *

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
			tok = ""
		elif (tok == "PRINT"):
			print("Found a print")
			tok = "" ##Reset te
		elif tok == "\"": #Found a string
			if state == 0:
				state = 1
			elif state == 1:
				print("Found a string")
				string = ""
				state = 0
		elif state == 1: #We found a double quote 
			string += char



def run():
	data = open_file(argv[1])
	lex(data)
	#Parser runs the tokens

run()