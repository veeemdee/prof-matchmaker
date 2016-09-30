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

def lotteryPick(popSize):
    """   Description:    Helper function that picks an index of a chromosome with
                          priority on better-fit ones
          Input:  popSize(int)    - number of chromosomes in the population
          Output: index of the selected chromosomes
    """
    first = random.randint(0, popSize-1)
    second = random.randint(0, popSize-1)
    return min(first, second)

def lotterySystem(popSize, geneticFunction, count):
    """   Description:    Implementation of a lottery system using tournament selection method
          Input:  popSize(int)        - number of chromosomes in the population
                  geneticFunction(str)- string indicating which genetic function is in context
                  count(int)          - number of chromosomes to undergo the genetic operation
          Output: a list containing indices of chromosomes in the population that have been
                  selected to undergo the genetic function
    """
    lotteryList = []
    if geneticFunction == 'crossover':
        for index in range(count):
            firstPick = lotteryPick(popSize)
            secondPick = lotteryPick(popSize)
            while secondPick == firstPick:
                secondPick = lotteryPick(popSize)
            lotteryList.append(firstPick)
            lotteryList.append(secondPick)
    else:
        for index in range(count):
            currentPick = lotteryPick(popSize)
            lotteryList.append(currentPick)
    return lotteryList

def crossover(chromosome1, chromosome2):
    crosspoint = random.randint(1, NUM_OF_SESSION-1)
    newChromosome1 = chromosome1[:crosspoint]+chromosome2[crosspoint:]
    newChromosome2 = chromosome2[:crosspoint]+chromosome1[crosspoint:]
    return newChromosome1, newChromosome2

def mutation(chromosome):
    def chromoSwap(chromosome, sessionIndex, profIndexA, profIndexB):
        if profIndexA > profIndexB:
            tmp = profIndexA
            profIndexA = profIndexB
            profIndexB = tmp
        session = chromosome[sessionIndex]
        newSession = (session[:profIndexA] + [session[profIndexB]] +
                      session[profIndexA+1:profIndexB] +
                      [session[profIndexA]] + session[profIndexB+1:])
        newChromosome = (chromosome[:sessionIndex] + newSession +
                         chromosome[sessionIndex + 1:])
        return newChromosome
        
    randomSessionIndex = random.randint(0, NUM_OF_SESSION-1)
    randomProfIndexA = random.randint(0, NUM_OF_PROF-1)
    print("A",randomProfIndexA)
    randomProfIndexB = randomProfIndexA
    while (randomProfIndexA // 2) == (randomProfIndexB // 2):
        print("B",randomProfIndexB)
        randomProfB = random.randint(0, NUM_OF_PROF-1)
    return chromoSwap(chromosome, randomSessionIndex, randomProfIndexA, randomProfIndexB)
    
def selection(chromosome):
    return chromosome

def test():
    aChromo = createChromosome()
    print(aChromo)
    newChromo = mutation(aChromo)
    print(newChromo)
