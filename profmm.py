import random
import itertools

NUM_OF_SESSION = 4
NUM_OF_PROF = 10
MAX_SCORE = NUM_OF_SESSION*(NUM_OF_PROF // 2)
PREFERENCES = [[1, 3, 7, 9],
               [0, 4, 5, 7],
               [3, 5, 8, 9],
               [0, 2, 4, 6],
               [1, 3, 5, 7],
               [1, 2, 4, 6],
               [3, 5, 8, 9],
               [0, 1, 4, 8],
               [2, 6, 7, 9],
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

def crossoverPopulation(population, crossoverCount):
    popSize = len(population)
    crossoverOrder = lotterySystem(popSize, "crossover", crossoverCount)
    myOffsprings = []
    for count in range(crossoverCount):
        chromosome1 = population[crossoverOrder[count*2]]
        chromosome2 = population[crossoverOrder[count*2+1]]
        myOffsprings.extend(list(crossover(chromosome1,chromosome2)))
    return myOffsprings

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
        newChromosome = (chromosome[:sessionIndex] + [newSession] +
                         chromosome[sessionIndex + 1:])
        return newChromosome

    randomSessionIndex = random.randint(0, NUM_OF_SESSION-1)
    randomProfIndexA = random.randint(0, NUM_OF_PROF-1)
    randomProfIndexB = randomProfIndexA
    while (randomProfIndexA // 2) == (randomProfIndexB // 2):
        randomProfIndexB = random.randint(0, NUM_OF_PROF-1)
    return chromoSwap(chromosome, randomSessionIndex, randomProfIndexA, randomProfIndexB)

def mutationPopulation(population, mutationCount):
    popSize = len(population)
    mutationOrder = lotterySystem(popSize, 'mutation', mutationCount)
    myOffsprings = []
    for count in range(mutationCount):
        myChromosome = population[mutationOrder[count]]
        myOffsprings.append(mutation(myChromosome))
    return myOffsprings

def selection(chromosome):
    return chromosome

def selectionPopulation(population, selectionCount):
    popSize = len(population)
    selectionOrder = lotterySystem(popSize, 'selection', selectionCount)
    myOffsprings = []
    for count in range(selectionCount):
        myChromosome = population[selectionOrder[count]]
        myOffsprings.append(selection(myChromosome))
    return myOffsprings

def newBlood():
    return createChromosome()

def newBloodPopulation(newBloodCount):
    return generatePopulation(newBloodCount)    



def findMatching(popSize, selectionCount, mutationCount,
                 newBloodCount, crossoverCount):
    currentPopulation = generatePopulation(popSize)
    currentPopulation = sortPopulation(currentPopulation)
    bestChromosome = currentPopulation[0]
    bestScore = evaluateChromosome(bestChromosome)
    currentGeneration = 0
    bestGeneration = currentGeneration
    while bestScore > 0:
        currentGeneration += 1
        newPopulation = []
        newPopulation.extend(selectionPopulation(currentPopulation,selectionCount))
        newPopulation.extend(mutationPopulation(currentPopulation,mutationCount))
        newPopulation.extend(newBloodPopulation(newBloodCount))
        newPopulation.extend(crossoverPopulation(currentPopulation,crossoverCount))

        newPopulation = sortPopulation(newPopulation)
        newBestScore = evaluateChromosome(newPopulation[0])
        if newBestScore < bestScore:
            bestChromosome = newPopulation[0]
            bestScore = newBestScore
            bestGeneration = currentGeneration
            print("Best Chromosome is",bestChromosome,
                  "with the score of",bestScore,
                  "found at generation",bestGeneration)
        currentPopulation = newPopulation
    return bestChromosome, bestScore, bestGeneration

def parseChromosome(chromosome):
    result = []
    for profIndex in range(NUM_OF_PROF):
        result.append([])
    for session in chromosome:
        for profIndex in range(0, NUM_OF_PROF, 2):
            profA = session[profIndex]
            profB = session[profIndex+1]
            result[profA].append(profB)
            result[profB].append(profA)
    return result

def generateTestCase(numOfProf):
    preferenceMatrix = []
    while True:
        for index in range(numOfProf):
            preferenceMatrix.append([])
        for prof in range(NUM_OF_PROF):
            pickCount = NUM_OF_SESSION - len(preferenceMatrix[prof])
            if pickCount > 0:
                if pickCount > NUM_OF_PROF - prof - 1:
                    break
                else:
                    profToPick = random.sample(range(prof+1,NUM_OF_PROF),pickCount)
                    preferenceMatrix[prof].extend(profToPick)
                    for pickedProf in profToPick:
                        preferenceMatrix[pickedProf].append(prof)
        return preferenceMatrix

def testTestGenerator(numOfProf,runCount):
    failCount = 0
    for index in range(runCount):
        if generateTestCase(numOfProf) == -1:
            failCount+=1
    return failCount, runCount
