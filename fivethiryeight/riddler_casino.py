"""
Suppose a casino invents a new game that you must pay $250 to play. The game
works like this: The casino draws random numbers between 0 and 1, from a
uniform distribution. It adds them together until their sum is greater than 1,
at which time it stops drawing new numbers. You get a payout of $100 each time
a new number is drawn.
 
For example, suppose the casino draws 0.4 and then 0.7. Since the sum is
greater than 1, it will stop after these two draws, and you receive $200. If
instead it draws 0.2, 0.3, 0.3, and then 0.6, it will stop after the fourth
draw and you will receive $400. Given the $250 entrance fee, should you play
the game?
 
Specifically, what is the expected value of your winnings?
 
From:
    http://fivethirtyeight.com/features/
        should-you-pay-250-to-play-this-casino-game
"""
 
import numpy as np
 
 
def trial():
    total = 0
    spins = 0
    while total < 1:
        total += np.random.random()
        spins += 1
    return spins
   
 
def main():
    n = 10000000
    dollar_return = (np.mean([trial() for _ in range(n)]))
    return_on_stake = 100 * dollar_return
    print(return_on_stake)
 
 
if __name__ == '__main__':
    main()
