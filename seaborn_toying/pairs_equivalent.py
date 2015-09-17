import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns


df = pd.DataFrame(np.random.randn(1000, 4), columns=['A','B','C','D'])

grid = sns.FacetGrid(df, col_wrap=5, size=1.5)


plt.savefig('scatter_matrix.png')