import tkinter
import pandas as pd
import environment as env
from tkinter.ttk import *
from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import csv
import threading
import PySimpleGUI as sg
import time
import tools
from ocr import process, get_text
import os
# import psutil

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "9", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def start_process():
    #vid = tools.files(env.image_frames)
    #process(vid)
    if not env.is_high_FPS:
        get_text()


def show_csv():


    # root = tkinter.Tk()
    #
    # root.geometry("1010x710")
    # root.pack_propagate(True)
    #
    # # Frame for TreeView
    # frame1 = tkinter.LabelFrame(root, text="Excel Data", background='black')
    # frame1.place(height=700, width=1000)
    #
    # ## Treeview Widget
    # tv1 = ttk.Treeview(frame1)
    # tv1.place(relheight=1, relwidth=1)
    #
    # treescrolly = tkinter.Scrollbar(frame1, orient="vertical", command=tv1.yview)
    # treescrollx = tkinter.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
    # tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
    # treescrollx.pack(side="bottom", fill="x")
    # treescrolly.pack(side="right", fill="y")
    #
    # file_path = "files/output.csv"
    #
    # df = pd.read_csv(file_path)
    #
    # tv1["column"] = list(df.columns)
    # tv1["show"] = "headings"
    # for column in tv1["columns"]:
    #     tv1.heading(column, text=column)  # let the column heading = column name
    # df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
    # for row in df_rows:
    #     tv1.insert("", "end", values=row)
    #
    # root.mainloop()

    filename = 'files/output.csv'
    with open(filename, "r") as infile:
        reader = csv.reader(infile)
        header_list = next(reader)
        data = list(reader)
    sg.SetOptions(element_padding=(0, 10),
                  background_color='black')

    layout = [
        [sg.Table(
            key='table1',
            values=data,
            headings=header_list,
            max_col_width=25,
            auto_size_columns=False,
            justification='left',
            background_color='#444444',
            alternating_row_color='black',
            num_rows=25,
            enable_events=True)],
    ]

    window = sg.Window(
        title='CSV File',
        return_keyboard_events=True,
        grab_anywhere=False).Layout(layout)

    while True:
        event, values = window.Read()

        if event is None or event == 'Exit':
            window.close()
            break

        if event == 'Escape:27':  # Exit on ESC
            window.close()
            break
    s.theme_use("alt")
    return mainloop()



b_filename = ""


def browse_files():
    global b_filename
    b_filename = filedialog.askopenfilename(initialdir="/",
                                            title="Select a File",
                                            filetypes=(("Video",
                                                        "*.mp4*"),
                                                       ("csv file",
                                                        "*.csv")))
    if b_filename == "":
        env.label_information.configure(text="File could not be opened !!! " + b_filename)
    else:
        env.label_information.configure(text="File Opened: " + b_filename)


def minimize_window():
    env.window.wm_state('iconic')
    env.window.iconify()


def thread_handling():
    t = threading.Thread(target=start_process)
    if not t.is_alive():
        t.daemon = True
        t.start()
    else:
        t.join()
        t = threading.Thread(target=start_process)
        t.daemon = True
        t.start()


def thread_handling_for_cvs():
    t = threading.Thread(target=show_csv)
    if not t.is_alive():
        t.daemon = True
        t.start()
    else:
        t.join()
        t = threading.Thread(target=show_csv)
        t.daemon = True
        t.start()


def restart_program():
    os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)

    python = sys.executable
    os.execl(python, python, *sys.argv)

def change_label():
    env.label_information['text'] = "kjhkhk"


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()



env.init()
env.window.title('Aircraft Data Scanning and Processing Program')
env.window.geometry("1280x720")
#env.window.overrideredirect(True)
env.window.resizable(False, False)


filename = PhotoImage(file="res/background_img.png")
background_label = Label(env.window, image=filename)



exit_icon = Image.open("res/exit_icon.png")
exit_icon = exit_icon.resize((35, 35))
exit_icon = ImageTk.PhotoImage(exit_icon)

minimize_icon = Image.open("res/minimize_icon.png")
minimize_icon = minimize_icon.resize((35, 35))
minimize_icon = ImageTk.PhotoImage(minimize_icon)

browse_folder_icon = Image.open("res/browse_video.png")
browse_folder_icon = browse_folder_icon.resize((60, 60))
browse_folder_icon = ImageTk.PhotoImage(browse_folder_icon)

fps_icon = Image.open("res/fps_icon.png")
fps_icon = fps_icon.resize((55, 55))
fps_icon = ImageTk.PhotoImage(fps_icon)

start_icon = Image.open("res/start_icon.png")
start_icon = start_icon.resize((60, 60))
start_icon = ImageTk.PhotoImage(start_icon)

create_kml_icon = Image.open("res/kml_icon.png")
create_kml_icon = create_kml_icon.resize((60, 60))
create_kml_icon = ImageTk.PhotoImage(create_kml_icon)

