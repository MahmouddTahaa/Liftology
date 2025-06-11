from flask import Flask, Response
import cv2
import mediapipe as mp
from types_of_exercise import TypeOfExercise
import numpy as np
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MotionTrackingService:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        
        # Global variables to track stats
        self.current_stats = {
            'reps': 0,
            'status': True,
            'form_score': 0
        }
        
        # Global variable for exercise type
        self.current_exercise_type = 'bicep-curl'  # Default exercise type

    def calculate_form_score(self, landmarks, exercise_type):
        # This is a placeholder - implement actual form scoring logic
        # based on exercise type and landmark positions
        return 85  # Example score

    def generate_frames(self, exercise_type):
        logger.debug(f"Starting video feed for exercise: {exercise_type}")
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                logger.error("Failed to open camera")
                return
                
            logger.debug("Camera opened successfully")
            cap.set(3, 800)  # width
            cap.set(4, 480)  # height
            
            with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        logger.error("Failed to read frame from camera")
                        break
                        
                    frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
                    
                    # Convert to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_rgb.flags.writeable = False
                    
                    # Make detection
                    results = pose.process(frame_rgb)
                    
                    # Convert back to BGR
                    frame_rgb.flags.writeable = True
                    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                    
                    try:
                        landmarks = results.pose_landmarks.landmark
                        self.current_stats['reps'], self.current_stats['status'] = TypeOfExercise(landmarks).calculate_exercise(
                            exercise_type, self.current_stats['reps'], self.current_stats['status']
                        )
                        self.current_stats['form_score'] = self.calculate_form_score(landmarks, exercise_type)
                    except Exception as e:
                        logger.error(f"Error in motion tracking: {str(e)}")
                        pass
                    
                    # Draw landmarks
                    self.mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                        self.mp_drawing.DrawingSpec(color=(174, 139, 45), thickness=2, circle_radius=2),
                    )
                    
                    # Convert frame to JPEG
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            logger.error(f"Error in generate_frames: {str(e)}")
        finally:
            if 'cap' in locals():
                cap.release()
                logger.debug("Camera released")

    def get_stats(self):
        return {
            'reps': self.current_stats['reps'],
            'form_score': self.current_stats['form_score'],
            'status': 'Up' if self.current_stats['status'] else 'Down',
            'exercise_type': self.current_exercise_type
        }

    def reset_stats(self):
        self.current_stats = {
            'reps': 0,
            'status': True,
            'form_score': 0
        }
        return {'status': 'success'}

    def set_exercise_type(self, exercise_type):
        self.current_exercise_type = exercise_type

# Create a singleton instance
motion_tracker = MotionTrackingService()

# Flask app for standalone service
app = Flask(__name__)

@app.route('/video_feed/<exercise_type>')
def video_feed(exercise_type):
    logger.debug(f"Video feed requested for exercise: {exercise_type}")
    motion_tracker.set_exercise_type(exercise_type)
    return Response(motion_tracker.generate_frames(exercise_type),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_stats')
def get_stats():
    return json.dumps(motion_tracker.get_stats())

@app.route('/reset_stats')
def reset_stats():
    return json.dumps(motion_tracker.reset_stats())

if __name__ == '__main__':
    app.run(debug=True, port=8001)  # Use a different port than server.py 