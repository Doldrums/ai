import random
from typing import List, Tuple, Union

import numpy as np
from music21 import midi, converter, harmony
from music21.harmony import ChordSymbol

PATH_TO_MIDI = "input1.midi"


def midi_parse(midi_file_path):
    return converter.parse(midi_file_path)


def find_key(music):
    return music.analyze("key")


def get_chords_by_key(key):
    if str(key) == "d minor":
        return [
            harmony.ChordSymbol(root="D", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="E", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="F", kind="major", writeAsChord=True),
            harmony.ChordSymbol(root="G", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="A", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="B", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="C", kind="major", writeAsChord=True),
        ]

    elif str(key) == "F major":
        return [
            harmony.ChordSymbol(root="F", kind="major", writeAsChord=True),
            harmony.ChordSymbol(root="G", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="A", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="B", kind="major", writeAsChord=True),
            harmony.ChordSymbol(root="C", kind="major", writeAsChord=True),
            harmony.ChordSymbol(root="D", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="E", kind="major", writeAsChord=True),
        ]

    elif str(key) == "e minor":
        return [
            harmony.ChordSymbol(root="E", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="F", kind="major", writeAsChord=True),
            harmony.ChordSymbol(root="G", kind="major", writeAsChord=True),
            harmony.ChordSymbol(root="A", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="B", kind="minor", writeAsChord=True),
            harmony.ChordSymbol(root="C", kind="major", writeAsChord=True),
            harmony.ChordSymbol(root="D", kind="major", writeAsChord=True),
        ]


def play_music(music):
    sp = midi.realtime.StreamPlayer(music)
    sp.play()


def get_music_chords(music):
    return music.chordify().flatten().getElementsByClass("Chord")


def get_individual(
        related_chords: List[object], music_duration: int
) -> list[Union[object, list[object]]]:
    return [related_chords[random.randint(0, 6)] for i in range(music_duration * 2)]


def get_fitness(individual: object) -> object:
    # fitness функция у аккомпанимента
    # fun(individual)
    return 0


def get_population(
        population_size: int, related_chords: List[object], music_duration: int
) -> list[list[Union[object, list[object]]]]:
    return [
        get_individual(related_chords, music_duration) for i in range(population_size)
    ]


def population_fitness(population: List[object]) -> Tuple[List[object], float]:
    # returns list of individual's fitness and average fitness of the population
    fitness = [get_fitness(individual) for individual in population]
    return (fitness, np.mean(fitness))


def crossover(population: List[object], fitness: List[object], size: int) -> List[object]:
    # selects two parents to generate offspring
    # this process continues "size" times
    # returns list of ofssprings
    for i in range(size):
        index1 = random.randint(0, len(population) - 1)
        index2 = random.randint(0, len(population) - 1)
        tmp = population[index1][5:10]
        population[index1][5:10] = population[index2][5:10]
        population[index2][5:10] = tmp
    offsprings = population
    return offsprings


def mutate(offsprings: List[object], related_chords: List[object]) -> list[object]:
    # mutates by adding some noise to the number
    offsprings[random.randint(0, len(offsprings) - 1)] = related_chords[random.randint(0, len(related_chords) - 1)]
    return offsprings


def select(
        population: List[object],
        population_fitness: List[object],
        offsprings: List[object],
        offsprings_fitness: List[object],
        size: int,
) -> List[object]:
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


def evolution(generations: int, population_size: int, music):
    related_chords = get_chords_by_key(find_key(music))
    music_duration = int(music.flatten()[-1].offset)

    population = get_population(population_size, related_chords, music_duration)
    print(population)
    for generation in range(generations):
        fitness, avg_fitness = population_fitness(population)

        # plotFunction(f'Generation: {generation} Population average fitness: {round(avg_fitness, 3)}', x, y, population,
        #             fitness)

        offsprings = crossover(population, fitness, 5)
        offsprings = mutate(offsprings, related_chords)
        offsprings_fitness, offsprings_fitness_avg = population_fitness(offsprings)
        population = select(
            population, fitness, offsprings, offsprings_fitness, 3
        )

    return population


music = midi_parse(PATH_TO_MIDI)
chords = get_music_chords(music)
chords.show("text")
population = evolution(generations=15, population_size=49, music=music)
