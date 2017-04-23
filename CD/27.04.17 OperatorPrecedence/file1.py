#
# file1.py for Operator Precedence Parser in /media/aseemarora/3b912a2c-a205-4208-a8a9-f009304a914f/College/Labs/CD/27.04.17 OperatorPrecedence
# 
# Made by Aseem Arora
# Login	 <aseemarora1995@gmail.com>
# 
# Started on	Sat Apr	22 23:50:28 2017 Aseem Arora
# Last update	Sat Apr	22 23:50:28 2017 Aseem Arora
#


import copy

productions = ['S->A', 'A->T|A+T|A-T', 'T->F|T*F|T/F', 'F->P|P^F', 'P->i|n|(A)']

variables_used, terminals_used = [], ['$']
rules, first, last, temp_first, temp_last = {}, {}, {}, {}, {}
op_prec_table = {}

variables = [chr(a) for a in range(65, 91)] # stores all variables
terminals = [chr(a) for a in range(97, 123)] # store all terminals
terminals.extend(['(', ')', '*', '+', '$', '/', '-', '^'])


def print_stuff():
	print '\n---productions---'
	for p in productions:
		print p
	
	print '\n---first---'
	for key in variables_used:
		print key + ':',
		print first[key]
	
	print '\n---last---'
	for key in variables_used:
		print key + ':',
		print last[key]
	
	print '\n---operator_precedence_table---'
	for key in all_variables:
		print key, ':', parsing_table[key]
	

def initialisations():
	for p in productions:
		variables_used.append(p[0])
		rules[p[0]], first[p[0]], last[p[0]] = p[3:], [], []
		temp_first[p[0]], temp_last[p[0]] = [], []
		op_prec_table[p[0]] = {} 
	
	for key, value in rules.iteritems():
		for v in value:
			if v in terminals:
				terminals_used.append(v)
	# terminals_used.append('$')
	terminals_used = list(set(terminals_used))
	
	for key, value in op_prec_table.iteritems():
		for terminal in terminals_used:
			value[t] = []


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
			if v1.sort() != v2.sort():
				return False
		return True

	elif flag == 'last':
		for (k1, v1), (k2, v2) in zip(last.iteritems(), temp_last.iteritems()):
			if v1.sort() != v2.sort():
				return False
		return True


def find_first():
	global temp_first
	while True:
		for variable in reversed(variables_used):
			temp = rules[variable].split('|')
			for rule in temp:
				for i, ch in enumerate(rule):
					if ch in terminals:
						first[variable].append(ch)
						break
					elif ch in variables_used:
						first[variable].extend(first[ch])
					remove_duplicates(first)

		remove_duplicates(first)
		remove_duplicates(temp_first)
		
		if compare_dictionaries('first'):
			break
		else:
			temp_first = copy.deepcopy(first)


def find_last():
	global temp_last
	while True:
		for variable in reversed(variables_used):
			temp = rules[variable].split('|')
			for rule in temp:
				for i, ch in enumerate(reversed(rule)):
					if ch in terminals:
						last[variable].append(ch)
						break
					elif ch in variables_used:
						last[variable].extend(last[ch])
					remove_duplicates(last)

		remove_duplicates(last)
		remove_duplicates(temp_last)
		
		if compare_dictionaries('last'):
			break
		else:
			temp_last = copy.deepcopy(last)


def op_precedence_table():
	# terminal precedes non_terminal => terminal < first[non_terminal]


	# terminal succedes non_terminal => terminal > last[non_terminal]

	# aBc => a = c
	pass

def main():
	initialisations()
	find_first()
	find_last()
	print_stuff()


if __name__ == "__main__":
	main()