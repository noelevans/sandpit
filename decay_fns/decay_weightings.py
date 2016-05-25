import numpy as np
import pandas as pd
 
 
def decay_mean(ol, half_life=5):
    years = np.array([2012, 2013, 2014, 2016, 2017])
    ratings = np.array([9, 11, 14, 11, 4])
    today = 2016 + 1
   
    print(ratings.mean())
   
    elapsed_time = years - today
    half_life = 2
   
    weights = np.e ** -(elapsed_time  * half_life)
    print weights
    print weights / sum(weights)
    print(sum(ratings * weights) / sum(weights))


def main():
	
	print(decay_mean(ratings, 2))
	print(decay_mean(ratings, 5))
    print(ratings.mean())


if __name__ == '__main__':
	main()
