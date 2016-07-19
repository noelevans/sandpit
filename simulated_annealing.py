import numpy as np


"""
Implementing the challenge set here:
    http://blog.pluszero.ca/blog/2016/07/17/
        using-simulated-annealing-to-solve-logic-puzzles/
"""

# house          1            2          3          4            5
animals       = ['bird',      'dog',     'cat',     'horse',     'fish']
cigarettes    = ['pall mall', 'dunhill', 'blends',  'prince',    'blue master']
nationalities = ['british',   'danish',  'swedish', 'norwegian', 'german']
house_colours = ['yellow',    'red',     'white',   'green',     'blue']
drinks        = ['water',     'tea',     'milk',    'coffee',    'root beer']

houses = np.array([animals, cigarettes, nationalities, house_colours, drinks])


def adjacents(arr):
    return (np.arange(len(filter(None, arr))) == arr.nonzero()[0] - min(arr.nonzero()[0])).all()


def cost(cfg):
    """
    The Brit lives in the house with red walls.
    The Swede has a dog.
    The Dane drinks tea.
    The house with green walls is directly to the left of the house with white walls.
    The owner of the house with green walls drinks coffee.
    The person who smokes Pall Mall cigars owns a bird.
    The owner of the house with yellow walls smokes Dunhill.
    The man living in the center house drinks milk.
    The Norwegian lives in the first house.
    The man who smokes blends lives next to the cat owner.
    The horse's owner lives next to the man who smokes Dunhill.
    The man who smokes Blue Master drinks root beer.
    The German smokes Prince.
    The Norwegian lives next to the house with blue walls.
    The man who smokes Blends lives next to the man who drinks water.
    """
    price = 0
    if 2 in ((cfg == 'british') | (cfg == 'red')).sum(axis=0):
        price -= 1
    if 2 in ((cfg == 'swedish') | (cfg == 'dog')).sum(axis=0):
        price -= 1
    if 2 in ((cfg == 'danish') | (cfg == 'tea')).sum(axis=0):
        price -= 1
    if list(cfg[3,:]).index('green') - list(cfg[3,:]).index('white') == 1:
        price -= 1
    if 2 in ((cfg == 'green') | (cfg == 'coffee')).sum(axis=0):
        price -= 1
    if 2 in ((cfg == 'bird') | (cfg == 'pall mall')).sum(axis=0):
        price -= 1
    if 2 in ((cfg == 'yellow') | (cfg == 'dunhill')).sum(axis=0):
        price -= 1
    if 'milk' in cfg[:, 2]:
        price -= 1
    if 'norwegian' in cfg[:, 0]:
        price -= 1
    if adjacents(((cfg == 'blends') | (cfg == 'cat')).sum(0)):
        price -= 1
    if adjacents(((cfg == 'horse') | (cfg == 'dunhill')).sum(0)):
        price -= 1
    if 2 in ((cfg == 'blue master') | (cfg == 'root beer')).sum(axis=0):
        price -= 1
    if 2 in ((cfg == 'german') | (cfg == 'prince')).sum(axis=0):
        price -= 1
    if adjacents(((cfg == 'norwegian') | (cfg == 'blue')).sum(0)):
        price -= 1
    if adjacents(((cfg == 'blends') | (cfg == 'water')).sum(0)):
        price -= 1

    return price


def main():
    print cost(houses)


if __name__ == '__main__':
    main()
