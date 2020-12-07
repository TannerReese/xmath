import collections

class Permutation:
	def __init__(self, *cycles):
		try:  # Test to see if elements of cycles are iterables
			self.cycles = tuple(map(tuple, cycles))
		except TypeError:
			self.cycles = (cycles,)
		
		self._disjointify()
	
	def _disjointify(self):
		""" Make cycles disjoint """
		moved = []
		isdisjoint = True
		for cyc in self.cycles:
			fromcyc = []
			for x in cyc:
				if x not in moved:
					moved.append(x)
				else:
					isdisjoint = False
				
				if x in fromcyc:
					raise ValueError(f"Cycle ({'  '.join(map(str, cyc))}) has duplicate value {x}")
				fromcyc.append(x)
		
		if isdisjoint:
			# Clean fixed cycles out
			self.cycles = tuple(filter(lambda cyc: len(cyc) > 1, self.cycles))
			return
		
		newcycles = []
		while len(moved) > 0:
			head = moved[0]
			newcyc = [head]
			del moved[0]
			
			curr = self(head, assumeDisjoint=False)
			while curr != head:
				newcyc.append(curr)
				moved.remove(curr)
				curr = self(curr, assumeDisjoint=False)
			
			if len(newcyc) > 1:
				newcycles.append(newcyc)
		
		self.cycles = newcycles
	
	def moved(self):
		moved = []
		for cyc in self.cycles:
			for x in cyc:
				if x not in moved:
					moved.append(x)
					yield x
	
	
	@staticmethod
	def fromfunc(func, domain):
		domain = [d for d in domain]
		used = []  # Elements that have already been assigned to a cycle
		
		cycles = []
		while len(domain) > 0:
			head = domain[0]
			cyc = [head]
			
			# Move head to used set
			used.append(domain[0])
			del domain[0]
			
			curr = func(head)
			while curr != head:
				if curr in used or curr not in domain:
					raise TypeError("Given function does not form a bijection on domain")
				
				cyc.append(curr)
				used.append(curr)
				domain.remove(curr)
				curr = func(curr)
			
			if len(cyc) > 1:
				cycles.append(cyc)
		
		return Permutation(*cycles)
	
	
	def __eq__(self, other):
		if other == 1:
			return len(self.cycles) == 0
		
		if not isinstance(other, Permutation):
			return False
		
		othercycs = list(other.cycles)
		for cyc in self.cycles:
			found, x = False, cyc[0]
			for ocyc in othercycs:
				if x in ocyc:
					i = ocyc.index(x)
					if cyc != ocyc[i:] + ocyc[:i]: # Rotate and compare cycles
						return False
					else:
						othercycs.remove(ocyc)
						found = True
						break
			
			if not found:
				return False
		
		return len(othercycs) == 0
	
	def __neq__(self, other):
		return not self.__eq__(other)
	
	
	
	def __mul__(self, other):
		if other == 1:
			return Permutation(*self.cycles)
		
		if not isinstance(other, Permutation):
			raise TypeError("Permutation can only be multiplied by another Permutation")
		
		return Permutation(*self.cycles, *other.cycles)
	
	def __rmul__(self, other):
		if other == 1:
			return Permutation(*self.cycles)
		
		return other.__mul__(self)
	
	def __div__(self, other):
		if other == 1:
			return Permutation(*self.cycles)
		
		return self.__mul__(other.inverse())
	
	def __rdiv__(self, other):
		return self.inverse().__mul__(other)
	
	def __truediv__(self, other):
		if other == 1:
			return Permutation(*self.cycles)
		
		return self.__mul__(other.inverse())
	
	def __rtruediv__(self, other):
		return self.inverse().__mul__(other)
	
	def __pow__(self, other):
		if other < 0:
			other = -other
			step = self.inverse()
		elif other > 0:
			step = self
		else:
			return Permutation()
		
		accum = Permutation()
		for i in range(other.bit_length() - 1, -1, -1):
			accum *= accum
			
			if (other >> i) & 1:
				accum *= step
		return accum
	
	def __rpow__(self, other):
		return other.__pow__(self)
	
	
	
	def parity(self):
		par = 1
		for cyc in self.cycles:
			if len(cyc) % 2 == 0:
				par = -par
		return par
	
	def order(self):
		def _lcm(a, b):
			m, n = max(a, b), min(a, b)
			while n > 0:
				m, n = n, m % n
			return a * b // m
		
		order = 1
		for cyc in self.cycles:
			order = _lcm(order, len(cyc))
		return order
	
	def inverse(self):
		return Permutation(*map(reversed, self.cycles))
	
	def __call__(self, value, assumeDisjoint=True):
		for cyc in reversed(self.cycles):
			try:
				i = cyc.index(value)
				value = cyc[(i + 1) % len(cyc)]
				
				if assumeDisjoint:
					break
			except ValueError:
				pass
		
		return value
	
	
	
	def __str__(self):
		cycstrs = ['(' + '  '.join(map(str, cyc)) + ')' for cyc in self.cycles]
		return ' '.join(cycstrs)
	
	def __repr__(self):
		cycstrs = ['(' + ', '.join(map(str, cyc)) + ')' for cyc in self.cycles]
		return f"Permutation({', '.join(cycstrs)})"
