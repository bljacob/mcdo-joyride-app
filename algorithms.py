"""
File: algorithms.py
Graph-processing algorithms
"""
from linkedstack import LinkedStack
import math

def topoSort(g, startLabel = None):
  """Returns a stack of vertices representing a topological
order of vertices in the graph."""
  stack = LinkedStack()
  g.clearVertexMarks()
  for v in g.vertices():
    if not v.isMarked():
      dfs(g, v, stack)
  return stack
  
def dfs(g, v, stack):
  v.setMark()
  for w in g.neighboringVertices(v.getLabel()):
    if not w.isMarked():
      
      dfs(g, w, stack)
  stack.push(v)


###### TO FIX vvvvvvv

def shortestPaths(g, startLabel):
  """Returns a two-dimensional grid of N rows and three
columns, where N is the number of vertices. The first
column contains the vertices. The second column contains the distance from the start vertex to this vertex.
The third column contains the immediate parent vertex
of this vertex, if there is one, or None otherwise.

INITIALIZATION STEP:
for each vertex in the graph
  Store vertex in the current row of the results grid
If vertex = source vertex
  Set the row’s distance cell to 0
  Set the row’s parent cell to undefined
  Set included[row] to True
Else if there is an edge from source vertex to vertex
  Set the row’s distance cell to the edge’s weight
  Set the row’s parent cell to source vertex
  Set included[row] to False
Else
  Set the row’s distance cell to infinity
  Set the row’s parent cell to undefined
  Set included[row] to False
Go to the next row in the results grid

COMPUTATION STEP:
Do
  Find the vertex F that is not yet included and has the minimal
  distance in the results grid
  Mark F as included
  For each other vertex T not included
    If there is an edge from F to T
        Set new distance to F’s distance + edge’s weight
        If new distance < T’s distance in the results grid
          Set T’s distance to new distance
          Set T’s parent in the results grid to F
While at least one vertex is not included
"""

  ### INITIATION STEP
  cols = 3
  rows = len(g)
  results = [[0 for i in range(cols)] for j in range(rows)]
  included = [False for i in range(rows)]
  s = ""
  i = 0
  # print("startLabel",startLabel)
  for v in g.vertices():
    if str(v) == startLabel:
      results[i][0] = str(v)
      results[i][1] = 0
      results[i][2] = "undefined"
      included[i] = True

    elif v in g.getVertex(startLabel).neighboringVertices():
      # print(v, "connected to source")
      start = g.getVertex(startLabel)
      e = start.getEdgeTo(v)
      # print(e)
      results[i][0] = str(v)
      results[i][1] = e.getWeight()
      results[i][2] = str(start)
      included[i] = False

    else:
      results[i][0] = str(v)
      results[i][1] = math.inf
      results[i][2] = "undefined"
      included[i] = False
      
    i += 1

  # print(results)
  # print(included)

  included_count = 0

  
  ### COMPUTATION STEP
  while included_count < len(g):
  # for j in range(5):
  
    # look for min_distance
    min_dist = math.inf
    min_index = -1
    for i in range(len(g)):
      if included[i] == False:
        if (float(results[i][1]) < min_dist):
          min_dist = results[i][1]
          # print("min_dist:",min_dist)
          min_index = i
    included[min_index] = True

    # update vertices connected to the min_distance vertex
    for v in g.getVertex(results[min_index][0]).neighboringVertices():
      e = g.getEdge(str(results[min_index][0]), str(v))
      # print(e.getWeight())

      # search for the index of v
      v_idx = -1
      for i in range(len(results)):
        if results[i][0] == str(v):
          v_idx = i

      # update weight and parent
      if results[min_index][1] + e.getWeight() < results[v_idx][1]:
        results[v_idx][1] = results[min_index][1] + e.getWeight()
        results[v_idx][2] = results[min_index][0]

    # print(results)
    # print(included)

    # j += 1
    ### exit condition:
    included_count = 0
    for i in range(len(g)):
      if included[i] == True:
        included_count += 1


        

  s += "%10s %10s %12s\n" % ("Vertex", "Min Cost", "Parent") 
  for i in range(len(g)):
    # s += results[i][0] + "\t" + str(results[i][1]) + "\t" + results[i][2] + "\n"
    s += "%10s %10s %12s\n" % (results[i][0], str(results[i][1]), results[i][2]) 
        
  # print(results)
  # print(included)
  return s


