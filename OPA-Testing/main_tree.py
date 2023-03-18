import functions as f
import networkx as nx

def main():
    num = int(input("How many nodes would you like created?: "))
    graph = f.createRandomNodeGraph(num)
    print(nx.forest_str(graph))
    jsondict = f.getjson(graph)
    nodelist = f.sortjson(jsondict)
    f.uploadmicroserviceshells(nodelist)
    f.modifypolicytemplate(nodelist)
main()