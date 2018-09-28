import numpy as np
import cv2
import time
import predict

#import the cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def TakeSnapshotAndSave():
    # access the webcam (every webcam has a number, the default is 0)
    cap = cv2.VideoCapture(0)

    num = 0 
    while num<1:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # to detect faces in video
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        

        x = 0
        y = 20
        text_color = (0,255,0)

        cv2.imwrite('opencv'+str(num)+'.jpg',frame)
        num = num+1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    emo=predict.predict()
    return emo


if __name__ == "__main__":
    TakeSnapshotAndSave()



