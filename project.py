import matplotlib.pyplot as plt
import random
import math
import numpy as np
from collections import deque

def getInstance(p, a, globP, globA):
    
    players = []
    arms = []
    
    # construct player preference list
    if (globA):
        temp = [i for i in range(a)]
        random.shuffle(temp)
        for i in range(p):
            players.append(temp)
    else:
        for i in range(p):
            temp = [i for i in range(a)]
            random.shuffle(temp)
            players.append(temp)
        
    # construct arm preference list
    if (globP):
        temp = [i for i in range(p)]
        random.shuffle(temp)
        for i in range(a):
            arms.append(temp)  
    else:
        for i in range(a):
            temp = [i for i in range(p)]
            random.shuffle(temp)
            arms.append(temp)
 
                       
    return players, arms


def pull(players, armP):
    for rank in armP:
        for player in players:
            if (player == rank):
                return player


def gs(pPre, aPre):
    
    # init all player and woman to free
    freePlayers = deque()
    armMatches = {i: None for i in range(len(aPre))}
    assignment = {i: None for i in range(len(pPre))}
    for i in range(len(pPre)):
        freePlayers.append(i)
        
    availablePropose = {i: deque() for i in range(len(pPre))}
    for i in range(len(pPre)):
        for arm in pPre[i]:
            availablePropose[i].append(arm)
    
    while (len(freePlayers) is not 0):
        curPlayer = freePlayers.popleft()
        curPropose = availablePropose[curPlayer].popleft()
        
        # target arm is free
        if (armMatches[curPropose] == None):
            armMatches[curPropose] = curPlayer
            assignment[curPlayer] = curPropose
        
        else:
            compitator = armMatches[curPropose]
            if (aPre[curPropose].index(curPlayer) < aPre[curPropose].index(compitator)):
                armMatches[curPropose] = curPlayer
                assignment[curPlayer] = curPropose
                freePlayers.append(compitator)
            else:
                freePlayers.append(curPlayer)
            
    result = []
    score = 0
    
    for i in range(0, len(pPre)):
        result.append(tuple((i, assignment[i])))
    
    for j in range(len(result)):
        score += pPre[j].index(result[j][1])
        
    return result, score


def greedy(pPre, aPre, itr, eps):
    assignmentRecord = []
    winRecord = {i: {} for i in range(len(pPre))}
    totRecord = {i: {} for i in range(len(pPre))}
    assignment = {}
    
    for t in range(1, itr):
        
        candidate = {arm: [] for arm in range(len(aPre))}

        for player in range(len(pPre)):
            if (t == 1):
                for arm in range(len(aPre)):
                    winRecord[player][arm] = 0
                    totRecord[player][arm] = 1
                    candidate[arm].append(player)
                
            else:
                currentEps = pow(eps, t/100)
                r = random.random()
                if (r > currentEps): 
                    utility = {}
                    for arm in range(len(aPre)):                      
                        utility[arm] = winRecord[player][arm] / totRecord[player][arm] * (1 / (pPre[player].index(arm) + 1))
                    action = max(utility, key=utility.get)
                    totRecord[player][action] += 1
                    candidate[action].append(player)
                    
                else:
                    action = random.randint(0, len(aPre)-1)
                    totRecord[player][action] += 1
                    candidate[action].append(player)
 
        for arm in range(len(aPre)):
            if (len(candidate[arm]) > 0):
                winner = pull(candidate[arm], aPre[arm])
                winRecord[winner][arm] += 1  
                assignment[winner] = arm
        
        tempResult = []
        score = 0
    
        for player in range(0, len(pPre)):
            utility = {}
            for arm in range(len(aPre)):                      
                utility[arm] = winRecord[player][arm] / totRecord[player][arm] * (1 / (pPre[player].index(arm) + 1))
            tempResult.append(tuple((player, max(utility, key=utility.get))))
    
        for j in range(len(tempResult)):
            score += pPre[j].index(tempResult[j][1])      
        assignmentRecord.append(score)
                
    result = []
    score = 0
    
    for player in range(0, len(pPre)):
        utility = {}
        for arm in range(len(aPre)):                      
            utility[arm] = winRecord[player][arm] / totRecord[player][arm] * (1 / (pPre[player].index(arm) + 1))
        result.append(tuple((player, max(utility, key=utility.get))))
    
    for j in range(len(result)):
        score += pPre[j].index(result[j][1])
        
    return result, assignmentRecord
    

