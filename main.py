import subprocess
import threading
import tkinter as tk

import PIL.Image
from PIL import ImageTk

import gui_tools
import ocr
import tools
from gui_tools import *
from ocr import get_text, process
import webview
import time
import sys
import time
#from screeninfo import get_monitors
#import pyautogui
# import psutil


def start_process():
    vid = tools.files(env.image_frames)
    process(vid)
    if not env.is_high_FPS:
        get_text()


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


# def thread_handling_for_cvs():
#     t = threading.Thread(target=show_csv)
#     if not t.is_alive():
#         t.daemon = True
#         t.start()
#     else:
#         t.join()
#         t = threading.Thread(target=show_csv)
#         t.daemon = True
#         t.start()


def fun():
    print(threading.active_count())


env.thread_map[env.t_m] = threading.Thread(target=tools.create_kml)
env.t_m = 0



def thread_handling_for_map():
    print('t_m', env.t_m)
    print('len', env.thread_map.__len__())
    print('act thre', threading.active_count())
    #if not env.thread_map[0].daemon:
    #    # print('inside')
    #    env.thread_map[env.t_m].daemon = True
    #    env.thread_map[env.t_m].start()
#
    #    env.t_m += 1
    #else:
    #    env.thread_map[env.t_m - 1].join()
    #    thread_map = (threading.Thread(target=tools.create_kml))
    #    thread_map.daemon = True
    #    thread_map.start()
#
    #width, height= pyautogui.size()



    tools.create_kml()



    if env.map_ready==True:
        webwindow=webview.create_window('FDAMS', "map.html", width=1920,height=1080)
        webwindow.events.closed+=env.window.deiconify
        webview.start(env.window.withdraw())


    #class Api:
    #    def __init__(self):
    #        self._window = None
#
    #    def set_window(self, window):
    #        self._window = window
#
    #    def destroy(window):
    #        print('Destroying window..')
    #        window.destroy()
    #        print('Destroyed!')
#
    #if __name__ == '__main__':
    #    api = Api()
    #    window = webview.create_window('Blackjack', 'map.html', js_api=api, min_size=(1000, 800), fullscreen=True)
    #    webview.start()

    # t = threading.Thread(target=tools.create_kml)
    # if not env.thread_map.is_alive():
    #     print('49')
    #     # env.thread_map.daemon = True
    #     env.thread_map.start()
    #     # env.thread_map.join()
    # else:
    #     # env.thread_map.join()
    #     print(threading.active_count())
    #     env.thread_map = threading.current_thread()
    #     # print(env.thread_map.daemon)
    #     # env.thread_map.join()
    #     # env.thread_map.
    #     # env.thread_map.daemon = False
    #
    #     # print(env.thread_map.daemon)
    #     # env.thread_map = threading.Thread(target=tools.create_kml)
    #     # env.thread_map = threading.Thread(target=tools.create_kml)
    #     # tools.create_kml()
    #     # print(env.thread_map.daemon)
    #     # env.thread_map.daemon = True
    #
    #     # print(env.thread_map.daemon)
    #     # env.thread_map.start()
    #
    #     # print(env.thread_map.daemon)
