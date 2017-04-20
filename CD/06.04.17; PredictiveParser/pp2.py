import copy
from stack import MyStack

LLstack = MyStack()
############################################################################
# productions = ['S->ABCDE', 'A->a|e', 'B->b|e', 'C->c', 'D->d|e', 'E->f|e']
productions = ['S->C', 'C->S|a|e']
# productions = ['E->E+T|T', 'T->T*F|F', 'F->i|(E)'] # not LL(1)
# productions = ['S->ABC', 'A->C|b', 'B->c|Sd', 'C->f']
# productions = ['S->ABC|d', 'A->a|e|B', 'B->b|e', 'C->c']
# productions = ['S->Bb|Cd', 'B->aB|e', 'C->cC|e']
# productions = ['S->aAcBe', 'A->Ab|b', 'B->d']
# productions = ['S->ACB|CbB|Ba', 'A->da|BC', 'B->g|e', 'C->h|e']
# productions = ['S->aABb', 'A->c|e', 'B->d|e']
# productions = ['S->aBDh', 'B->cC', 'C->bC|e', 'D->EF', 'E->g|e', 'F->f|e']

# productions = ['E->TX', 'X->+TX|e', 'T->FY', 'Y->*FY|e', 'F->i|(E)']
# productions = ['S->(S)|e']
# productions = 
# productions = ['S->AaAb|BbBa', 'A->e', 'B->e']
# productions = ['S->aABb', 'A->c|e', 'B->d|e']
# productions = ['S->A|a', 'A->a']
# productions = ['S->aB|e', 'B->bC|e', 'C->cS|e']
# productions = ['S->AB', 'A->a|e', 'B->b|e']
# productions = ['S->F|(S+F)', 'F->a']
# productions = ['S->AA', 'A->aA|b']
# productions = ['S->aAS|c', 'A->ba|SB', 'B->bA|S']
# productions = ['S->aAS|e', 'A->ba|SB', 'B->cA|S'] # not LL(1)
## productions = ['S->aAS|c', 'A->ba|SB', 'B->bA|S']
############################################################################

# declarations
first = {} # store firsts
temp_first = {} # temp storage for 'firsts'
follow = {} # store 'follows'
rules = {} # store RHS of productions with variables as keys
temp_follow = {} # temp storage for follows
all_variables = [] # variables used in productions
all_terminals = ['$']
parsing_table = {}

variables = [chr(a) for a in range(65, 91)] # stores all variables
terminals = [chr(a) for a in range(97, 123)] # store all terminals
terminals.extend(['(', ')', '*', '+'])


def isLL1():
	for key, value in parsing_table.iteritems():
		for k, v in value.iteritems():
			if len(v)>1:
				print '\ngrammar is not LL(1)'
				return False
	print '\ngrammar is LL(1)'
	return True

 
def print_stuff():
	print '\n---productions---'
	for p in productions:
		print p
	
	print '\n---first---'
	for key in all_variables:
		print key + ':',
		print first[key]
	
	print '\n---follow---'
	for key in all_variables:
		print key + ':',
		print follow[key]
	print '\n---parsing_table---'
	for key in all_variables:
		print key, ':', parsing_table[key]


def initialise_dictionaries():
	global all_terminals
	start = productions[0][0]
	print 'start:', start
	for p in productions:
		first[p[0]] = []
		temp_first[p[0]] = []
		temp_follow[p[0]] = []
		follow[p[0]] = []
		rules[p[0]] = p[3:]
		all_variables.append(p[0])
		parsing_table[p[0]] = {}
	follow[start].append('$')

	for key, value in rules.iteritems():
		for v in value:
			if v in terminals:
				all_terminals.append(v)
	all_terminals = list(set(all_terminals))
	if 'e' in all_terminals:
		all_terminals.remove('e')
	all_terminals.sort()
	# print all_terminals

	for key, value in parsing_table.iteritems():
		for t in all_terminals:
			value[t] = []
	# print parsing_table


def remove_duplicates(temp, pt=None):
	if pt == 1:
		for key, value in temp.iteritems():
			for t in all_terminals:
				value[t] = list(set(value[t]))
	else:
		for key, values in temp.iteritems():
			temp[key] = list(set(values))


def compare_dictionaries(flag):
	if flag == 'first':
		for (k1, v1), (k2, v2) in zip(first.iteritems(), temp_first.iteritems()):
			if v1 != v2:
				return False
		return True

	elif flag == 'follow':
		for (k1, v1), (k2, v2) in zip(follow.iteritems(), temp_follow.iteritems()):
			if v1 != v2:
				return False
		return True


