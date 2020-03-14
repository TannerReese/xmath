from abc import ABC

class Group(ABC):
	@property
	def _identity(self):
		""" Returns the identity element for this group """
		pass
	
	def _inverse(self, x):
		""" Return the inverse for a given element of the group """
		pass
	
	def _combine(self, x, y):
		""" Combine two group elements using the binary operator """
		pass
	
	def _isvalue(self, x):
		""" Return boolean indicating whether the given element is within the group """
		pass
	
	@property
	def identity(self):
		""" Return the group identity wrapped in the Group Element class """
		return GroupElement(self, self._identity)
	
	def __mul__(self, other):
		if not isinstance(other, Group):
			raise TypeError("Group can only be direct producted with another Group")
		
		return GroupProd(self, other)


class GroupProd(Group):
	def __init__(self, first, second):
		self.first = first
		self.second = second
	
	def _identity(self):
		return (self.first.identity, self.second.identity)
	
	def _inverse(self, gh):
		g, h = gh
		return (self.first.inverse(g), self.second.inverse(h))
	
	def _combine(self, gh1, gh2):
		(g1, h1), (g2, h2) = gh1, gh2
		return (self.first.combine(g1, g2), self.second.combine(h1, h2))
	
	def _isvalue(self, gh):
		g, h = gh
		return self.first.isvalue(g) and self.second.isvalue(h)

class GroupElement:
	def __init__(self, group, value):
		if not isinstance(group, Group):
			raise TypeError("Group Element must have a Group")
		
		assert group._isvalue(value), "Element's value is not part of the group"
		
		self.group = group
		self.value = value
	
	def __mul__(self, other):
		if not isinstance(other, GroupElement):
			raise TypeError("Group element may only be multiplied by another group element")
		
		if self.group is not other.group:
			raise ValueError("Group elements may only be multiplied by elements of the same group")
		
		newval = self.group._combine(self.value, other.value)
		return GroupElement(self.group, newval)
	
	def __truediv__(self, other):
		if not isinstance(other, GroupElement):
			raise TypeError("Group element may only be divided by another group element")
		
		if self.group is not other.group:
			raise ValueError("Group elements may only be divided by elements of the same group")
		
		newval = self.group._combine(self.value, self.group._inverse(other.value))
		return GroupElement(self.group, newval)
	
	def order(self):
		ident = self.group._identity
		
		count, work = 1, self.value
		while ident != self.value
			work = self.group._combine(work, self.value)
			count += 1
		
		return count



class CyclicGroup(Group):
	def __init__(self, size):
		self.size = size
	
	def _identity(self):
		return 0
	
	def _inverse(self, x):
		return (- x) % self.size
	
	def _combine(self, x, y):
		return (x + y) % self.size
	
	def _isvalue(self, x):
		return isinstance(x, int)

class SymmetricGroup(Group):
	def __init__(self, size):
		self.size = size
	
	def _identity(size):
		return list(range(size))
	
	def _inverse(self, perm):
		inv = [0] * self.size
		for i in range(self.size):
			inv[perm[i]] = i
		return inv
	
	def _combine(self, p1, p2):
		comb = [0] * self.size
		for i in range(self.size):
			comb[i] = p1[p2[i]]
		return comb
	
	def _isvalue(self, perm):
		if not isinstance(perm, list) or len(perm) != self.size or not isinstance(perm[0], int):
			return False
		
		for x in range(size):
			if x not in perm:
				return False
		return True



class Permutation:
	"""
	Represent a Permutation on a set using cycle notation
	
	Generics:
		T -- type of underlying set
	
	Attributes:
		cycles (list of list of T) -- list of cycles on the underlying set
	"""
	
	def __init__(self, cycles):
		self.cycles = cycles
	
	def __mul__(self, other):
		if not isinstance(other, Permutation):
			raise TypeError('Permutations can only be multiplied by other permutations')
		
		cycs = []
		for selfcyc in self.cycles:
			other(selfcyc)
		return Permutation(cycs)
	
	def __call__(self, value):
		for cyc in self.cycles:
			lencyc = len(cyc)
			for i in range(lencyc):
				if cyc[i] == value:
					if i < lencyc - 1:
						return cyc[i + 1]
					else:
						return cyc[0]
		
		return value
