import os
import pathlib

import cv2
import enchant
import numpy as np
import pandas as pd
import simplekml

import environment as env


def files(image_frames):
    try:
        os.remove(image_frames)
    except OSError as s:
        # print(s)
        pass

    if not os.path.exists(image_frames):
        os.makedirs(image_frames)

    src_vid = cv2.VideoCapture("yeni.mp4")
    return src_vid


def open_file():
    from os import startfile
    file = pathlib.Path("files/output.txt")
    if file.exists():
        print("File exist")
        startfile("files/output.txt")
    else:
        print("File not exist")
        env.label_information.configure(text="File not exist !!! ")


def fix_image(image):
    start_point = (0, 150)
    end_point = (1920, 920)
    color = (0, 0, 0)
    thickness = -1

    image = cv2.rectangle(image, start_point, end_point, color, thickness)
    image = cv2.medianBlur(image, 3)
    image = cv2.bitwise_not(image)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)[1]
    image = cv2.medianBlur(image, 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    image = cv2.dilate(image, kernel)

    return image


def fix_strings(row):
    my_dict = enchant.PyPWL("res/words.txt")
    row = row.values.tolist()
    length_of_arr = len(row)

    for i in range(length_of_arr):
        word_exists = my_dict.check(row[i])
        if not word_exists:
            if i != 0 and i != length_of_arr - 1:
                if row[i + 1] == row[i - 1]:
                    row[i] = row[i + 1]
                elif i >= 2 and row[i - 1] == row[i - 2]:
                    row[i] = row[i - 1]
                else:
                    row[i] = my_dict.suggest(row[i])[0]

            elif i == 0:
                row[i] = my_dict.suggest(row[i])[0]

            elif i == length_of_arr - 1:
                row[i] = my_dict.suggest(row[i])[0]

    return row

def fix_int(row):
    my_dict = enchant.PyPWL("res/min.txt")
    row = row.values.tolist()
    length_of_arr = len(row)

    for i in range(length_of_arr):
        word_exists = my_dict.check(row[i])
        if not word_exists:
            if i != 0 and i != length_of_arr - 1:
                if row[i + 1] == row[i - 1]:
                    row[i] = row[i + 1]
                elif i >= 2 and row[i - 1] == row[i - 2]:
                    row[i] = row[i - 1]
                else:
                    row[i] = my_dict.suggest(row[i])[0]

            elif i == 0:
                row[i] = my_dict.suggest(row[i])[0]

            elif i == length_of_arr - 1:
                row[i] = my_dict.suggest(row[i])[0]

    return row


def fix_anomalies(row, change_sensitivity):
    print(row)

    arr = pd.to_numeric(row.array, errors='coerce')
    print(arr)

    length_of_arr = len(arr)

    elements = np.array(arr)
    mean = int(np.nanmean(elements, axis=0))
    sd = int(np.nanstd(elements, axis=0))
    print(mean, sd)
    print(mean - change_sensitivity * sd)
    print(mean + change_sensitivity * sd)
    arr[np.isnan(arr)] = -99999


    for i in range(length_of_arr):

        if not (mean + change_sensitivity * sd) >= arr[i] >= (mean - change_sensitivity * sd):

            if i != 0 and i != length_of_arr - 1:
                if not (mean + change_sensitivity * sd) >= arr[i + 1] >= (mean - change_sensitivity * sd):
                    arr[i + 1] = mean

                if arr[i + 1] == arr[i - 1]:
                    arr[i] = arr[i + 1]
                elif i >= 2 > abs(arr[i - 1] - arr[i - 2]):
                    arr[i] = (arr[i - 1] + arr[i - 2]) / 2
                else:
                    arr[i] = (arr[i + 1] + arr[i - 1]) / 2

            elif i == 0:
                arr[i] = arr[i + 1]
            elif i == length_of_arr - 1:
                arr[i] = arr[i - 1]

    arr = arr.astype(pd.Int64Dtype)
    arr = arr.astype(int)

    print(arr)
    return arr


def create_kml():
    df = pd.read_csv("files/output.csv")

    kml = simplekml.Kml()

    for degree_lat, minute_lat, second_lat, direction_lat, degree_lon, minute_lon, second_lon, direction_lon in zip(
            df['degree_lat'], df['minute_lat'], df['second_lat'], df['direction_lat'],
            df['degree_lon'], df['minute_lon'], df['second_lon'], df['direction_lon']):
        latitude = str(degree_lat) + "-" + str(minute_lat) + "-" + str(second_lat) + direction_lat
        N = 'N' in latitude
        d, m, s = map(float, latitude[:-1].split('-'))
        latitude = (d + m / 60. + s / 3600.) * (1 if N else -1)
        longitude = str(degree_lon) + "-" + str(minute_lon) + "-" + str(second_lon) + direction_lon
        W = 'W' in longitude
        d, m, s = map(float, longitude[:-1].split('-'))
        longitude = (d + m / 60. + s / 3600.) * (-1 if W else 1)

        kml.newpoint(coords=[(longitude, latitude)])

    kml.save('files/coordinates.kml')

    env.label_information.configure(text="KML file is created")
