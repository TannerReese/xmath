from math import sqrt, sin, cos

class Vector:
	def __init__(self, *comps):
		self.components = tuple(comps)
	
	def __len__(self):
		return len(self.components)
	
	def __eq__(self, other):
		selfDim = len(self.components)
		if selfDim != len(other.components):
			return False
		
		for i in range(selfDim):
			if self.components[i] != other.components[i]:
				return False
		return True
	
	def __neq__(self, other):
		return not self.__eq__(other)
	
	def iszero(self, zeroVal=0):
		return all(c == zeroVal for c in self.components)
	
	
	
	def __abs__(self):
		total = None
		for c in self.components:
			if total is None:
				total = c * c
			else:
				total += c * c
		
		if total is None:
			return 0
		else:
			return sqrt(total)
	
	def __getitem__(self, key):
		return self.components[key]
	
	
	
	def __add__(self, other):
		if not isinstance(other, Vector):
			raise TypeError("Vectors can only be added to other Vectors")
		
		selfDim, otherDim = len(self), len(other)
		if selfDim != otherDim:
			raise ValueError(f"Vector dimensions do not match: {selfDim} and {otherDim}")
		
		return Vector(*(self.components[i] + other.components[i] for i in range(selfDim)))
	
	def __sub__(self, other):
		if not isinstance(other, Vector):
			raise TypeError("Vectors can only be added to other Vectors")
		
		selfDim, otherDim = len(self), len(other)
		if selfDim != otherDim:
			raise ValueError(f"Vector dimensions do not match: {selfDim} and {otherDim}")
		
		return Vector(*(self.components[i] - other.components[i] for i in range(selfDim)))
	
	def __mul__(self, other):
		selfDim = len(self)
		if isinstance(other, Vector):
			otherDim = len(other)
			if selfDim != otherDim:
				raise ValueError(f"Vector dimensions do not match: {selfDim} and {otherDim}")
			
			dot = None
			for i in range(selfDim):
				prod = self.components[i] * other.components[i]
				
				if dot is None:
					dot = prod
				else:
					dot += prod
			return dot
		else:
			return Vector(*(other * self.components[i] for i in range(selfDim)))
	
	def __rmul__(self, other):
		return self.__mul__(other)
	
	def __div__(self, other):
		return self.__truediv__(other)
	
	def __truediv__(self, other):
		selfDim = len(self)
		return Vector(*(self.components[i] / other for i in range(selfDim)))
	
	def __floordiv__(self, other):
		selfDim = len(self)
		return Vector(*(self.components[i] // other for i in range(selfDim)))
	
	
	def __repr__(self):
		return 'Vector(' + ', '.join(map(str, self.components)) + ')'
	
	def rotate(self, rotand, angle):
		"""
		Rotate the `rotand` about the rotator defined by `self`
		by an angle of `angle` counterclockwise.
		Note: Uses Rodriguez Rotation Formula
		
		Args:
			rotand (Vector) -- Vector to rotate around self
			angle (float) -- angle by which to rotate in radians
		
		Returns:
			Vector -- rotated vector
		"""
		
		c, s = cos(angle), sin(angle)
		selfMag = abs(self)
		
		total = rotand * c
		total += cross(self, rotand) * (s / selfMag)
		total += self * (self * rotand) * ((1 - c) / (selfMag * selfMag))
		return total



def gramschmidt(*vectors):
	basis, first = [], True
	for v in vectors:
		if first:
			basis.append(v)
		else:
			for b in basis:
				v -= (v * b) / (b * b) * b
			
			if not v.iszero():
				basis.append(v)
	
	return basis



def zero(dims=3, zeroVal=0):
	return Vector(*(zeroVal for i in range(dims)))

def cross(vec1, vec2):
	if not isinstance(vec1, Vector) or not isinstance(vec2, Vector):
		raise TypeError("Cross Product only defined between Vectors")
	
	dim1, dim2 = len(vec1), len(vec2)
	if dim1 != dim2:
		raise ValueError(f"Vector dimensions do not match: {dim1} and {dim2}")
	
	if dim1 == 2:
		return vec1.components[0] * vec2.components[1] - vec1.components[1] * vec2.components[0]
	elif dim1 == 3:
		x = vec1.components[1] * vec2.components[2] - vec1.components[2] * vec2.components[1]
		y = vec1.components[2] * vec2.components[0] - vec1.components[0] * vec2.components[2]
		z = vec1.components[0] * vec2.components[1] - vec1.components[1] * vec2.components[0]
		return Vector(x, y, z)
	else:
		raise ValueError(f"Cross Product not defined on Vectors of dimension {dim1}")