def start_window():
    process_frame = tk.Frame(env.window, bg="black")
    process_frame.place(x=0, y=0, width=140, height=1000)

    back_icon = PIL.Image.open("res/back.png")
    back_icon = back_icon.resize((65, 65))
    back_icon = ImageTk.PhotoImage(back_icon)
    back_btn = tk.Button(process_frame, image=back_icon, command=process_frame.destroy, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = back_icon
    back_btn.place(x=20, y=100)


    fps_icon = PIL.Image.open("res/fps_icon.png")
    fps_icon = fps_icon.resize((65, 65))
    fps_icon = ImageTk.PhotoImage(fps_icon)
    env.fps_variable = DoubleVar(env.window)
    env.fps_variable.set("0.15")
    select_fps = tk.OptionMenu(process_frame, env.fps_variable, "0.15", "0.2", "0.5", "1", "2", "3", "4", "5")
    select_fps.config(image=fps_icon, background='black', borderwidth=0, highlightthickness=0, activebackground="black")
    #CreateToolTip(select_fps, text='Select FPS')
    select_fps.image = fps_icon
    select_fps.place(x=20, y=180)

    simulate_icon = PIL.Image.open("res/show_ocr_places.png")
    simulate_icon = simulate_icon.resize((65, 65))
    simulate_icon = ImageTk.PhotoImage(simulate_icon)
    back_btn = tk.Button(process_frame, image=simulate_icon, command=ocr.check_ocr, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = simulate_icon
    back_btn.place(x=20, y=260)

    browse_file_icon = PIL.Image.open("res/browse_folder.png")
    browse_file_icon = browse_file_icon.resize((75, 75))
    browse_file_icon = ImageTk.PhotoImage(browse_file_icon)
    back_btn = tk.Button(process_frame, image=browse_file_icon, command=gui_tools.browse_files, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = browse_file_icon
    back_btn.place(x=20, y=420)

    show_kml_icon = PIL.Image.open("res/start_ocr.png")
    show_kml_icon = show_kml_icon.resize((110, 110))
    show_kml_icon = ImageTk.PhotoImage(show_kml_icon)
    back_btn = tk.Button(process_frame, image=show_kml_icon, command=thread_handling, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = show_kml_icon
    back_btn.place(x=8, y=550)

    show_kml_icon = PIL.Image.open("res/set_pixels.png")
    show_kml_icon = show_kml_icon.resize((60, 60))
    show_kml_icon = ImageTk.PhotoImage(show_kml_icon)

    env.cropping_selection.set(list(env.crop_options.keys())[0])
    dropdown = tk.OptionMenu(
        process_frame,
        env.cropping_selection,
        #list(env.crop_options.keys())[0],
        *list(env.crop_options.keys()),
        command=ocr.select_option_cropping
    )
    dropdown.config(image=show_kml_icon, background='black', borderwidth=0, highlightthickness=0, activebackground="black")
    dropdown.image = show_kml_icon
    dropdown.place(x=20, y=340)

def earth_on_web():
    webwindow = webview.create_window('Google Earth', "https://earth.google.com/", width=1920, height=1080)
    webwindow.events.closed += env.window.deiconify
    webview.start(env.window.withdraw())

def open_kml_file():
    filename = "files/flight.kml"
    os.system("start " + filename)


def show_kml():
    show_kml_frame = tk.Frame(env.window, bg="black")
    show_kml_frame.place(x=110, y=0, width=110, height=1000)

    back_icon = PIL.Image.open("res/back.png")
    back_icon = back_icon.resize((65, 65))
    back_icon = ImageTk.PhotoImage(back_icon)
    back_btn = tk.Button(show_kml_frame, image=back_icon, command=show_kml_frame.destroy, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = back_icon
    back_btn.place(x=8, y=100)


    simulate_icon = PIL.Image.open("res/earth_pc.png")
    earth_pc_icon = simulate_icon.resize((75, 75))
    earth_pc_icon = ImageTk.PhotoImage(earth_pc_icon)
    back_btn = tk.Button(show_kml_frame, image=earth_pc_icon, command=open_kml_file, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = earth_pc_icon
    back_btn.place(x=8, y=180)

    show_kml_icon = PIL.Image.open("res/earth_web.png")
    show_kml_icon = show_kml_icon.resize((75, 75))
    show_kml_icon = ImageTk.PhotoImage(show_kml_icon)
    back_btn = tk.Button(show_kml_frame, image=show_kml_icon, command=earth_on_web, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = show_kml_icon
    back_btn.place(x=8, y=260)



def mapping_window():
    mapping_frame = tk.Frame(env.window, bg="black")
    mapping_frame.place(x=0, y=0, width=110, height=1000)

    back_icon = PIL.Image.open("res/back.png")
    back_icon = back_icon.resize((65, 65))
    back_icon = ImageTk.PhotoImage(back_icon)
    back_btn = tk.Button(mapping_frame, image=back_icon, command=mapping_frame.destroy, background='black',
                           activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = back_icon
    back_btn.place(x=8, y=100)

    simulate_icon = PIL.Image.open("res/simulating_icon.png")
    simulate_icon = simulate_icon.resize((65, 65))
    simulate_icon = ImageTk.PhotoImage(simulate_icon)
    back_btn = tk.Button(mapping_frame, image=simulate_icon, command=thread_handling_for_map, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = simulate_icon
    back_btn.place(x=8, y=180)

    show_kml_icon = PIL.Image.open("res/3d_kml_icon.png")
    show_kml_icon = show_kml_icon.resize((75, 75))
    show_kml_icon = ImageTk.PhotoImage(show_kml_icon)
    back_btn = tk.Button(mapping_frame, image=show_kml_icon, command=show_kml, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = show_kml_icon
    back_btn.place(x=8, y=260)

env.init()
env.window.title('FLIGHT DATA ANALYSER AND FLIGHT SIMULATER')
env.window.geometry("1280x720")
# env.window.overrideredirect(True)
env.window.resizable(False, False)

background_img = PIL.Image.open("res/background_img.png")
background_img = background_img.resize((1280,800))
background_img = ImageTk.PhotoImage(background_img)
background_label = Label(env.window, image=background_img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)



exit_icon = PIL.Image.open("res/exit_icon.png")
exit_icon = exit_icon.resize((35, 35))
exit_icon = ImageTk.PhotoImage(exit_icon)

minimize_icon = PIL.Image.open("res/minimize_icon.png")
minimize_icon = minimize_icon.resize((35, 35))
minimize_icon = ImageTk.PhotoImage(minimize_icon)

#browse_folder_icon = PIL.Image.open("res/browse_video.png")
#browse_folder_icon = browse_folder_icon.resize((60, 60))
#browse_folder_icon = ImageTk.PhotoImage(browse_folder_icon)

start_icon = PIL.Image.open("res/start_icon.png")
start_icon = start_icon.resize((100, 100))
start_icon = ImageTk.PhotoImage(start_icon)

mapping_icon = PIL.Image.open("res/mapping.png")
mapping_icon = mapping_icon.resize((90, 90))
mapping_icon = ImageTk.PhotoImage(mapping_icon)

#how_csv_icon = PIL.Image.open("res/show_csv_icon.png")
#how_csv_icon = show_csv_icon.resize((60, 60))
#how_csv_icon = ImageTk.PhotoImage(show_csv_icon)

#browse_csv_icon = PIL.Image.open("res/browse_csv_icon.png")
#browse_csv_icon = browse_csv_icon.resize((60, 60))
#browse_csv_icon = ImageTk.PhotoImage(browse_csv_icon)

#options_icon = PIL.Image.open("res/options_icon.png")
#options_icon = options_icon.resize((65, 65))
#options_icon = ImageTk.PhotoImage(options_icon)

# Create a File Explorer label
label_window = tk.Label(env.window,
                        text="FLIGHT DATA ANALYSER AND FLIGHT SIMULATER",
                        fg="white", background='black')

label_window.config(font=("Verdana", 20))
env.label_information = tk.Label(env.window,
                                 text="",
                                 fg="red", background='black')

env.label_information.config(font=("Verdana", 15))

env.label_information2 = tk.Label(env.window,
                                  text="WELCOME",
                                  fg="gray", background='black', font=("Verdana", 18))

label_window.after(3000, env.label_information2.destroy)

label_buttons = tk.Label(env.window, background='black')

#button_explore = tk.Button(env.window, command=browse_files, background='black', image=browse_folder_icon, relief=FLAT,
#                           borderwidth=0)
# button_explore.config(font=("Verdana", 9))
# text_FPS = Label(env.window, text="Please Select FPS:")

#button_start_process = tk.Button(env.window, image=start_icon, command=thread_handling, relief=FLAT, borderwidth=0)
button_start_process = tk.Button(env.window, image=start_icon, command=start_window, relief=FLAT, borderwidth=0)
button_start_process.config(bg="black")

# button_start_process.config(font=("Verdana", 9))
#button_loadCSV = tk.Button(env.window, image=browse_csv_icon, command=browse_files, background='black',
#                           activebackground="#ff73c8", relief=FLAT, borderwidth=0)
#button_loadCSV.config(font=("Verdana", 9))
button_exit = tk.Button(env.window, command=exit, width=35, height=35, background='black', image=exit_icon)
button_simulate = tk.Button(env.window, image=mapping_icon, command=mapping_window, background='black',
                            relief=FLAT,
                            borderwidth=0)
button_simulate.config(font=("Verdana", 9))
#button_showCSV = tk.Button(env.window, image=show_csv_icon, command=show_csv, background='black', relief=FLAT,
#                           borderwidth=0)
# button_showCSV.config(font=("Verdana", 9))
#button_reset = tk.Button(env.window, image=reset_icon, background='black', relief=FLAT, borderwidth=0,
#                         command=restart_program)
#button_reset.config(font=("Verdana", 9))

#button_options = tk.Button(env.window, image=options_icon, background='black', relief=FLAT, borderwidth=0,
#                         command=ocr.start_window)
#button_options.config(font=("Verdana", 9))

button_minimize = tk.Button(env.window, width=35, height=35, command=minimize_window,
                            background='black', image=minimize_icon)

#CreateToolTip(button_explore, text='Browse video file')
#CreateToolTip(button_loadCSV, text='Browse CSV File\nfor load manually CSV file')
#CreateToolTip(button_showCSV, text='Show CSV File')
#CreateToolTip(button_reset, text='Reset')
CreateToolTip(button_simulate, text='Simulate On Map\nShow KML File')
CreateToolTip(button_start_process, text='Start to process')



label_window.place(x=0, y=0, width=1280, height=60)
env.label_information2.place(x=127, y=525, width=1000, height=50)
env.label_information.place(x=127, y=525, width=1000, height=50)
# button_exit.place(x=900, y=900, relwidth=0.06, relheight=0.05)
label_buttons.place(x=0, y=0, width=120, height=1000)
#button_explore.place(x=8, y=100)

# text_FPS.place(x=100, y=175, relwidth=0.07, relheight=0.015)
button_simulate.place(x=8, y=400)
#button_showCSV.place(x=9, y=400)
#button_loadCSV.place(x=13, y=325)
button_start_process.place(x=8, y=250)
#button_reset.place(x=8, y=550)
#button_options.place(x=8, y=625)
button_exit.place(x=1230, y=10)
button_minimize.place(x=1175, y=10)

env.s.theme_use("alt")
env.s.configure("TProgressbar", thickness=5, background='yellow', troughcolor='black')

env.read_progress_bar = Progressbar(env.window, orient=HORIZONTAL,
                                    length=500, mode='determinate', style="TProgressbar")

env.process_progress_bar = Progressbar(env.window, orient=HORIZONTAL,
                                       length=500, mode='determinate', style="TProgressbar")


center(env.window)
env.window.mainloop()

