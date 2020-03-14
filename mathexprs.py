import math
import operator

class Expression:
	"""
	Represents an expression containing variables
	
	Generic:
	V -- type of underlying calculations
	
	Attributes:
	function (function) -- function to apply to arguments when evaluated
	arguments (list of V or Expression) -- list of arguments to evaluate
	name (str) -- Name of the function to use in the string representation
	"""
	
	def __init__(self, func, *args, name=None, infix=False, prec=10):
		""" Initialize the Expression using the func and arguments """
		self.arguments = []
		
		isConst = True
		for a in args:
			if isinstance(a, Expression):
				if not a.constant:
					isConst = False
					self.arguments.append(a)
				else:
					self.arguments.append(a.value)
			else:
				self.arguments.append(a)
		
		if isConst and func is not None:
			self.value = func(*self.arguments)
			self.arguments = []
			self.function = None
		else:
			self.value = None
			self.function = func
		
		if name is None:
			self.name = func.__name__
		else:
			self.name = name
		
		self.infix = infix
		self.prec = prec
	
	
	def __abs__(self):
		""" Take absolute value of Expression """
		return Expression(operator.abs, self)
		
	def __pos__(self):
		""" Don't change object for positve sign """
		return self
	
	def __neg__(self):
		""" Negate Expresion """
		return Expression(operator.neg, self, name='-', infix=True, prec=8)
	
	
	
	def __add__(self, other):
		""" Add Expressions together """
		return Expression(operator.add, self, other, name='+', infix=True, prec=4)
		
	def __sub__(self, other):
		""" Subtract Expressions """
		return Expression(operator.sub, self, other, name='-', infix=True, prec=4)
	
	def __mul__(self, other):
		""" Multiply Expressions """
		return Expression(operator.mul, self, other, name='*', infix=True, prec=5)
	
	def __truediv__(self, other):
		""" Divide Expressions """
		return Expression(operator.truediv, self, other, name='/', infix=True, prec=5)
	
	def __floordiv__(self, other):
		""" Floor Division Expressions """
		return Expression(operator.floordiv, self, other, name='//', infix=True, prec=5)
	
	
	def __radd__(self, other):
		return Expression(operator.add, other, self, name='+', infix=True, prec=4)
	
	def __rsub__(self, other):
		return Expression(operator.sub, other, self, name='-', infix=True, prec=4)
	
	def __rmul__(self, other):
		return Expression(operator.mul, other, self, name='*', infix=True, prec=5)
	
	def __rtruediv__(self, other):
		return Expression(operator.truediv, other, self, name='/', infix=True, prec=5)
	
	def __rfloordiv__(self, other):
		return Expression(operator.floordiv, other, self, name='//', infix=True, prec=5)
	
	
	def __pow__(self, other):
		""" Take one Expression to the power of another """
		return Expression(operator.pow, self, other, name='**', infix=True, prec=6)
	
	def __rpow__(self, other):
		""" Same as __pow__ but allows for non-Expresion on left """
		return Expression(operator.pow, other, self, name='**', infix=True, prec=6)
	
	def __matmul__(self, other):
		""" Perform matrix multiplication on Expressions """
		return Expression(operator.matmul, self, other, name='@', infix=True, prec=5)
	
	def __rmatmul(self, other):
		return Expression(operator.matmul, other, self, name='@', infix=True, prec=5)
	
	
	@property
	def constant(self):
		return self.function is None and self.value is not None
	
	@property
	def precedence(self):
		if self.infix:
			return self.prec
		else:
			return None
	
	
	def __call__(self, **kwargs):
		"""
		Evaluate Expression using the variables in kwargs
		
		Generics:
		V -- type of value stored as values in kwargs
		
		Keyword Argument:
		**kwargs (dict of variable names and values (V)) --
			the variables used to evaluate the Expression
		
		Return: (V)
		-- evaluated result of the expression
		"""
		
		evaled = []
		for arg in self.arguments:
			if isinstance(arg, Expression):
				# Evaluate Expression before placing in the `evaled` list
				evaled.append(arg(**kwargs))
			else:
				evaled.append(arg)
		
		return self.function(*evaled)
	
	
	def __repr__(self):
		""" Create String representation of Expression using Function name and Arguments """
		argstrs = [repr(arg) for arg in self.arguments]
		
		# Use name of function if self.name not set
		name = self.function.__name__
		if self.name is not None:
			name = self.name
		
		if self.infix and len(argstrs) > 0:
			if len(argstrs) > 1:
				selfprec = self.precedence
				[arg1, arg2] = self.arguments
				
				argprec1, argprec2 = None, None
				if isinstance(arg1, Expression):
					argprec1 = arg1.precedence
				if isinstance(arg2, Expression):
					argprec2 = arg2.precedence
				
				if selfprec is not None:
					if argprec1 is not None and selfprec > argprec1:
						argstrs[0] = '(' + argstrs[0] + ')'
					
					if argprec2 is not None and selfprec > argprec2:
						argstrs[1] = '(' + argstrs[1] + ')'
				
				return argstrs[0] + ' ' + self.name + ' ' + argstrs[1]
			else:
				return self.name + ' ' + argstrs[0]
		else:
			if len(argstrs) > 0:
				return self.function.__name__ + '(' + ', '.join(argstrs) + ')'
			else:
				return name



class Var(Expression):
	"""
	Represents a variable in an expression
	
	Attribute:
	name (str) -- variable's name
	"""
	
	def __init__(self, name):
		super().__init__(None, name=name)
	
	def __call__(self, **kwargs):
		"""
		Evaluate the variable
		Returning the value of the variable from kwargs
		"""
		return kwargs[self.name]
	
	def __repr__(self):
		return self.name


def variabled(func):
	""" Expression decorator to allow use with Expression class """
	
	if not callable(func):
		return func
	
	def constant(args): # Check if all of the arguments are non-Expressions
		for a in args:
			if isinstance(a, Expression) and not a.constant:
				return False
		return True
	
	def wrapper(*args):
		if constant(args):
			return func(*args)
		else:
			# Embed func inside of Expression class
			# if some arguments are Expression classes
			return Expression(func, *args)
	
	# Retain name of original function
	wrapper.__name__ = func.__name__
	
	return wrapper


# Add all of the functions from math into mathexprs
# Making them @variabled in the process
for name, obj in vars(math).items():
	vars()[name] = variabled(obj)

