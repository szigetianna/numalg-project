class Graph:
#format of the graph class is dict[int, dict[int, float]]
#Undirected graph stored as dict[node,dict[neighbor, weight]].


    def __init__(self, n=0):
        self.adj={}   # creating self, which with zero nodes as a default
        # n = the amount of nodes that will be created
        for i in range(n):
            self.adj[i]={} #each node gets its won dictionary

    def AddNode(self, u):
        self.adj.setdefault(u, {})

    def AddEdge(self, u, v, w=1.0):   # connects node u to node v with weight w 
        #the default weight is 1.0
        if u==v:
            return  # no self-loops
        self.AddNode(u)
        self.AddNode(v)
        self.adj[u][v]=w # the connection has no direction
        self.adj[v][u]=w # it is stored in both

    def RemoveEdge(self, u, v): #removed the edge between node u and v
        if u in self.adj and v in self.adj[u]: # checking if they are neighbours
            self.adj[u].pop(v, None)
            self.adj[v].pop(u, None) #pop removing v from u and vice versa
        #none is there in case the edge does not exist

    def HasEdge(self, u, v):
        if u not in self.adj:   # u doesn't even exist in the graph
            return False
        NeighboursOfU=self.adj[u]  
        return v in NeighboursOfU # checking if v is an element of NeighboursOfU
      # return a bool !!

    def Neighbours(self, u):
        return list(self.adj[u].keys())  #returning only the keys of the dict

    def Degree(self, u):
        return len(self.adj[u])

    def Nodes(self):
        return list(self.adj)

    def Edges(self):
        result=[]
        for u, nb in self.adj.items():  # each node u and its neighbour dict nb
            for v, w in nb.items():  #each neighbour v of u, with weight w
                if u<v:  # only keep the edge once 
                    result.append((u, v, w))
        return result #return each edge just once, with weight

    def NumberOfNodes(self):
        return len(self.adj)

    def NumberOfEdges(self):
        total=0
        for u in self.adj:  # go through every node
            NeighbourOfU=self.adj[u]  
            total=total+len(NeighbourOfU)   # add how many connections u has
        return total//2  # each edge was counted twice
    #// for integer divison bc ofc this has to be an integer

    def MeanDegree(self): #Average of number of neighbours per node
        n=self.NumberOfNodes()
        if n!=0:
            return 2*self.NumberOfEdges()/n
        else:
            return 0.0 

    def ToNetworkX(self):  
        import networkx as nx #we need to connect the functions in networkx 
        #to the graph class 
        G=nx.Graph()
        G.add_nodes_from(self.adj) #adding each node
        G.add_weighted_edges_from(self.Edges())  #adds each edge w weight
        # Edges() return a tuple of ( u , v , w) which the add_weighted_edges
        #function uses
        return G #returning a graph that networkc can use 