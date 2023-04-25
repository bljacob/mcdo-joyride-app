class LinkedDirectedGraph():
  
  def __init__(self, sourceCollection = None):
    """Adds a vertex with the given label to the graph."""
    self._edgeCount = 0
    self._vertices = dict() # Dictionary of vertices
    self._size = 0
    
    if sourceCollection:
      for item in sourceCollection:
        self.add(item)

  def addVertex(self, label):
    self._vertices[label] = LinkedVertex(label)
    self._size += 1

  def removeVertex(self, label):
    """Returns True if the vertex was removed, or False otherwise."""
    removedVertex = self._vertices.pop(label, None)
    if removedVertex is None:
      return False
    # Examine all other vertices to remove edges
    # directed at the removed vertex
    for vertex in self.vertices():
      if vertex.removeEdgeTo(removedVertex):
        self._edgeCount -= 1
    # Examine all edges from the removed vertex to others
    for edge in removedVertex.incidentEdges():
      self._edgeCount -= 1
    self._size -= 1
    return True

  def addEdge(self, fromLabel, toLabel, weight):
    """Connects the vertices with an edge with the given weight."""
    if self.containsVertex(fromLabel) and self.containsVertex(toLabel):
      # print("contains fromLabel", self.containsVertex(fromLabel))
      # print("contains toLabel",   self.containsVertex(toLabel))
      fromVertex = self.getVertex(fromLabel)
      toVertex = self.getVertex(toLabel)
      # print("fromVertex", fromVertex)
      # print("toVertex", toVertex)
      fromVertex.addEdgeTo(toVertex, weight)
      self._edgeCount += 1
    
  def getEdge(self, fromLabel, toLabel):
    """Returns the edge connecting the two vertices, or None if
    no edge exists."""
    fromVertex = self.getVertex(fromLabel)
    toVertex = self.getVertex(toLabel)
    return fromVertex.getEdgeTo(toVertex)
    
  def removeEdge(self, fromLabel, toLabel):
    """Returns True if the edge was removed, or False otherwise."""
    fromVertex = self.getVertex(fromLabel)
    toVertex = self.getVertex(toLabel)
    edgeRemovedFlg = fromVertex.removeEdgeTo(toVertex)
    if edgeRemovedFlg:
      self._edgeCount -= 1
    return edgeRemovedFlg

  def edges(self):
    """Supports iteration over the edges in the graph."""
    result = list()
    for vertex in self.vertices():
      edges = vertex.incidentEdges()
      for e in edges:
        if not e in result:
          result.append(e)
      # print(edges)
      # result = result.update(edges)
    return result

####### TO FIX vvvv
  def containsVertex(self, v):
    """Returns True if the graph contains a vertex with
the specified label, or False otherwise."""
    if v in self._vertices: 
      # print(v, "in", self._vertices)
      return True
    return False

  def containsEdge(self,fromLabel, toLabel):
    """Returns True if the graph contains an edge
from a vertex with fromLabel to a vertex with
toLabel, or False otherwise."""
    fromVertex = self.getVertex(fromLabel)
    toVertex = self.getVertex(toLabel)
    if fromVertex and toVertex:
      if toVertex in fromVertex.neighboringVertices():
        # print(bool(fromVertex.getEdgeTo(toVertex)))
        return bool(fromVertex.getEdgeTo(toVertex))
    else:
      return False

  
  def getVertex(self, label):
    """Returns the vertex with the specified label, or
None if there is no such vertex."""
    if self._vertices[label]:
      return self._vertices[label]
    else: return None


  def __str__(self):
    """Same as str(g). Returns the string representation of the graph
    example:
      5 Vertices: A C B E D
      5 Edges: A>B:3 A>C:2 B>D:1 C>D:1 D>E:2
    """
    s = str(self._size) + " Vertices: "
    for v in self._vertices:
      s += str(v) + " "
    s += "\n"
    s += str(self._edgeCount) + " Edges: "
    for v in self._vertices:
      v = self.getVertex(v)
      # print(v._edgeList)
      for e in v._edgeList:
        s += str(e) + " "
    return s

  ######## Q4 W1 cutoff #######

  def clearVertexMarks(self):
    """Clears all vertex marks."""
    for v in self._vertices:
      self._vertices[v]._mark = False

  def vertices(self):
    """Same as iter(g) or for vertex in g:. Returns an
iterator over the vertices in the graph"""
    return self._vertices.values()

  def neighboringVertices(self, label):
    v = self.getVertex(label)
    return v.neighboringVertices()

      ###### Q4 W2 cutoff ######

  def __len__(self):
    """The len function returns the number of the graph’s vertices"""
    return self._size

  def sizeVertices(self):
    """Same as len(g). Returns the number of vertices
in the graph."""
    return self._size

    ####### Q4 W3 cutoff ######

  def clearEdgeMarks(self):
    """Clears all edge marks."""
    for v in self._vertices:
      vertex = self.getVertex(v)
      for e in vertex._edgeList:
        e.clearMark()

    ###### Q4 W4 cutoff ######
    
  def mermaidGraph(self):
    """Creates mermaid graph code that can be put into html
    """
    # place opening html code into a string
    # for each edge in the edgeList
      # transform edge into mermaid code
      # add mermaid code to the string
    # add closing html code to the string
    # return the string
    s = ""
    s += ' <div class="mermaid"> \n'
    s += 'graph TD \n'
    for e in self.edges():
      s += e._vertex1.getLabel() + " --> |" +  str(e._weight)  + "| "+ e._vertex2.getLabel() + "\n"
      print(e)

    s += '\n </div> '
    print(s)
    return s 

    
    
