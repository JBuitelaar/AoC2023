# Shortest path using Dijkstra's algorithm
import time
from heapq import heappush, heappop
from aocd.models import Puzzle

puzzle = Puzzle(2023,17)
data = puzzle.input_data
# data = puzzle.examples[0].input_data

N,S,W,E = -1,1,-1j,1j

lines = data.strip().split('\n')
R = len(lines)
C = len(lines[0])

loss_grid = {r+1j*c: int(v) for r,row in enumerate(lines) for c,v in enumerate(row)}

start_loc = 0
end_loc = R-1+(C-1)*1j

def print_path(path):
    for r,row in enumerate(lines):
        print("".join("█" if r+1j*c in path else val for c,val in enumerate(row)))


def solve(min_steps,max_steps): 
    to_do = [] # priority queue of nodes to evaluate (starting with the lowest value)
    seen = {}  # each element is a tuple of location and vertical (== a boolean indicating whether we just moved vertically or not)
    path = []  # for debugging and printing, keep track of the path
    # start off with the two directions
    heappush(to_do,(0,0,start_loc,True,[start_loc]))
    heappush(to_do,(0,1,start_loc,False,[start_loc]))
    counter=1  # need some way to sort the heap if the values are equal

    while to_do:
        (heat_lost,_,loc,prev_vertical,path) = heappop(to_do)

        if loc == end_loc:
            # DONE!
            # print_path(path)
            print(f"cache_size={len(seen)}")
            return heat_lost

        directions = (E,W) if prev_vertical else (N,S)

        # turn 90 degrees in both directions
        for dir in directions:
            new_loc=loc
            new_cost = heat_lost
            new_path = [p for p in path]  # copy
            for step in range(1,max_steps+1):
                new_loc += dir
                if new_loc not in loss_grid:   # don't go outside of the grid
                    break
                
                new_cost += loss_grid[new_loc]
                new_path.append(new_loc)
                if step < min_steps:  # can't turn before making min_steps
                    continue
                vertical = not prev_vertical
                key = (new_loc,vertical)
                if key in seen and seen[key]<=new_cost:
                    continue
                seen[key] = new_cost
                counter+=1
                heappush(to_do,(new_cost,counter,new_loc,vertical,new_path))


inputs = [(1,3),(4,10)]

for q,(min_steps,max_steps) in enumerate(inputs,1):
    start_time = time.time()
    ans = solve(min_steps,max_steps)
    timer = time.time()-start_time
    print(f"ans{q}={ans}, {timer=:.2f}")
