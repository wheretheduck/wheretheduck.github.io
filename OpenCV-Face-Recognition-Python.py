"""
Author: Will Irwin
Date: 3/14/2018
Inputs:
    Training pictures in specific folder for a person
    Picture(s) in specific folder from camera to test
Outputs:
    true if image contains person
    else false
"""
import cv2
import os
import numpy as np
from random import randint
import time


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    if (len(faces) == 0):
        return None, None

    (x, y, w, h) = faces[0]

    return gray[y:y+w, x:x+h], faces[0]

def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)

    faces = []

    labels = []

    for dir_name in dirs:

        if not dir_name.startswith("s"):
            continue;

        label = int(dir_name.replace("s", ""))

        subject_dir_path = data_folder_path + "/" + dir_name

        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:

            if image_name.startswith("."):
                continue;

            image_path = subject_dir_path + "/" + image_name


            image = cv2.imread(image_path)

            face, rect = detect_face(image)

            if face is not None:

                faces.append(face)

                labels.append(label)
            else:
                print(image_path)

    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    return faces, labels

def validate(data_folder_path):

    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    confidence_threshold = 0.0
    for dir_name in dirs:

        if not dir_name.startswith("s"):
            continue;

        label = int(dir_name.replace("s", ""))

        subject_dir_path = data_folder_path + "/" + dir_name

        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:

            if image_name.startswith("."):
                continue;

            image_path = subject_dir_path + "/" + image_name

            image = cv2.imread(image_path)

            face, rect = detect_face(image)

            if face is not None:
                faces.append(face)
                labels.append(label)
            else:
                print(image_path)


    thresholds = []

    for face in faces:
        guess = face_recognizer.predict(face)
        thresholds.append(guess[1])

    confidence_threshold = (sum(thresholds)/len(thresholds)) + 3
    print(confidence_threshold)
    print("")

    return confidence_threshold

def predict(test_img, confidence_threshold):
    img = test_img.copy()

    face, rect = detect_face(img)

    if face is not None:
        pass
    else:
        print(test_img)
        return 0

    label = face_recognizer.predict(face)

    if label[1] > confidence_threshold:
        label_text = subjects[label[0]]
    else:
        label_text = subjects[0]

    return label_text


def main(capture, confidence_threshold):
    print("Predicting images...")

    test_img = cv2.imread(capture)

    prediction = predict(test_img, confidence_threshold)

    if prediction == subjects[0]:
        print(subjects[0] + "...")
        print("")
        return True
    else:
        print("UNKNOWN...")
        print("")
        return False


test_location = "test-data/"
training_location = "training-data"
validation_location = "validating-data"
subjects = ["Dagan Martinez","UNKNOWN"]

#let's first prepare our training data
#data will be in two lists of same size
#one list will contain all the faces
#and other list will contain respective labels for each face
print("Preparing data...")
print("")
faces, labels = prepare_training_data(training_location)
print("Data prepared")

#print total faces and labels
print("Total faces: "+ str(len(faces)))
print("Total labels: "+ str(len(labels)))
print("")

#create our LBPH face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

#train our face recognizer of our training faces
face_recognizer.train(faces, np.array(labels))

#test with separate pictures known correct
confidence_threshold = validate(validation_location)

while True:
    time.sleep(5)
    if len(os.listdir(test_location)) != 1:
        #need to mess with this to make sure it looks at and deletes the oldest file
        #and leaves newest 1 to prevent errors
        capture = test_location + os.listdir(test_location)[len(os.listdir(test_location)) -1]
        main(capture, confidence_threshold)
        os.remove(capture)
    else:
        pass
