from tkinter import Tk, DoubleVar
from tkinter.ttk import Progressbar, Label, Style

window = Tk()
label_information = Label()

process_progress_bar = Progressbar()
read_progress_bar = Progressbar()

pb_style = Style()
fps_variable = DoubleVar()

image_frames = 'image_frames'
is_high_FPS = False


def init():
    global window
    global label_information
    global process_progress_bar
    global read_progress_bar
    global pb_style
    global fps_variable
    global image_frames
    global is_high_FPS
