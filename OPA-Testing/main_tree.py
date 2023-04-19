import functions as f
import networkx as nx
import os

def main():
    num = int(input("How many nodes would you like created?: "))
    graph = f.createRandomNodeGraph(num)
    jsondict = f.getjson(graph)
    nodelist = f.sortjson(jsondict)
    servicenames = f.uploadmicroserviceshells(nodelist)
    f.modifypolicytemplate(nodelist)
    filternames = f.createenvFilter(nodelist)
    os.system("rm output_files/*.txt")
    f.createBashScript(servicenames, filternames)
main()