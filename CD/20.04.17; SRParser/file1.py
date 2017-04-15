from stack import MyStack

SRstack = ''

#######################################################
productions = ['S->aAcBe', 'A->Ab|b', 'B->d']
# productions = ['S->aAS|c', 'A->ba|SB', 'B->bA']
# productions = ['S->aAS|c', 'A->ba|SB', 'B->bA|S']
# productions = ['E->E+E|E*E|(E)|E->i']
#######################################################


all_variables = []
rules = {}


def initialise():
	for p in productions:
		all_variables.append(p[0])
		rules[p[0]] = []
		rules[p[0]].extend(p[3:].split('|'))
	print rules

def reduce_it():
	global SRstack
	for key, value in rules.iteritems():
		for v in value:
			if len(SRstack) >= len(v):
				# print 'inside 1..'
				if v == SRstack[-len(v):]:
					# print 'inside 2..'
					print v, SRstack[-len(v):]
					for _ in range(len(v)):
						SRstack = SRstack[:-1] # pop()
					SRstack = SRstack + key
					# print 'True'
					return True
	# print 'False'
	return False

def SR_Parser():
	global SRstack
	start = productions[0][0]
	SRstack += '$'
	string = raw_input('enter string: ')
	string = string + '$'
	sr_counter = 0
	while True:
		if string[sr_counter] == '$' and flag == 0:
			if SRstack[-1] == start:
				print 'string valid!'
			else:
				print 'string invalid!'
			break
		flag = 0
		if reduce_it():
			flag = 1
			# print 'inside 3..'
		elif not reduce_it():
			if string[sr_counter] != '$':
				SRstack = SRstack + string[sr_counter]
				sr_counter += 1
				flag = 1
		print '->>', SRstack, string[sr_counter:]

initialise()
SR_Parser()