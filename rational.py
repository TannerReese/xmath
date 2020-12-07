def gcd(a, b):
	while b != 0:
		a, b = b, a % b
	
	return a

def bezout(a, b):
	x1, x2 = 1, 0
	y1, y2 = 0, 1
	
	while b != 0:
		q, r = a // b, a % b
		a, b = b, r
		
		x1, x2 = x2, x1 - q * x2
		y1, y2 = y2, y1 - q * y2
	
	return (x1, y1, a)

class Ratio:
	def __init__(self, n, d):
		g = gcd(n, d)
		self.num = n // g
		self.den = d // g
	
	def simplify(self):
		g = gcd(self.num, self.den)
		self.num //= g
		self.den //= g
	
	def __eq__(self, other):
		if isinstance(other, Ratio):
			return self.num * other.den == self.den * other.num
		else:
		 	return self.num == self.den * other
	
	def __req__(self, other):
		return self.__eq__(other)
	
	
	
	def __int__(self):
		return int(self.num) // int(self.den)
	
	def __float__(self):
		return float(self.num) / float(self.den)
	
	
	
	def __abs__(self):
		return Ratio(abs(self.num), abs(self.den))
	
	def __pos__(self):
		return self
	
	def __neg__(self):
		return Ratio(-self.num, self.den)
	
	
	
	def __add__(self, other):
		if isinstance(other, Ratio):
			num = self.num * other.den + other.num * self.den
			den = self.den * other.den
		else:
			num = self.num + other * self.den
			den = self.den
		return Ratio(num, den)
	
	def __sub__(self, other):
		if isinstance(other, Ratio):
			num = self.num * other.den - other.num * self.den
			den = self.num * self.den
		else:
			num = self.num - other * self.den
			den = self.den
		return Ratio(num, den)
	
	def __mul__(self, other):
		if isinstance(other, Ratio):
			return Ratio(self.num * other.num, self.den * other.den)
		else:
			return Ratio(self.num * other, self.den)
	
	def __div__(self, other):
		if isinstance(other, Ratio):
			return Ratio(self.num * other.den, self.den * other.num)
		else:
			return Ratio(self.num, self.den * other)
	
	def __truediv__(self, other):
		return self.__div__(other)
	
	
	def __radd__(self, other):
		return self.__add__(other)
	
	def __rsub__(self, other):
		return self.__neg__().__add__(other)
	
	def __rmul__(self, other):
		return self.__mul__(other)
	
	def __rdiv__(self, other):
		return Ratio(self.den, self.num).__mul__(other)
	
	def __rtruediv__(self, other):
		return Ratio(self.den, self.num).__mul__(other)
	
	
	def __str__(self):
		self.simplify()
		return f"{self.num} / {self.den}"
	
	def __repr__(self):
		self.simplify()
		return f"rational.Ratio({self.num}, {self.den})"



if __name__ == '__main__':
	a, b = 4839483, 1739372
	x, y, g = bezout(a, b)
	print(f"{x} * {a} + {y} * {b} = {g} ; {x * a + y * b}")
