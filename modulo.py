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
