from matplotlib import pyplot as plt
import numpy as np
 
 
def main():
    half_life = 5
    x = np.linspace(0, 20, 100)
    y_1 = 0.5 ** (x / half_life)
    y_2 = np.e ** - (x * half_life)
 
    label_1 = r'$y = (\frac{1}{2})^{x / t_{\frac{1}{2}}}$'
    label_2 = r'$y = e^{x.t_{\frac{1}{2}}}$'
    plt.plot(x, y_1, linewidth=2, label=label_1)
    plt.plot(x, y_2, linewidth=2, label=label_2)
    plt.legend(fontsize='xx-large')
    plt.show()
 
 
if __name__ == '__main__':
    main()
