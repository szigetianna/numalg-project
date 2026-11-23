# numalg-project
Our chosen topic is graph exploration and analysis. We have a previous project as a source and the plan is to further advance that work, using some ideas both from the given pdf and of our own..

##starting Plan
1. fix issues in current code, improve and understand
2. implement analysis steps listed in the project ideas from moodle
3. visualsss
4. try this on another graph model chosen from moodle project ideas
## Setup
Install the necessary libraries
    python -m pip install networkx matplotlib numpy

## Structure
-`library/graph.py` – the  `Graph` class
-`library/generators/` – network generators
-`library/analysis/` - metrics will go here
-`1.py` – original social model script THIS WILL NEED UPDATES

### The Graph class
All generators return a `Graph` and all analysis functions take one as a parameter.

### Storage of Graph class
- An undirected graph stored as a dictionary of dictionaries, `{node: {neighbour: weight}}`. 
- Every edge is stored in both directions.

### Methods of Graoh class
| Method : what it does |
|`Graph(n)` : new graph with nodes [0 ... n-1] and no edges |
|`AddNode(u)` : adds node `u` if it doesn't exist yet |
|`AddEdge(u, v, w=1.0)` : connects `u` and `v` with weight `w` (no self-loops ; overwrites an existing weight) |
| `RemoveEdge(u, v)` : checks if the node exists ; deletes if it does |
|`HasEdge(u, v)` : True if `u` and `v` are connected |
|`Neighbours(u)` : list of `u`'s neighbours |
|`Degree(u)` : number of neighbours of `u`|
|`Nodes()` : list of all nodes |
|`Edges()` : list of `(u, v, w)`, each edge once|
|`NumberOfNodes()` / `NumberOfEdges()` : counts nodes and edges respectively |
|`MeanDegree()`  : average number of neighbours |
|`ToNetworkX()` : creates a copy as a networkx graph |


