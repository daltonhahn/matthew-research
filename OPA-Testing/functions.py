import networkx as nx
import plotly.graph_objects as go
import json
import sys
import os
import getopt   
import shutil

#The following functions are general functions

def createRandomNodeGraph(numnodes:int):
    #G = nx.binomial_graph(numnodes, .05, directed=True) try one
    #G = nx.fast_gnp_random_graph(numnodes, .05, directed=True) try two
    #G = nx.random_tree(numnodes) try three - do not repeat
    G = nx.binomial_tree(numnodes)
    return G

def printGraph(G, numnodes): #look into changing this into graphtools
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='Earth',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    node_adjacencies = []
    
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    
    if numnodes < 2501: #please understand that if you attempt to do any more than this without a beefy computer, you will break your computer. i don't care that you have an nvidia 3090. don't do it.
        fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='<br>Network graph made with Python',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
        fig.show()
    return

def getjson(graph):
    data1 = nx.node_link_data(graph)
    s1 = json.dumps(data1) #this creates the JSON serial
    #print(s1)
    os.system("rm output_files/*")
    f = open("output_files/graph.json", "w")
    f.write(s1)
    return s1

class MultiThreadedNode:
    def __init__(self, idnum, port, servicename):
        self.id = idnum
        self.targets = []
        self.portnum = port
        self.servicename = servicename
        self.message = "Fake service %s" % idnum
        
    def addTarget(self, target):
        self.targets.append(target)
        return
    
    def __str__ (self):
        return ("ID: "+str(self.id) + "\nTargets: "+ ' '.join(str(self.targets)) + "\nPort: "+str(self.portnum)+"\nService Name: "+self.servicename+"\nMessage: "+self.message+"\n")

def sortjson(jsondict):
        #parts of the json dict
        #directed - ignore
        #multigraph - ignore
        #nodes - the ids of the nodes + any additional descriptors. this is currently coded to only pay attention to the ids.
        #links - two parts - source and target. you'll look for the source to match with the node, then attach the node to the target.
        jsondict = json.loads(jsondict)
        nodelist = []
        port = 80
        for i in jsondict["nodes"]:
            node = MultiThreadedNode(i["id"], port, "fs%s" % i["id"])
            nodelist.append(node)
            port += 1

        for i in jsondict["links"]:
            for j in nodelist:
                if j.id == i["source"]:
                    j.addTarget(i["target"])
        return nodelist

#The following functions are meant for use with fake-service-tempalte.yaml

def uploadmicroserviceshells(nodelist):
    for i in nodelist:
        print(i)
    for i in nodelist:
        os.system("cp fake-service-template.yaml output_files/fake-service-"+str(i.id)+".txt")#note that this command only works in linux - if used for windows, change the cp to copy
        listoflines = []
        with open("output_files/fake-service-%s.txt" % i.id, "r") as fakeservicedoc:
            listoflines = fakeservicedoc.readlines()
        modifiedLines = list()
        for j in listoflines:
            if "{name}" in j:
                j = j.replace("{name}", i.servicename)
            elif "{port}" in j:
                j = j.replace("{port}", str(i.portnum))
            elif "{upstreamuris}" in j:
                fullstr = ""
                for t in i.targets:
                    for s in nodelist:
                        if s.id == t:
                            fullstr += "http://"+s.servicename+":"+str(s.portnum)+","
                j = j.replace("{upstreamuris}", fullstr[:-1])
            modifiedLines.append(j)
        with open("output_files/fake-service-%s.txt" % i.id, "w") as fakeservicedoc:
            fakeservicedoc.writelines(modifiedLines)
        os.system("cp output_files/fake-service-"+str(i.id)+".txt output_files/fake-service-"+str(i.id)+".yaml")
        os.system("rm output_files/fake-service-"+str(i.id)+".txt")

#The following functions are meant for use with policy-template.rego

def path_recursive(nodelist, currentid, currentpath):

    if len(currentpath) == 0:
        currentpath += f"{nodelist[currentid].servicename}"
    else: 
        currentpath += f",{nodelist[currentid].servicename}" #fix the print issues with this
    if len(nodelist[currentid].targets) == 0:
        return [currentpath]
    else:
        temp = []
        for i in nodelist[currentid].targets:
            temp += path_recursive(nodelist, int(i), currentpath)
        return temp


def modifypolicytemplate(nodelist):
    os.system("cp policy-template.rego output_files/policy.txt")
    listoflines = []
    with open("output_files/policy.txt", "r") as policy:
        listoflines = policy.readlines()
    #modifying the policy template will require two seperate processes - one to do the token map and one to do the paths. both require inserting into the list of lines instead of creating a seperate list.
    #this is the paths process
    pathlist = path_recursive(nodelist, 0, "")
    count = 0
    for i in listoflines:
        count += 1
        if "{paths}" in i:
            break
    print(count)
    for i in pathlist:
        if count - 16 == len(pathlist): #checking for last path in list
            tempstr = "		\"{path}\""
            tempstr = tempstr.replace("{path}", i)
            listoflines.insert(count, tempstr[0:len(tempstr-2)])
            count += 1
        else:
            tempstr = "		\"{path}\",\n"
            tempstr = tempstr.replace("{path}", i)
            listoflines.insert(count, tempstr)
            count += 1
    #this is the token process
    count = 0
    for i in listoflines:
        count += 1
        if "{\"sName\": \"{name}\", \"tokVal\": \"{token}\"}," in i:
            break
    gap = count
    print(count)
    for i in nodelist:
        if count - gap == len(nodelist): #checking for last node in list
            tempstr = "        {\"sName\": \"{name}\", \"tokVal\": \"{token}\"}"
            tempstr = tempstr.replace("{name}", i.servicename)
            tempstr = tempstr.replace("{token}", f"token{i.id}")
            listoflines.insert(count, tempstr)
            count += 1
        else:
            tempstr = "        {\"sName\": \"{name}\", \"tokVal\": \"{token}\"},\n"
            tempstr = tempstr.replace("{name}", i.servicename)
            tempstr = tempstr.replace("{token}", f"token{i.id}")
            listoflines.insert(count, tempstr)
            count += 1
    #post process
    with open("output_files/policy.txt", "w") as policy:
        policy.writelines(listoflines)
    os.system("cp output_files/policy.txt output_files/policy.rego")
    os.system("rm output_files/policy.txt")
    return

#the following functions are meant to be used with envFilter-template.yaml

def createenvFilter(nodelist):
    

#to do this week
#   check in overleaf
#   tackle envFilter-template - this will mainly be recycling code from upload microservice shells