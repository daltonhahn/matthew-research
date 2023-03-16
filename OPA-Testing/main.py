import functions as f
import networkx as nx

def main():
    num = int(input("How many nodes would you like created?: "))
    graph = f.createRandomNodeGraph(num)

    conn_flag = False
    while conn_flag is False:
        graph = f.createRandomNodeGraph(num)
        if nx.is_weakly_connected(graph):
            conn_flag = True
            break

    if conn_flag is True:
        jsondict = f.getjson(graph)
        nodelist = f.sortjson(jsondict)
        f.uploadmicroserviceshells(nodelist)
    
main()