def thompson(pPre, aPre, itr):
    assignmentRecord = []
    aRecord = {i: {} for i in range(len(pPre))}
    bRecord = {i: {} for i in range(len(pPre))}
    assignment = {i: None for i in range(len(pPre))}
    
    for t in range(1, itr):
        candidate = {arm: [] for arm in range(len(aPre))}
        
        for player in range(len(pPre)):
            if (t == 1):
                for arm in range(len(aPre)):
                    aRecord[player][arm] = 1
                    bRecord[player][arm] = 1
        
            else:          
                beta = {}
            
                for arm in range(len(aPre)):
                    beta[arm] = (1 / (pPre[player].index(arm) + 1)) * np.random.beta(aRecord[player][arm], bRecord[player][arm])
            
                action = max(beta, key=beta.get)
                candidate[action].append(player)                                
            
        for arm in range(len(aPre)):
            if (len(candidate[arm]) > 0):
                winner = pull(candidate[arm], aPre[arm])
                assignment[winner] = arm
                for c in candidate[arm]:
                    if (c == winner):
                        aRecord[c][arm] += 1
                    else:
                        bRecord[c][arm] += 1
                        
                        
        tempResult = []
        score = 0
        for i in range(0, len(pPre)):
            tempResult.append(tuple((i, assignment[i])))
            
        for j in range(len(tempResult)):
            if(tempResult[j][1] is not None):
                score += pPre[j].index(tempResult[j][1])
        assignmentRecord.append(score)
        
    result = []
    score = 0
    for i in range(0, len(pPre)):
        result.append(tuple((i, assignment[i])))
    
    for j in range(len(result)):
        score += pPre[j].index(result[j][1])
        
    return result, assignmentRecord

def caucb(pPre, aPre, itr, lam):
    assignmentRecord = []
    ucb = {i: {} for i in range(len(pPre))}
    winRecord = {i: {} for i in range(len(pPre))}
    totRecord = {i: {} for i in range(len(pPre))}
    lastAction = {}
    lastCandidate = {}
    assignment = {i: None for i in range(len(pPre))}

    for t in range(1, itr):
        
        action = {}
        candidate = {arm: [] for arm in range(len(aPre))}

        for player in range(len(pPre)):
            if (t == 1):
                for arm in range(len(aPre)):
                    ucb[player][arm] = np.inf
                    winRecord[player][arm] = 0
                    totRecord[player][arm] = 0
                    
                action[player] = random.randint(0, len(aPre)-1)
                totRecord[player][action[player]] += 1
                candidate[action[player]].append(player)
                
            else:
                r = random.random()
                if (r > lam): 
                    plausible = []
                    for arm in range(len(aPre)):
                        plause = True
                        for previousPlayer in lastCandidate[arm]:
                            if (aPre[arm].index(player) > aPre[arm].index(previousPlayer)):
                                plause = False
                                break
                        if (plause):
                            plausible.append(arm)
                            
                    partialUcb = {}
                    for arm in plausible:
                        partialUcb[arm] = ucb[player][arm]
                    action[player] = max(partialUcb, key=partialUcb.get)
                    totRecord[player][action[player]] += 1
                    candidate[action[player]].append(player)
                    
                else:
                    action[player] = lastAction[player]
                    totRecord[player][action[player]] += 1
                    candidate[action[player]].append(player)
 
        for player in range(len(pPre)):
            if (pull(candidate[action[player]], aPre[action[player]]) == player):
                winRecord[player][action[player]] += 1
                ucb[player][action[player]] = (1 / (pPre[player].index(action[player]) + 1)) * (winRecord[player][action[player]] / totRecord[player][action[player]]) + math.sqrt(3 * math.log(t) / totRecord[player][action[player]]) 
                assignment[player] = action[player]
                
        tempResult = []
        score = 0
        for i in range(0, len(pPre)):
            tempResult.append(tuple((i, assignment[i])))
            
        for j in range(len(tempResult)):
            if (tempResult[j][1] is not None):
                score += pPre[j].index(tempResult[j][1])
        assignmentRecord.append(score)
        
        lastAction = action.copy()
        lastCandidate = candidate.copy()
        
    
    result = []
    score = 0
    
    for i in range(0, len(pPre)):
        result.append(tuple((i, assignment[i])))
    
    for j in range(len(result)):
        score += pPre[j].index(result[j][1])
        
    return result, assignmentRecord

