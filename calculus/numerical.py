
def differentiate(func, h=0.001):
	"""
	Take numerical derivative with given difference in the input
	
	Args:
		func (function) -- function to take derivative of
		h (float) -- size of interval used
	
	Returns:
		function -- derivative of func
	"""
	
	halfh = h / 2
	def wrapped(x):
		return (func(x + halfh) - func(x - halfh)) / (2 * h)
	return wrapped



def stdmesh(dx=0.001):
	"""
	Creates a mesh with a given dx
	
	Args:
		dx (float) -- size of rectangles in sum
	
	Returns:
		mesh function -- mesh that has a constant dx
	"""
	
	def msh(x, fx, px, fpx):
		return dx
	return msh

def adaptmesh(dxrate=100, default=0.01):
	"""
	Creates a mesh with a varying dx
	
	Args:
		dxrate (float) -- rate of change of dx with respect to dy/dx
			default: 100
		default (float) -- initial dx and largest possible dx
			default: 0.01
	
	Returns:
		mesh function -- mesh whose dx varies with the slope of the function
	"""
	
	invdef = 1 / default
	def msh(x, fx, px, fpx):
		if px is None or fpx is None:
			return default
		else:
			diff = abs((fx - fpx) / (x - px))
			return 1 / (diff * dxrate + invdef)
	return msh

def integrate(func, bounds=(0, 1), mesh=stdmesh(), dx=None):
	"""
	Take a definite integral numerically over a given bonud with a given mesh
	
	Args:
		func (function) -- function to integrate
		bounds (tuple of float and float) -- the lower and upper bound of the integral
			default: (0, 1)
		
		mesh (mesh function) -- function to generate the dx values to integrate over
			default: stdmesh()
		dx (float) -- if not None this will be used to create a stdmesh of this size ignoring the given mesh
			default: None
	
	Returns:
		float -- value of the integral
	"""
	
	if dx is not None:
		mesh = stdmesh(dx)
	
	lower, upper = bounds
	
	priorX, currX = None, lower
	priorFx, currFx = None, func(lower)
	
	total = None
	while currX < upper:
		dx = mesh(currX, currFx, priorX, priorFx)
		priorX, currX = currX, currX + dx
		if currX > upper: # If at the top of the bound prevent overshooting
			currX, dx = upper, upper - priorX
		priorFx, currFx = currFx, func(currX)
		
		value = (currFx + priorFx) * dx / 2
		if total is None:
			total = value
		else:
			total += value
	
	return total
