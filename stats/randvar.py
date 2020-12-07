import math

class RandVar:
	def __init__(self, probs):
		self.probabilities = probs
		self.normalize()
	
	@staticmethod
	def fromCases(*cases):
		probs = {}
		for (c, pr) in cases:
			if c in probs:
				probs[c] += pr
			else:
				probs[c] = pr
		
		return RandVar(probs)
	
	@staticmethod
	def fromConstant(const):
		return RandVar((const, 1))
	
	@staticmethod
	def fromSample(collection):
		probs = {}
		for c in collection:
			if c in probs:
				probs[c] += 1
			else:
				probs[c] = 1
		
		return RandVar(probs)
	
	
	
	def __getitem__(self, key):
		if key in self.probabilities:
			return self.probabilities[key]
		else:
			return 0
	
	
	
	def normalize(self):
		total = sum(self.probabilities.values())
		self.probabilities = {x: px / total for x, px in self.probabilities.items()}
	
	def likelihood(self, pred):
		cond, total = None, None
		for x, px in self.probabilities.items():
			if pred(x):
				if cond is None:
					cond = px
				else:
					cond += px
			
			if total is None:
				total = px
			else:
				total += px
		
		if total is None:
			return None
		else:
			return cond / total
	
	def conditional(self, pred):
		probs = {}
		for x, px in self.probabilities.items():
			if pred(x):
				if x in probs:
					probs[x] += px
				else:
					probs[x] = px
		return RandVar(probs)
	
	def expected(self, expr):
		xsum, totprob = None, None
		for x, px in self.probabilities.items():
			if xsum is None:
				xsum = expr(x) * px
			else:
				xsum += expr(x) * px
			
			if totprob is None:
				totprob = px
			else:
				totprob += px
		
		if totprob is None:
			raise ZeroDivisionError("Total Probability is Zero")
		else:
			return xsum / totprob
	
	def mean(self):
		return self.expected(lambda x: x)
	
	def variance(self):
		x2m, xm = self.expected(lambda x: x * x), self.mean()
		return x2m - xm * xm
	
	def stddev(self):
		return math.sqrt(self.variance())
	
	
	
	def median(self):
		ordered = sorted(self.probabilities.items(), key = lambda x: x[0])
		tot = 0
		lastX = None
		for x, px in ordered:
			if 2 * tot < 1 and 1 < 2 * (tot + px):
				return x
			elif tot == 1 / 2:
				return (x + lastX) / 2
			
			lastX, lastPx = x, px
			tot += px
		
		return lastX
	
	
	
	def apply(self, func):
		probs = {}
		for x, px in self.probabilities.items():
			res = func(x)
			if res in probs:
				probs[res] += px
			else:
			 	probs[res] = px
		
		return RandVar(probs)
	
	def lift(self, other, operator):
		probs = {}
		if isinstance(other, RandVar):
			for x, px in self.probabilities.items():
				for y, py in other.probabilities.items():
					res = operator(x, y)
					if res in probs:
						probs[res] += px * py
					else:
						probs[res] = px * py
			
		else:
			# other is constant
			for x, px in self.probabilities.items():
				res = operator(x, other)
				if res in probs:
					probs[res] += px
				else:
				 	probs[res] = px
		
		return RandVar(probs)
	
	def __add__(self, other):
		return self.lift(other, lambda x, y: x + y)
	
	def __radd__(self, other):
		return self.lift(other, lambda x, y: y + x)
	
	def __sub__(self, other):
		return self.lift(other, lambda x, y: x - y)
	
	def __rsub__(self, other):
		return self.lift(other, lambda x, y: y - x)
	
	def __mul__(self, other):
		return self.lift(other, lambda x, y: x * y)
	
	def __rmul__(self, other):
		return self.lift(other, lambda x, y: y * x)
	
	def __div__(self, other):
		return self.lift(other, lambda x, y: x / y)
	
	def __rdiv__(self, other):
		return self.lift(other, lambda x, y: y / x)
	
	def __pow__(self, other):
		return self.lift(other, lambda x, y: x ** y)
	
	def __rpow__(self, other):
		return self.lift(other, lambda x, y: y ** x)
	
	def __truediv__(self, other):
		return self.lift(other, lambda x, y: x / y)
	
	def __rtruediv__(self, other):
		return self.lift(other, lambda x, y: y / x)
	
	def __floordiv__(self, other):
		return self.lift(other, lambda x, y: x // y)
	
	def __rfloordiv__(self, other):
		return self.lift(other, lambda x, y: y // x)
	
	
	
	def __repr__(self):
		return "RandVar({" + ', '.join(repr(x) + ": " + repr(px) for x, px in self.probabilities.items()) + "})"
	
	def __str__(self):
		return self.__repr__()



def binomial(trials, success):
	comp = 1 - success
	probs = {}
	for i in range(trials + 1):
		probs[i] = math.comb(trials, i) * (success ** i) * (comp ** (trials - i))
	return RandVar(probs)

def geometric(success, iters):
	comp = 1 - success
	probs, total = {}, 0
	for i in range(iters):
		probs[i] = success * (comp ** i)
		total += probs[i]
	
	probs[iters] = 1 - total
	return RandVar(probs)

def poisson(average, iters):
	expAver = math.exp(-average)
	probs, total = {}, 0
	weight = 1
	for i in range(iters):
		probs[i] = expAver * weight
		total += probs[i]
		
		weight *= average / (i + 1)
	
	probs[iters] = 1 - total
	return RandVar(probs)

