from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, template_folder='./Web_Dashboard/templates/', static_folder='./Web_Dashboard/static')

# define images directory
IMAGE_FOLDER = './logs/motion_frames/'

# Route to serve the images
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

# home route
@app.route('/')
def index():
    # store images in an array to pass later
    image_files = [filename for filename in os.listdir(IMAGE_FOLDER) if filename.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    image_files = sorted(os.listdir(IMAGE_FOLDER), reverse=True) # make sure to show the latest images first
    
    # render HTML and pass images
    return render_template('index.html', image_files=image_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2425, debug=True)
