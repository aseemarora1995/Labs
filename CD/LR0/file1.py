from stack import MyStack
import pandas as pd
# productions = ['S->AA', 'A->aA|b']
# productions = ['E->E+T|T', 'T->T*F|F', 'F->(E)|i']
productions = ['E->E+T', 'E->T', 'T->T*F', 'T->F', 'F->(E)', 'F->i']
LRStack = MyStack()


parsing_table ={'0':{'i':'s5', '+':'', '*':'', '(':'s4', ')':'', '$':'', 'E':'1', 'T':'2', 'F':'3'},\
				'1':{'i':'', '+':'s6', '*':'', '(':'', ')':'', '$':'accept', 'E':'', 'T':'', 'F':''},\
				'2':{'i':'', '+':'r2', '*':'s7', '(':'', ')':'r2', '$':'r2', 'E':'', 'T':'', 'F':''},\
				'3':{'i':'', '+':'r4', '*':'r4', '(':'', ')':'r4', '$':'r4', 'E':'', 'T':'', 'F':''},\
				'4':{'i':'s5', '+':'', '*':'', '(':'s4', ')':'', '$':'', 'E':'8', 'T':'2', 'F':'3'},\
				'5':{'i':'', '+':'r6', '*':'r6', '(':'', ')':'r6', '$':'r6', 'E':'', 'T':'', 'F':''},\
				'6':{'i':'s5', '+':'', '*':'', '(':'s4', ')':'', '$':'', 'E':'', 'T':'9', 'F':'3'},\
				'7':{'i':'s5', '+':'', '*':'', '(':'s4', ')':'', '$':'', 'E':'', 'T':'', 'F':'10'},\
				'8':{'i':'', '+':'r6', '*':'', '(':'', ')':'s11', '$':'', 'E':'', 'T':'', 'F':''},\
				'9':{'i':'', '+':'r1', '*':'s7', '(':'', ')':'r1', '$':'r1', 'E':'', 'T':'', 'F':''},\
			   '10':{'i':'', '+':'r3', '*':'r3', '(':'', ')':'r3', '$':'r3', 'E':'', 'T':'', 'F':''},\
			   '11':{'i':'', '+':'r5', '*':'r5', '(':'', ')':'r5', '$':'r5', 'E':'', 'T':'', 'F':''}
			   }
			
def print_table():
	for state in parsing_table:
		print state, ':' 
		for key in parsing_table[state]:
			print '('+key + ':' + parsing_table[state][key]+')', 
		print '\n'	

def parser():
	df = pd.DataFrame(parsing_table).T
	# print_table()
	print df
	lr_counter = 0
	string = raw_input('enter string: ')
	string += '$'
	# LRStack.push('$')
	LRStack.push('0')
	LRStack.show()
	counter = 0
	while True:
		counter += 1
		top = LRStack.top()
		s = string[lr_counter]
		print '->>', top, s, '->> move:', parsing_table[top][s]
		
		if parsing_table[top][s] == 'accept':
			print 'string valid!'
			break
		if parsing_table[top][s] == '':
			print 'string invalid'
			break
		
		if parsing_table[top][s][0] == 's': # shift
			LRStack.push(s)
			LRStack.push(parsing_table[top][s][1:])
			lr_counter += 1
			LRStack.show()
		elif parsing_table[top][s][0] == 'r': # reduce
			index = int(parsing_table[top][s][1:]) - 1 
			length = len(productions[index][3:])
			for _ in range(2*length):
				LRStack.pop()
			LRStack.push(productions[index][0])
			LRStack.show()
			
			var_c = LRStack.top()
			LRStack.pop()
			var_r = LRStack.top()
			LRStack.push(var_c)
			
			LRStack.push(parsing_table[var_r][var_c])
			LRStack.show()
		pass
		'''
		if counter > 12:
			print 'breaking..'
			break
		'''

def main():
	parser()
	

if __name__ == "__main__":
	main()