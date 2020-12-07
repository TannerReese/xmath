class Modulo:
	def __init__(self, residue, modulo):
		self.residue = residue % modulo
		self.modulo = modulo
	
	def __neg__(self):
		return Modulo(-self.residue, self.modulo)

	
	def lift(self, other, operator):
		res, mod = self.residue, self.modulo
		if isinstance(other, Modulo):
			if other.modulo != mod:
				raise ValueError("Modulo Objects must have same modulo to apply operations")
			
			res = operator(res, other.residue)
		else:
			res = operator(res, other)
		
		res %= mod
		return Modulo(res, mod)
	
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
		if isinstance(other, Modulo):
			return self.__mul__(other.inverse())
		else:
			return self.__mul__(Modulo(other, self.modulo).inverse())
	
	def __rdiv__(self, other):
		if isinstance(other, Modulo):
			return other.inverse().__mul__(self)
		else:
			return Modulo(other, self.modulo).__mul__(self.inverse())
	
	def __truediv__(self, other):
		return self.__div__(other)
	
	def __rtruediv__(self, other):
		return self.__rdiv__(other)
	
	def __pow__(self, other):
		respow, accum, p = self.residue, 1, other
		while p > 0:
			if p & 1:
				accum *= respow
				accum %= self.modulo
			
			respow *= respow
			respow %= self.modulo
			p >>= 1
		
		return Modulo(accum, self.modulo)
	
	def __rpow__(self, other):
		return other.__rpow__(self)
	
	
	
	def inverse(self):
		return Modulo(self.invert(self.residue, self.modulo), self.modulo)
	
	@staticmethod
	def invert(r, m):
		a, b = r % m, m
		x0, x1 = 0, 1
		while a > 0:
			x0, x1 = x1, x0 - (b // a) * x1
			a, b = b % a, a
		
		if b > 1:
			raise ZeroDivisionError(f'{self.residue} (mod {self.modulo}) is not a unit / invertible')
		else:
			return x0
	
	def order(self):
		a, b = self.residue % self.modulo, self.modulo
		while a > 0:
			a, b = b % a, a
		
		if b > 1:
			return 0
		
		power, count = self.residue % self.modulo, 1
		while power != 1:
			power *= self.residue
			power %= self.modulo
			count += 1
		
		return count
	
	
	def __str__(self):
		return f'{self.residue} (mod {self.modulo})'
	
	def __repr__(self):
		return f'Modulo({self.residue}, {self.modulo})'

def mod(m):
	return Modulo(1, m)

