

import copy
import pandas as pd

# productions = ['S->A', 'A->T|A+T|A-T', 'T->F|T*F|T/F', 'F->P|P^F', 'P->i|n|(A)']
productions = ['E->E+E|E*E|i']

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
	'''
	for key in terminals_used:
		print key, ':', op_prec_table[key]
	'''
	df = pd.DataFrame(op_prec_table).T
	print df


def initialisations():
	global terminals_used
	for p in productions:
		variables_used.append(p[0])
		rules[p[0]], first[p[0]], last[p[0]] = p[3:], [], []
		temp_first[p[0]], temp_last[p[0]] = [], []
		# op_prec_table[p[0]] = {}
	# print terminals_used
	
	for key, value in rules.iteritems():
		for v in value:
			if v in terminals:
				# print v
				terminals_used.append(v)
	# terminals_used.append('$')
	terminals_used = list(set(terminals_used))
	
	for terminal in terminals_used:
		op_prec_table[terminal] = {}

	for key, value in op_prec_table.iteritems():
		for terminal in terminals_used:	
			value[terminal] = []


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
	print terminals_used, variables_used
	# terminal immediately precedes non_terminal => terminal < first[non_terminal]
	for key, value in rules.iteritems():
		print key, value
		for i, v in enumerate(value):
			if i == len(value)-1:
				continue
			elif value[i] in terminals_used and value[i+1] in variables_used:
				print '-->>', value[i], value[i+1]
				for ch in first[value[i+1]]:
					op_prec_table[v][ch].append('<')

	# terminal succedes non_terminal => terminal > last[non_terminal]
	for key, value in rules.iteritems():
		for i, v in enumerate(value):
			if i == len(value)-1:
				continue
			elif value[i] in variables_used and value[i+1] in terminals_used:
				for ch in last[value[i]]:
					op_prec_table[ch][value[i+1]].append('>')

	# $
	start = productions[0][0]
	for ch in first[start]:
		op_prec_table['$'][ch].append('<')
	for ch in last[start]:
		op_prec_table[ch]['$'].append('>')

	# aBc => a = c
	pass

def main():
	initialisations()
	find_first()
	find_last()
	op_precedence_table()
	print_stuff()


if __name__ == "__main__":
	main()