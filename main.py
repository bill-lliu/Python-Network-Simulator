import math
# import numpy
import random
import matplotlib

def main():
    print("Hello World!")
    # L A/S/N/K
    length = given # (L) average packet length in bits
    serviceR = 0 # (S) service process rate
    numServers = 0 # (N) number of servers
    queueSize = 0 # (K) queue size
    rho = given # utilization
    A = S * rho / L # arrival rate
    simulation(L, A, S, N, K)
    packets[] # <- 2d list
    # λ = Average number of packets generated /arrived (packets per second)
    # L = Average length of a packet in bits.
    # α = Average number of observer events per second
    # C = The transmission rate of the output link in bits per second.
    # ρ = Utilization of the queue (= input rate/service rate = L λ/C)
    # E[N] = Average number of packets in the buffer/queue
    # PIDLE = The proportion of time the server is idle, i.e., no packets in the queue nor a packet is being transmitted.
    # PLOSS = The packet loss probability (for M/M/1/K queue). It is the ratio of the total number of packets lost due to
    # buffer full condition to the total number of generated packets


if __name__ == "__main__":
    main()



def poisson(lmbd):
	#poisson distribution
    return (-(1 / lmbd) * math.log(1 - random.random()))


def simulation(avgPktLength, rho, serviceRate, queueSize, maxTime):
    #Generate packets
    arrPktRate = (rho * serviceRate) / avgPktLength
    prevArrv = 0
    prevDpt = 0

    packets = []

    while (prevArrv < maxTime):
        currArrv = prevArrv + poisson(arrPktRate)
        pktLength = poisson(1/avgPktLength)
        #since average of poisson is 1/lambda and lamba is 1/avg then average = avgpktlength
        serviceTime = pktLength/serviceRate
        if prevDpt <= currArrv:
            #nothing in queue
            currDpt = currArrv + serviceTime
        else:
            #Have to wait in queue
            currDpt = prevDpt + serviceTime

        packets.append([currArrv, pktLength, serviceTime, currDpt])
        prevArrv = currArrv
        prevDpt = currDpt
	
    #generate observers
    observers = []
    prevObs = 0
    while (prevObs < maxTime):
        currObs = prevObs + poisson(5*arrPktRate)
        observers.append(currObs)
        prevObs = currObs

    events = []

    for pkt in packets:
        events.append(["Arrival", pkt[0], pkt[2]])
        events.append(["Departure", pkt[1]])

    for obs in observers:
        events.append(["Observer", obs])


    events.sort(key = lambda e: e[1])

    c_arr = 0
    c_dpt = 0
    c_obs = 0

    c_idle = 0
    c_queue = 0
    c_loss = 0

    dpts = []
    prevDpt = 0


    for event in events:
        if event[1] < maxTime:
            if queueSize == math.inf:
                if event[0] == "Arrival":
                    c_arr = c_arr + 1
                elif event[0] == "Departure":
                    c_dpt = c_dpt + 1
                elif event[0] == "Observer":
                    c_obs = c_obs + 1
                    if (c_arr == c_dpt):
                        c_idle = c_idle + 1
                    else:
                        c_queue = c_queue + c_arr - c_dpt
            else:
                #Need to flush departures before next event
                while len(dpts) > 0 & dpts[0] < event[1]:
                    c_dpt = c_dpt + 1
                    dpts.remove(0)
                #Need to generate departures since pre-sim ones are ignored
                if event[0] == "Arrival":
                    if c_arr - c_dpt < queueSize:
                        c_arr = c_arr + 1
                        if prevDpt <= event[1]:
                            #nothing in queue
                            currDpt = event[1] + event[2]
                        else:
                            #Have to wait in queue
                            currDpt = prevDpt + event[2]
                        dpts.append(currDpt)
                        prevDpt = currDpt
                    else:
                        c_drop = c_drop + 1
                        c_arr = c_arr + 1
                        c_dpt = c_dpt + 1
                elif event[0] == "Observer":
                    c_obs = c_obs + 1
                    if (c_arr == c_dpt):
                        c_idle = c_idle + 1
                    else:
                        c_queue = c_queue + (c_arr - c_dpt)
                
    
    #Need to flush departures before maxTime after maxTime exceeded in events
    while len(dpts) > 0 & dpts[0] < maxTime:
        c_dpt = c_dpt + 1
        dpts.remove(0)

    avgPkts = c_queue / c_obs
    rateLoss = c_loss/c_arr
    rateIdle = c_idle/c_obs
    return avgPkts, rateLoss, rateIdle
    

