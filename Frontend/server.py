from flask import Flask, render_template, send_from_directory, Response, request
import os
import logging
from motion_tracking_service import motion_tracker

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
            static_folder='.',
            template_folder='templates')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

@app.route('/templates/<path:path>')
def serve_template(path):
    return send_from_directory('templates', path)

@app.route('/video_feed/<exercise_type>')
def video_feed(exercise_type):
    logger.debug(f"Video feed requested for exercise: {exercise_type}")
    motion_tracker.set_exercise_type(exercise_type)
    return Response(motion_tracker.generate_frames(exercise_type),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_stats')
def get_stats():
    return motion_tracker.get_stats()

@app.route('/reset_stats')
def reset_stats():
    return motion_tracker.reset_stats()

if __name__ == '__main__':
    logger.info("Starting server")
    app.run(debug=True, port=8000) 