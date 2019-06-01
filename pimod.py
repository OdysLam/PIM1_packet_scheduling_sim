#!/usr/bin/env python

import copy
from sys import exit
from random import choice, sample,randint
import matplotlib.pyplot as plt 
import numpy as np



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



def pim(inputs):
    
    while(1):
        grants = [[], [], [], []] #map to inputs
        requests = [[], [], [], []] #map to outputs
        accepts = [[], [], [], []] #map to inputs
        departed = []
        while(1):
            for input in inputs:			
                if input != []:
                    for request in input:#request = packet = [output, arr_time, input]
                        requests[request[0]].append(request) # put packet in output reuqest
            # For every packet in input, put a request in requests, it maps to outputs
            #request = [ [0,3], .. ]
            for request in requests: 
                if request != []:
                    grant = sample(request,1)[0]
                    grants[grant[2]].append(grant)
            
            for grant in grants:
                if grant != []:
                    accept = sample(grant, 1)[0]
                    accepts[accept[2]].append(accept)
            
            for i in range(len(inputs)):
                if inputs[i] != [] and accepts[i] != []:
                    index = inputs[i].index(accepts[i][0])
                    inputs[i].remove(accepts[i][0])
                    departed.append(accepts[i][0])
            break
        return departed 


def main (): 
    iterations = 10**4
    size = 4
    averages = []
    loads =  np.linspace(0,1,10, endpoint= False)
    for load in loads:
        avg, time = simulation(iterations,load,size)
        averages.append(avg)

    print("~~~~~~~~~~~~~~~~~~~~")
    print ("Total Delay: " + str(avg) + "  Time Slot: " + str(iterations))

    plt.plot(loads, averages)
    plt.xlabel("network load")
    plt.ylabel("average packet delay")
    title = "PIM simulation for various loads and " + str(iterations) + " time-slots"
    filename = "simulations/time_" + str(iterations) + "-size_" + str(size)+ "-id_" + str(randint(0,1000000)) + ".png"
    plt.title(title)
    plt.savefig(filename)
    plt.show()

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
    average_delay = total_delay/packet_counter
    return average_delay, time_slot

if __name__ == '__main__':
    main()