show_csv_icon = Image.open("res/show_csv_icon.png")
show_csv_icon = show_csv_icon.resize((60, 60))
show_csv_icon = ImageTk.PhotoImage(show_csv_icon)

browse_csv_icon = Image.open("res/browse_csv_icon.png")
browse_csv_icon = browse_csv_icon.resize((60, 60))
browse_csv_icon = ImageTk.PhotoImage(browse_csv_icon)

reset_icon = Image.open("res/reset_icon.png")
reset_icon = reset_icon.resize((60, 60))
reset_icon = ImageTk.PhotoImage(reset_icon)

# Create a File Explorer label
label_window = Label(env.window,
                     text="Aircraft Data Scanning and Processing Program",
                     fg="white", background='black')

label_window.config(font=("Verdana", 20))
env.label_information = Label(env.window,
                              text="",
                              fg="red", background='black')

env.label_information.config(font=("Verdana", 15))



env.label_information2 = Label(env.window,
                              text="WELCOME",
                              fg="gray", background='black', font=("Verdana", 18))

label_window.after(3000, env.label_information2.destroy)


label_buttons = Label(env.window, background='black')

button_explore = Button(env.window, command=browse_files,  background='black', image = browse_folder_icon, relief=FLAT, borderwidth = 0)
#button_explore.config(font=("Verdana", 9))
env.fps_variable = DoubleVar(env.window)
env.fps_variable.set("0.15")
select_fps = OptionMenu(env.window, env.fps_variable, "0.1", "0.15", "0.2", "1", "5", "10", "20", "30", "60")






select_fps.config(image=fps_icon, background='black',  borderwidth = 0, highlightthickness = 0, activebackground="black")
#text_FPS = Label(env.window, text="Please Select FPS:")

button_start_process = Button(env.window, image = start_icon,  command=thread_handling, relief=FLAT, borderwidth = 0)
button_start_process.config(bg="black")

#button_start_process.config(font=("Verdana", 9))
button_loadCSV = Button(env.window, image = browse_csv_icon, command=browse_files, background = 'black',  activebackground="#ff73c8", relief=FLAT, borderwidth = 0)
button_loadCSV.config(font=("Verdana", 9))
button_exit = Button(env.window, command=exit, width=35, height=35, background='black', image = exit_icon)
button_create_kml = Button(env.window, image = create_kml_icon, command=tools.create_kml, background = 'black', relief=FLAT, borderwidth = 0)
button_create_kml.config(font=("Verdana", 9))
button_showCSV = Button(env.window, image = show_csv_icon, command=show_csv, background = 'black', relief=FLAT, borderwidth = 0)
#button_showCSV.config(font=("Verdana", 9))
button_reset = Button(env.window, image = reset_icon, background = 'black', relief=FLAT, borderwidth = 0, command= restart_program)
button_reset.config(font=("Verdana", 9))
button_minimize = Button(env.window, width=35, height=35, command=minimize_window,
                         background='black', image=minimize_icon)

CreateToolTip(button_explore, text = 'Browse video file')
CreateToolTip(button_loadCSV, text = 'Browse CSV File\nfor load manually CSV file')
CreateToolTip(button_showCSV, text = 'Show CSV File')
CreateToolTip(button_reset, text = 'Reset')
CreateToolTip(button_create_kml, text = 'Create KML file')
CreateToolTip(button_start_process, text = 'Start to process')
CreateToolTip(select_fps, text = 'Select FPS')

background_label.place(x=0, y=0, relwidth=1, relheight=1)
label_window.place(x=0, y=0, width=1280, height=60)
env.label_information2.place(x=127, y=525, width=1000, height=50)
env.label_information.place(x=127, y=525, width=1000, height=50)
# button_exit.place(x=900, y=900, relwidth=0.06, relheight=0.05)
label_buttons.place(x=0, y=0, width=100, height=1000)
button_explore.place(x=8, y=100)
select_fps.place(x=10, y=175)
#text_FPS.place(x=100, y=175, relwidth=0.07, relheight=0.015)
button_create_kml.place(x=8, y=475)
button_showCSV.place(x=9, y=400)
button_loadCSV.place(x=13, y=325)
button_start_process.place(x=8, y=250)
button_reset.place(x=8, y=550)
button_exit.place(x=1230, y=10)
button_minimize.place(x=1175, y=10)


s = Style()
s.theme_use("alt")
s.configure("TProgressbar", thickness=5, background='yellow', troughcolor='black')

env.read_progress_bar = Progressbar(env.window, orient=HORIZONTAL,
                                    length=500, mode='determinate', style="TProgressbar")

env.process_progress_bar = Progressbar(env.window, orient=HORIZONTAL,
                                       length=500, mode='determinate', style="TProgressbar")



center(env.window)
env.window.mainloop()
