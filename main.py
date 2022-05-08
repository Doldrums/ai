from typing import List, Tuple

import numpy as np
from music21 import midi, converter, stream

PATH_TO_MIDI = "input1.midi"


def midi_parse(midi_file_path):
    return converter.parse(midi_file_path)


def find_key(file):
    return file.analyze("key")


def play_music(file):
    sp = midi.realtime.StreamPlayer(file)
    sp.play()


music = midi_parse(PATH_TO_MIDI)
chords = music.chordify().flatten().getElementsByClass("Chord")
chords.show('text')


## EA

def get_individual() -> float:
    # здесь генерим аккорды по тональности
    smth = []
    return smth


def get_fitness(individual: float) -> float:
    # fitness функция у аккомпанимента
    # fun(individual)
    return 0


def get_population(population_size: int) -> List[float]:
    return [get_individual() for i in range(population_size)]


def population_fitness(population: List[float]) -> Tuple[List[float], float]:
    # returns list of individual's fitness and average fitness of the population
    fitness = [get_fitness(individual) for individual in population]
    return (fitness, np.mean(fitness))


def roulette_wheel_select(fitness: List[float]) -> int:
    # returns index of a selected parent
    # you may use np.random.choice
    pass


def crossover(population: List[float], fitness: List[float], size: int) -> List[float]:
    # selects two parents to generate offspring
    # this process continues "size" times
    # returns list of ofssprings
    offsprings = []
    return offsprings


def mutate(offsprings: List[float]) -> List[float]:
    # mutates by adding some noise to the number
    # np.random.normal might help
    pass


def replace_parents(population: List[float], population_fitness: List[float], offsprings: List[float],
                    offsprings_fitness: List[float], size: int) -> List[float]:
    # replace "size" number of least fit population members
    # with most fit "size" offsprings
    # returns new population
    sort_index = np.argsort(population_fitness)
    population_sorted = np.take(population, sort_index)
    sort_index = np.argsort(offsprings_fitness)
    offsprings_sorted = np.take(offsprings, sort_index)

    parents = population_sorted[size:]
    offsprings = offsprings_sorted[-size:]

    return [*parents, *offsprings]


def evolution(generations: int, population_size: int):
    population = get_population(population_size)

    for generation in range(generations):
        fitness, avg_fitness = population_fitness(population)

        #plotFunction(f'Generation: {generation} Population average fitness: {round(avg_fitness, 3)}', x, y, population,
        #             fitness)

        offsprings = crossover(population, fitness, 5)
        offsprings = mutate(offsprings)
        offsprings_fitness, offsprings_fitness_avg = population_fitness(offsprings)
        population = replace_parents(population, fitness, offsprings, offsprings_fitness, 3)

    return population


population = evolution(generations=15, population_size=49)