
def sucess_down():
	for x in xrange(1,10):
		print ' ' * (x),
		print '*' * (2 * (10-x) -1)

def sucess_up():
	for x in xrange(3,6):

		print ' ' * (5-x),
		print '*' * (2 * x - 1),
		if x < 5:
			print ' ' * (2 * (5-x) -1),
		print '*' * (2 * x - 1)

def sucess():
	sucess_up()
	sucess_down()