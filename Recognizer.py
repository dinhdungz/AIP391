import cv2
from FaceDetection.face_detection import face
from keras.models import load_model
import numpy as np
import os
from embedding import emb
from MongoDB.retrieve_pymongo_data import database
import pandas as pd
import warnings
import time
import datetime
import csv
warnings.filterwarnings("ignore")
import re

def check(dt):
    lst = os.listdir('Attendance')
    dt = dt + ".csv"
    for i in lst:
        date = i.split('_')
        if dt == date[1]:
            return True
    return False

def Recognition():
    label = None
    person = None
    Id = None

    def Create_labels():
        people = sorted(os.listdir('people'))
        students = {}
        attendance_count = {}
        Ids = []
        for i in people:
            students[(int(i[0]) - 1)] = i[1:]
            s1 = re.findall(r'\d', i)
            m1 = "".join(s1)
            m1 = int(m1)
            Ids.append(m1)
            attendance_count[(int(i[0]) - 1)] = 0
        return students, attendance_count, Ids

    people, attendance_count, Ids = Create_labels()
    completed_label = "Attendance is Completed"
    e = emb()
    fd = face()
    col_names = ['Id', 'Name','Time']
    attendance = pd.DataFrame(columns=col_names)
    model = load_model('Model')

    data = database()  ##### Intitalising the Mongo Database

    color = (0, 255, 0)
    cap = cv2.VideoCapture(0)
    ret = True

    while ret:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        det, coor = fd.detectFace(frame)

        if (det is not None):
            for i in range(len(det)):
                detected = det[i]
                k = coor[i]
                f = detected
                detected = cv2.resize(detected, (160, 160))
                detected = detected.astype('float') / 255.0
                detected = np.expand_dims(detected, axis=0)
                feed = e.calculate(detected)
                feed = np.expand_dims(feed, axis=0)
                prediction = model.predict(feed)[0]

                result = int(np.argmax(prediction))
                # acc = np.max(prediction) #add
                # acc = round(acc, 2)
                # print("accuracy: ", acc)
                if (np.max(prediction) > .85):
                    for i in people:
                        if (result == i):
                            label = people[i]
                            if (attendance_count[i] < 30):
                                attendance_count[i] = attendance_count[i] + 1
                                if (attendance_count[i] == 30):
                                    continue  # ,lecture
                            person = i
                            Id = Ids[i]
                else:
                    label = 'unknown'

                try:
                    if (int(attendance_count[person]) >= 30):
                        cv2.putText(frame, completed_label, (k[0], k[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                                    2)
                        cv2.rectangle(frame, (k[0], k[1]), (k[0] + k[2], k[1] + k[3]), (0, 255, 0), 3)
                    else:
                        cv2.putText(frame, label, (k[0], k[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        cv2.rectangle(frame, (k[0], k[1]), (k[0] + k[2], k[1] + k[3]), (255, 0, 0), 3)
                except:
                    pass
         #hiển thị cái cũ nhất
        cv2.imshow('Say Hi and Press "q" to Quite', frame)
        if (cv2.waitKey(1) & 0XFF == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance" + os.sep + "Attendance_" + date + ".csv"
    if check(date) == False:
        attendance.loc[len(attendance)] = [Id, label, timeStamp]
        attendance.to_csv(fileName, index=False)
    else:
        data = pd.read_csv(fileName)
        data.loc[len(data)] = [Id, label, timeStamp]
        data = data.drop_duplicates(subset=['Id'], keep='first')
        data.to_csv(fileName, index=False)

    print("Attendance Successful")
    cap.release()
    cv2.destroyAllWindows()
    return fileName

