import threading
from flask import Flask, render_template, request, jsonify
from oven_watcher import OvenWatcher  # Import the OvenWatcher class

app = Flask(__name__)

# Create an instance of OvenWatcher
oven = Oven()
watcher = OvenWatcher(oven)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_cone_mode', methods=['POST'])
def start_cone_mode():
    watcher.activate_cone_mode()
    return jsonify({'message': 'Cone mode activated'})

@app.route('/stop_cone_mode', methods=['POST'])
def stop_cone_mode():
    watcher.deactivate_cone_mode()
    return jsonify({'message': 'Cone mode deactivated'})

if __name__ == '__main__':
    # Start the OvenWatcher thread
    watcher.start()

    # Start the Flask application
    app.run(debug=True)
