import random
from chromosome import Chromosome
import pandas as pd
import csv

dim = 10
chromosome_length = dim  
source=0
destination=9
w=pd.read_csv(u'/home/disha-khanted/abc.csv')
w=w.drop(columns=['Unnamed: 0'])
weights=[]
for i in w:
    weights.append(w[i])
quite = False
mutate_prob=10
class GeneNetwork(object):
    def __init__(self, dim, weights, chromosome_length):
        if source >= dim or destination >= dim:
            raise ValueError
        self.chromosome_length = chromosome_length
        self.dim = dim
        self.weights = weights
        self.source= source
        self.destination = destination
        self.population = []
        self.population_size = 0
        self.results = []
        self.best = None

    def start(self, gen_max, pop_size):
        gen = 1 
        self.generate_population(pop_size) 
        self.population_size = pop_size
        if not quite:
            pretty_print('Initital:')
            self.print_chromosomes(self.population)
        while gen <= gen_max:
            gen += 1
            p = 1
            new_population = list()
            mutate_count=0
            while p <= pop_size:
                p += 1
                parents = random.sample(range(self.population_size), 2)
                child = self.crossover(self.population[parents[0]], self.population[parents[1]])
                mutate_count +=1
                if(mutate_prob%mutate_count==0):
                	child.mutate()
                fit = self.fitness(child)
                self.results.append((child, fit))
                new_population.append(child)
                if self.best is None or self.best[1] > fit:
                    self.best = (child, fit)
            if not quite:
            	self.selection(self.population, new_population)
            #if not quite:
		return self.best

    def selection(self, prev, now):
        prev.extend(now)
        prev.sort(lambda x, y: self.fitness(x) - self.fitness(y))
        self.population = prev[:self.population_size]

    def generate_population(self, n):
        chromosomes = list()
        for i in range(n):
            chromosomes.append(self._gen_chromosome())
        self.population = chromosomes

    def _gen_chromosome(self):
        chromosome = random.sample(list(set(range(self.dim)) - {self.source, self.destination}),
                                   self.chromosome_length - 2)
        chromosome.insert(0, self.source)
        chromosome.append(self.destination)
       	"""
        my_list = list(xrange(1,n))
    	random.shuffle(my_list)
    	my_list.insert(0,0)
    	"""
        return Chromosome(chromosome)

    def crossover(self, mother, father):
        mother_list = mother.get()
        father_list = father.get()
        cut = random.randint(0, self.chromosome_length - 1)
        child = mother_list[0:cut] + father_list[cut:]
        return Chromosome(child)

    def fitness(self, chromosome):
        chromosome_list = chromosome.get()
        return sum([self.weights[i][j] for i, j in zip(chromosome_list[:-1], chromosome_list[1:])])

    def print_chromosomes(self, chromosomes):
        for chromosome in chromosomes:
            print str(chromosome) + ' ' + str(self.fitness(chromosome))


def pretty_print(to_print, hint=''):
    print ''
    print '=================='
    print hint + str(to_print)
    print '=================='


if __name__ == "__main__":
    	gene_network = GeneNetwork(dim, weights,chromosome_length)
    	res = gene_network.start(1000, 11)  
    	pretty_print(res, 'Solution: ')