##############################################33

def spanTree(g, startLabel):
  """Returns a list containing the edges in the minimum
spanning tree of the graph.

minimumSpanningTree(graph):
  mark all vertices and edges as unvisited
  mark some vertex, say v, as visited
  for all the vertices:
    find the least weight edge from a visited vertex to an
    unvisited vertex, say w
    mark the edge and w as visited

"""
  # mark all vertices and edges as unvisited
  g.clearVertexMarks()
  g.clearEdgeMarks()
  # mark some vertex, say v, as visited
  v = g.getVertex(startLabel)
  v.setMark()

  span_tree = list()

  for vv in g.vertices():
    min_weight = math.inf
    min_edge = None
    min_vertex = None
    for v in g.vertices():
      # find the least weight edge from a visited vertex to an    unvisited vertex, say w
      if v.isMarked():
        for n in v.neighboringVertices():
          if not n.isMarked():
            # print(v.getLabel(), n.getLabel())
            e = g.getEdge(v.getLabel(),n.getLabel())
            if e.getWeight() < min_weight:
              min_weight = e.getWeight()
              min_edge = e
              min_vertex = v

    if min_edge:
      # mark the edge and w as visited
      min_edge.setMark()
      other_vertex = min_edge.getOtherVertex(min_vertex)
      other_vertex.setMark()
      span_tree.append(str(min_edge))
      # print(span_tree)

  return span_tree  
      
#########################################3

def mermaidSort(sorted):
    """Creates mermaid topsorted graph code that can be put into html
    """
    # place opening html code into a string
    # for each vertex in the sorted 
      # transform edge into mermaid code
      # add mermaid code to the string
    # add closing html code to the string
    # return the string
    sorted = sorted.split()
    s = ""
    s += ' <div class="mermaid"> \n'
    s += 'graph RL \n'
    for i in range(1,len(sorted)):
      s += sorted[i-1] + " --> " +  sorted[i]  + "\n"

    s += '\n </div> '
    print(s)
    return s 


###############################################


def dataTablePaths(g, startLabel):
  """Uses Dijkstra's algorithm to find the single-source shortest paths for the vertices of a graph.
  Formats the results for HTML presentation using Data Tables
  """
  ### INITIATION STEP
  cols = 3
  rows = len(g)
  results = [[0 for i in range(cols)] for j in range(rows)]
  included = [False for i in range(rows)]

  i = 0
  # print("startLabel",startLabel)
  for v in g.vertices():
    if str(v) == startLabel:
      results[i][0] = str(v)
      results[i][1] = 0
      results[i][2] = "undefined"
      included[i] = True

    elif v in g.getVertex(startLabel).neighboringVertices():
      # print(v, "connected to source")
      start = g.getVertex(startLabel)
      e = start.getEdgeTo(v)
      # print(e)
      results[i][0] = str(v)
      results[i][1] = e.getWeight()
      results[i][2] = str(start)
      included[i] = False

    else:
      results[i][0] = str(v)
      results[i][1] = math.inf
      results[i][2] = "undefined"
      included[i] = False
      
    i += 1

  # print(results)
  # print(included)

  included_count = 0

  
  ### COMPUTATION STEP
  while included_count < len(g):
  # for j in range(5):
  
    # look for min_distance
    min_dist = math.inf
    min_index = -1
    for i in range(len(g)):
      if included[i] == False:
        if (float(results[i][1]) < min_dist):
          min_dist = results[i][1]
          # print("min_dist:",min_dist)
          min_index = i
    included[min_index] = True

    # update vertices connected to the min_distance vertex
    for v in g.getVertex(results[min_index][0]).neighboringVertices():
      e = g.getEdge(str(results[min_index][0]), str(v))
      # print(e.getWeight())

      # search for the index of v
      v_idx = -1
      for i in range(len(results)):
        if results[i][0] == str(v):
          v_idx = i

      # update weight and parent
      if results[min_index][1] + e.getWeight() < results[v_idx][1]:
        results[v_idx][1] = results[min_index][1] + e.getWeight()
        results[v_idx][2] = results[min_index][0]

    # print(results)
    # print(included)

    # j += 1
    ### exit condition:
    included_count = 0
    for i in range(len(g)):
      if included[i] == True:
        included_count += 1

  return (results)
###### TO FIX ^^^^^^