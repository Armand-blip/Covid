import os
import math
import json
import networkx as nx
import random
from tqdm import tqdm
import time
import matplotlib.pyplot as plt

# load the data for building the graph
with open('data/dpc-covid19-ita-province.json') as f:
    data = json.load(f)
  # Used for plot with networkx
def plot_graph(graph, name, layout, path):
    pos = nx.layout.spring_layout(graph)
    if layout == "spring":
        pos = nx.layout.spring_layout(graph)
    elif layout == "random":
        pos = nx.layout.random_layout(graph)
    plt.subplots(1, 1, figsize=(15, 15))
    nx.draw_networkx_nodes(graph, pos, node_size=20, node_color="#ff0000", alpha=0.8)
    nx.draw_networkx_edges(graph, pos, edge_color="#0000ff", width=2)
    plt.axis('on')
    plt.savefig(os.path.join(path, name + ".png"))
    
# Euclidean distance used for calculate the distance with longitude and latitude
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

# Used for plot with networkx
def provinces_graph(provinces):
    graph = nx.Graph()
    # filter reference date because in the data the provinces are repeated
    reference_date = provinces[0]['data']
    # filter data using date and 'denominazione_provincia' and remove the data that have fields
    # 'In fase di definizione/aggiornamento' and 'Fuori Regione \/ Provincia Autonoma'
    id = 0
    for province in (provinces for provinces in data if
                     provinces['denominazione_provincia'] != 'In fase di definizione/aggiornamento' and 'Fuori Regione \/ Provincia Autonoma'  ):
        if province['data'] == reference_date:
            graph.add_node(id, city=province['denominazione_provincia'], long=province['long'],
                           lat=province['lat'])
            id += 1
        else:
            break
    return graph

def random_graph(nodes_num, x_low, x_high, y_low, y_high):
    graph = nx.Graph()
    for node_id in range(nodes_num):
        graph.add_node(node_id, city=str(node_id), long=random.uniform(x_low, x_high), lat=random.uniform(y_low, y_high))
    return graph

''' add edges'''
def set_edges(graph, dist):
    for v in graph.nodes(data=True):
        for u in (n for n in graph.nodes(data=True) if (n != v)):
            if (v[1]['long'] - dist < u[1]['long'] < v[1]['long'] + dist) \
                    and (v[1]['lat'] - dist < u[1]['lat'] < v[1]['lat'] + dist):
                graph.add_edge(v[0], u[0], a=v[1]['city'], b=u[1]['city'],
                               weight=euclidean_distance(v[1]['long'], v[1]['lat'], u[1]['long'], u[1]['lat']))
    return graph

def not_repeated(list, number):
    for item in list:
        if item == number:
            return False
    return True

''' To calculate the dimension of the intersection between the neighborhood of v and the
neighborhood of each of its neighbors using the list intersection algorithm  '''
# take all those elements which are common to both of the initial lists and store them into another list
def list_intersection(list1, list2):
    intersection = []
    #iterate through both lists, comparing items
    for i in list1:
        for j in list2:
            #if they have a common element,
            if i == j:
                #check if it is already accounted for.
                if not_repeated(intersection, j):
                    intersection.append(i)
    return intersection

def clustering_coefficient(graph, intersection=False):
    cc_list = {} # an empty dictionary
    sum = 0
    for node in graph.nodes()(data=True):
        degree = [n for n in nx.neighbors(graph, node[0])]  # degree is the number of edges that are coincident to the vertex
        num_neighbours = len(degree)
        num_links = 0    # nr of links beween neighbours of node 0
        if num_neighbours > 1: # we take one because 0 doe not let us to find the coeff,we can not divide by 0 in line 101
            if intersection == False:
                for node1 in degree:
                    for node2 in degree:
                        if graph.has_edge(node1, node2):   #Return True if the edge between nodes is in the graph
                            num_links += 1
                # the number of edge is divided by 2 because we have an undirected graph and we measure the same edge two times
                # this is also the number of triangles
                coeff = (num_links) / (num_neighbours * (num_neighbours - 1)) #since in the formula we multiply by 2 the numerator,here we divide te numerator again by 2
                sum += coeff
                cc_list[node[1]['city']] = coeff
            #  count the number of triangles by using list intersection
            if intersection == True:
                num_triangles = 0
        
                for u in degree:
                    u_neighbors = list(graph.neighbors(u))
                    list_intersection1 = list_intersection(degree, u_neighbors)
                    num_triangles += len(list_intersection1)
                coeff = num_triangles / (num_neighbours * (num_neighbours - 1))
                sum += coeff
                cc_list[node[1]['city']] = coeff
        else:
            cc_list[node[1]['city']] = 0
    return cc_list, sum / graph.number_of_nodes()  # return the list of coefficient and the average




if __name__ == '__main__':
       
        provinces = []
        for i in range(len(data)):
            provinces.append([data[i].get("denominazione_provincia"), data[i].get("lat"), data[i].get("long")])
        num_test = 1
       
        for i in tqdm(range(num_test)):

            P = set_edges(provinces_graph(data), 0.8)

            R = set_edges(random_graph(2000, 30, 49, 10, 19), 0.08)

        plot_graph(P,name="Provices Graph",layout="spring",path="images/")
        plot_graph(R, name="Random Graph", layout="random", path="images/")
        
        
        start = time.time()
        print("CLUSTERING COEFFICIENT USING NETWORKX FOR P AND R")
        print("For each node in provinces graph: ", nx.clustering(P))
        print("Average: ", nx.average_clustering(P))
        end = time.time()
        time_cluster_networkx_P = (end - start)
        
        start = time.time()
        print("For each node in random graph: ", nx.clustering(R))
        print("Average: ", nx.average_clustering(R))
        end = time.time()
        time_cluster_networkx_R = (end - start)
        
        print("\nCLUSTERING COEFFICIENT WITH LIST INTERSECTION")
        clustering_coefficient_intersection_P, avg_intersection_P = clustering_coefficient(P, intersection=True)
        print("For each node in provinces graph: ", clustering_coefficient_intersection_P)
        print("Average: ", avg_intersection_P)
        end = time.time()
        time_cluster_intersect_P = (end - start)
        
        start = time.time()
        clustering_coefficient_intersection_R, avg_intersection_R = clustering_coefficient(R, intersection=True)
        print("For each node in random graph: ", clustering_coefficient_intersection_R)
        print("Average: ", avg_intersection_R)
        end = time.time()
        time_cluster_intersectR = (end - start)

        print("\nTime for calculate clustering coefficient")
        print("The time is referred to the calculation of clusering coefficient on P and R")
        print("Using NetworkX Function on P: ", time_cluster_networkx_P , " on R: ",
        time_cluster_networkx_R)
        
        print("Using list intersect implementation on P: ", time_cluster_intersect_P, " on R: ",
        time_cluster_intersectR)
        
        
        
        
        
        
        
        