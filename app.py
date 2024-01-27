# app.py
from flask import Flask, render_template, request, jsonify
from oven import Oven, OvenWatcher

app = Flask(__name)
oven = Oven()

@app.route('/')
def index():
    return render_template('index.html')

# Update the routes in app.py
@app.route('/activate_cone', methods=['POST'])
def activate_cone():
    oven_watcher = oven.get_watcher()
    oven_watcher.activate_cone_mode()
    toggleConeLight(True)  # Turn on the light
    return jsonify({'status': 'Cone mode activated'})

@app.route('/deactivate_cone', methods=['POST'])
def deactivate_cone():
    oven_watcher = oven.get_watcher()
    oven_watcher.deactivate_cone_mode()
    toggleConeLight(False)  # Turn off the light
    return jsonify({'status': 'Cone mode deactivated'})


if __name__ == '__main__':
    app.run(debug=True)


@route('/activate_cone_mode', method='POST')
def activate_cone_mode():
    cone_number = request.json.get('cone_number')
    oven.cone_mode.activate_cone_mode(cone_number)
    return {'status': 'Cone mode activated'}

@route('/deactivate_cone_mode', method='POST')
def deactivate_cone_mode():
    oven.cone_mode.deactivate_cone_mode()
    return {'status': 'Cone mode deactivated'}
