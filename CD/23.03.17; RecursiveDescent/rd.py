"""
productions 
	E -> iF
	F -> +aF | -bF | *cF | /dF
	i - i
"""
counter = 0

def match(ch):
	# print ch
	global counter
	if ch == 'i':
		if s[counter] == ch:
			counter += 1
			return True
	elif ch == '+':
		if s[counter] == ch:
			counter += 1
			if s[counter] == 'a':
				counter += 1
				return True
	elif ch == '-':
		if s[counter] == ch:
			counter += 1
			if s[counter] == 'b':
				counter += 1
				return True
	elif ch == '*':
		if s[counter] == ch:
			counter += 1
			if s[counter] == 'c':
				counter += 1
				return True
	elif ch == '/':
		if s[counter] == ch:
			counter += 1
			if s[counter] == 'd':
				counter += 1
				return True
	return False

def F():
	global counter
	if counter >= max_length:	
		return True
	if match('+') or match('-') or match('*') or match('/'):
		return F()
	return False
	
def E():
	global counter
	if match('i'):
		if F() == True:
			print 'string accpeted!'
		else:
			print 'string not accepted' 
		return
	print 'string not accepted!'
	return 

s = raw_input('enter string to process: ')
global max_length
max_length = len(s)
E()