import random
import itertools

NUM_OF_SESSION = 4
NUM_OF_PROF = 10
MAX_SCORE = NUM_OF_SESSION*(NUM_OF_PROF // 2)
PREFERENCES = [[1, 3, 7, 9],
               [0, 4, 5, 7],
               [3, 5, 8, 9],
               [0, 2, 4, 6],
               [1, 3, 5, 7, 8],
               [1, 2, 4, 6],
               [3, 5, 8, 9],
               [0, 1, 4, 8],
               [2, 4, 6, 7, 9],
               [0, 2, 6, 8]]

def createChromosome():
    myChromosome = []
    for count in range(NUM_OF_SESSION):
        myProfs = list(range(NUM_OF_PROF))
        random.shuffle(myProfs)
        myChromosome.append(myProfs)
    return myChromosome

def generatePopulation(popSize):
    newPopulation = []
    for count in range(popSize):
        newPopulation.append(createChromosome())
    return newPopulation

def getKey(item):
    return item[1]

def sortPopulation(population):
    newList = []
    for chromosome in population:
        score = evaluateChromosome(chromosome)
        newList.append((chromosome,score))
    newList = sorted(newList, key = getKey)

    newPopulation = []
    for index in range(len(newList)):
        newPopulation.append(newList[index][0])
    return newPopulation

def evaluateChromosome(chromosome):
    score = MAX_SCORE
    pairList = []
    for session in chromosome:
        for index in range(0, NUM_OF_PROF, 2):
            profA = min(session[index],session[index + 1])
            profB = max(session[index],session[index + 1])
            if profB in PREFERENCES[profA] and (profA, profB) not in pairList:
                score -= 1
                pairList.append((profA, profB))
    return score

def test():
    popSize = 10
    myPopulation = generatePopulation(popSize)
    for chromosome in myPopulation:
        score = evaluateChromosome(chromosome)
        print(chromosome, score)
    print("-----")
    myPopulation = sortPopulation(myPopulation)
    for chromosome in myPopulation:
        score = evaluateChromosome(chromosome)
        print(chromosome, score)
