import numpy as np
from body_part_angle import BodyPartAngle
from utils import *


class TypeOfExercise(BodyPartAngle):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    def push_up(self, counter, status):
        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_right_arm()
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2
        
        print(f"Push-up angles - Left: {left_arm_angle}, Right: {right_arm_angle}, Avg: {avg_arm_angle}")

        if status:
            if avg_arm_angle < 70:
                counter += 1
                status = False
                print("Push-up rep completed")
        else:
            if avg_arm_angle > 160:
                status = True
                print("Push-up position reset")

        return [counter, status]


    def pull_up(self, counter, status):
        nose = detection_body_part(self.landmarks, "NOSE")
        left_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        right_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        avg_shoulder_y = (left_elbow[1] + right_elbow[1]) / 2

        if status:
            if nose[1] > avg_shoulder_y:
                counter += 1
                status = False

        else:
            if nose[1] < avg_shoulder_y:
                status = True

        return [counter, status]

    def squat(self, counter, status):
        left_leg_angle = self.angle_of_the_left_leg()  
        right_leg_angle = self.angle_of_the_right_leg()  
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2

        if status:
            if avg_leg_angle < 70:
                counter += 1
                status = False
        else:
            if avg_leg_angle > 160:
                status = True

        return [counter, status]

    def walk(self, counter, status):
        right_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        left_knee = detection_body_part(self.landmarks, "LEFT_KNEE")

        if status:
            if left_knee[0] > right_knee[0]:
                counter += 1
                status = False

        else:
            if left_knee[0] < right_knee[0]:
                counter += 1
                status = True

        return [counter, status]

    def sit_up(self, counter, status):
        angle = self.angle_of_the_abdomen()
        if status:
            if angle < 55:
                counter += 1
                status = False
        else:
            if angle > 105:
                status = True

        return [counter, status]
    
    def bicep_curl(self, counter, status):
        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_right_arm()

        avg_arm_angle = (left_arm_angle + right_arm_angle) / 2


        if status:
            if avg_arm_angle > 160:
                status = False
                counter += 1
        else:
            if avg_arm_angle < 90:
                status = True

        return [counter, status]
    
    def shoulder_press(self, counter, status):
        # Get the coordinates of the left and right shoulders
        left_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        right_shoulder = detection_body_part(self.landmarks, "RIGHT_SHOULDER")
        
        # Midpoint of the shoulders
        shoulder_midpoint = [(left_shoulder[0] + right_shoulder[0]) / 2,
                            (left_shoulder[1] + right_shoulder[1]) / 2]
        
        # Get the angle between the shoulder midpoint and the elbows (adjust as necessary)
        left_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        right_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        
        # Calculate shoulder angle for both left and right arms
        left_shoulder_angle = calculate_angle(shoulder_midpoint, left_shoulder, left_elbow)
        right_shoulder_angle = calculate_angle(shoulder_midpoint, right_shoulder, right_elbow)
        
        # Use the average angle between both sides
        avg_shoulder_angle = (left_shoulder_angle + right_shoulder_angle) / 2

        
        if status:
            if avg_shoulder_angle < 100:  
                status = False
                counter += 1
        else:
            
            if avg_shoulder_angle > 170:  
                status = True

        return [counter, status]

    def calculate_exercise(self, exercise_type, counter, status):
        print(f"Calculating exercise: {exercise_type}, Current counter: {counter}, Status: {status}")
        
        if exercise_type == "push-up":
            counter, status = self.push_up(counter, status)
        elif exercise_type == "pull-up":
            counter, status = self.pull_up(counter, status)
        elif exercise_type in ["Barbell Squats", "Front Squats", "Bodyweight or Assisted Squats"]:
            counter, status = self.squat(counter, status)
        elif exercise_type == "Light Walk":
            counter, status = self.walk(counter, status)
        elif exercise_type == "Inclined Weighted Situps":
            counter, status = self.sit_up(counter, status)
        elif exercise_type == "Bicep Curls":
            counter, status = self.bicep_curl(counter, status)
        elif exercise_type == "Dumbbell Shoulder Press":
            counter, status = self.shoulder_press(counter, status)
        else:
            print(f"Unknown exercise type: {exercise_type}")
            
        print(f"After calculation - Counter: {counter}, Status: {status}")
        return [counter, status]
