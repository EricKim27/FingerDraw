from draw import *
import time
import mediapipe as mp
import cv2
import datetime
import warnings
import sys

warnings.filterwarnings("ignore")

try:
    print(ascii_art)
    print(f"FingerDraw v{version}\n")
    print(f"New in v1.1:\n{patches}")
    print("")
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    print("Starting Camera...")
    cap = cv2.VideoCapture(1)
    cv2.startWindowThread()
    text = "Black"
    # Initialize drawing utils
    pen = Pen()
    pen.coordinate_list.append([23456, 23456, pen.colors])
    array = []
    if not cap.isOpened():
        print("Error: Camera not accessible")
        raise Exception("Camera not accessible")
    
    finger_detected = True

    while cap.isOpened():
        suc, img = cap.read()
        if(suc != True):
            print("camera not opening")
            continue
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = hands.process(img2)
        if res.multi_hand_landmarks:
            pen.get_dist(res)
            if pen.dist < 0.065:
                pen.update_current_location(res)
                array = pen.coordinate_list[-1]
                finger_detected = False
            if finger_detected:
                if len(pen.coordinate_list) >= 1:
                    if pen.coordinate_list[-1][0] != 100000:
                        pen.separate_plot()
            finger_detected = True
        else:
            if finger_detected and pen.coordinate_list[-1][0] != 100000:
                pen.separate_plot()
            finger_detected = False
        pen.draw(img)
        img = cv2.flip(img, 1)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'):
            pen.clear_canvas()
        elif chr(key) in color_map:
            pen.colors, text = color_map[chr(key)]
            pen.separate_plot()
        elif key == ord('p'):
            print(pen.coordinate_list)
        elif key == ord('q'):
            break
        elif key == ord('z'):
            pen.undo()
        elif key == ord('s'):
            imname = f"{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.png"
            cv2.imwrite(imname, img)
            cv2.putText(img,f"Image saved as{imname}",(0,200),cv2.FONT_HERSHEY_PLAIN, 8, pen.colors, 5)
        cv2.putText(img, text, (0,130), cv2.FONT_HERSHEY_PLAIN, 12, pen.colors, 5)
        cv2.imshow('FingerDraw', img)
except Exception as e:
    print('\033[91m' + f"ERROR OCCURED: {e}" + '\033[0m')
    print("Doing cleanup job...")
    imname = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.png"
    print("Saving your drawings as png")
    cv2.imwrite(imname, img)
    cap.release()
    cv2.destroyAllWindows()
    for i in range(1, 5):
        cv2.waitKey(1)
    sys.exit(250)
finally:
    cap.release()
    cv2.destroyAllWindows()
    for i in range(1, 5):
        cv2.waitKey(1)
    
    print('\033[92m' + "Done." + '\033[0m')
