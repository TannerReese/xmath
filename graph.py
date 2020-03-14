class Graph:
    """
    Class to represent a graph as a collection of vertices and edges
    
    Generics:
    I -- type to index and identify different vertices
    V -- value stored in each vertex
    
    Attributes:
    vertices (dict of (I, V)) -- identifies the value of each vertex using the vertex id
    inedges (dict of (I, list of I)) -- for each key `v` the dict holds a list of vertices that connect to `v`
    outedges (dict of (I, list of I)) -- for each key `v` the dict holds a list of vertices that `v` connects to
    """
    
    def __init__(self, verts = {}, edges = []):
        """
        Initialize Graph with vertices and edges
        
        Keyword Arguments:
        verts (dict of (I, V)) -- the vertex values keyed by the associated vertex ids
        edges (list of (tuple of I and I)) -- pairs of vertex ids corresponding to each edge
        """
        
        self.vertices = verts
        self.inedges = {v: [] for v in verts}
        self.outedges = {v: [] for v in verts}
        
        for e in edges:
            start, end = e
            if start in verts and end in verts:
                self.inedges[end].append(start)
                self.outedges[start].append(end)
    
    def adjacent(self, x, y, isdirected = False):
        """
        Check adjacency between vertices
        
        Arguments:
        x (I) -- First vertex
        y (I) -- Second vertex
        
        Keyword Arguments:
        isdirected (bool) -- Whether to only check edges from `x` to `y`
        
        Return: (bool)
        -- Bool representing whether vertices `x` and `y` are adjacent in the graph
        """
        
        if x not in self.vertices:
            raise IndexError("First object in edge pair is not a valid vertex")
        
        if y not in self.vertices:
            raise IndexError("Second object in edge pair is not a valid vertex")
        
        for v in self.outedges[x]:
            if v == y:
                return True
        
        if not isdirected:
            for v in self.outedges[y]:
                if v == x:
                    return True
        
        return False
    
    
    
    def __getitem__(self, key):
        """
        Get the value associated with a vertex
        
        Arguments:
        key (I) -- id for the vertex of interest
        
        Return: (V)
        -- value stored at that vertex
        """
        
        if key not in self.vertices:
            raise IndexError("Index argument is not a valid Vertex")
        
        return self.vertices[key]
    
    def __setitem__(self, key, value):
        """
        Set the value associated with a vertex
        
        Arguments:
        key (I) -- id for the vertex of interest
        value (V) -- value to store at that vertex
        """
        
        if key not in self.vertices:
            raise IndexError("Index argument is not a valid Vertex")
        
        self.vertices[key] = value
    
    
    
    def indegree(self, x):
        """
        Find the number of edges entering a vertex
        
        Arguments:
        x (I) -- id for the vertex of interest
        
        Return: (int)
        -- number of edges entering the vertex `x`
        """
        
        return len(self.inedges[x])
    
    def outdegree(self, x):
        """
        Find the number of edges exiting a vertex
        
        Arguments:
        x (I) -- id for the vertex of interest
        
        Return: (int)
        -- number of edges exiting the vertex `x`
        """
        
        return len(self.outedges[x])
    
    def degree(self, x):
        """
        Find the number of edges connected to a vertex
        
        Arguments:
        x (I) -- id for the vertex of interest
        
        Return: (int)
        -- number of edges connected to the vertex `x`
        """
        
        return len(self.inedges[x]) + len(self.outedges[x])
    
    
    
    def transpose(self):
        """ Reverse the direction of all of the edges """
        
        self.inedges, self.outedges = self.outedges, self.inedges
	
	def __mul__(self, other):
		"""
		Take the cartesian graph product of two Graphs
		Given graph G with identifiers I and vertices X
		Given graph H with identifiers J and vertices Y
		The resultant graph will have identifiers (I, J) and vertices (X, Y)
		"""
		
		if not isinstance(other, Graph):
			raise TypeError("Graphs may only be multiplied with other Graphs")
		
		verts = {}
		edges = []
		for i, x in self.vertices.items():
			for j, y in other.vertices.items():
				verts[(i, j)] = (x, y)
				
				for i2 in self.outedges[i]:
					edges.append(((i, j), (i2, j)))
				
				for j2 in other.outedges[j]:
					edges.append(((i, j), (i, j2)))
		
		return Graph(verts, edges)
    
    
    
    def addvertex(self, val, v, outs = [], ins = []):
        """
        Add a vertex to the graph with optional connections
        
        Arguments:
        val (V) -- value to store in new vertex
        v (I) -- id for the new vertex
        
        Keyword Arguments:
        outs (list of I) -- vertices to connect the new vertex to
        ins (list of I) -- vertices from which to connect edges to new vertex
        """
        
        self.vertices[v] = val
        
        for i in ins:
            if i not in self.vertices:
                raise IndexError(f'Object {i} among the in-vertices is not a valid Vertex')
            self.outedges[i].append(v)
        self.inedges[v] = ins
        
        for o in outs:
            if o not in self.vertices:
                raise IndexError(f'Object {o} among the out-vertices is not a valid Vertex')
            self.inedges[o].append(v)
        self.outedges[v] = outs
    
    def addedge(self, start, end):
        """
        Add new edge to the graph
        
        Arguments:
        start (I) -- source of edge
        end (I) -- destination of edge
        """
        
        if start not in self.vertices:
            raise IndexError("First object in edge pair is not a valid Vertex")
        
        if end not in self.vertices:
            raise IndexError("Second object in edge pair is not a valid Vertex")
        
        self.inedges[end].append(start)
        self.outedges[start].append(end)
    
    
    
    def geodesic(self, x, y, isdirected = False):
        """
        Find the shortest path between two vertices
        
        Arguments:
        x (I) -- id of vertex to start from
        y (I) -- id of vertex to go to
        
        Keyword Arguments:
        isdirected (bool) -- Whether to allow paths that go against direction of edges
		
		Return: (list of I)
		-- list of vertex ids representing the shortest path fro `x` to `y`
        """
        
        if x not in self.vertices:
            raise IndexError("First argument is not a valid Vertex")
        
        if y not in self.vertices:
            raise IndexError("Second argument is not a valid Vertex")
        
        if x == y:
            return [x]
        
        
        checkedVerts = []
        
        def extend(ps):
            nps = {}
            for end, path in ps.items():
                
                searchArea = self.outedges[end]
                if not isdirected:
                    searchArea += self.inedges[end]
                
                for v in searchArea:
                    if v not in checkedVerts:
                       if v not in nps or len(nps[v]) > path + 1:
                           nps[v] = path + [v]
            
            checkedVerts += ps.values()
            return nps
        
        
        Xpaths, Ypaths = {x: [x]}, {y: [y]}
        shortest = [x]
        def hasconnect():
            for v in Xpaths.values():
                if v in Ypaths:
                    shortest = Xpaths[v][:-1] + list(reversed(Ypaths[v]))
                    return True
            
            return False
        
        while True:
            Xpaths = extend(Xpaths)
            if hasconnect():
                break
            
            Ypaths = extend(Ypaths)
            if hasconnect():
                break
        
        return shortest
    
    def distance(self, x, y, isdirected = False):
        """
        Find the length of the geodesic between two vertices

        Arguments:
        x (I) -- first vertex id
        y (I) -- second vertex id
        
        Keyword Arguments:
        isdirected (bool) -- whether to allow traveling across edge in wrong direction
        
        Return: (Int)
        -- number of edges needed to travel to get from `x` to `y`
        """
        
        return len(self.geodesic(x, y, isdirected)) - 1
    
    def digeodesic(self, x, y):
        """ Find shortest path that follows edge directions """
        
        return self.geodesic(x, y, True)
    
    def didistance(self, x, y):
        """ Find length of the shortest path that follows edge directions """
        
        return self.distance(x, y, True)
