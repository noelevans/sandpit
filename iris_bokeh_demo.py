###
# Taken from http://bokeh.pydata.org/en/latest/docs/gallery/iris.html
###

from bokeh.sampledata.iris import flowers
import bokeh.plotting as plt


def main():

    colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
    flowers['color'] = flowers['species'].map(lambda x: colormap[x])

    plt.output_file("iris.html", title="iris.py example")

    p = plt.figure(title = "Iris Morphology")
    p.xaxis.axis_label = 'Petal Length'
    p.yaxis.axis_label = 'Petal Width'

    p.circle(flowers["petal_length"], flowers["petal_width"],
            color=flowers["color"], fill_alpha=0.2, size=10, )

    plt.show(p)


if __name__ == '__main__':
    main()