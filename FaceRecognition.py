import numpy as np
import cv2
import dlib
import pickle
import argparse
if True:  # Include project path
    import sys
    import os
    ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
    CURR_PATH = os.path.dirname(os.path.abspath(__file__))+"/"
    sys.path.append(ROOT)

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('./facialLandmarks/shape_predictor_68_face_landmarks.dat')
model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
FACE_DESC, FACE_NAME = pickle.load(open('./tempmodel/trainset.pk', 'rb'))

def parse_args():
        print(f"\n AI Test Face Recognition\n")
        parser = argparse.ArgumentParser(
            description="Test Face Recognition on \n"
            "(1) a video, (2) a folder of images, (3) or web camera.")
        parser.add_argument("-v", "--video", required=False, default="",
                            help="path to a video file, or images, or webcam. \n")

        args = parser.parse_args()
        return args
args = parse_args()

# cap = cv2.VideoCapture('./data_test/face_test.mp4')
cap = cv2.VideoCapture(args.video)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w][:, :, ::-1]
        dets = detector(face, 1)
        for k, d in enumerate(dets):
            shape = sp(face, d)
            face_desc0 = model.compute_face_descriptor(face, shape, 10)
            distance = []
            for face_desc in FACE_DESC:
                distance.append(np.linalg.norm(np.array(face_desc) - np.array(face_desc0)))
            distance = np.array(distance)
            idx = np.argmin(distance)
            if distance[idx] < 0.5:
                name = FACE_NAME[idx]
                print(name)
                cv2.putText(frame, name, (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (255, 255, 255), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color=(255, 0, 0), thickness=1)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), color=(255, 0, 0), thickness=1)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
