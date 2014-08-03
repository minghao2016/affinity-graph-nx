import csv
import networkx as nx
import matplotlib.pyplot as plt
import math

# ----------------------------------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------------------------------

#every node in the graph is an object that contains a list of attributes and a list of items that share such attributes
class Cluster:

    def __init__(self,idnum,attributes,items):
        self.idnum = idnum
        self.attributes = attributes
        self.items = items
        self.weight = float((len(items)*len(items)))/2
        self.strength = len(attributes)

    def __repr__(self):
        return "\n".join(self.items)
 

# ----------------------------------------------------------------------------------------
#FUNCTIONS FOR THE PREPARATION OF DATA
# ----------------------------------------------------------------------------------------

#Function that builds the list of edges on the basis of the attributes shared by each node with each other.
#It creates one edge for every pairing where, given n the number of attributes of the first node, the second node has n-1 elements (or less, if the n-1 is not present, and so on), and all elements of the second node are included in the first
def edges1(nodes,edges):
    for a in nodes:
        counter = 1
        nodesnum = 0
        while counter < maxattr:
            for b in nodes:                
                if (a,b) not in edges and (b,a) not in edges and a.attributes!=b.attributes and set(a.attributes).issuperset(set(b.attributes)) and len(a.attributes)==(len(b.attributes)+counter): #need to correct for non-continuous :
                    if a.attributes!=b.attributes and set(a.attributes).issuperset(set(b.attributes)) and len(a.attributes)==(len(b.attributes)+counter): 
                        edges.append((a,b))
                        nodesnum +=1
            if nodesnum == 0:
                counter +=1
            else: counter = maxattr
    return edges

# ----------------------------------------------------------------------------------------
#SCRIPT FOR THE PREPARATION OF DATA
# ----------------------------------------------------------------------------------------

#Take the csv file and transform the data into a dictionary where the each key is an item and each value is a list of the attributes of the item
listcsv = open('itemstable.csv',"rb")
itemstable = csv.DictReader(listcsv, dialect="excel")

listitems= {}
for row in itemstable:
    #put item as key
    #create empty list for values
    #if value equal to 1, add key to value list
    item = row.pop("Item")
    listitems[item] = []
    for i in row:
        if row[i]=="1":
            listitems[item].append(i)

#Create a list of clusters, i.e. sets of attributes shared by one or more items           
clusterlist = []
for individual in listitems:
    if listitems[individual] not in clusterlist:
        clusterlist.append(listitems[individual])

#Identify the maximum number of attributes in a cluster
maxattr = len(max(clusterlist, key=len))

#Create a list of objects of the class above, that will later become nodes of the graph
nodes=[]

idnumber = 0 #the idnumber is currently not used anywhere in the script but could be used for working on the plotting

for u in clusterlist:
    itemlist = [] 
    idnumber +=1
    for individual in listitems:
        if listitems[individual]==u:
            itemlist.append(individual)
    nodes.append(Cluster(idnumber,u,itemlist))

#Create a list of edges. Each edge is a pair of nodes.
edgelist = []
edges = edges1(nodes,edgelist)  

#Initiate the graph
G=nx.Graph()

#Add each of the nodes in the list to the graph
for i in nodes:
    G.add_node(i)

#Add each edge to the graph
G.add_edges_from(edges)

#Create a label for each edge. The label corresponds to the item attributes shared by each pair of nodes.
edge_labels= {}
for i in G.edges():
    edge_labels[i]="\n".join(list(set(i[0].attributes).intersection(i[1].attributes)))

# ----------------------------------------------------------------------------------------
# FUNCTIONS FOR THE DRAWING OF GRAPHS
# ----------------------------------------------------------------------------------------

#Each function creates a set of node positions corresponding to a different type of graph. They are "customized" to the structure of our dataset.

#Spring graph
def drawgraphspring():
    pos = nx.spring_layout(G, dim=2, k=1, pos=None, fixed=None, iterations=5, weight='weight', scale=1.0)
    return pos

#Shell graph
def drawgraphshell():
    shell = maxattr
    shellist = []
    for i in range(maxattr):
        newshell = []
        for node in nodes:
            if node.strength == maxattr-i:
                newshell.append(node)
        shellist.append(newshell)

    pos = nx.shell_layout(G, nlist=shellist, dim=2, scale=1)
    return pos

#Spectral graph, which is the best so far
def drawgraphspectral():
    pos = nx.spectral_layout(G, dim=2, weight="weight", scale=1)
    return pos

#Random graph
def drawgraphrandom():
    pos = nx.random_layout(G, dim=2)
    return pos


# ----------------------------------------------------------------------------------------
#SCRIPT FOR DRAWING THE GRAPH
# ----------------------------------------------------------------------------------------

plt.figure(1,figsize=(50,25))  #This can be changed to modify the size of the figure, in inches

#Uncomment the desired graph type

#pos = drawgraphshell()
#pos = drawgraphspring()
#pos = drawgraphspectral()
pos = drawgraphspectral()

nx.draw(G, pos=pos, node_size=[(v.weight)*1000 for v in G.nodes()])
nx.draw_networkx_edge_labels(G,pos, edge_labels=edge_labels)

plt.savefig("graph.png") #This can be changed for other image attributes so Google for plt instructions


#ta daaaaa