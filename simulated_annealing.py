import math, random

#SA function pseudo code described here http://en.wikipedia.org/wiki/Simulated_annealing

def cooling(start_temp,alpha):
    temp=start_temp
    while True:
        yield temp
        temp=alpha*temp

#Based on current function temparture, returns a value corresponding to the "chance" the the next value is < the current. The higher the temp, the less risk the function will take.
def probability(current_score,next_score,temperature):
    if next_score > current_score:
        return 1.0
    else:
        return math.exp( -abs(next_score-current_score)/temperature )

def anneal(new_start,random_tour_permutation,tour_length,max_runs,start_temp,alpha):    
    current=new_start()
    current_score=tour_length(current)

    tours=[] #List to store the tour lengths
    path=[] #List to store the paths
    
    num_evaluations=1
    
    cooling_schedule=cooling(start_temp,alpha)
    
    for temperature in cooling_schedule:
        done = False
 
        for next in random_tour_permutation(current):
            if num_evaluations >= max_runs:
                done=True
                break
        
            next_score=tour_length(next)
            tours.append(next_score)
            num_evaluations+=1
            
            change=probability(current_score,next_score,temperature)
            if random.random() < change:
                current=next
                current_score=next_score
                path=next
                break
        if done: break

    return (max(tours),path)