class Modulo:
	def __init__(self, residue, modulo):
		self.residue = residue % modulo
		self.modulo = modulo
	
	
	def __neg__(self):
		return Modulo(-self.residue, self.modulo)
	
	
	def __add__(self, other):
		res, mod = self.residue, self.modulo
		if isinstance(other, Modulo):
		else:
			res += other
			res %= mod
		
		return Modulo(res, mod)
	
	def __mul__(self, other):
		return self.other
