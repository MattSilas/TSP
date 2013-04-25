#!/usr/bin/python

import random
import sys
import getopt
import re
import math

'''Creates a random tour permuation'''
def random_tour_permutations(tour):
        i=int(random.random()*(len(tour)))
        j=int(random.random()*(len(tour)))
        if i != j:
            copy=tour[:]
            if i < j:
                copy[i:j+1]=reversed(tour[i:j+1])
            else:
                copy[i+1:]=reversed(tour[:j])
                copy[:j]=reversed(tour[i+1:])
            if copy != tour:
                yield copy
                
'''Creates a dictionary of all possible routing pairs and their distances'''
def routing(cities):
    routes = {}
    for i,(x1,y1) in enumerate(cities):
        for j,(x2,y2) in enumerate(cities):
            distance = int(math.sqrt((x1-x2)**2+(y1-y2)**2))
            routes[i,j]=distance
    return routes

'''Returns the length of the tour'''
def tour_length(matrix,tour):
    total=0
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        total+=matrix[city_i,city_j]
    return total

'''Restarts the SA process at a new city'''
def random_start(tour_length):
   start=range(tour_length)
   random.shuffle(start)
   return start

def anneal(new_start,random_tour_permutations,tour_function,runs,start_temp,alpha):
    from simulated_annealing import anneal
    score,path=anneal(new_start,random_tour_permutations,tour_function,runs,start_temp,alpha)
    return score,path

def getCities(filename):
    f = open(filename,'r')
    line = f.readline()
    cities = []
    while len(line) > 1:
        lineparse = re.findall(r'[^,;\s]+', line)
        cities.append([int(lineparse[1]),int(lineparse[2])])
        line = f.readline()
    f.close()
    return cities

def main():
    runs=10000
    start_temp,alpha=10000,0.9995
    city_file="test-input-1.txt"
    output_file = open("test-output-1.txt",'w')

    cities = getCities(city_file)
    if len(cities) > 1000:
        runs = 100000


    new_start = lambda: random_start(len(cities))
    routes = routing(cities)
    tour_function=lambda tour: -tour_length(routes,tour)
    
    
    score,path=anneal(new_start,random_tour_permutations,tour_function,runs,start_temp,alpha)
    score = score*-1
    score_str=str(score)
    output_file.write(score_str)
    output_file.write("\n")
    for city in path:
         city_str = str(city)
         output_file.write(city_str)
         output_file.write("\n")
    output_file.close()
    

if __name__ == "__main__":
    main()
