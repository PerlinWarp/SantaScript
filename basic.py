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
		if (tok == " "):
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
			if var != "":
				tokens.append("VAR:" + var)
				var = ""
				varStarted = False
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
		print("TRUE")
		return symbols[varname]
	else:
		return("VARIABLE ERROR: Undefined Variable")


#Parser
def parse(toks):
	print(toks)
	i = 0 #Idk why he isnt using a for loop
	while (i < len(toks)):
		#print("DOES THIS EVER END? " + (str(i)) + "len(toks) " + str(len(toks)))
		if(toks[i] + " " + toks[i+1][0:6] == "UNWRAP STRING" or toks[i] + " " + toks[i+1][0:3] == "UNWRAP NUM" or toks[i] + " " + toks[i+1][0:4] == "UNWRAP EXPR" or toks[i] + " " + toks[i+1][0:3] == "UNWRAP VAR"):
			if(toks[i+1][0:6] == "STRING"):
					doPRINT(toks[i+1]) #Prints the 6 character onwards
			elif(toks[i+1][0:3]== "NUM"):
					doPRINT(toks[i+1])
			elif(toks[i+1][0:4]== "EXPR"):
					doPRINT(toks[i+1])
			elif(toks[i+1][0:4]== "VAR"):
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
	print(symbols)
def run():
	data = open_file(argv[1])
	toks = lex(data) #Gets the tokens from the lex
	#Parser runs the tokens
	parse(toks)

run()