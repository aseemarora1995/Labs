def break_string(string):
	strings_list = []
	alphabets = [chr(a) for a in range(65, 91)]\
		+[chr(a) for a in range(97, 123)] 
	empty = ''

	# store productions in a list 
	for i, char in enumerate(string):
		if char in alphabets:
			empty += char
		else:
			strings_list.append(empty)
			empty = ''
	strings_list.append(empty)
	strings_list = filter(None, strings_list)

	return strings_list


def check_factoring(strings_list):
	pass	


def left_factoring(new, string):
	strings_list = break_string(string)
	length = len(strings_list[1])
	final_index = []
	final_j = -1

	for j in range(1, length):
		index = []
		flag = 0
		a = strings_list[1][:j]
		for i, s in enumerate(strings_list):
			if i == 0:
				continue
			if s[:j] == a:
				index.append(i)
		if len(index) > 1:
			final_j = j
			final_index = index

	new_string_list = []
	if final_j > -1:
		final_string = []
		new_string_list = []
		common = strings_list[index[0]][:final_j]
		new_start_symbol = chr(70 + new)
		new_string_list.append(new_start_symbol)

		for i in final_index:
			new = strings_list[i][final_j:] 
			new_string_list.append(new)
			strings_list[i] = strings_list[i][:final_j] + new_start_symbol

	unique = []
	[unique.append(i) for i in strings_list if i not in unique]

	empty1 = ''
	empty2 = ''
	for j, s in enumerate(unique):
		if j == 0:
			empty1 = s[0] + '->'
			continue
		empty1 += s + '|'

	for j, s in enumerate(new_string_list):
		if j == 0:
			empty2 = s[0] + '->'
			continue
		empty2 += s + '|'
	final_string = []
	final_string.append(empty1[:-1])
	final_string.append(empty2[:-1])
	return final_string
	

def check_recursion(start_symbol, strings_list):
	index = []
	for i, string in enumerate(strings_list):
		if i == 0:
			continue
		if start_symbol == string[0]:
			index.append(i)
	return index
	pass


def left_recursion_removal(string):
	new_productions = []
	strings_list = break_string(string)
	start_symbol = strings_list[0]
	index = check_recursion(start_symbol, strings_list)
	# print strings_list
	empty1 = ''
	empty2 = ''
	new_start_symbol = 'Z'
		
	for j, s in enumerate(strings_list):
		if j == 0:
			continue
		if j not in index:
			empty1 += s + new_start_symbol + '|'
		if j in index:
			empty2 += strings_list[j][1:] + new_start_symbol + '|'
	
	empty1 = start_symbol + '->' + empty1[:-1]
	empty2 = new_start_symbol + '->' + empty2 + 'epsilon'
	
	new_productions.append(empty1)
	new_productions.append(empty2)	
	
	return new_productions


def print_stuff(stuff):
	stuff = list(filter(None, stuff))
	# print stuff
	for some_stuff in stuff:
		print some_stuff

# main program
final = []
null = 'epsilon'
grammar = raw_input('Enter grammar: ')
new_grammar = left_recursion_removal(grammar)

print '\n*left recursion removed*'
print_stuff(new_grammar)


print '\n*calling left factoring...*'
for i, string in enumerate(new_grammar):
	lfc = left_factoring(i, string)
	print_stuff(lfc)
