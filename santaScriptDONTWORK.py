#!/usr/bin/python
from sys import *

tokens = [] #List of tokens
stack = []
#Symbol table for variable assignment
symbols = {}

#Opens the file to be interpreted
def open_file(filename):
	data = open(filename, "r").read()
	data += "<EOF>"
	return data 

#Lex checks for keywords, and tokens 
def lex(filecontents):
	#NUM is a number
	#EXPR is an expression 
	#STRING is a string
	tok = ""
	#Strings
	state = 0
	string = ""
	#Expressions and Numbers
	expr = ""
	isexpr = False #is this is an expression or a number? 
	n = "" #number
	#Variables
	varStarted = False #To define variables 
	var = ""
	
	filecontents = list(filecontents)
	for char in filecontents:
		tok += char #Adding every letter to token to make it make sence
		if (tok == "elf" or tok == "ELF"):
			tokens.append("ELF")
			tok = ""
		elif (tok == "endif" or tok == "ENDIF"):
			tokens.append("ENDIF")
			tok = ""
		elif (tok == " "):
			if (state == 0):
			##If there isnt a string null the space
				tok = ""
			else:
				tok = " " 
		elif (tok == "\n" or tok == "<EOF>"): #Every new line or at the end of the file in the code
			if expr != "" and isexpr == True :
				tokens.append("EXPR:"+expr)
				expr = ""
			elif expr != "" and isexpr == 0:
				#expr is a number
				tokens.append("NUM:"+expr)
				expr = ""
			elif (var != ""):
				tokens.append("VAR:" + var)
				var = ""
				varStarted = False
			tok = ""
		elif (tok == "=" and state == False):
			if(expr != "" and isexpr == 0):
				tokens.append("NUM:" + expr)
				expr = ""
			if var != "":
				tokens.append("VAR:" + var)
				var = ""
				varStarted = False
			if (tokens[-1] == "EQUALS"):
				tokens[-1] = "EQEQ" #Replace EQUALS with EQEQ for ==
			else:
				tokens.append("EQUALS")
			tok = ""
		elif (tok == "$" and state == False): ##
			varStarted = True
			var += tok
			tok = ""
		elif varStarted == True:
			if (tok == "<" or tok == ">"):
				if var != "":
					tokens.append("VAR:" + var)
					var = ""
					varStarted = False
			var += tok
			tok = ""
		elif (tok == "UNWRAP" or tok == "unwrap"):
			#print("Found a print")
			tokens.append("UNWRAP")
			tok = "" ##Reset token
		elif (tok == "ENDIF" or tok == "endif"):
			tokens.append("endif")
			tok = ""
		elif (tok == "IF" or tok == "if"):
			tokens.append("IF")
			tok = ""
		elif (tok == "THEN" or tok == "then"):
			if (expr != "" and isexpr == 0):
				tokens.append("NUM:" + expr)
				expr = ""
			tokens.append("THEN")
			tok = ""
		elif  (tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9"):
			#If the token is a number
			expr += tok
			#tokens.append("NUMBER:" + tok + "\"")
			tok = ""
		elif (tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == ")" or tok == "("):
			#Brackets for BidMas
			isexpr = True
			expr += tok
			tok = ""
		elif (tok == "\t"):
			tok = "" #Ignore tabs 
		elif tok == "\"": #Found a string
			if state == 0:
				state = 1
			elif state == 1:
				#print("Found a string")
				tokens.append("STRING:" + string + "\"")
				string = ""
				state = 0
				tok = ""
		elif state == 1: #We found a double quote 
			string += tok
			tok = ""
	return tokens
	#DEBUGGING
	#return tokens
def evalExpression(expr):
	return eval(expr)

#Gets rid of the double quote marks on what we are printing
def doPRINT(toPRINT):
	if(toPRINT[0:6] == "STRING"):
		toPRINT = toPRINT[8:]
		toPRINT = toPRINT[:-1] #To get rid of the last "
	elif(toPRINT[0:3] == "NUM"):
		toPRINT = toPRINT[4:]
	elif(toPRINT[0:4] == "EXPR"):
		toPRINT = evalExpression(toPRINT[5:])
	print(toPRINT)

def doASSIGN(varname, varvalue):
	symbols[varname[4:]] = varvalue

def getVARIABLE(varname):
	varname = varname[4:]
	if varname in symbols:
		return symbols[varname]
	else:
		return("VARIABLE ERROR: Undefined Variable")


#Parser
def parse(toks):
	print("STARTING PARSING")
	print(toks)
	condition = False
	i = 0 
	while (i < len(toks)):
		#if(toks[i] == "ELF"):

		if(toks[i] == "ENDIF"):
			#print("Found an end if")
			i+=1
		#print("DOES THIS EVER END? " + (str(i)) + "len(toks) " + str(len(toks)))
		elif(toks[i] + " " + toks[i+1][0:6] == "UNWRAP STRING" or toks[i] + " " + toks[i+1][0:3] == "UNWRAP NUM" or toks[i] + " " + toks[i+1][0:4] == "UNWRAP EXPR" or toks[i] + " " + toks[i+1][0:3] == "UNWRAP VAR"):
			if(toks[i+1][0:6] == "STRING"):
					doPRINT(toks[i+1]) #Prints the 6 character onwards
			elif(toks[i+1][0:3]== "NUM"):
					doPRINT(toks[i+1])
			elif(toks[i+1][0:4]== "EXPR"):
					doPRINT(toks[i+1])
			elif(toks[i+1][0:3]== "VAR"):
					doPRINT(getVARIABLE(toks[i+1]))
			i+=2 # As we used 2 tokens
		elif (toks[i][0:3] + " " + toks[i + 1] + " " + toks[i + 2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i + 1] + " " + toks[i + 2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i + 1] + " " + toks[i + 2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i + 1] + " " + toks[i + 2][0:3] == "VAR EQUALS VAR"):
			if(toks[i+2][0:6] == "STRING"):
					doASSIGN(toks[i], toks[i+2]) #Prints the 6 character onwards
			elif(toks[i+2][0:3]== "NUM"):
					doASSIGN(toks[i], toks[i+2])
			elif(toks[i+2][0:4]== "EXPR"):
					doASSIGN(toks[i], "NUM:" + str(eval(toks[i+2][5:])))
			elif(toks[i+2][0:3] == "VAR"):
					doASSIGN(toks[i], getVARIABLE(toks[i+2]))
			i+=3 #As we used 3 tokesn
		elif (toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i + 4] == "IF NUM EQEQ NUM THEN"):
			#print("Found an if statement")
			#Checking if the if statement is true
			if (toks[i+1][4:] == toks[i+3][4:]):
				condition = True
				i += 5
			else:
				condition = False
				#print("tokens = " + str(toks))
				#print("i = " + str(i))
				i += (toks.index("ENDIF") - i)
				print(toks.index("ENDIF"))
			print(str(condition))
		elif (toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i + 4] == "IF VAR EQEQ NUM THEN"):
			#print("Found an if statement")
			#Checking if the if statement is true
			if ((getVARIABLE(toks[i+1]))[4:] == toks[i+3][4:]):
				condition = True
				i += 5
			else:
				condition = False
				i += (toks.index("ENDIF") - i)

		

	#Debugging		
	print("SYMBOL TABLE = " + str(symbols))
def run():
	if(len(argv) != 2):
		print("Usage: ./SantaScript test.lang")
		quit()
	data = open_file(argv[1])
	toks = lex(data) #Gets the tokens from the lex
	#Parser runs the tokens
	parse(toks)
run()