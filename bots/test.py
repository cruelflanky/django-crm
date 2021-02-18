import string
import random
import hashlib

def get_random_string(length):
	letters = string.ascii_letters
	result_str = ''.join(random.choice(letters) for i in range(random.randint(5,10)))
	m = hashlib.md5()
	m.update(result_str.encode('utf-8'))
	print (m)
	print (m.hexdigest())
	#return result_str

get_random_string(6)
print('\n')
get_random_string(10)
print('\n')
get_random_string(7)
