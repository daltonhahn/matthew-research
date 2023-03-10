import functions.py as f

def main():
    num = int(input("How many nodes would you like created?: "))
    graph = f.createRandomNodeGraph(num)
    #printGraph(graph)
    jsondict = f.getjson(graph)
    nodelist = f.sortjson(jsondict)
    

main()