def ffconverge(itr):
    count11 = 0
    count12 = 0
    count13 = 0
    
    count21 = 0
    count22 = 0
    count23 = 0
    
    count31 = 0
    count32 = 0
    count33 = 0
    
    count41 = 0
    count42 = 0
    count43 = 0
    
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    
    for i in range(0, itr):
        print(i)
        
        
        players, arms = getInstance(5, 5, True, True)
        answer = gs(players, arms)
        if (greedy(players, arms, 30000, 0.9) == answer): count11 += 1
        if (thompson(players, arms, 30000) == answer): count12 += 1
        if (caucb(players, arms, 30000, 0.2) == answer): count13 += 1
        
        
        players, arms = getInstance(5, 5, True, False)
        answer = gs(players, arms)
        if (greedy(players, arms, 30000, 0.9) == answer): count21 += 1
        if (thompson(players, arms, 30000) == answer): count22 += 1
        if (caucb(players, arms, 30000, 0.2) == answer): count23 += 1
        
        players, arms = getInstance(5, 5, False, True)
        answer = gs(players, arms)
        if (greedy(players, arms, 30000, 0.9) == answer): count31 += 1
        if (thompson(players, arms, 30000) == answer): count32 += 1
        if (caucb(players, arms, 30000, 0.2) == answer): count33 += 1
        
        players, arms = getInstance(5, 5, False, False)
        answer = gs(players, arms)
        if (greedy(players, arms, 30000, 0.9) == answer): count41 += 1
        if (thompson(players, arms, 30000) == answer): count42 += 1
        if (caucb(players, arms, 30000, 0.2) == answer): count43 += 1
        
        
        

    data1.append(count11 / itr)
    data1.append(count12 / itr)
    data1.append(count13 / itr)
    
    data2.append(count21 / itr)
    data2.append(count22 / itr)
    data2.append(count23 / itr)
    
    data3.append(count31 / itr)
    data3.append(count32 / itr)
    data3.append(count33 / itr)
    
    data4.append(count41 / itr)
    data4.append(count42 / itr)
    data4.append(count43 / itr)
    
    labels = ['greedy', 'thompson', 'ca-ucb']
    
    x = np.arange(len(labels))
    width = 0.2
    
    fig, ax = plt.subplots()
    
    rects1 = ax.bar(x - 3 *width/2, data1, width, label='Global Both')
    for rect, data in zip(rects1, data1):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, data, ha='center', va='bottom')
    
    rects2 = ax.bar(x - width/2, data2, width, label='Global Player')
    for rect, data in zip(rects2, data2):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, data, ha='center', va='bottom')
    
    rects3 = ax.bar(x + width/2, data3, width, label='Global Arm')
    for rect, data in zip(rects3, data3):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, data, ha='center', va='bottom')
    
    rects4 = ax.bar(x + 3 * width/2, data4, width, label='Arbitrary Both')
    for rect, data in zip(rects4, data4):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, data, ha='center', va='bottom')
        
        
    ax.set_ylabel('P to Stable Matching')
    ax.set_title('Convergence')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='lower center')

    fig.tight_layout()

    plt.show()


