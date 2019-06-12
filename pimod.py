#!/usr/bin/env python

import copy
from sys import exit
from random import choice, sample,randint
import matplotlib.pyplot as plt 
import numpy as np
import time
from math import log2


def event(inputs, time_slot, load, iterations):
    n = len(inputs) #number of inputs 
    counter = 0
    packet_counter = 0
    prob = ( load * iterations ) # 0,4  prob for each input to have a packet
    for input in inputs:
        b  = randint(0, iterations)
        if b < prob:
            out = randint(0, n-1)
            input.append([out, time_slot, counter])
            packet_counter = packet_counter + 1 
        counter = counter + 1 
    return packet_counter



def pim(inputs): #log(N) iterations, N = switch_size
    switch_size = len(inputs)
    locked_input = []
    locked_output = []
    departed = [] #packets that got scheduled in this time_slot and thus are no longer present 
    iterations = int(log2(switch_size))
    for round in range(iterations):
        grants = []
        requests = []
        accepts = []
        for i in range(switch_size):
            grants.append([]) #inputs and their grants
            requests.append([]) #outputs and their requests
            accepts.append([]) #inputs and their accepted packets
            if round == 0:
                locked_input.append([]) # maps to inputs, inputs that have accepted    
                locked_output.append([])
        # In each iteration, it loops through all the inputs that are not locked, meaning that they have not been scheduled 
        # in a previous iteration. For each input, that is not already scheduled, it puts a request at each output.
        # Then each output, selects randomly an input to grant passage. Then finaly, each input that has received
        # a grant, picks randomly an output and accepts it's offer to schedule it's packet.
        # Finally, it loops through all the accepted packets (maximum 1/input) and it performs the following:
        # 1) Remove the packet from the input queue (it is scheduled, thus departs from the switch
        # 2) Lock both the input and the output of the packet for the current run, meaning that in next iterations the algorithm
        #    will not schedule packages from that input and to that output.
        # 3) Put the packet in the list of departed packets, this is needed to calculate the delay of each packet

        for input in inputs:			
            if input != [] and locked_input[inputs.index(input)] != True:
                for request in input:#request = packet = [output, arr_time, input]
                    if locked_output[request[0]] != True: #check if that request is already scheduled
                        requests[request[0]].append(request) # put packet in output reuqest
        # For every packet in input, put a request in requests, it maps to outputs
        #request = [ [0,3], .. ]
        for request in requests: #It's a list [ [], [], ...] where each element is an ouptut. If the element != [], then it has received a requst from an input
            if request != []: #if it has a request
                grant = sample(request,1)[0] #select one in random and put the packet that requested the grant, into the grant list
                grants[grant[2]].append(grant)
        
        for grant in grants: #a list of lists, where each element is an input that has received a grant request, from each element it chooses a packet in random to accept the grant.
            if grant != []:
                accept = sample(grant, 1)[0]
                accepts[accept[2]].append(accept)
        
        for i in range(switch_size):
            if accepts[i] != []: #For each input that has a corresponding accept.
                inputs[i].remove(accepts[i][0]) #accepts[i][0] = packet = [output, arr_time, input]. Remove the packet from the input
                locked_input[i] = True #that input got scheduled, not active for next iteration
                output_number = accepts[i][0][0] #get the output_number from the packet
                locked_output[output_number] = True
                departed.append(accepts[i][0])
    return departed 

def simulation(iterations,load,size):
    time_slot = 0
    inputs = []
    for i in range(size):
        inputs.append([])
    total_delay = 0
    packet_counter = 0
    for i in range (iterations):
        number_of_new_packets = event(inputs, time_slot, load, iterations)
        packet_counter = packet_counter + number_of_new_packets
        departed_packets = pim(inputs)
        delay = 0 
        for packet in departed_packets: #packet = [output, arr_time,input]
            delay = time_slot - packet[1] 
        total_delay = total_delay + delay       
        time_slot = time_slot + 1 
        if packet_counter == 0:
            packet_counter = 1
    average_delay = (total_delay/packet_counter)
    print (f"total delay: {total_delay}, average delay: {average_delay}, packet counter: {packet_counter}")
    return average_delay, time_slot

def main (): 
    iterations = 10**4
    size = 8
    averages = []
    loads =  np.linspace(0,1,10, endpoint= False)
    start_time = time.time()
    for load in loads:
        avg, final_time_slot = simulation(iterations,load,size)
        averages.append(avg)

    finish_time = time.time()
    run_time = finish_time - start_time
    run_minutes, run_seconds = divmod(run_time, 60)
    run_hours, run_minutes = divmod(run_minutes, 60)    
    print("~~~~~~~~~~~~~~~~~~~~")
    print ("Total Delay: " + str(avg) + "  Time Slot: " + str(iterations))

    plt.plot(loads, averages)
    plt.xlabel("network load")
    plt.ylabel("average packet delay")
    title = f"log(N) PIM | time slots: {iterations} | switch: {size} | Time: {run_hours}h:{run_minutes}m:{run_seconds:.2f}s"
    filename = "v2_simulations/time_" + str(iterations) + "-size_" + str(size)+ "-id_" + str(randint(0,1000000)) + ".png"
    plt.title(title)
    plt.savefig(filename)
    plt.show()


if __name__ == '__main__':
    main()