def find_first(all_variables):
	global temp_first
	
	for t in reversed(all_variables):
		# loop over every variable (or production)
		sub_rules = rules[t].split('|') # break pipes
		for j, sub in enumerate(sub_rules):
			# loop over every sub rule (or every pipe)
			for k, ch in enumerate(sub):
				# loop over each character of sub rule
				remove_duplicates(first) # remove duplicates
				if ch in terminals:
					first[t].append(ch)
					break
				elif ch in variables:
					if 'e' not in first[ch]:
						first[t].extend(first[ch])
						break
					elif 'e' in first[ch]:
						first[t].extend(first[ch])
						first[t].remove('e')
						if k == len(sub)-1: # if subrule has only variables with epsilons
							first[t].append('e')

	remove_duplicates(first)
	remove_duplicates(temp_first)
	if compare_dictionaries('first'):
		return
	else:
		temp_first = copy.deepcopy(first)
		find_first(all_variables)

def find_indices(v, var):
	return [i for i, ch in enumerate(v) if ch == var]

def find_follow(all_variables):
	global temp_follow
	temp = 0
	for var in all_variables:
		# loop over every variable (or production)
		for key, key_val in rules.iteritems():
			# loop over every complete production
			value = key_val.split('|') # break at pipes
			# print value
			for v in value:
				# loop over every pipe (or subrule)
				indices = find_indices(v, var)
				# index = v.find(var) # variable in subrule or not
				if indices == []:
					continue
				for index in indices:
					# if index < 0:
						# continue
					if index == len(v)-1: # case var is the last character in subrule
						follow[var].extend(follow[key])
					for k in range(index+1, len(v)):
						if v[k] in terminals:
							follow[var].append(v[k])
							break
						elif v[k] in variables:
							follow[var].extend(first[v[k]])
							if 'e' not in first[v[k]]:
								break
							#  and k!=len(v)-1
							elif 'e' in first[v[k]]:
								# if k == len(v)-1 ->> last variable in subrule with 'e'
								follow[var].remove('e')
								if k == len(v)-1:
									follow[var].extend(follow[key])
	remove_duplicates(follow)
	remove_duplicates(temp_follow)

	if compare_dictionaries('follow'):
		return
	else:
		temp_follow = copy.deepcopy(follow)
		find_follow(all_variables)			


def create_parsing_table():
	for variable in all_variables:
		sub_rules = rules[variable].split('|')
		# print sub_rules
		for j, rule in enumerate(sub_rules):
			for k, r in enumerate(rule):
				if r in terminals: 
					"""
					parsing_table[variable][r].append(variable+'->'+rule)
					break
					"""					
					if r != 'e':
						parsing_table[variable][r].append(variable+'->'+rule)
						break
					elif r == 'e':
						for m, ch in enumerate(follow[variable]):
							parsing_table[variable][ch].append(variable+'->e')
					
				elif r in all_variables:
					if 'e' not in first[r]:
						for ch in first[r]:
							parsing_table[variable][ch].append(variable+'->'+rule)
						break
					elif 'e' in first[r]:
						for ch in first[r]:
							if ch != 'e':
								parsing_table[variable][ch].append(variable+'->'+rule)
							#####
							'''
							elif ch == 'e':
								for m, ch1 in enumerate(follow[variable]):
									parsing_table[variable][ch1].append(variable+'->'+rule)
							'''
							#####
						if k == len(rule)-1:
							for ch in follow[variable]:
								parsing_table[variable][ch].append(variable+'->'+rule)
	remove_duplicates(parsing_table, 1)						
	# check if grammar is LL(1) or not.
	

def predictive_parser():
	if not isLL1():
		return
	start = productions[0][0]
	LLstack.push('$')
	LLstack.push(start)
	string = raw_input('enter string: ')
	string += '$'
	print string
	# LLstack.show()
	ll_counter = 0
	while True:
		'''
		if string[ll_counter] not in all_terminals:
			print 'string invalid!!'
			break
		'''
		if LLstack.top() in all_variables:
			# print 'inside 1..'
			# LLstack.show()
			temp = parsing_table[LLstack.top()][string[ll_counter]][0][3:]
			# print '->>', LLstack.top(), string[ll_counter]
			# print temp
			LLstack.pop()
			for j, ch in enumerate(reversed(temp)):
				if ch != 'e':
					LLstack.push(ch)
			# LLstack.show()
			# print all_terminals
			# print terminals
		elif LLstack.top() in all_terminals:
			# print 'inside 2..'
			if LLstack.top() == string[ll_counter]:
				LLstack.pop()
				ll_counter += 1
			# LLstack.show()
		# LLstack.show()
		if string[ll_counter] == '$' or LLstack.top() == '$':
		 	if LLstack.top() == '$' and string[ll_counter] == '$':
				print 'string accepted!!'
			else:
				print 'string invalid!!'
			break


def main():
	initialise_dictionaries()
	find_first(all_variables)	
	find_follow(all_variables)
	create_parsing_table()
	print_stuff()
	predictive_parser()


if __name__ == "__main__":
	main()