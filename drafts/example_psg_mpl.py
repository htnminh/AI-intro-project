import PySimpleGUI as sg
import numpy as np

from AI_intro_project.State import Coordinate, Road, State

class State(State):
    def visualize(self):
        '''
        Visualize the current state in matplotlib
        Most of the things below are reversed in some way,
        since the x coordinate of the game is the y
        coordinate in math, etc.
        '''

        # move x axis to the top
        plt.rcParams['xtick.bottom'] = \
            plt.rcParams['xtick.labelbottom'] = False
        plt.rcParams['xtick.top'] = \
            plt.rcParams['xtick.labeltop'] = True
        
        # black board 
        for i in range(self.board_size[1] + 1):
            plt.plot(
                    [i,i],
                    [0,self.board_size[0]],
                    color='black'
            )
        for i in range(self.board_size[0] + 1):
            plt.plot(
                    [0,self.board_size[1]],
                    [i,i],
                    color='black'
            )

        # walked_roads
        for index, road in enumerate(self.walked_roads):
            plt.plot(
                [road.coordinate_start.y,
                        road.coordinate_end.y],
                [road.coordinate_start.x,
                        road.coordinate_end.x],
                color='red'
            )
            plt.text(road.coordinate_start.y/2+road.coordinate_end.y/2,
                     road.coordinate_start.x/2+road.coordinate_end.x/2,
                     index,
                     ha='center',
                     va='center',
                     fontfamily='monospace',
                     color='blue'
                     )
        # current tax text
        plt.text(
                self.board_size[1]/2,
                self.board_size[0]+3/4,
                f'Current tax: {self.current_tax}',
                ha='center',
                va='center',)

        # limit the plot by board size
        plt.xlim(-1, self.board_size[1] + 1)
        plt.ylim(-1, self.board_size[0] + 1)

        # invert y axis (oriented downward)
        plt.gca().invert_yaxis()

        # scale axes equally, so squares are displayed
        plt.gca().set_aspect('equal', adjustable='box')

        # show every value on the axes, and exclude -1
        plt.xticks([x for x in range(self.board_size[1] + 1)])
        plt.yticks([y for y in range(self.board_size[0] + 1)])

        # show
        plt.plot()
        # plt.show()

    

"""
    Embedding the Matplotlib toolbar into your application

"""

# ------------------------------- This is to include a matplotlib figure in a Tkinter canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


# ------------------------------- PySimpleGUI CODE

layout = [
    [sg.T('Graph: y=sin(x)')],
    [sg.B('Plot'), sg.B('Exit')],
    [sg.T('Controls:')],
    [sg.Canvas(key='controls_cv')],
    [sg.T('Figure:')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(600, 600)
                       )]
        ],
        background_color='#DAE0E6',
        pad=(0, 0)
    )],
    [sg.B('Alive?')]

]

window = sg.Window('Graph with controls', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):  # always,  always give a way out!
        break
    elif event == 'Plot':
        # ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE
        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))
        # -------------------------------
        # x = np.linspace(0, 2 * np.pi)
        # y = np.sin(x)
        # plt.plot(x, y)
        # plt.title('y=sin(x)')
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # plt.grid()
        s = State()
        s.board_size = (15,15)
        s.visualize()

        # ------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

window.close()
