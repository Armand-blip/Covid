''' 
Step1:First, take an empty stack and an empty path.
Step2:If all the vertices have an even number of edges then start from any of them. 
If two of the vertices have an odd number of edges then start from one of them. 
Set variable current to this starting vertex.
Step3:If the current vertex has at least one adjacent node then first discover that 
node and then discover the current node by backtracking. To do so add the current node 
to stack, remove the edge between the current node and neighbor node, set current to the neighbor node.
Step4:If the current node has not any neighbor then add it to the path and pop stack 
set current to popped vertex.
Step5:Repeat process 3 and 4 until the stack 
is empty and the current node has not any neighbor.

'''



# Function to find out the path
# It takes the adjacency matrix
# representation of the graph as input
def findpath(graph, n):
     
    numofadj = []
 
    # Find out number of edges each
    # vertex has
    for i in range(n):
        numofadj.append(sum(graph[i]))
 
    # Find out how many vertex has 
    # odd number edges
    startpoint, numofodd = 0, 0
    for i in range(n - 1, -1, -1):
        if (numofadj[i] % 2 == 1):
            numofodd += 1
            startpoint = i
 
    # If number of vertex with odd number of edges
    # is greater than two return "no Eulerian path ".
    if (numofodd > 2):     # The base case 
        print("no Eulerian path ")
        return
 
    # If there is a path find the path
    # Initialize empty stack and path
  
    stack = []
    path = []
    cur = startpoint
 
    # Loop will run until there is element in the
    # stack or current edge has some neighbour.
    while (len(stack) > 0 or sum(graph[cur])!= 0):
         
        # If current node has not any neighbour
        # add it to path and pop(Deletes the top most element from the stack) stack set new 
        # current to the popped element
        if (sum(graph[cur]) == 0):
            path.append(cur)
            cur = stack[-1]
            del stack[-1]
 
        # If the current vertex has at least one
        # neighbour add the current vertex to stack,
        # remove the edge between them and set the
        # current to its neighbour.
        else:
            for i in range(n):
                if (graph[cur][i] == 1):
                    stack.append(cur)
                    graph[cur][i] = 0
                    graph[i][cur] = 0
                    cur = i
                    break
 
    # Print the path
    for ele in path:
        print(ele, end = " -> ")
         
    print(cur)
 
# Driver Code
if __name__ == '__main__':
     
    # Test case 1
    graph1 = [ [ 0, 1, 0, 0, 1 ],
               [ 1, 0, 1, 1, 0 ],
               [ 0, 1, 0, 1, 0 ],
               [ 0, 1, 1, 0, 0 ],
               [ 1, 0, 0, 0, 0 ] ]
    n = len(graph1)
    findpath(graph1, n)
 
    # Test case 2
    graph2 = [ [ 0, 1, 0, 1, 1 ],
               [ 1, 0, 1, 0, 1 ],
               [ 0, 1, 0, 1, 1 ],
               [ 1, 1, 1, 0, 0 ],
               [ 1, 0, 1, 0, 0 ] ]
    n = len(graph2)
    findpath(graph2, n)
 
    # Test case 3
    graph3 = [ [ 0, 1, 0, 0, 1 ],
               [ 1, 0, 1, 1, 1 ],
               [ 0, 1, 0, 1, 0 ],
               [ 0, 1, 1, 0, 1 ],
               [ 1, 1, 0, 1, 0 ] ]
    n = len(graph3)
    findpath(graph3, n)

