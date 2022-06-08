import os
from tkinter import BOTTOM, S

import PIL
import cv2
import numpy as np
import pandas as pd
import easyocr
from PIL import ImageTk

import environment as env
import gui_tools
from data_correction import fix_df
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
import threading
from tkinter import messagebox



def process(src_vid):
    env.flag = False

    env.process_progress_bar.pack(pady=10, side=BOTTOM, anchor=S)

    video_len = int(src_vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = src_vid.get(cv2.CAP_PROP_FPS)
    frame_range = int(fps / env.fps_variable.get())

    index = 1
    if env.fps_variable.get() <= int(fps):
        env.is_high_FPS = False
        while src_vid.isOpened():

            prog = int(100 * index / video_len)
            env.process_progress_bar['value'] = prog
            env.window.update_idletasks()

            ret, frame = src_vid.read()
            if not ret:
                break

            # name each frame and save as png
            if index < 10:
                name = './image_frames/frame000' + str(index) + '.png'
            elif index < 100:
                name = './image_frames/frame00' + str(index) + '.png'
            elif index < 1000:
                name = './image_frames/frame0' + str(index) + '.png'
            else:
                name = './image_frames/frame' + str(index) + '.png'

            if index % frame_range == 0:
                print('Extracting frames ...' + name)

                # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # lower = np.array([39, 50, 125])
                # upper = np.array([178, 255, 255])
                # mask = cv2.inRange(hsv, lower, upper)
                #
                # mask = fix_image(mask)

                cv2.imwrite(name, frame)

            index = index + 1

            # if cv2.waitKey(10) & 0xFF == ord('q'):
            #    break

        env.label_information.configure(text='Video frames are extracted')
        src_vid.release()
        # cv2.destroyAllWindows()
    else:
        env.label_information.configure(text="The FPS value you selected is higher than the FPS value of the video.\n"
                                             "FPS of video is:" + str(fps))
        env.is_high_FPS = True



def get_text():
    env.read_progress_bar.pack(pady=10, side=BOTTOM, anchor=S)

    if env.flag == True:

        try:
            os.remove("cropped_images")
        except OSError:
            pass

        if not os.path.exists("cropped_images"):
            os.makedirs("cropped_images")

        # progress['value'] = 0

        data = {
            'day': [],
            'month': [],
            'year': [],
            'hour': [],
            'min': [],
            'sec': [],
            'degree_lat': [],
            'minute_lat': [],
            'second_lat': [],
            'direction_lat': [],
            'degree_lon': [],
            'minute_lon': [],
            'second_lon': [],
            'direction_lon': [],
            'heading_angle': [],
            'target_degree_lat': [],
            'target_minute_lat': [],
            'target_second_lat': [],
            'target_direction_lat': [],
            'target_degree_lon': [],
            'target_minute_lon': [],
            'target_second_lon': [],
            'target_direction_lon': [],
        }

        reader = easyocr.Reader(['en'])
        df = pd.DataFrame(data)
        crops_pixels_df = pd.read_csv(env.crop_pixels_file_path)
        crop = {}



        j = 0
        for i in os.listdir(env.image_frames): # Dosyadaki tüm frameleri okuyor !!! HATA
            print(str(i))
            frame = cv2.imread(env.image_frames + "/" + i)

            for col_name in crops_pixels_df.columns:
                crop[col_name] = frame[crops_pixels_df[col_name][0]:     crops_pixels_df[col_name][1] ,   crops_pixels_df[col_name][2] :   crops_pixels_df[col_name][3]]



            #crop = {'day':                  frame[crops_pixels_df['day'                 ][0]:     crops_pixels_df['day'                 ][1] ,   crops_pixels_df['day'                 ][2] :   crops_pixels_df['day'                 ][3] ],
            #        'month':                frame[crops_pixels_df['month'               ][0]:     crops_pixels_df['month'               ][1] ,   crops_pixels_df['month'               ][2] :   crops_pixels_df['month'               ][3] ],
            #        'year':                 frame[crops_pixels_df['year'                ][0]:     crops_pixels_df['year'                ][1] ,   crops_pixels_df['year'                ][2] :   crops_pixels_df['year'                ][3] ],
            #        'hour':                 frame[crops_pixels_df['hour'                ][0]:     crops_pixels_df['hour'                ][1] ,   crops_pixels_df['hour'                ][2] :   crops_pixels_df['hour'                ][3] ],
            #        'min':                  frame[crops_pixels_df['min'                 ][0]:     crops_pixels_df['min'                 ][1] ,   crops_pixels_df['min'                 ][2] :   crops_pixels_df['min'                 ][3] ],
            #        'sec':                  frame[crops_pixels_df['sec'                 ][0]:     crops_pixels_df['sec'                 ][1] ,   crops_pixels_df['sec'                 ][2] :   crops_pixels_df['sec'                 ][3] ],
            #        'degree_lat':           frame[crops_pixels_df['degree_lat'          ][0]:     crops_pixels_df['degree_lat'          ][1] ,   crops_pixels_df['degree_lat'          ][2] :   crops_pixels_df['degree_lat'          ][3] ],
            #        'minute_lat':           frame[crops_pixels_df['minute_lat'          ][0]:     crops_pixels_df['minute_lat'          ][1] ,   crops_pixels_df['minute_lat'          ][2] :   crops_pixels_df['minute_lat'          ][3] ],
            #        'second_lat':           frame[crops_pixels_df['second_lat'          ][0]:     crops_pixels_df['second_lat'          ][1] ,   crops_pixels_df['second_lat'          ][2] :   crops_pixels_df['second_lat'          ][3] ],
            #        'direction_lat':        frame[crops_pixels_df['direction_lat'       ][0]:     crops_pixels_df['direction_lat'       ][1] ,   crops_pixels_df['direction_lat'       ][2] :   crops_pixels_df['direction_lat'       ][3] ],
            #        'degree_lon':           frame[crops_pixels_df['degree_lon'          ][0]:     crops_pixels_df['degree_lon'          ][1] ,   crops_pixels_df['degree_lon'          ][2] :   crops_pixels_df['degree_lon'          ][3] ],
            #        'minute_lon':           frame[crops_pixels_df['minute_lon'          ][0]:     crops_pixels_df['minute_lon'          ][1] ,   crops_pixels_df['minute_lon'          ][2] :   crops_pixels_df['minute_lon'          ][3] ],
            #        'second_lon':           frame[crops_pixels_df['second_lon'          ][0]:     crops_pixels_df['second_lon'          ][1] ,   crops_pixels_df['second_lon'          ][2] :   crops_pixels_df['second_lon'          ][3] ],
            #        'direction_lon':        frame[crops_pixels_df['direction_lon'       ][0]:     crops_pixels_df['direction_lon'       ][1] ,   crops_pixels_df['direction_lon'       ][2] :   crops_pixels_df['direction_lon'       ][3] ],
            #        'heading_angle':        frame[crops_pixels_df['heading_angle'       ][0]:     crops_pixels_df['heading_angle'       ][1] ,   crops_pixels_df['heading_angle'       ][2] :   crops_pixels_df['heading_angle'       ][3] ],
            #        'altitude':             frame[crops_pixels_df['altitude'            ][0]:     crops_pixels_df['altitude'            ][1] ,   crops_pixels_df['altitude'            ][2] :   crops_pixels_df['altitude'            ][3] ],
            #        'target_degree_lat':    frame[crops_pixels_df['target_degree_lat'   ][0]:     crops_pixels_df['target_degree_lat'   ][1] ,   crops_pixels_df['target_degree_lat'   ][2] :   crops_pixels_df['target_degree_lat'   ][3] ],
            #        'target_minute_lat':    frame[crops_pixels_df['target_minute_lat'   ][0]:     crops_pixels_df['target_minute_lat'   ][1] ,   crops_pixels_df['target_minute_lat'   ][2] :   crops_pixels_df['target_minute_lat'   ][3] ],
            #        'target_second_lat':    frame[crops_pixels_df['target_second_lat'   ][0]:     crops_pixels_df['target_second_lat'   ][1] ,   crops_pixels_df['target_second_lat'   ][2] :   crops_pixels_df['target_second_lat'   ][3] ],
            #        'target_direction_lat': frame[crops_pixels_df['target_direction_lat'][0]:     crops_pixels_df['target_direction_lat'][1] ,   crops_pixels_df['target_direction_lat'][2] :   crops_pixels_df['target_direction_lat'][3] ],
            #        'target_degree_lon':    frame[crops_pixels_df['target_degree_lon'   ][0]:     crops_pixels_df['target_degree_lon'   ][1] ,   crops_pixels_df['target_degree_lon'   ][2] :   crops_pixels_df['target_degree_lon'   ][3] ],
            #        'target_minute_lon':    frame[crops_pixels_df['target_minute_lon'   ][0]:     crops_pixels_df['target_minute_lon'   ][1] ,   crops_pixels_df['target_minute_lon'   ][2] :   crops_pixels_df['target_minute_lon'   ][3] ],
            #        'target_second_lon':    frame[crops_pixels_df['target_second_lon'   ][0]:     crops_pixels_df['target_second_lon'   ][1] ,   crops_pixels_df['target_second_lon'   ][2] :   crops_pixels_df['target_second_lon'   ][3] ],
            #        'target_direction_lon': frame[crops_pixels_df['target_direction_lon'][0]:     crops_pixels_df['target_direction_lon'][1] ,   crops_pixels_df['target_direction_lon'][2] :   crops_pixels_df['target_direction_lon'][3] ],
            #        }

            k = 0

            text = {'frame': i}

            for c in crop.keys():

                if c == 'month':
                    text[c] = reader.readtext(crop[c], allowlist='ABCDEFGHIJKLMNOPRSTUVWXYZ', workers=3)
                elif c == 'direction_lat' or c == 'target_direction_lat':
                    text[c] = reader.readtext(crop[c], allowlist='SN',  workers=3)
                elif c == 'direction_lon' or c == 'target_direction_lon':
                    text[c] = reader.readtext(crop[c], allowlist='EW',  workers=3)
                else:
                    text[c] = reader.readtext(crop[c], allowlist='0123456789',  workers=3)

                cv2.imwrite("cropped_images/" + i + "_" + str(k) + '.' + c + ".png", crop[c])

                # image = cv2.imread("cropped_images/" + i + "_" + str(k) + '.' + c + ".png")
                # print(image)

                k += 1
                if text[c] != []:
                    text[c] = (text[c][0][1].replace(" ", ""))
                    print(text[c])

                j += 1
                prog = int(100 * j / (os.listdir(env.image_frames).__len__() * crop.__len__()))
                env.read_progress_bar['value'] = prog
                env.window.update_idletasks()

            df = df.append(text, ignore_index=True)
        df.to_csv('files/unfixed_output.csv', index=False)

    else:
        df = pd.read_csv('files/unfixed_output.csv')

        df['month'] = (df['month']).astype(str)
        df['direction_lat'] = (df['direction_lat']).astype(str)
        df['direction_lon'] = (df['direction_lon']).astype(str)
        df['year'] = (df['year']).astype(str)

    df = fix_df(df)

    df.to_csv('files/fixed_output.csv', index=False)

    env.label_information.configure(text='CSV file is complete')

    env.read_progress_bar['value'] = 100
    env.window.update_idletasks()


def region_selection(event, x, y, flags, param):


    if event == cv2.EVENT_LBUTTONDOWN:
        # Left mouse button down: begin the selection.
        # The first coordinate pair is the centre of the square.
        env.select_coords = [(x, y)]
        env.selecting = True

    elif event == cv2.EVENT_MOUSEMOVE and env.selecting:
        # If we're dragging the selection square, update it.
        env.image = env.clone.copy()
        x0, y0, x1, y1 = (x, y, *env.select_coords[0])
        cv2.rectangle(env.image, (x0, y0), (x1, y1), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        # Left mouse button up: the selection has been made.
        env.select_coords.append((x, y))
        env.selecting = False

def thread_handling_cropping():
    t = threading.Thread(target=set_cropping_selection)
    if not t.is_alive():
        t.daemon = True
        t.start()
    else:
        t.join()
        t = threading.Thread(target=set_cropping_selection)
        t.daemon = True
        t.start()


def thread_handling_region_selection(event, x, y, flags, param):
    t = threading.Thread(target=region_selection(event, x, y, flags, param))
    if not t.is_alive():
        t.daemon = True
        t.start()
    else:
        t.join()
        t = threading.Thread(target=region_selection(event, x, y, flags, param))
        t.daemon = True
        t.start()

def draw_rectangles(crops_pixels_df, img):
    #cv2.rectangle(img1, pt1=(400,200), pt2=(100,50), color=(255,0,0), thickness=10))
    for col_name in crops_pixels_df.columns:
        cv2.rectangle(img, (crops_pixels_df[col_name][3],crops_pixels_df[col_name][1] ),(crops_pixels_df[col_name][2],crops_pixels_df[col_name][0]), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['day'                 ][3],     crops_pixels_df['day'                 ][1] ),   (crops_pixels_df['day'                 ][2] ,crops_pixels_df['day'                 ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['month'               ][3],     crops_pixels_df['month'               ][1] ),   (crops_pixels_df['month'               ][2] ,crops_pixels_df['month'               ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['year'                ][3],     crops_pixels_df['year'                ][1] ),   (crops_pixels_df['year'                ][2] ,crops_pixels_df['year'                ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['hour'                ][3],     crops_pixels_df['hour'                ][1] ),   (crops_pixels_df['hour'                ][2] ,crops_pixels_df['hour'                ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['min'                 ][3],     crops_pixels_df['min'                 ][1] ),   (crops_pixels_df['min'                 ][2] ,crops_pixels_df['min'                 ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['sec'                 ][3],     crops_pixels_df['sec'                 ][1] ),   (crops_pixels_df['sec'                 ][2] ,crops_pixels_df['sec'                 ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['degree_lat'          ][3],     crops_pixels_df['degree_lat'          ][1] ),   (crops_pixels_df['degree_lat'          ][2] ,crops_pixels_df['degree_lat'          ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['minute_lat'          ][3],     crops_pixels_df['minute_lat'          ][1] ),   (crops_pixels_df['minute_lat'          ][2] ,crops_pixels_df['minute_lat'          ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['second_lat'          ][3],     crops_pixels_df['second_lat'          ][1] ),   (crops_pixels_df['second_lat'          ][2] ,crops_pixels_df['second_lat'          ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['direction_lat'       ][3],     crops_pixels_df['direction_lat'       ][1] ),   (crops_pixels_df['direction_lat'       ][2] ,crops_pixels_df['direction_lat'       ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['degree_lon'          ][3],     crops_pixels_df['degree_lon'          ][1] ),   (crops_pixels_df['degree_lon'          ][2] ,crops_pixels_df['degree_lon'          ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['minute_lon'          ][3],     crops_pixels_df['minute_lon'          ][1] ),   (crops_pixels_df['minute_lon'          ][2] ,crops_pixels_df['minute_lon'          ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['second_lon'          ][3],     crops_pixels_df['second_lon'          ][1] ),   (crops_pixels_df['second_lon'          ][2] ,crops_pixels_df['second_lon'          ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['direction_lon'       ][3],     crops_pixels_df['direction_lon'       ][1] ),   (crops_pixels_df['direction_lon'       ][2] ,crops_pixels_df['direction_lon'       ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['heading_angle'       ][3],     crops_pixels_df['heading_angle'       ][1] ),   (crops_pixels_df['heading_angle'       ][2] ,crops_pixels_df['heading_angle'       ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['altitude'            ][3],     crops_pixels_df['altitude'            ][1] ),   (crops_pixels_df['altitude'            ][2] ,crops_pixels_df['altitude'            ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['target_degree_lat'   ][3],     crops_pixels_df['target_degree_lat'   ][1] ),   (crops_pixels_df['target_degree_lat'   ][2] ,crops_pixels_df['target_degree_lat'   ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['target_minute_lat'   ][3],     crops_pixels_df['target_minute_lat'   ][1] ),   (crops_pixels_df['target_minute_lat'   ][2] ,crops_pixels_df['target_minute_lat'   ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['target_second_lat'   ][3],     crops_pixels_df['target_second_lat'   ][1] ),   (crops_pixels_df['target_second_lat'   ][2] ,crops_pixels_df['target_second_lat'   ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['target_direction_lat'][3],     crops_pixels_df['target_direction_lat'][1] ),   (crops_pixels_df['target_direction_lat'][2] ,crops_pixels_df['target_direction_lat'][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['target_degree_lon'   ][3],     crops_pixels_df['target_degree_lon'   ][1] ),   (crops_pixels_df['target_degree_lon'   ][2] ,crops_pixels_df['target_degree_lon'   ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['target_minute_lon'   ][3],     crops_pixels_df['target_minute_lon'   ][1] ),   (crops_pixels_df['target_minute_lon'   ][2] ,crops_pixels_df['target_minute_lon'   ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['target_second_lon'   ][3],     crops_pixels_df['target_second_lon'   ][1] ),   (crops_pixels_df['target_second_lon'   ][2] ,crops_pixels_df['target_second_lon'   ][0]   ), color=(255,0,0),thickness=2)
    #cv2.rectangle(img, (crops_pixels_df['target_direction_lon'][3],     crops_pixels_df['target_direction_lon'][1] ),   (crops_pixels_df['target_direction_lon'][2] ,crops_pixels_df['target_direction_lon'][0]   ), color=(255,0,0),thickness=2)
    return img,

def check_ocr():
    #env.window.withdraw()
    crops_pixels_df = pd.read_csv(env.crop_pixels_file_path)

    cam = cv2.VideoCapture(env.video_file_path)

    try:
        if not os.path.exists('data'):
            os.makedirs('data')

    except OSError:
        print('Error')

    ret, frame = cam.read()
    if ret:
        name = 'frame_for_settings.png'
        print('Created...' + name)
        cv2.imwrite(name, frame)

    basename = os.path.basename('frame_for_settings.png')
    env.image = cv2.imread(basename)
    env.clone = env.image.copy()
    cv2.namedWindow(basename, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(basename, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    draw_rectangles(crops_pixels_df, env.image)

    while True:
        cv2.imshow(basename, env.image)


        key = cv2.waitKey(1) & 0xFF
        if key == ord("s") or key == 27 or cv2.getWindowProperty(basename, cv2.WND_PROP_VISIBLE) < 1:
            cv2.destroyAllWindows()
            break
    #env.window.deiconify()


def ShowChoice():
    print(env.data_place.get())


def set_crops_pixels_df(crops_pixels_df, y1, y0, x1, x0):

    crops_pixels_df[env.data_place.get()][0] = y1
    crops_pixels_df[env.data_place.get()][1] = y0
    crops_pixels_df[env.data_place.get()][2] = x1
    crops_pixels_df[env.data_place.get()][3] = x0

    return crops_pixels_df



def set_cropping_selection():
    env.window.withdraw()
    crops_pixels_df = pd.read_csv(env.crop_pixels_file_path)
    setCropsWindow = Toplevel(env.window)




    setCropsWindow.attributes('-topmost', True)
    #setCropsWindow.title("New Window")
    setCropsWindow.geometry("1280x720")
    gui_tools.center(setCropsWindow)
    setCropsWindow.overrideredirect(True)

    #btn = Button(setCropsWindow, text='Set pixels for selected value', command=thread_handling_cropping)
    back_btn = Button(setCropsWindow, text='back to settings', command=lambda:[setCropsWindow.destroy(),exit_from_crop_screen()])

    #env.data_place.set(1)
    data_types = [('day'                 , 'day'                 ),
                 ('month'               , 'month'               ),
                 ('year'                , 'year'                ),
                 ('hour'                , 'hour'                ),
                 ('min'                 , 'min'                 ),
                 ('sec'                 , 'sec'                 ),
                 ('degree_lat'          , 'degree_lat'          ),
                 ('minute_lat'          , 'minute_lat'          ),
                 ('second_lat'          , 'second_lat'          ),
                 ('direction_lat'       , 'direction_lat'       ),
                 ('degree_lon'          , 'degree_lon'          ),
                 ('minute_lon'          , 'minute_lon'          )

                 ]
    data_types2 = [
                  ('second_lon', 'second_lon'),
                  ('direction_lon', 'direction_lon'),
                  ('heading_angle', 'heading_angle'),
                  ('altitude', 'altitude'),
                  ('target_degree_lat', 'target_degree_lat'),
                  ('target_minute_lat', 'target_minute_lat'),
                  ('target_second_lat', 'target_second_lat'),
                  ('target_direction_lat', 'target_direction_lat'),
                  ('target_degree_lon', 'target_degree_lon'),
                  ('target_minute_lon', 'target_minute_lon'),
                  ('target_second_lon', 'target_second_lon'),
                  ('target_direction_lon', 'target_direction_lon'),

                  ]

    frame1 = LabelFrame(setCropsWindow)
    frame1.grid(row=1, column=1, padx=10)

    frame2 = LabelFrame(setCropsWindow)
    frame2.grid(row=1, column=2)


    #Label(setCropsWindow,
    #         text="""Select the data type you want to set""",
    #         justify=LEFT).pack()

    for data_type, val in data_types:
        tk.Radiobutton(frame1,
                    text=data_type,
                    font=("arial", 10, "bold"),
                    indicator=0,
                    background="light green",
                    #padx=10,


                    #padx=20,
                    variable=env.data_place,
                    command=ShowChoice,
                    value=val).pack()

    for data_type, val in data_types2:
        tk.Radiobutton(frame2,
                    text=data_type,
                    font=("arial", 10, "bold"),
                    indicator=0,
                    background="light green",
                    #padx=40,


                    #padx=20,
                    variable=env.data_place,
                    command=ShowChoice,
                    value=val).pack()



    #btn.pack()
    back_btn.grid(row=1, column=3)

    #env.window.attributes('-topmost', True)


    cam = cv2.VideoCapture(env.video_file_path)
    try:
        if not os.path.exists('data'):
            os.makedirs('data')

    except OSError:
        print('Error')

    ret, frame = cam.read()
    if ret:
        name = 'frame_for_settings.png'
        print('Created...' + name)
        cv2.imwrite(name, frame)

    basename = os.path.basename('frame_for_settings.png')
    env.image = cv2.imread(basename)
    env.clone = env.image.copy()
    cv2.namedWindow(basename, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(basename, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    #cv2.setMouseCallback(basename, region_selection)

    while True:
        cv2.setMouseCallback(basename, thread_handling_region_selection)
        draw_rectangles(crops_pixels_df,env.image)
        cv2.imshow(basename, env.image)


        #selected_img = PIL.Image.open("res/background_img.png")
        #selected_img = selected_img.resize((600,400))
        #selected_img = ImageTk.PhotoImage(selected_img)
        #selected_img_label = Label(setCropsWindow, image=selected_img)
#
        #selected_img_label.place(x=0, y=0, relwidth=1, relheight=1)

        key = cv2.waitKey(1) & 0xFF
        #if key == ord("s") or key == 27 or cv2.getWindowProperty(basename, cv2.WND_PROP_VISIBLE) < 1 or env.exit == True:
        if env.exit_check == True:
            #HEPSİNİN KAYDI BURADA YAPILACAK
            crops_pixels_df.to_csv(env.crop_pixels_file_path)
            cv2.destroyAllWindows()
            #env.window.attributes('-topmost', False)
            break

        if len(env.select_coords) == 2:
            x1, y1 = env.select_coords[0]
            x0, y0 = env.select_coords[1]
            crop_values_dict = {}
            print(y1, y0, x1, x0)
            if (env.data_place.get() != "Not Selected"):

                crops_pixels_df = set_crops_pixels_df(crops_pixels_df, y1, y0, x1, x0)

            else:
               warninglabel = tk.Label(setCropsWindow,
                                       text="Please Select DataType to set",
                                       fg="red", background='white', font=("arial", 10, "bold"))
               warninglabel.grid(row=1, column=4)
               warninglabel.after(10, warninglabel.destroy)
            #cv2.waitKey(0)
    env.exit_check = False
    env.window.deiconify()
    #cv2.rectangle(env.image, (x1, y1), (x2, y2), (255, 0, 0), 2) !!!! Gsötermk için kullanılacak

def select_option_cropping(self):
    selection = env.cropping_selection.get()

    if selection == "INDIVIDUAL":
        env.crop_pixels_file_path = "res/crop_pixels_individual.csv"
        thread_handling_cropping()

    elif selection == "DEFAULT":
        env.crop_pixels_file_path = "res/crop_pixels.csv"

    elif selection == "DEFAULT2":
        env.crop_pixels_file_path = "res/crop_pixels_default2.csv"

    elif selection == "BROWSE FILE":
        path = gui_tools.browse_csv()
        env.crop_pixels_file_path = path



    #elif selection == "BROWSE FILE":







    #env.window.columnconfigure(0, weight=1)
    #env.window.columnconfigure(1, weight=3)
    #env.window.rowconfigure(1, weight=3)



    #settingsFrame= Frame(env.window)
    #background_img = PIL.Image.open("res/background_img.png")
    #background_img = background_img.resize((1280,800))
    #background_img = ImageTk.PhotoImage(background_img)
    #background_label = Label(settingsFrame, image=background_img)
    ##setCropsWindow = Frame(env.window)
    ##settingsWindow.config(width=500, height=500, background='black')
    ##setCropsWindow.config(width=500, height=500)
    ##settingsWindow.pack(side=BOTTOM)
    ##setCropsWindow.pack(side=BOTTOM)
#
#
    ##button_loadCSV = tk.Button(env.window, image=browse_csv_icon, command=browse_files, background='black',
    ##                           activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    ##button_loadCSV.config(font=("Verdana", 9))
#
#
    ##for frame in (settingsFrame, setCropsWindow):
    ##    frame.config(width=1280, height=800)
    ##    frame.grid(row=1, column=1, sticky="news")
#
    #settingsFrame.config(width=1280, height=800 )
    #settingsFrame.place(x=0, y=0, relwidth=1, relheight=1)
    #background_label.pack()
    ##background_label.place(x=0, y=0, relwidth=1, relheight=1)
    ##settingsFrame.grid(row=1, column=1, sticky="news")
#
#
    ##gui_tools.center(setCropsWindow)
    ##setCropsWindow.resizable(False, False)
#
    #set_crops_btn = Button(settingsFrame, text='set_crops', command=lambda:thread_handling_cropping())
    #exit_btn = Button(settingsFrame, text='exit',command=lambda:settingsFrame.destroy())
#
#
#
    ## Set the position of button on the top of window.
#
    #set_crops_btn.pack()
    #exit_btn.pack()
    #raise_frame(settingsFrame)
    ##env.window.mainloop()



def raise_frame(frame):
    frame.tkraise()

def exit_from_crop_screen():
    env.exit_check = True