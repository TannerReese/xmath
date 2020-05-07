from . import vector

class Matrix:
	def __init__(self, *rows):
		self.rows = tuple(map(tuple, rows))
		assert len(self.rows) > 0, "Matrix must have non-zero number of rows"
		
		colNum = len(self.rows[0])
		for row in self.rows:
			if len(row) != colNum:
				raise ValueError(f"Dimension of row Vectors does not match {colNum} and {len(row)}")
	
	@staticmethod
	def fromRows(*rowVecs):
		return Matrix(v.components for v in rowVecs)
	
	@staticmethod
	def fromColumns(colVecs):
		return Matrix(v.components for v in colVecs).transpose()
	
	
	
	@property
	def shape(self):
		return (len(self.rows), len(self.rows[0]))
	
	def __eq__(self, other):
		if not isinstance(other, Matrix):
			return False
		
		rows, cols = self.shape
		if (rows, cols) != other.shape:
			return False
		
		for r in range(rows):
			for c in range(cols):
				if self.rows[r][c] != other.rows[r][c]:
					return False
		return True
	
	def __neq__(self, other):
		return not self.__eq__(other)
	
	
	
	def __getitem__(self, key):
		return self.rows[key[0]][key[1]]
	
	def row(self, key):
		return vector.Vector(*self.rows[key])
	
	def column(self, key):
		return vector.Vector(*(r[key] for r in self.rows))
	
	
	
	def __add__(self, other):
		if not isinstance(other, Matrix):
			raise TypeError("Matrix can only be added to another Matrix")
		
		selfRows, selfCols = self.shape
		otherRows, otherCols = other.shape
		if selfCols != otherCols:
			raise ValueError(f"Matrix Column mismatch between {selfCols} and {otherCols}")
		elif selfRows != otherRows:
			raise ValueError(f"Matrix Row mismatch between {selfRows} and {otherRows}")	
		
		return Matrix(*(tuple(self.rows[r][c] + other.rows[r][c] for c in range(selfCols)) for r in range(selfRows)))
	
	def __sub__(self, other):
		if not isinstance(other, Matrix):
			raise TypeError("Matrix can only be added to another Matrix")
		
		selfRows, selfCols = self.shape
		otherRows, otherCols = other.shape
		if selfCols != otherCols:
			raise ValueError(f"Matrix Column mismatch between {selfCols} and {otherCols}")
		elif selfRows != otherRows:
			raise ValueError(f"Matrix Row mismatch between {selfRows} and {otherRows}")
		
		return Matrix(*(tuple(self.rows[r][c] - other.rows[r][c] for c in range(selfCols)) for r in range(selfRows)))
	
	def __mul__(self, other):
		rs, cs = self.shape  # Get number of rows and columns in `self`
		if isinstance(other, Matrix):
			otherRows, otherCols = other.shape
			if cs != otherRows:
				raise ValueError(f"Matrix Row-Column mismatch between {cs} and {otherRows}")
			
			rows = []
			for r in range(rs):
				rowtmp = [None] * otherCols
				for c in range(otherCols):
					total = None
					for k in range(cs):
						prod = self.rows[r][k] * other.rows[k][c]
						
						if total is None:
							total = prod
						else:
							total += prod
					
					rowtmp[c] = total
				rows.append(rowtmp)
			
			return Matrix(*rows)
		elif isinstance(other, vector.Vector):
			comps = [None] * cs
			for r in range(rs):
				total = None
				for k in range(cs):
					prod = self.rows[r][k] * other.components[k]
					
					if total is None:
						total = prod
					else:
						total += prod
				comps[r] = total
			return vector.Vector(*comps)
		else:
			return Matrix(*(tuple(other * self.rows[r][c] for c in range(cs)) for r in range(rs)))
	
	def __rmul__(self, other):
		if isinstance(other, Matrix):
			return other.__mul__(self)
		else:
			return self.__mul__(other)
	
	def __matmul__(self, other):
		return self.__mul__(other)
	
	def __div__(self, other):
		return self.__truediv__(other)
	
	def __truediv__(self, other):
		rs, cs = self.shape
		if isinstance(other, Matrix):
			otherInv = other.inverse()
			return self.__mul__(otherInv)
		else:
			return Matrix(*(tuple(self.rows[r][c] / other for c in range(cs)) for r in range(rs)))
	
	def __floordiv__(self, other):
		rs, cs = self.shape
		return Matrix(*(tuple(self.rows[r][c] // other for c in range(cs)) for r in range(rs)))
	
	def __rdiv__(self, other):
		if isinstance(other, Matrix):
			return other.__div__(self)
		else:
			return self.inverse().__mul__(other)
	
	def __rtruediv__(self, other):
		return self.__rdiv__(other)
	
	
	
	def __pow__(self, other):
		if not isinstance(other, int):
			raise TypeError("Matrix can only be raised to integer powers")
		
		rows, cols = self.shape
		if rows != cols:
			raise ValueError("Only Square Matrices can be taken to a power")
		
		if other == 0:
			return identity(rows)
		elif other < 0:
			other = -other
			work = self.inverse()
		else:
			work = self
		
		prod = None
		while other > 0:
			if other & 1 == 1:
				if prod is None:
					prod = work
				else:
					prod *= work
			
			other >>= 1
			work *= work
		
		return identity(rows) if prod is None else prod
	
	
	
	def __repr__(self):
		rowgen = ('(' + ', '.join(map(str, row)) + ')' for row in self.rows)
		return 'Matrix(' + ', '.join(rowgen) + ')'
	
	def __str__(self):
		return '\n'.join('[' + ', '.join(map(str, row)) + ']' for row in self.rows)
	
	
	
	def transpose(self):
		rows, cols = self.shape
		return Matrix(*(tuple(self.rows[r][c] for r in range(rows)) for c in range(cols)))
	
	def rref(self):
		aug = AugmentedMatrix(self)
		aug.reduce(0)
		return aug[0]
	
	def inverse(self):
		rs, cs = self.shape
		if rs != cs:
			raise ValueError("Matrix Inverse can only be calculated for Square Matrices")
		
		aug = AugmentedMatrix(self, identity(rs))
		aug.reduce(0)
		if aug[0] != identity(rs):
			raise ZeroDivisionError("Matrix is Singular")
		
		return aug[1]
	
	def nullspace(self):
		rs, cs = self.shape
		aug = AugmentedMatrix(self)
		aug.reduce(0)
		
		# Get pivots
		pivots = []
		for r in range(rs):
			col, _ = aug.leading(0, r)
			if col is not None:
				pivots.append(col)
			else:
				break
		
		# Get null space basis
		basis = []
		for c in range(cs):
			if c not in pivots:
				comps = [0] * cs
				freeVec = aug[0].column(c)
				
				for r in range(len(pivots)):
					comps[pivots[r]] = freeVec[r]
				
				comps[c] = -1
				basis.append(vector.Vector(*comps))
		return basis



class AugmentedMatrix:
	def __init__(self, *matrices):
		assert len(matrices) > 0, "Augmented Matrix must contain at least one Matrix"
		
		self.matrices = list(map(lambda mat: list(map(list, mat.rows)), matrices))
		self.rows = len(self.matrices[0])
		
		for mat in self.matrices:
			if self.rows != len(mat):
				raise ValueError(f"Row number mismatch in Augmented Matrix between {self.rows} and {len(mat)}")
			
			cols = len(mat[0])
			for row in mat:
				if len(row) != cols:
					raise ValueError(f"Column number mismatch in Augmented Matrix between {len(row)} and {cols}")
	
	def __getitem__(self, key):
		return Matrix(*(self.matrices[key]))
	
	
	
	def swap(self, r1, r2):
		if r1 < 0 or self.rows <= r1:
			raise IndexError(f"Augmented Matrix Row index out of bounds {r1}")
		elif r2 < 0 or self.rows <= r2:
			raise IndexError(f"Augmented Matrix Row index out of bounds {r2}")
		
		for mat in self.matrices:
			tmp = mat[r1]
			mat[r1] = mat[r2]
			mat[r2] = tmp
	
	def add(self, targetRow, sourceRow, scale):
		if targetRow < 0 or self.rows <= targetRow:
			raise IndexError(f"Augmented Matrix Row index out of bounds {targetRow}")
		elif sourceRow < 0 or self.rows <= sourceRow:
			raise IndexError(f"Augmented Matrix Row index out of bounds {sourceRow}")
		
		for mat in self.matrices:
			for c in range(len(mat[0])):
				mat[targetRow][c] += scale * mat[sourceRow][c]
	
	def scale(self, row, scale):
		if row < 0 or self.rows <= row:
			raise IndexError(f"Augmented Matrix Row index out of bounds {row}")
		
		for mat in self.matrices:
			for c in range(len(mat[row])):
				mat[row][c] *= scale
	
	
	
	def leading(self, matrixInd, row, zeroVal=0):
		mat = self.matrices[matrixInd]
		if row < 0 or self.rows <= row:
			raise IndexError(f"Augmented Matrix Row index out of bounds {row}")
		
		for c in range(len(mat[row])):
			val = mat[row][c]
			if val != zeroVal:
				return (c, val)
		
		return (None, zeroVal)
	
	def reduce(self, targetMat, zeroVal=0):
		pivotRow = 0
		cols = len(self.matrices[targetMat][0])
		
		for c in range(cols):
			p = pivotRow
			while p < self.rows:
				leadVal = self.matrices[targetMat][p][c]
				if leadVal != zeroVal:
					break
				
				p += 1
			
			if p >= self.rows:
				# Column contains no viable pivots and so is free
				continue
			self.scale(p, 1 / leadVal)
			self.swap(p, pivotRow)
			
			for r in range(self.rows):
				if r != pivotRow:
					self.add(r, pivotRow, -self.matrices[targetMat][r][c])
			
			# Shift pivotRow so rows that are already
			# used for pivots are not reused
			pivotRow += 1



def identity(dims=3, zeroVal=0, oneVal=1):
	return Matrix(*(tuple(oneVal if r == c else zeroVal for c in range(dims)) for r in range(dims)))

def zero(shape=(3, 3), zeroVal=0):
	return Matrix(*((zeroVal for c in range(shape[1])) for r in range(shape[0])))
