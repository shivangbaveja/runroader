import pickle

import click
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from runroader.constants import S_0, S_F, T_MAX
from runroader.environment import Rectangle, Environment


class EnvironmentBuilder:
    def __init__(self, name):
        self.name = name
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('drag to build rectangles')
        self.ax.set_xlim([S_0, S_F])
        self.ax.set_ylim([0, T_MAX])
        self.rectangles = []
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def on_press(self, event):
        self.starting_pos = (event.xdata, event.ydata)

    def on_release(self, event):
        self.ending_pos = (event.xdata, event.ydata)
        bottom_left_corner = (min(self.starting_pos[0], self.ending_pos[0]), min(self.starting_pos[1], self.ending_pos[1]))
        width = abs(self.starting_pos[0] - self.ending_pos[0])
        height = abs(self.starting_pos[1] - self.ending_pos[1])
        rectangle_patch = patches.Rectangle(bottom_left_corner, width, height)
        self.rectangles.append(Rectangle(bottom_left_corner, width, height))
        self.ax.add_patch(rectangle_patch)
        self.fig.canvas.draw()

    def on_key(self, event):
        if event.key == 'enter':
            environment = Environment(self.rectangles)
            environment.to_pickle(self.name)
            plt.close()


@click.command()
@click.option('--name', help='The name of this newly-built environment. Providing this option means you want to save the model permanently')
def main(name):
    """Simple program for building the time-distance environment.

    Drag your mouse to build the environment.

    Press `enter` for the end of the process
    """
    builder = EnvironmentBuilder(name)
    plt.show()


if __name__ == "__main__":
    main()
