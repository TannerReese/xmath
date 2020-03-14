

def unique(lst):
	""" Removes all duplicate elements from a list """
	
	nlst = []
	for e in lst:
		if e not in nlst:
			nlst.append(e)
	return nlst

class Equivalence:
	"""
	Represent an equivalence relation by mapping
	
	Attribute:
	morphism (function) -- a mapping from one set to another
		Default: the identity mapping
	"""
	
	def __init__(self, morphism=lambda x: x):
		""" Initialize Equivalence by setting the morphism """
		self.morphism = morphism
	
	def equivalent(self, x, y):
		""" Check whether `x` and `y` are equal after application of the morphism """
		return self.morphism(x) == self.morphism(y)



class Set:
	"""
	Set of values supporting standard set operations
	
	Generic:
	V -- type of elements stored in Set
	
	Attributes:
	elements (list of V) -- list of elements in the Set
	"""
	
	def __init__(self, *args):
		""" Initialize a Set using a variable length list of arguments """
		
		self.__index = 0
		self.elements = unique(args)
	
	def copy(self):
		return Set(*self.elements)
	
	
	
	def __eq__(self, other):
		""" Check equality between Sets """
		
		assert isinstance(other, Set), "Second argument to equality is not Set"
		return self.includes(other) and other.includes(self)
	
	def includes(self, other):
		"""
		Check if Set `A` includes Set `B`
		or equivalently `B` is a subset of `A`
		"""
		
		assert isinstance(other, Set), "Argument to inclusion is not Set"
		for el in other.elements:
			if el not in self.elements:
				return False
		return True
	
	
	def __len__(self):
		""" Number of unique elements in the set """
		
		self.elements = unique(self.elements)
		return len(self.elements)
	
	def __contains__(self, val):
		""" Check whether this set contains a value `val` """
		
		return val in self.elements
	
	
	def __iter__(self):
		""" Initialize iterator over this set """
		
		self.__index = 0
		self.elements = unique(self.elements)
		return self
	
	def __next__(self):
		""" Obtain next element while iterating over the set """
		
		if self.__index < len(self.elements):
			return self.elements(self.__index)
		else:
			raise StopIteration
	
	
	
	def __and__(self, other):
		""" Find the intersection between the two sets """
		
		assert isinstance(other, Set), "Second argument to conjunction is not Set"
		nelems = []
		for el in self.elements:
			if el in other.elements and el not in nelems:
				nelems.append(el)
		return Set(*nelems)
	
	
	
	def __add__(self, other):
		""" Find the union between the two sets """
		
		assert isinstance(other, Set), "Second argument to addition is not Set"
		return self.__or__(other)
	
	def __or__(self, other):
		""" Find the union between the two sets """
		
		assert isinstance(other, Set), "Second argument to disjunction is not Set"
		
		nelems = unique(self.elements)
		for el in other.elements:
			if el not in nelems:
				nelems.append(el)
		return Set(*nelems)
	
	
	
	def __sub__(self, other):
		""" Find the set difference between two sets """
		
		assert isinstance(other, Set), "Second argument to subtraction is not Set"
		
		nelems = []
		for el in self.elements:
			if el not in nelems and el not in other.elements:
				nelems.append(el)
		return Set(*nelems)
	
	
	
	def __xor__(self, other):
		""" Find the symmetrix difference (XOR) between two sets """
		
		assert isinstance(other, Set), "Second argument to exclusive disjunction is not Set"
		
		nelems = []
		for el in self.elements:
			if el not in nelems and el not in other.elements:
				nelems.append(el)
		
		for el in other.elements:
			if el not in nelems and el not in self.elements:
				nelems.append(el)
		
		return Set(*nelems)
	
	
	
	@staticmethod
	def join(a, b):
		""" Find the union between the two sets """
		assert type(a) == Set and type(b) == Set, "Only sets can be joined"
		return a.__or__(b)
	
	@staticmethod
	def meet(a, b):
		""" Find the intersection between the two sets """
		assert type(a) == Set and type(b) == Set, "Only sets can be meeted"
		return a.__and__(b)
	
	@staticmethod
	def diff(a, b):
		""" Find the set difference between two sets """
		assert type(a) == Set and type(b) == Set, "Only sets can be diffed"
		return a.__sub__(b)
	
	@staticmethod
	def symmdiff(a, b):
		""" Find the symmetric difference between two sets """
		
		assert type(a) == Set and type(b) == Set, "Only sets can be diffed"
		return a.__xor__(b)
	
	
	
	def __mul__(self, other):
		""" Find the cartesian product between two sets """
		
		assert isinstance(other, Set), "Second argument to multiplication is not Set"
		
		pairs = []
		for sElem in unique(self.elements):
			for oElem in unique(other.elements):
				pairs.append((sElem, oElem))
		return Set(*pairs)
	
	def __div__(self, other):
		""" Find the quotient set of a set by an equivalence relation """
		
		assert type(other) == Equivalence, "Second argument to division is not Equivalence"
		
		classes = []
		for el in unique(self.elements):
			fits = False # Track whether `el` fits into an existing equivalence class
			for cls in classes:
				if len(cls) > 0 and other.equivalent(cls[0], el):
					cls.append(el)
					fits = True
					break
			
			if not fits:
				classes.append([el])
		
		return Set(*classes)
	
	
	
	def __str__(self):
		""" Use mathematical notation to show Set """
		ss = []
		for el in self.elements:
			# Use mathematical notation for internal Sets
			if isinstance(el, Set):
				ss.append(str(el))
			else:
				ss.append(repr(el))
		return '{' + ', '.join(ss) + '}'
	
	def __repr__(self):
		""" Use python appropriate constructor to show Set """
		return 'sets.Set(' + ', '.join(map(repr, self.elements)) + ')'
	
	
	
	def insert(self, value):
		""" Insert `value` into the set """
		if value not in self.elements:
			self.elements.append(value)
	
	
	
	def powerset(self):
		""" Generate the Set of all subsets of this one """
		
		subsets = [Set()]
		for el in unique(self.elements):
			newsets = []
			for s in subsets:
				newsets.append(Set(*s.elements, el))
			subsets += newsets
		return Set(*subsets)


def powerset(self):
	return self.powerset()



def image(func):
	""" Convert a function into one that takes sets and returns there images """
	
	def imageOfSet(s): # Function wrapper that will take set and return image
		assert type(s) == Set, "Only set can have images"
		return Set(*unique([func(x) for x in s.elements]))
	
	return imageOfSet


def preimage(domain, func=None):
	"""
	Convert a function into one that takes sets and returns there preimage within domain
		Note: `domain` must be the Set of inputs to `func`
	"""
	
	assert type(domain) == Set, "Domain is not a Set"
	def funcgen(f): # Function decorator to convert to function on set
		def preimageOfSet(s): # Function wrapper that will take set and return preimage
			assert type(s) == Set, "Only sets can have preimages"
			return Set(*[x for x in domain.elements if f(x) in s.elements])
		
		return preimageOfSet
	
	if func is None:
		return funcgen
	else:
		return funcgen(func)