def ftconverge(itr):
    count11 = 0
    count12 = 0
    count13 = 0
    
    count21 = 0
    count22 = 0
    count23 = 0
        
    data1 = []
    data2 = []
    
    for i in range(itr):
        print(i)
        players, arms = getInstance(5, 5, False, False)
        answer = gs(players, arms)
        if (greedy(players, arms, 30000, 0.9) == answer): count11 += 1
        if (thompson(players, arms, 30000) == answer): count12 += 1
        if (caucb(players, arms, 30000, 0.2) == answer): count13 += 1
        
        players, arms = getInstance(5, 10, False, False)
        answer = gs(players, arms)
        if (greedy(players, arms, 30000, 0.9) == answer): count21 += 1
        if (thompson(players, arms, 30000) == answer): count22 += 1
        if (caucb(players, arms, 30000, 0.2) == answer): count23 += 1
        
        
    data1.append(count11 / itr)
    data1.append(count12 / itr)
    data1.append(count13 / itr)
    
    data2.append(count21 / itr)
    data2.append(count22 / itr)
    data2.append(count22 / itr)
    
    labels = ['greedy', 'thompson', 'ca-ucb']
    
    x = np.arange(len(labels))
    width = 0.2
    
    fig, ax = plt.subplots()
    
    rects1 = ax.bar(x - width/2, data1, width, label='5 arms')
    for rect, data in zip(rects1, data1):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, data, ha='center', va='bottom')
    
    rects2 = ax.bar(x + width/2, data2, width, label='10 arms')
    for rect, data in zip(rects2, data2):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, data, ha='center', va='bottom')
        
    ax.set_ylabel('P to Stable Matching')
    ax.set_title('Convergence')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='lower center')

    fig.tight_layout()

    plt.show()


def fftime1(itr):
    data1 = {i: 0 for i in range(29999)}
    data2 = {i: 0 for i in range(29999)}
    data3 = {i: 0 for i in range(29999)}
    
    for i in range(itr):
        print(i)

        players, arms = getInstance(5, 5, True, True)
        assignmentRecord1 = greedy(players, arms, 30000, 0.9)[1]
        assignmentRecord2 = thompson(players, arms, 30000)[1]
        assignmentRecord3 = caucb(players, arms, 30000, 0.2)[1]
        
        for i in range(len(assignmentRecord1)):
            data1[i] += assignmentRecord1[i]
            data2[i] += assignmentRecord2[i]
            data3[i] += assignmentRecord3[i]   
    
    for i in range(29999):
        data1[i] /= itr
        data2[i] /= itr
        data3[i] /= itr

        
    plt.figure(1)
    plt.plot(data1.keys(), data1.values())
    plt.plot(data2.keys(), data2.values())
    plt.plot(data3.keys(), data3.values())
    plt.legend(["greedy", "thompson", "caucb"], loc ="lower right")
    plt.xlabel("t")
    plt.ylabel("Total Rank")
    plt.title("Global Both")
    
    plt.show()
    

def fftime2(itr):
    data1 = {i: 0 for i in range(29999)}
    data2 = {i: 0 for i in range(29999)}
    data3 = {i: 0 for i in range(29999)}
    
    for i in range(itr):
        print(i)

        players, arms = getInstance(5, 5, True, False)
        assignmentRecord1 = greedy(players, arms, 30000, 0.9)[1]
        assignmentRecord2 = thompson(players, arms, 30000)[1]
        assignmentRecord3 = caucb(players, arms, 30000, 0.2)[1]
        
        for i in range(len(assignmentRecord1)):
            data1[i] += assignmentRecord1[i]
            data2[i] += assignmentRecord2[i]
            data3[i] += assignmentRecord3[i]   
    
    for i in range(29999):
        data1[i] /= itr
        data2[i] /= itr
        data3[i] /= itr

        
    plt.figure(1)
    plt.plot(data1.keys(), data1.values())
    plt.plot(data2.keys(), data2.values())
    plt.plot(data3.keys(), data3.values())
    plt.legend(["greedy", "thompson", "caucb"], loc ="lower right")
    plt.xlabel("t")
    plt.ylabel("Total Rank")
    plt.title("Global Players")
    
    plt.show()


