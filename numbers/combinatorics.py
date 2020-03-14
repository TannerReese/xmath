def factorial(n, fall=None, rise=None):
	if fall is not None:
		falling = True
		iters = fall
	elif rise is not None:
		falling = False
		iters = rise
	else:
		falling = True
		iters = int(n)
	
	prod = 1
	for i in range(iters):
		if falling:
			prod *= n - i
		else:
			prod *= n + i
	
	return prod


def choose(n, k):
	c = factorial(n, fall=k) / factorial(k)
	
	if c - int(c) == 0:
		return int(c)
	else:
		return c

def nCr(n, k):
	return choose(n, k)

def nPr(n, k):
	p = factorial(n, fall=k)
	
	if p - int(p) == 0:
		return int(p)
	else:
		return p


def catalan(n):
	ct = choose(2 * n, n) / (n + 1)
	
	if ct - int(ct) == 0:
		return int(ct)
	else:
		return ct



def permutations(lst, size=None):
	lst = list(lst)  # Convert iterables to lists
	
	if size is None:
		size = len(lst)
	
	if size <= 0:
		yield []
		return
	
	for i in range(len(lst)):
		perms = permutations(lst[:i] + lst[i + 1:])
		for p in perms:
			yield [lst[i]] + p

def combinations(lst, size=None):
	lst = list(lst)  # Convert iterables to lists
	
	if size is None:
		if len(lst) == 0:
			yield []
			return
		
		x = lst[0]
		for c in combinations(lst[1:]):
			yield c
			yield [x] + c
	elif size > len(lst):
		yield None
	elif size <= 0 or len(lst) <= 0:
		yield []
	else:
		for c in combinations(lst[1:], size):
			if c is not None:
				yield c
		
		x = lst[0]
		for c in combinations(lst[1:], size - 1):
			yield [x] + c



def partitions(n, maxpart=None):
	if maxpart is None or maxpart > n:
		maxpart = n
	
	if n == 0:
		yield []
		return
	
	for i in range(1, maxpart + 1):
		for part in partitions(n - i, maxpart=i):
			part.append(i)
			yield part

def partcount(n, maxpart=None):
	if maxpart is None or maxpart > n:
		maxpart = n
	
	if n == 0:
		return 1
	
	count = 0
	for i in range(1, maxpart + 1):
		count += partcount(n - i, maxpart=i)
	
	return count
