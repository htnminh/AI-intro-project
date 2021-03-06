# Source code of some of the setup below
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Embedded_Toolbar.py

import webbrowser

import PySimpleGUI as sg
sg.change_look_and_feel('DarkAmber')

from AI_intro_project.State import State

"""
    Embedding the Matplotlib toolbar into your application
"""

# ------------------------------- This is to include a matplotlib figure in a Tkinter canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# plt.style.use('dark_background')


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


col1 = [
    [
        sg.T('Initialize:'),
        sg.B('4x4 (default)'),
        sg.B('6x6 (default)'),
        sg.B('8x8 (default)'),
        # sg.B('12x12 (dev)'),
        sg.B('mxn (random)')],
    [
        sg.B('Play 5 random legal moves'),
        sg.B('Show 4x4 best solution'),
        # TODO: show the best solution that algorithms found
    ],
]
col2 = [
    [
        sg.B('▲', key='U')],
    [
        sg.B('◄', key='L'),
        sg.B('⟲', key='undo'),
        sg.B('►', key='R')],
    [
        sg.B('▼', key='D')],
]
col3 = [
    [
        sg.B('Exit')],
    [
        sg.B('About')]
]


layout = [
    [
        sg.Column(col1, element_justification='center'),
        sg.VerticalSeparator(),
        sg.Column(col2, element_justification='center'),
        sg.VerticalSeparator(),
        sg.Column(col3, element_justification='center')],
    [
        sg.Column(
            layout=[
                [sg.Canvas(key='fig_cv',
                        # it's important that you set this size
                        size=(633, 633)  # 633 633
                        )]
            ],
            background_color='#DAE0E6',
            pad=(0, 0),
            element_justification='center'
            )],
    [
        sg.Column(
            layout=[[sg.Canvas(key='controls_cv')]],
            element_justification='center'
        )]
]

window = sg.Window('The Penniless Pilgrim Riddle | https://github.com/htnminh/AI-intro-project', layout, resizable = True, finalize = True)
window.bind('<Up>', 'U')
window.bind('<Down>', 'D')
window.bind('<Left>', 'L')
window.bind('<Right>', 'R')



# EVENT LOOP --------------------------------------------------------------
while True:
    event, values = window.read()
    # print(event, values)

    if event in (sg.WIN_CLOSED, 'Exit'):  # always,  always give a way out!
        break

    elif event == 'About':
        webbrowser.get('windows-default')\
                    .open_new_tab('https://github.com/htnminh/AI-intro-project')

    elif event == '4x4 (default)':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        s = State()
        s.initialize_4x4_default()
        s._plt_prepare()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event == '6x6 (default)':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        s = State()
        s.initialize_6x6_default()
        s._plt_prepare()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event == '8x8 (default)':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        s = State()
        s.initialize_8x8_default()
        s._plt_prepare()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event == '12x12 (dev)':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        s = State()
        s.board_size = (12,12)
        s._plt_prepare()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event == 'mxn (random)':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        s = State()
        s.initialize_mxn_random()
        s._plt_prepare()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event == 'Show 4x4 best solution':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        s = State()
        for _ in range(2):
            s.move_to_direction('D')
        s.move_to_direction('L')
        s.move_to_direction('D')
        s.move_to_direction('R')
        for _ in range(2):
            s.move_to_direction('R')
        for _ in range(3):
            s.move_to_direction('U')
        s.move_to_direction('L')
        s.move_to_direction('D')
        for _ in range(3):
            s.move_to_direction('L')
        for _ in range(3):
            s.move_to_direction('D')
        for _ in range(4):
            s.move_to_direction('R')

        s._plt_prepare()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event == 'Play 5 random legal moves':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        # check if s is defined
        assert 's' in locals(), \
                    'THE GAME DOES NOT EXIST, INITIALIZE FIRST'
        s.random_play(number_of_moves=5, silent=True)
        s._plt_prepare()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event in ('L', 'R', 'U', 'D'):
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        assert 's' in locals(), \
                    'THE GAME DOES NOT EXIST, INITIALIZE FIRST'
        s.move_to_direction(event[0])
        s._plt_prepare()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event == 'undo':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        assert 's' in locals(), \
                    'THE GAME DOES NOT EXIST, INITIALIZE FIRST'
        s.undo_last_move()
        s._plt_prepare()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

window.close()
