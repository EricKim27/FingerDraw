import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
version = 1.1
patches = "Now can change the color of the line without having to change the entire color!\nAlso now can Undo by pressing Z!"
color_map = {
    '1': ((0, 0, 255), "Red"),
    '2': ((0, 165, 255), "Orange"),
    '3': ((0, 255, 255), "Yellow"),
    '4': ((0, 255, 0), "Green"),
    '5': ((255, 0, 0), "Blue"),
    '6': ((130, 0, 75), "Purple"),
    '7': ((238, 130, 238), "Pink"),
    '8': ((0, 0, 0), "Black"),
    '9': ((255, 255, 255), "White")
}
ascii_art = """
    _______                       ____                     
   / ____(_)___  ____ ____  _____/ __ \_________ __      __
  / /_  / / __ \/ __ `/ _ \/ ___/ / / / ___/ __ `/ | /| / /
 / __/ / / / / / /_/ /  __/ /  / /_/ / /  / /_/ /| |/ |/ / 
/_/   /_/_/ /_/\__, /\___/_/  /_____/_/   \__,_/ |__/|__/  
              /____/                                       
"""

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
                
                self.coordinate_list.append([finger[0], finger[1], self.colors])
    
    def draw(self, img):
        if len(self.coordinate_list) != 0:
            thickness = 5
            for i in range(len(self.coordinate_list) - 1):
                start = self.coordinate_list[i]
                end = self.coordinate_list[i + 1]
                color = self.coordinate_list[i + 1][2]
                if start == [100000, 100000, color] or end == [100000, 100000, color]:
                    continue
                start_point = (int(start[0] * img.shape[1]), int(start[1] * img.shape[0]))
                end_point = (int(end[0] * img.shape[1]), int(end[1] * img.shape[0]))
                cv2.line(img, start_point, end_point, color, thickness)
    def clear_canvas(self):
        self.coordinate_list = []
        self.coordinate_list.append([123456, 123456, self.colors])
    def undo(self):
        if not self.coordinate_list:
            print("Coordinate list is empty. Nothing to undo.")
            return

        # Remove the last point
        self.coordinate_list.pop()

        # Continue removing points until we find the marker
        while self.coordinate_list and (self.coordinate_list[-1][0] != 100000 or self.coordinate_list[-1][1] != 100000):
            self.coordinate_list.pop()

    def separate_plot(self):
        self.coordinate_list.append([100000, 100000, self.colors])
        