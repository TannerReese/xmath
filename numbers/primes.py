import math

def primes(upto=None):
	"""
	Return a generator over all prime numbers until and including `upto` (default is None)
	If `upto` is None then generate to infinity
	"""
	
	if upto is None:
		n = 2
		while True:
			if isprime(n):
				yield n
			n += 1
	else:
		isprm = [i % 2 != 0 and i % 3 != 0 for i in range(upto + 1)]
		
		if 2 <= upto:
			yield 2
		if 3 <= upto:
			yield 3
		
		n = 5 # Current check location in sequence
		yldn = 4 # Number after last one yielded
		while yldn <= upto:
			for y in range(yldn, min(n * n, upto + 1)):
				if isprm[y]:
					yield y
			yldn = n * n
			
			if isprm[n]:
				for i in range(2 * n, upto + 1, n):
					isprm[i] = False
			
			n += 1


def isprime(x):
	""" Check whether `x` is prime """
	
	if x <= 0 or x == 1:
		return False
	elif x == 2 or x == 3:
		return True
	elif x % 2 == 0 or x % 3 == 0:
		return False
	
	i = 5
	while i * i <= x:
		if x % i == 0 or x % (i + 2) == 0:
			return False
		
		i += 6
	
	return True


def primorial(x):
	""" Return the product of all primes less than `x` """
	prms = primes(int(x))
	prod = 1
	
	for p in prms:
		prod *= p
	return prod
