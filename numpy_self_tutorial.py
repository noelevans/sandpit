import numpy as np


# Example from http://www.python-course.eu/matrix_arithmetic.php

# Lucas bought 100g of brand A, 175g of brand B and 210 of C. 
# Mia choose 90g of A, 160g of B and 150g of C. 
# Leon bought 200g of A, 50 of B and 100g of C. 
# Hannah bought 120g of A and 310g of C.
# So we represent the table:
# 
#               A       B       C
#   Lucas     100     175     210
#   Mia        90     160     150
#   Leon      200      50     100
#   Hannah    120       0     310
# 
# With this matrix
purchases = np.array([[100, 175, 210],
                      [ 90, 160, 150],
                      [200,  50, 100],
                      [120,   0, 310]])

# Cost of each chocolate A, B, C:
cost_per_100_grams = np.array([2.98, 3.9, 1.99])


# Convert the cost to cost per gram rather than cost per 100 grams
cost_per_gram = cost_per_100_grams / np.repeat(100, 4)
cost_per_gram = cost_per_100_grams / 100     # Quicker way to do same assignment

# To get the amount Lucas, Mia, Leon and Hannah spent in total
spend_of_each_person = np.dot(purchases, cost_per_gram)
# array([ 13.984,  11.907,   9.9  ,   9.745])
