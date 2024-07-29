import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize drawing utils
mp_drawing = mp.solutions.drawing_utils

def dist(P1, P2):
    point1 = np.array([P1.x, P1.y, P1.z])
    point2 = np.array([P2.x, P2.y, P2.z])
    return np.sqrt(sum((point1 - point2)**2))

class Pen:
    def __init__(self):
        self.coordinate_list = []
        self.colors = (0, 0, 0)
        self.dist = 0
    def get_dist(self ,res):
        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:
                index = hand_landmarks.landmark[8]
                thumb = hand_landmarks.landmark[4]
                self.dist = dist(index, thumb)
    def update_current_location(self, results):
        finger = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index = hand_landmarks.landmark[8]
                thumb = hand_landmarks.landmark[4]
                finger = [index.x, index.y]
                self.dist = dist(index, thumb)
                
                self.coordinate_list.append([finger[0], finger[1]])
    
    def draw(self, img):
        if len(self.coordinate_list) != 0:
            color = self.colors
            thickness = 5
            for i in range(len(self.coordinate_list) - 1):
                start = self.coordinate_list[i]
                end = self.coordinate_list[i + 1]
                if start == [100000, 100000] or end == [100000, 100000]:
                    continue
                start_point = (int(start[0] * img.shape[1]), int(start[1] * img.shape[0]))
                end_point = (int(end[0] * img.shape[1]), int(end[1] * img.shape[0]))
                cv2.line(img, start_point, end_point, color, thickness)
    def clear_canvas(self):
        self.coordinate_list = []
    def separate_plot(self):
        self.coordinate_list.append([100000, 100000])
        