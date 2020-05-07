class Polynomial:
	def __init__(self, *coefs):
		self.coefficients = tuple(coefs)
		self.__trimmed = False
	
	def __eq__(self, other):
		self._trimzeros()
		if isinstance(other, Polynomial):
			other._trimzeros()
			if len(other) != len(self):
				return False
			
			for i in range(len(self)):
				if self.coefficients[i] != other.coefficients[i]:
					return False
			return True
		else:
			if len(self.coefficients) > 1:
				return False
			else:
				if len(self.coefficients) == 0:
					return other == 0
				else:
					return other == self.coefficients[0]
	
	def __neq__(self, other):
		return not self.__eq__(other)
	
	
	
	def copy(self):
		return Polynomial(*self.coefficients)
	
	@staticmethod
	def variable():
		return Polynomial(0, 1)
	
	@staticmethod
	def fromroots(leading, *roots):
		cfs = [leading]
		for r in roots:
			last = cfs[0]
			ncfs = [-r * last]
			for c in cfs[1:]:
				ncfs.append(last - r * c)
				last = c
			ncfs.append(last)
			cfs = ncfs
		return Polynomial(*cfs)
	
	def _trimzeros(self):
		if self.coefficients == []:
			return
		
		i = len(self.coefficients) - 1
		while i >= 0 and self.coefficients[i] == 0:
			i -= 1
		self.coefficients = tuple(list(self.coefficients)[:i + 1])
		self.__trimmed = True
	
	
	
	def __len__(self):
		if not self.__trimmed:
			self._trimzeros()
		return len(self.coefficients)
	
	@property
	def degree(self):
		return max(len(self) - 1, 0)
	
	@property
	def leading(self):
		self._trimzeros()
		return self.coefficients[-1]
	
	def __getitem__(self, power):
		self._trimzeros()
		if power < 0 or len(self) <= power:
			return 0
		else:
			return self.coefficients[power]
	
	
	
	def __int__(self):
		return int(self.coefficients[0]) if len(self.coefficients) > 0 else 0
	
	def __float__(self):
		return float(self.coefficients[0]) if len(self.coefficients) > 0 else 0
	
	
	
	def __neg__(self):
		return Polynomial(*[-c for c in self.coefficients])
	
	
	
	def __add__(self, other):
		self._trimzeros()
		ncfs = [c for c in self.coefficients]
		
		if isinstance(other, Polynomial):
			for i in range(len(other)):
				if i < len(ncfs):
					ncfs[i] += other.coefficients[i]
				else:
			 		ncfs.append(other.coefficients[i])
		else:
			if len(ncfs) == 0:
				ncfs.append(other)
			else:
				ncfs[0] += other
		
		return Polynomial(*ncfs)
	
	def __radd__(self, other):
		return self.__add__(other)
	
	def __sub__(self, other):
		if isinstance(other, Polynomial):
			return other.__neg__().__add__(self)
		else:
			ncfs = [c for c in self.coefficients]
			if len(ncfs) == 0:
				ncfs.append(-other)
			else:
				ncfs[0] -= other
			return Polynomial(*ncfs)
	
	def __rsub__(self, other):
		return self.__neg__().__add__(other)
	
	
	
	def __mul__(self, other):
		self._trimzeros()
		
		if isinstance(other, Polynomial):
			ncfs = [0] * (self.degree + other.degree + 1)
			
			for i in range(len(self)):
				for j in range(len(other)):
					ncfs[i + j] += self.coefficients[i] * other.coefficients[j]
		else:
			ncfs = [c * other for c in self.coefficients]
		
		return Polynomial(*ncfs)
	
	def __rmul__(self, other):
		return self.__mul__(other)
	
	
	
	def __pow__(self, other):
		assert type(other) == int, "Polynomial can only be brought to an integer power"
		prod = None
		while other > 0:
			if prod is None:
				prod = self.copy()
			else:
				prod *= self
			
			other -= 1
		
		if prod is None:
			prod = Polynomial(1)
		
		return prod
	
	
	
	@staticmethod
	def divmod(a, b):
		a._trimzeros()
		b._trimzeros()
		
		if a.degree < b.degree:
			return (Polynomial(), a.copy())
		elif len(b.coefficients) == 0:
			raise ZeroDivisionError('Polynomial divided by zero')
		else:
			qcfs, rcfs = [], [c for c in a.coefficients]
			divcf = b.leading
			divis = [c / divcf for c in b.coefficients]
			
			diff = len(rcfs) - len(divis)
			while diff >= 0:
				lead = rcfs[-1]
				if lead != 0:
					for i in range(len(rcfs)):
						if i - diff >= 0:
							rcfs[i] -= lead * divis[i - diff]
				
				rcfs = rcfs[:-1]
				qcfs.insert(0, lead / divcf)
				diff -= 1
			
			return (Polynomial(*qcfs), Polynomial(*rcfs))
	
	def __floordiv__(self, other):
		if not isinstance(other, Polynomial):
			return Polynomial(*[c / other for c in self.coefficients])
		else:
			return Polynomial.divmod(self, other)[0]
	
	def __mod__(self, other):
		if not isinstance(other, Polynomial):
			return Polynomial()
		else:
			return Polynomial.divmod(self, other)[1]
	
	
	
	def __call__(self, x):
		total = self.leading
		for i in range(len(self) - 2, -1, -1):
			total *= x
			total += self.coefficients[i]
		return total
	
	def __str__(self):
		self._trimzeros()
		if len(self) == 0:
			return '0'
		
		ss, isfirst = '', True
		for i in range(len(self.coefficients)):
			cf = self.coefficients[i]
			if cf == 0:
				continue
			
			if i == 0:
				term = str(abs(cf))
			else:
				if i == 1:
					term = 'x'
				else:
					term = f'x^{i}'
				
				if abs(cf) != 1:
					term = str(abs(cf)) + ' * ' + term
			
			
			if isfirst:
				if cf < 0:
					ss += '-'
				
				ss += term
				isfirst = False
			else:
				if cf > 0:
					ss += ' + '
				elif cf < 0:
					ss += ' - '
				
				ss += term
		
		return ss
	
	def __repr__(self):
		self._trimzeros()
		return 'polynomial.Polynomial(' + ', '.join(map(repr, self.coefficients)) + ')'