def fftime3(itr):
    
    data1 = {i: 0 for i in range(29999)}
    data2 = {i: 0 for i in range(29999)}
    data3 = {i: 0 for i in range(29999)}
    
    for i in range(itr):
        print(i)

        players, arms = getInstance(5, 5, False, True)
        assignmentRecord1 = greedy(players, arms, 30000, 0.9)[1]
        assignmentRecord2 = thompson(players, arms, 30000)[1]
        assignmentRecord3 = caucb(players, arms, 30000, 0.2)[1]
        
        for i in range(len(assignmentRecord1)):
            data1[i] += assignmentRecord1[i]
            data2[i] += assignmentRecord2[i]
            data3[i] += assignmentRecord3[i]   
    
    for i in range(29999):
        data1[i] /= itr
        data2[i] /= itr
        data3[i] /= itr

        
    plt.figure(1)
    plt.plot(data1.keys(), data1.values())
    plt.plot(data2.keys(), data2.values())
    plt.plot(data3.keys(), data3.values())
    plt.legend(["greedy", "thompson", "caucb"], loc ="lower right")
    plt.xlabel("t")
    plt.ylabel("Total Rank")
    plt.title("Global Arms")
    
    plt.show()


def fftime4(itr):
    
    data1 = {i: 0 for i in range(29999)}
    data2 = {i: 0 for i in range(29999)}
    data3 = {i: 0 for i in range(29999)}
    
    for i in range(itr):
        print(i)

        players, arms = getInstance(5, 5, False, False)
        assignmentRecord1 = greedy(players, arms, 30000, 0.9)[1]
        assignmentRecord2 = thompson(players, arms, 30000)[1]
        assignmentRecord3 = caucb(players, arms, 30000, 0.2)[1]
        
        for i in range(len(assignmentRecord1)):
            data1[i] += assignmentRecord1[i]
            data2[i] += assignmentRecord2[i]
            data3[i] += assignmentRecord3[i]   
    
    for i in range(29999):
        data1[i] /= itr
        data2[i] /= itr
        data3[i] /= itr

        
    plt.figure(1)
    plt.plot(data1.keys(), data1.values())
    plt.plot(data2.keys(), data2.values())
    plt.plot(data3.keys(), data3.values())
    plt.legend(["greedy", "thompson", "caucb"], loc ="lower right")
    plt.xlabel("t")
    plt.ylabel("Total Rank")
    plt.title("Arbitrary Both")
    
    plt.show()



def fftime5(itr):
    
    data1 = {i: 0 for i in range(29999)}
    data2 = {i: 0 for i in range(29999)}
    data3 = {i: 0 for i in range(29999)}
    
    for i in range(itr):
        print(i)

        players, arms = getInstance(5, 10, False, False)
        assignmentRecord1 = greedy(players, arms, 30000, 0.9)[1]
        assignmentRecord2 = thompson(players, arms, 30000)[1]
        assignmentRecord3 = caucb(players, arms, 30000, 0.2)[1]
        
        for i in range(len(assignmentRecord1)):
            data1[i] += assignmentRecord1[i]
            data2[i] += assignmentRecord2[i]
            data3[i] += assignmentRecord3[i]   
    
    for i in range(29999):
        data1[i] /= itr
        data2[i] /= itr
        data3[i] /= itr

        
    plt.figure(1)
    plt.plot(data1.keys(), data1.values())
    plt.plot(data2.keys(), data2.values())
    plt.plot(data3.keys(), data3.values())
    plt.legend(["greedy", "thompson", "caucb"], loc ="lower right")
    plt.xlabel("t")
    plt.ylabel("Total Rank")
    plt.title("Arbitrary Both 10 arms")
    
    plt.show()



if __name__=="__main__": 
    players, arms = getInstance(5, 5, False, False)
    print(players, arms)
    print(gs(players, arms)[0])
    print(players, arms)
    print(greedy(players, arms, 30000, 0.9)[0])
    print(thompson(players, arms, 30000)[0])
    print(caucb(players, arms, 30000, 0.2)[0])
    #fftime1(500)
    #fftime2(500)
    #fftime3(500)
    #fftime4(500)
    #fftime5(500)
    #ffconverge(50)
    #ftconverge(500)
    