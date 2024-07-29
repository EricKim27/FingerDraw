from draw import *
import mediapipe as mp
import cv2

try:
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    cap = cv2.VideoCapture(1)
    cv2.startWindowThread()

    # Initialize drawing utils
    pen = Pen()
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
        cv2.imshow('Canvas', img)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = hands.process(img2)
        if res.multi_hand_landmarks:
            pen.get_dist(res)
            if pen.dist < 0.065:
                pen.update_current_location(res)
                array = pen.coordinate_list[-1]
                finger_detected = False
            if finger_detected:
                pen.separate_plot()
            finger_detected = True
        else:
            if finger_detected:
                pen.separate_plot()
            finger_detected = False
        pen.draw(img)
        img = cv2.flip(img, 1)
        cv2.imshow('img', img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'):
            pen.clear_canvas()
        elif key == ord('1'):
            pen.colors = (0, 0, 255)
        elif key == ord('2'):
            pen.colors = (0, 165, 255)
        elif key == ord('3'):
            pen.colors = (0, 255, 255)
        elif key == ord('4'):
            pen.colors = (0, 255, 0)
        elif key == ord('5'):
            pen.colors = (255, 0, 0)
        elif key == ord('6'):
            pen.colors = (130, 0, 75)
        elif key == ord('7'):
            pen.colors = (238, 130, 238)
        elif key == ord('8'):
            pen.colors = (0,0,0)
        elif key == ord('9'):
            pen.colors = (255,255,255)
        elif key == ord('q'):
            print("INTERRUPT detected!!")
            break

except Exception as e:
    cap.release()
    cv2.destroyAllWindows()
    for i in range(1, 5):
        cv2.waitKey(1)
finally:
    cap.release()
    cv2.destroyAllWindows()
    for i in range(1, 5):
        cv2.waitKey(1)