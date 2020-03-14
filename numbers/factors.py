def factors(num):
	if num == 0 or num == 1:
		return []
	
	facs = []
	
	def extract(k):
		nonlocal num
		
		count = 0
		while num % k == 0:
			num //= k
			count += 1
		
		if count > 0:
			facs.append((k, count))
	
	extract(2)
	extract(3)
	
	i = 6
	while (i - 1) * (i - 1) <= num and num > 1:
		extract(i - 1)
		extract(i + 1)
		i += 6
	
	if num > 1:
		facs.append((num, 1))
	return facs

def squarefree(x):
	if x == 0:
		return False
	elif x == 1:
		return True
	
	if x % 4 == 0 or x % 9 == 0:
		return False
	
	i = 6
	while i * i <= x:
		l, u = i - 1, i + 1
		if x % (l * l) == 0 or x % (u * u) == 0:
			return False
		
		i += 6
	
	return True



def divisors(x):
	divs = [1]
	for p, k in factors(x):
		ndivs = []
		ppow = 1
		for _ in range(k + 1):
			ndivs += [d * ppow for d in divs]
			ppow *= p
		divs = ndivs
	
	return divs

def divisorsum(x):
	total = 1
	for p, k in factors(x):
		total *= (p ** (k + 1) - 1) // (p - 1)
	return total

def aliquot(x):
	return divisorsum(x) - x

def divisorcount(x):
	count = 1
	for _, k in factors(x):
		count *= k + 1
	return count



def eulertotient(x):
	return jordantotient(x, 1)

def jordantotient(x, k):
	tot = 1
	for p, r in factors(x):
		tot *= (p ** k - 1) * p ** (k * (r - 1))
	return tot
