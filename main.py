import math
import numpy
import random
import matplotlib.pyplot as plt
import time

# FOR TESTING
# Near the bottom of the file, you will see our main function, 
# where the function calls are located. For example, Q4() is uncommented, 
# meaning our code will simulate the response for Q4(). If you would like to 
# personally test the data, simply call the simulation() function 
# with your desired parameters, and print out the data() value that is returned 
# afterwards to see the result. 

# used to generate random numbers
def exponential_random(lmbd):
	#poisson distribution
    return (-(1 / lmbd) * math.log(1 - random.random()))


# simulate given parameters
def simulation(avgPktLength, rho, serviceRate, queueSize, maxTime):
    #Generate packets
    arrPktRate = (rho * serviceRate) / avgPktLength
    prevArrv = 0
    prevDpt = 0

    packets = []

    while (prevArrv < maxTime):
        currArrv = prevArrv + exponential_random(arrPktRate)
        pktLength = exponential_random(1/avgPktLength)
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
        currObs = prevObs + exponential_random(5*arrPktRate)
        observers.append(currObs)
        prevObs = currObs

    events = []

    for pkt in packets:
        events.append(["Arrival", pkt[0], pkt[2]])
        if (queueSize == math.inf):
            events.append(["Departure", pkt[3]])

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
                    c_arr += 1
                elif event[0] == "Departure":
                    c_dpt += 1
                elif event[0] == "Observer":
                    c_obs += 1
                    if (c_arr == c_dpt):
                        c_idle += 1
                    else:
                        c_queue += (c_arr - c_dpt)
            else:
                #Need to flush departures before next event
                while (len(dpts) > 0 and dpts[0] < event[1]):
                    c_dpt += 1
                    dpts.pop(0)
                #Need to generate departures since pre-sim ones are ignored
                if event[0] == "Arrival":
                    if c_arr - c_dpt < queueSize:
                        c_arr += 1
                        if prevDpt <= event[1]:
                            #nothing in queue
                            currDpt = event[1] + event[2]
                        else:
                            #Have to wait in queue
                            currDpt = prevDpt + event[2]
                        dpts.append(currDpt)
                        prevDpt = currDpt
                    else:
                        c_loss += 1
                        c_arr += 1
                        c_dpt += 1
                elif event[0] == "Observer":
                    c_obs += 1
                    if (c_arr == c_dpt):
                        c_idle += 1
                    else:
                        c_queue += (c_arr - c_dpt)

    avgPkts = c_queue / c_obs
    rateLoss = c_loss/c_arr
    rateIdle = c_idle/c_obs
    
    return avgPkts, rateLoss, rateIdle, rho


# question 1
def q1():
    nums = []
    for i in range(1000):
        nums.append(exponential_random(75))
    mean = numpy.mean(nums)
    variance = numpy.var(nums)
    print(mean)
    print(variance)

    #need to make sure the mean and variance are right
    #mean should be 1/75
    #variance should be 1/(75^2)

# question 3
def q3():
    data = []
    xaxis = []
    yaxis = []
    y2axis = []
    #Need to figure out a max time
    rho = 0.25
    while rho<=0.95:
        data.append(simulation(2000, rho, 1e6, math.inf, 2000))
        rho += 0.1
    print(data)

    for s in data:
        xaxis.append(s[3])
        yaxis.append(s[0]) # index 0 is E[N]
        y2axis.append(s[2]) # index 2 is P_idle

    # x = numpy.linspace(0.25, 0.1, 0.95)

    plt.figure(1)
    plt.plot(xaxis, yaxis, '-o')
    plt.xlabel('Rho')
    plt.ylabel('E[N]')
    plt.title("Rho vs. E[N]")

    
    plt.figure(2)
    plt.plot(xaxis, y2axis, '-o')
    plt.xlabel('Rho')
    plt.ylabel('P_idle')
    plt.title("Rho vs. P_idle")


    plt.show()


# question 4
def q4():
    data = simulation(2000, 1.2, 1e6, math.inf, 3000)
    print(data)

# question 6
def q6():
    data_k10 = []
    data_k25 = []
    data_k50 = []
    rho = 0.5
    while rho<=1.5:
        data_k10.append(simulation(2000, rho, 1e6, 10, 7000))
        data_k25.append(simulation(2000, rho, 1e6, 25, 7000))
        data_k50.append(simulation(2000, rho, 1e6, 50, 7000))
        rho += 0.1
    print(data_k10)
    print(data_k25)
    print(data_k50)

    xaxis = []
    yaxis_e1 = []
    yaxis_e2 = []
    yaxis_e3 = []
    yaxis_l1 = []
    yaxis_l2 = []
    yaxis_l3 = []
    yaxis_p1 = []
    yaxis_p2 = []
    yaxis_p3 = []

    for s in data_k10:
        xaxis.append(s[3])
        yaxis_e1.append(s[0]) # index 0 is E[N]
        yaxis_l1.append(s[1]) # index 1 is P_loss
        yaxis_p1.append(s[2]) # index 2 is P_idle
    for s in data_k25:
        yaxis_e2.append(s[0]) # index 0 is E[N]
        yaxis_l2.append(s[1]) # index 1 is P_loss
        yaxis_p2.append(s[2]) # index 2 is P_idle
    for s in data_k50:
        yaxis_e3.append(s[0]) # index 0 is E[N]
        yaxis_l3.append(s[1]) # index 1 is P_loss
        yaxis_p3.append(s[2]) # index 2 is P_idle
        
    plt.figure(1)
    plt.plot(xaxis, yaxis_e1, '-o', label = "k=10")
    plt.plot(xaxis, yaxis_e2, '-o', label = "k=25")
    plt.plot(xaxis, yaxis_e3, '-o', label = "k=50")
    plt.xlabel('Rho')
    plt.ylabel('E[N]')
    plt.title("Rho vs. E[N]")
    
    plt.figure(2)
    plt.plot(xaxis, yaxis_l1, '-o', label = "k=10")
    plt.plot(xaxis, yaxis_l2, '-o', label = "k=25")
    plt.plot(xaxis, yaxis_l3, '-o', label = "k=50")
    plt.xlabel('Rho')
    plt.ylabel('P_loss')
    plt.title("Rho vs. P_loss")

    plt.figure(3)
    plt.plot(xaxis, yaxis_p1, '-o', label = "k=10")
    plt.plot(xaxis, yaxis_p2, '-o', label = "k=25")
    plt.plot(xaxis, yaxis_p3, '-o', label = "k=50")
    plt.xlabel('Rho')
    plt.ylabel('P_idle')
    plt.title("Rho vs. P_idle")
    
    plt.show()
    plt.legend()


# returns amount of time required for simulation to be stable
def find_time():
    initial_sim = simulation(2000, 0.5, 1e6, 10, 1000)
    multiplier = 2
    continue_loop = True
    while(continue_loop):
        new_sim = simulation(2000, 0.5, 1e6, 10, 1000*multiplier)
        if ((abs(initial_sim[0]-new_sim[0])/initial_sim[0]<0.05) and 
            (abs(initial_sim[1]-new_sim[1])/initial_sim[1]<0.05) and 
            (abs(initial_sim[2]-new_sim[2])/initial_sim[2] < 0.05)):
            continue_loop = False
        initial_sim = new_sim
        multiplier += 1
    return 1000*(multiplier-1)

# main function
def main():
    start_time = time.time()
    print("simulation now running")
    # print(find_time())
    # q1()
    # q3()
    q4()
    # q6()
    print("simulation completed in %s seconds" % (time.time() - start_time))

if __name__ == "__main__":
    main()
