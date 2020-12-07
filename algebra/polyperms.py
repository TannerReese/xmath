import xmath.numbers.factors as fc
from . import polynomial as pl
from . import permutations as prm

class ModPoly(pl.Polynomial):
	def __init__(self, modulo, *coefs, maxpow=None, polyMod=None):
		super().__init__(*coefs, modulo=modulo)
		
		if maxpow is None:
			self.maxpow = fc.eulertotient(modulo) + 1
		else:
			self.maxpow = maxpow
		
		if polyMod is None:
			self.polyMod = pl.Polynomial(*([0, -1] + [0] * (self.maxpow - 2) + [1]))
		else:
			self.polyMod = polyMod
		
		self._modPower()
	
	@staticmethod
	def frompoly(modulo, poly, maxpow=None, polyMod=None):
		return ModPoly(modulo, *poly.coefficients, maxpow=maxpow, polyMod=polyMod)
	
	def _modPower(self):
		if self.degree >= self.maxpow:
			self = self.__mod__(self.polyMod)
	
	
	def __eq__(self, other):
		if not isinstance(other, ModPoly):
			return False
		
		return super().__eq__(other)
	
	def __neq__(self, other):
		return not self.__eq__(other)
	
	
	@staticmethod
	def fromroots(leading, modulo, *roots):
		return ModPoly(modulo, *pl.Polynomial.fromroots(leading, *roots, mod=modulo).coefficients)
	
	@staticmethod
	def variable(mod):
		return ModPoly(mod, 0, 1)
	
	
	
	def __add__(self, other):
		return ModPoly.frompoly(self.modulo, super().__add__(other), maxpow=self.maxpow, polyMod=self.polyMod)
	
	def __radd__(self, other):
		return ModPoly.frompoly(self.modulo, super().__radd__(other), maxpow=self.maxpow, polyMod=self.polyMod)
	
	def __sub__(self, other):
		return ModPoly.frompoly(self.modulo, super().__sub__(other), maxpow=self.maxpow, polyMod=self.polyMod)
	
	def __rsub__(self, other):
		return ModPoly.frompoly(self.modulo, super().__rsub__(other), maxpow=self.maxpow, polyMod=self.polyMod)
	
	def __mul__(self, other):
		return ModPoly.frompoly(self.modulo, super().__mul__(other), maxpow=self.maxpow, polyMod=self.polyMod)
	
	def __rmul__(self, other):
		return ModPoly.frompoly(self.modulo, super().__rmul__(other), maxpow=self.maxpow, polyMod=self.polyMod)
	
	def __pow__(self, other):
		return ModPoly.frompoly(self.modulo, super().__pow__(other), maxpow=self.maxpow, polyMod=self.polyMod)
	
	
	def __repr__(self):
		self._trimzeros()
		return 'ModPoly(modulo=' + str(self.modulo) + ', ' + ', '.join(map(repr, self.coefficients)) + ')'



def permToPoly(perm, modulo):
	fixed = list(range(0, modulo))
	mvd = tuple(perm.moved())
	
	for m in mvd:
		fixed.remove(m)
	
	# Generate fixed polynomial
	fixedPoly = ModPoly.fromroots(1, modulo, *fixed)
	
	# Generate shifter for elements that are moved
	shifter = ModPoly(modulo)
	for x in mvd:
		allButX = (m for m in mvd if m != x)
		shifter += ModPoly.fromroots(-(perm(x) - x), modulo, *allButX)
	
	return shifter * fixedPoly + ModPoly(modulo, 0, 1)

def polyToPerm(poly):
	if poly.modulo is None:
		raise TypeError("Polynomial must be over Modular Ring to correspond to Permutation")
	
	return prm.Permutation.fromfunc(poly, range(0, poly.modulo))
