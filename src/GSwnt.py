## Wnt Pathway through Graphspace

## 6/15/17
## Uploads the Wnt pathway to Graphspace

#Citations:

#Notes:
#DB = Debugging

#####################################
## Nick Egan
## Advisor: Anna Ritz
#####################################

# Plan of Attack!  (\\ means complete)
# Figure out how to handle nu Graphspace
## Set up for three shapes (receptor, tf, none)
## Set up for colored/individually directed connections (physical v phosphorylation)
## Set up for multiple possible connections to the same node
# Read in Wnt-edges.txt and Wnt-nodes.txt

##Start all functions with:
#Input:
#Processes:
#Output:
#Initialize variables:
#Variables initialized.

import sys
sys.path.insert(0, '/afs/reed.edu/user/n/i/nicegan/Desktop/Summer-Research-2017/packages')

import graphspace_python

def main():

    fileText = fileReader("Wnt-edges.txt", True)
    filePathways = NetPath_pathwayGenerator(fileText)
    fileText = fileReader("Wnt-nodes.txt", True)
    fileNodes = NetPath_nodeGenerator(fileText)

    NetPath_GraphSpace(filePathways, fileNodes, "Wnt Pathway", "The Wnt pathway, uplaoded to GraphSpace and generated using NetPath data.")

    return


def fileReader(fileName, separatecols):
    #Input: A text file, the lines to be read(set), the columns to be read(set), and if columns will be separated into different entries into the final array (bool)
    #Process: Processes the lines and columns into
    #Output: An array containing the information in the text files separated by column and line.

    #Initialize variables:
    fileContents = [] # The final array to contain the file information
    #Variables initialized.

    myFile = open(fileName,'r') ## open the file
    lineString = myFile.read() ## Read the file into one long string
    myFile.close() ## close the file
    lineString = lineString.strip() ## remove extra whitespace
    lineList = lineString.split('\n') ## Split the string by line
    if separatecols == True:
        for pattern in range(len(lineList)):
            lineList[pattern] = lineList[pattern].split('\t')  ## Split the list by col

    #print(lineList) #DB

    return lineList

def NetPath_pathwayGenerator(fileText):
    #Input: An array, containing the info of a text file separated by col internally and then line from a NetPath-edges.txt file.
    #Process: Takes the node and edge information of this text file, in the format of Wnt-edges.txt, so it will take the columns 0, 1, 5
    #Ouput: A smaller array, this time with only useful node and edge information

    #Initialize variables:
    colPathway = [] # Columns of the eventual pathway in a single line
    genPathway = [] # Final generated pathway in format of [input, output, edge type]
    #Variables initialized.
    for row in range(len(fileText)):
        for col in range(8):
            if col in [0, 1, 5]: # If in the columns containing the info we want...
                colPathway.append(fileText[row][col]) # Append onto the overall array
                print("colPathway is:", colPathway)
        genPathway.append(colPathway)
        colPathway = []

    print("The final pathway from this NetPath edges text files is: ") #DB
    for pattern in genPathway:
        print(pattern)

    genPathway.pop(0) #Removing header

    return genPathway

def NetPath_nodeGenerator(fileText):
    #Input: An array, containing the info of a text file separated by col internally and then line from a NetPath-nodes.txt file.
    #Process: Takes the node information from this file, every column.
    #Ouput: An array with column headers removed, for [Node, node_symbol, node_type]

    #Initialize variables:
    colNode = [] # Columns of the eventual pathway in a single line
    genNode = [] # Final generated pathway in format of [input, output, edge type]
    #Variables initialized.
    for row in range(len(fileText)):
        for col in range(3):
            colNode.append(fileText[row][col])
            print("colNode is:", colNode)
        genNode.append(colNode)
        colNode = []

    print("The nodes from this NetPath node text file is: ") #DB
    for pattern in genNode:
        print(pattern)

    genNode.pop(0) #Removing header

    return genNode

def NetPath_GraphSpace(genPathway, genNode, graphName, graphDescription):
     # Input: Array of arrays containing concatenated data from a NetPath-edges.txt file in the format of [Input, Output, Pathway type]
     # As well as a concatenated NetPath-nodes.txt files with additional information for node type.
     # Process: Create nodes with graphical information using NetPath-nodes.txt, and then connect them with graphically detailed connections from the edges information.

     #Initializing Graph
     from graphspace_python.graphs.classes.gsgraph import GSGraph
     G = GSGraph()
     G.set_name(graphName) #Applies name to graph
     G.set_data(data={'description': graphDescription}) #Applies graph description
     #Graph initialized
     for nodecounter in range(len(genNode)):
        node = genNode[nodecounter][0]
        node_symbol = genNode[nodecounter][1]

        G.add_node(node, popup = "sample node popup", label = node)
        if node_symbol == "tf":
            G.add_node_style(node, shape = 'vee', color = 'green', width = 90, height = 90)
        elif node_symbol == "receptor":
            G.add_node_style(node, shape = 'rectangle', color = 'red', width = 90, height = 90)
        else:
            G.add_node_style(node, shape = 'ellipse', color = 'yellow', width = 90, height = 90)

     for edgecounter in range(len(genPathway)):
        node1 = genPathway[edgecounter][0]
        node2 = genPathway[edgecounter][1]
        edgetype = genPathway[edgecounter][2]

        if edgetype == "Phosphorylation":
            G.add_edge(node1, node2, directed = True, popup = "Phosphorylation interaction.")
            G.add_edge_style(node1, node2, directed = True, edge_style = "solid", color = "yellow")
        elif edgetype == "Dephosphorylation":
            G.add_edge(node1, node2, directed = True, popup = "Dephosphorylation interaction")
            G.add_edge_style(node1, node2, directed = True, edge_style = "solid", color = "red")
        else:
            G.add_edge(node1, node2, directed = False, popup = "Physical connection")
            G.add_edge_style(node1, node2, directed = False, edge_style = "solid")

     #Uploading graph to Graphspace
     from graphspace_python.api.client import GraphSpace
     graphspace = GraphSpace('nicegan@reed.edu', 'Pitapop2@2')
     print graphspace.post_graph(G)
     #graphspace.update_graph(graphName, graph = G)

     return

if __name__ == '__main__':
    main()
