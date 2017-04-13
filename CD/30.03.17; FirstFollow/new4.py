import copy

############################################################################
# productions = ['S->ABCDE', 'A->a|e', 'B->b|e', 'C->c', 'D->d|e', 'E->f|e']
# productions = ['S->ABC', 'A->C|b', 'B->c|Sd', 'C->f']
# productions = ['S->ABC|d', 'A->a|e|B', 'B->b|e', 'C->c']
# productions = ['S->Bb|Cd', 'B->aB|e', 'C->cC|e']
productions = ['S->ACB|CbB|Ba', 'A->da|BC', 'B->g|e', 'C->h|e']
# productions = ['S->aABb', 'A->c|e', 'B->d|e']
# productions = ['S->aBDh', 'B->cC', 'C->bC|e', 'D->EF', 'E->g|e', 'F->f|e']
############################################################################

# declarations
first = {} # store firsts
temp_first = {} # temp storage for 'firsts'
follow = {} # store 'follows'
rules = {} # store RHS of productions with variables as keys
temp_follow = {} # temp storage for follows
all_variables = [] # variables used in productions

variables = [chr(a) for a in range(65, 91)] # stores all variables
terminals = [chr(a) for a in range(97, 123)] # store all terminals

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
	print ''
	

def initialise_dictionaries():
	for p in productions:
		first[p[0]] = []
		temp_first[p[0]] = []
		temp_follow[p[0]] = []
		follow[p[0]] = []
		rules[p[0]] = p[3:]
		all_variables.append(p[0])
	follow['S'].append('$')

def remove_duplicates(temp):
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
				index = v.find(var) # variable in subrule or not
				if index < 0:
					continue
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


initialise_dictionaries()
find_first(all_variables)	
find_follow(all_variables)
print_stuff()