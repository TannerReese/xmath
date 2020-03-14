import math


def derivative(func):
	"""
	Take the first derivative of `func`
	Note: `func` must only use implemented operations and functions
	"""
	def deriv(x):
		return func(Differential(x, 1)).deriv
	
	return deriv


class Differential:
	"""
	Represents zeroth and first order derivatives of a function at a point
	
	Generic:
	V -- type on which calculations are performed
	
	Attributes
	value (V) -- value of the function at the point
	deriv (V) -- derivative of the function at the point
	"""
	
	def __init__(self, value, deriv):
		self.value = value
		self.deriv = deriv
	
	
	def __pos__(self):
		""" Calculate positive of value """
		return Differential(self.value, self.deriv)
	
	def __neg__(self, other):
		""" Calculate negative of value """
		return Differential(-self.value, -self.deriv)
	
	def __add__(self, other):
		""" Calculate value and derivative of arguments sum """
		if isinstance(other, Differential):
			# Derivative's Linearity
			return Differential(self.value + other.value, self.deriv + other.deriv)
		else:
			return Differential(self.value + other, self.deriv)
	
	def __radd__(self, other):
		""" Calculate value and derivative of arguments sum
			Note: addition is assumed to be ommutative for __radd__
		"""
		return self.__add__(other)
	
	def __sub__(self, other):
		""" Calculate value and derivative of arguments difference """
		if isinstance(other, Differential):
			# Derivative's Linearity
			return Differential(self.value - other.value, self.deriv - other.deriv)
		else:
			return Differential(self.value - other, self.deriv)
	
	def __rsub__(self, other):
		""" Calculate value and derivative of arguments difference """
		if isinstance(other, Differential):
			return other.__sub__(self)
		else:
			return Differential(other - self.value, -self.deriv)
	
	def __mul__(self, other):
		""" Calculate value and derivative of arguments product """
		if isinstance(other, Differential):
			value = self.value * other.value
			# Product Rule
			deriv = self.deriv * other.value + self.value * other.deriv
			return Differential(value, deriv)
		else:
			# Derivative's Linearity
			return Differential(self.value * other, self.deriv * other)
	
	def __rmul__(self, other):
		""" Calculate value and derivative of arguments product
			Note: multiplication is assumed commutative for __rmul__
		"""
		return self.__mul__(other)
	
	def __div__(self, other):
		""" Calculate value and derivative of arguments quotient """
		if isinstance(other, Differential):
			value = self.value / other.value
			# Quotient Rule
			deriv = (self.deriv * other.value - self.value * other.deriv) / (other.value * other.value)
			return Differential(value, deriv)
		else:
			# Derivative's Linearity
			return Differential(self.value / other, self.deriv / other)
	
	def __rdiv__(self, other):
		""" Calculate value and derivative of arguments quotient """
		if isinstance(other, Differential):
			return other.__div__(self)
		else:
			return Differential(other / self.value, -other * self.deriv / (self.value * self.value))
	
	def __pow__(self, other):
		""" Combine differential to find value and derivative of their power """
		if isinstance(other, Differential):
			value = self.value ** other.value
			# Rule for derivative of powers in both the exponent and the base
			deriv = value * (log(self.value) * other.deriv + other.value * self.deriv / self.value)
			return Differential(value, deriv)
		else:
			return Differential(self.value ** other, self.deriv * other * self.value ** (other - 1))
	
	def __rpow__(self, other):
		""" Combine differential to find value and derivative of their power """
		if isinstance(other, Differential):
			return other.__pow__(self)
		else:
			return Differential(other ** self.value, log(other) * self.deriv * other ** self.value)
	
	def __matmul__(self, other):
		""" Calculate matrix multiplication using product rule """
		if isinstance(other, Differential):
			value = self.value * other.value
			# Product Rule
			deriv = self.deriv * other.value + self.value * other.deriv
			return Differential(value, deriv)
		else:
			return Differential(self.value * other, self.deriv * other)
	
	def __rmatmul__(self, other):
		""" Calculate matrix multiplication using product rule
			Note: matrix multiplication may be non-commutative
		"""
		if isinstance(other, Differential):
			return other.__matmul__(self)
		else:
			return Differential(other * self.value, other * self.deriv)



def differentiable(func, *drvs):
	"""
	Convert a function into one that can be applied to Differentials
	
	Arguments:
	func (function) -- function to be wrapped
	drvs (list of function) -- derivatives of function
		with respect to argument
	
	Return: (function)
	-- function that may take Differentials in place of numerical arguments
	"""
	
	def anyDiffer(args):
		for a in args:
			if isinstance(a, Differential):
				return True
		return False
	
	def onDiffer(*args):
		if not anyDiffer(args):
			return func(*args)
		
		# Get the arguments for the `func`
		evaled = []
		for a in args:
			if isinstance(a, Differential):
				evaled.append(a.value)
			else:
				evaled.append(a)
		
		# Iterate through derivatives for each argument
		# Summing the derivatives into `total`
		total = None
		for i in range(len(drvs)):
			if i < len(args):
				a = args[i]
			else:
			 	break
			
			# If `a` is a differential then calculate the partial derivative
			if isinstance(a, Differential):
				term = drvs[i](*evaled) * a.deriv
				
				if total is None:
					total = term
				else:
					total += term
		
		if total is None:
			total = 0
		
		return Differential(func(*evaled), total)
	
	return onDiffer



# Define math functions and their derivatives

exp = differentiable( math.exp, lambda x: math.exp(x) )
log = differentiable( math.log, lambda x: 1 / x )
sqrt = differentiable( math.sqrt, lambda x: 1 / (2 * math.sqrt(x)) )

sin = differentiable( math.sin, math.cos )
cos = differentiable( math.cos, lambda x: -math.sin(x) )
tan = differentiable( math.tan, lambda x: 1 / (math.cos(x) ** 2) )

sinh = differentiable( math.sinh, math.cosh )
cosh = differentiable( math.cosh, math.sinh )
tanh = differentiable( math.tanh, lambda x: 1 / (math.cosh(x) ** 2) )