####### TO FIX ^^^^

      
#######################################

      ######################################


class LinkedVertex(object):
  
  def __init__(self, label):
    self._label = label
    self._edgeList = list()
    self._mark = False
  
  def setLabel(self, label, g):
    """Sets the vertex’s label to label."""
    g._vertices.pop(self._label, None)
    g._vertices[label] = self
    self._label = label

  def neighboringVertices(self):
    """Returns the neighboring vertices of this vertex."""
    vertices = list()
    for edge in self._edgeList:
      vertices.append(edge.getOtherVertex(self))
    return iter(vertices)
    
  def removeEdgeTo(self, toVertex):
    """Returns True if the edge exists and is removed,
    or False otherwise."""
    edge = LinkedEdge(self, toVertex)
    if edge in self._edgeList:
      self._edgeList.remove(edge)
      return True
    else:
      return False

####### TO FIX vvvv
  def addEdgeTo(self, toVertex, weight):
    """Adds an edge with the given weight from v to toVertex"""
    edge = LinkedEdge(self, toVertex, weight )
    self._edgeList.append(edge)

  def getEdgeTo(self, toVertex):
    """Returns the edge from v to toVertex, or returns None if
the edge does not exist."""
    for e in self._edgeList:
      if e._vertex2 == toVertex:
        return e
    return None

  def setMark(self):
    """Marks the vertex."""
    self._mark = True

  def __str__(self):
    """Same as str(v). Returns a string representation of the
vertex."""
    return self._label

  ###### Q4 W1 cutoff ######

  def isMarked(self):
    """Returns True if the vertex is marked, or False otherwise."""
    return self._mark

  def getLabel(self):
    """Returns the label of the vertex."""
    return self._label

    ###### Q4 W3 cutoff ######

  def incidentEdges(self):
    """Returns an iterator over the incident edges of the
vertex."""
    return iter(self._edgeList)

    
####### TO FIX ^^^^

####################################################

    ######################################################33


class LinkedEdge(object):
  def __init__(self, fromVertex, toVertex, weight = None):
    self._vertex1 = fromVertex
    self._vertex2 = toVertex
    self._weight = weight
    self._mark = False
      
  def __eq__(self, other):
    """Two edges are equal if they connect
    the same vertices."""
    if self is other: return True
    if type(self) != type(other): return False
    return self._vertex1 == other._vertex1 and \
        self._vertex2 == other._vertex2 and \
        self._weight == other._weight


  ###### TO FIX vvvv
  def __str__(self):
    """Same as str(e). Returns the string representation of the edge."""
    s = str(self._vertex1) + ">" + str(self._vertex2) + ":" + str(self._weight)
    return s

  
  def getOtherVertex(self,vertex):
    """Returns the edge’s other vertex"""
    if vertex == self._vertex1:
      return self._vertex2
    elif vertex == self._vertex2:
      return self._vertex1
    else:
      print("there's a problem with the LinkEdge's getOtherVertex()'s input'")
      return None

  ###### Q4 W2 cutoff ######

  def getWeight(self):
    """Returns the weight of the edge."""
    return self._weight

  ###### Q4 W3 cutoff ######
  def clearMark(self):
    """Unmarks the edge."""
    self._mark = False

  def setMark(self):
    """Marks the edge."""
    self._mark = True

  ###### TO FIX ^^^^