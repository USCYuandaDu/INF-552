import sys
import numpy as np 
import math
import collections

def free_cell_locations(file):
    row=0
    free_cell=[]
    found=False
    with open(file) as f:
        for line in f:
            if 'Grid-World' in line: 
                found=True
                continue
            line=line.strip()
            if(line==''):
                continue
            line=line.split()
            if found:   
                for col,ele in enumerate(line):
                    if ele=='1':
                        free_cell.append([int(row),int(col)])
                row+=1
                if row==10:
                    break
    return free_cell

def tower_locations(file):
    tower_loc=[]
    row=0
    found=False
    with open(file) as f:
        for line in f:
            if 'Tower Locations' in line:
                found=True
                continue
            line=line.strip()
            if(line==''):
                continue
            if found:
                loc=line.split(':')[1].split()
                tower_loc.append([int(loc[0]),int(loc[1])])
                row+=1
            if row == 4:
                break
    return tower_loc

def robot_tower_dist(file):
    noisy_dist=[]
    row=0
    found=False
    with open(file) as f:
        for line in f:
            if 'Noisy' in line:
                found=True
                continue
            line=line.strip()
            if(line==''):
                continue
            if found:
                line=line.split()
                dist=[]
                for item in line:
                    dist.append(float(item))
                noisy_dist.append(dist)
                row+=1
            if row == 11:
                break
    return noisy_dist

def distance_to_tower(free_cell,tower_loc):
    distancetotower=[]
    for i,free in enumerate(free_cell):
        dist=[]
        for j,tower in enumerate(tower_loc):
            euclidean_dist=math.sqrt(pow(free[0]-tower[0],2) + pow(free[1]-tower[1],2))
            dist.append([euclidean_dist*0.7,euclidean_dist*1.3])
        distancetotower.append(dist)
    return distancetotower

def find_probable_free_cells(free_cell,noisy_dist,distancetotower):

    print "noisy_dist_____________________"
    print noisy_dist

    prob_states=[]
    for i in xrange(0,len(free_cell)):
        points=free_cell[i]
        count=0
        for j in xrange(0,len(noisy_dist)):
            elem=noisy_dist[j]
            if distancetotower[i][j][0] <= elem and elem <= distancetotower[i][j][1] :
                count+=1
        if count==len(noisy_dist):
            prob_states.append(points)
    return prob_states

def find_neighbours(location, grid_size):
    x = location[0]
    y = location[1]
    neighbours = []
    if x + 1 < grid_size:
        neighbours.append((x + 1, y))
    if y + 1 < grid_size:
        neighbours.append((x, y + 1))
    if x - 1 > 0:
        neighbours.append((x-1, y))
    if y - 1 > 0:
        neighbours.append((x, y - 1))
    return neighbours

def calculate_transition_probability(states_dic,neighbours):
    
    transition_prob_for_neighbours=collections.defaultdict(dict)
    total_trasition_prob=collections.defaultdict(int)
    trans_prob=collections.defaultdict(dict)
    for cell in states_dic:
        total_trasition_prob[cell]=0.0
        allowed_timesteps = states_dic[cell]
        neighbouring_cells=neighbours[cell]
        
        for timestep in allowed_timesteps:
            timestep += 1
            for nei in neighbouring_cells:
                if nei in states_dic:
                    if timestep in states_dic[nei]:
                        if nei not in transition_prob_for_neighbours[cell]:
                            transition_prob_for_neighbours[cell][nei] = 0.0
                        transition_prob_for_neighbours[cell][nei] += 1.0
                        total_trasition_prob[cell]+=1.0
        for nei in transition_prob_for_neighbours[cell]:
            trans_prob[cell][nei]=transition_prob_for_neighbours[cell][nei] / total_trasition_prob[cell]
    return trans_prob

def viterbi(free_cell,tower_loc,noisy_dist,distancetotower,probable_states,neighbours,trans_prob):
    states=[]
    timestep=0
    possible_paths=collections.defaultdict(dict)
    possible_paths[timestep] = collections.defaultdict(dict)
    for item in probable_states[timestep]:
        item = tuple(item)
        possible_paths[timestep][item] = {}
        possible_paths[timestep][item]['parent'] = ''
        possible_paths[timestep][item]['prob'] = 1.0 / len(probable_states[timestep])
        
    for timestep in xrange(1,len(noisy_dist)):
        possible_paths[timestep] = collections.defaultdict(dict)
        for items in possible_paths[timestep-1]:
            if items in trans_prob:
                for nei in trans_prob[items]:
                    if list(nei) in probable_states[timestep]:
                        if nei not in possible_paths[timestep]:
                            possible_paths[timestep][nei] = {}
                            possible_paths[timestep][nei]['parent'] = items
                            present_prob = possible_paths[timestep - 1][items]['prob'] * trans_prob[items][nei]
                            possible_paths[timestep][nei]['prob'] = present_prob
                        else:
                            present_prob = possible_paths[timestep - 1][items]['prob'] * trans_prob[items][nei]
                            if present_prob > possible_paths[timestep][nei]['prob']:
                                possible_paths[timestep][nei]['parent'] = items
                                possible_paths[timestep][nei]['prob'] = present_prob   
    return possible_paths

def backtrack(possible_paths,final_timestep=10):
    max_prob = 0.0
    cell = None
    timestep=final_timestep
    final_path=[]
    for c in possible_paths[timestep]:
        if max_prob < possible_paths[timestep][c]['prob']:
            max_prob = possible_paths[timestep][c]['prob']
            cell = c
    final_path.append(cell)
    for timestep in xrange(10,0,-1):
        parent_cell = possible_paths[timestep][cell]['parent']
        final_path.append(parent_cell)
        cell = parent_cell
    return final_path

def main():
    file='hmm-data.txt'
    free_cell=free_cell_locations(file)
    tower_loc=tower_locations(file)
    noisy_dist=robot_tower_dist(file)
    distancetotower=distance_to_tower(free_cell,tower_loc)
    probable_states_dic=collections.defaultdict(list)
    states_dic=collections.defaultdict(list)
    for i in xrange(0,len(noisy_dist)):
        probable_states_dic[i]=find_probable_free_cells(free_cell,noisy_dist[i],distancetotower)
        for cell in probable_states_dic[i]:
            states_dic[tuple(cell)].append(i)
    print "states_dic__________________________"
    print states_dic
    neighbours=collections.defaultdict(list)
    for cell in states_dic:
        neighbours[cell] = find_neighbours(cell, 10)
    print "neighbours__________________________"
    print neighbours
    trans_prob=calculate_transition_probability(states_dic,neighbours)
    print "trans_prob__________________________"
    print trans_prob
    possible_paths=viterbi(free_cell,tower_loc,noisy_dist,distancetotower,probable_states_dic,neighbours,trans_prob)
    print "possible_paths______________________"
    print possible_paths
    path=backtrack(possible_paths)
    print("Path is:")
    print(path[::-1])
    
if __name__ == "__main__":
    main()