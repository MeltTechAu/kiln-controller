#!/usr/bin/env python
#from oven_watcher import ConeModeController
import os
import sys
import logging
import json

import bottle
import gevent
import geventwebsocket
#from bottle import post, get
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket import WebSocketError

try:
    sys.dont_write_bytecode = True
    import config
    sys.dont_write_bytecode = False
except:
    print ("Could not import config file.")
    print ("Copy config.py.EXAMPLE to config.py and adapt it for your setup.")
    exit(1)

logging.basicConfig(level=config.log_level, format=config.log_format)
log = logging.getLogger("kiln-controller")
log.info("Starting kiln controller")

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_dir + '/lib/')
profile_path = config.kiln_profiles_directory

from oven import SimulatedOven, RealOven, Profile
from ovenWatcher import OvenWatcher

app = bottle.Bottle()

if config.simulate == True:
    log.info("this is a simulation")
    oven = SimulatedOven()
else:
    log.info("this is a real kiln")
    oven = RealOven()
ovenWatcher = OvenWatcher(oven)
# this ovenwatcher is used in the oven class for restarts
oven.set_ovenwatcher(ovenWatcher)

# Instantiating the ConeModeController
#cone_mode_controller = ConeModeController()
@app.route('/api/cone-mode', method='POST')
def set_cone_mode():
    data = bottle.request.json
    if data['activate']:
        ovenWatcher.activate_cone_mode()
    else:
        ovenWatcher.deactivate_cone_mode()
    return {"success": True}


@app.route('/')
def index():
    return bottle.redirect('/picoreflow/index.html')

@app.get('/api/stats')
def handle_api():
    log.info("/api/stats command received")
    if hasattr(oven,'pid'):
        if hasattr(oven.pid,'pidstats'):
            return json.dumps(oven.pid.pidstats)


@app.post('/api')
def handle_api():
    log.info("/api is alive")


    # run a kiln schedule
    if bottle.request.json['cmd'] == 'run':
        wanted = bottle.request.json['profile']
        log.info('api requested run of profile = %s' % wanted)

        # start at a specific minute in the schedule
        # for restarting and skipping over early parts of a schedule
        startat = 0;      
        if 'startat' in bottle.request.json:
            startat = bottle.request.json['startat']

        # get the wanted profile/kiln schedule
        profile = find_profile(wanted)
        if profile is None:
            return { "success" : False, "error" : "profile %s not found" % wanted }

        # FIXME juggling of json should happen in the Profile class
        profile_json = json.dumps(profile)
        profile = Profile(profile_json)
        oven.run_profile(profile,startat=startat)
        ovenWatcher.record(profile)

    if bottle.request.json['cmd'] == 'stop':
        log.info("api stop command received")
        oven.abort_run()

    if bottle.request.json['cmd'] == 'memo':
        log.info("api memo command received")
        memo = bottle.request.json['memo']
        log.info("memo=%s" % (memo))

    # get stats during a run
    if bottle.request.json['cmd'] == 'stats':
        log.info("api stats command received")
        if hasattr(oven,'pid'):
            if hasattr(oven.pid,'pidstats'):
                return json.dumps(oven.pid.pidstats)

    return { "success" : True }

def find_profile(wanted):
    '''
    given a wanted profile name, find it and return the parsed
    json profile object or None.
    '''
    #load all profiles from disk
    profiles = get_profiles()
    json_profiles = json.loads(profiles)

    # find the wanted profile
    for profile in json_profiles:
        if profile['name'] == wanted:
            return profile
    return None

@app.route('/picoreflow/:filename#.*#')
def send_static(filename):
    log.debug("serving %s" % filename)
    return bottle.static_file(filename, root=os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "public"))


def get_websocket_from_request():
    env = bottle.request.environ
    wsock = env.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    return wsock


@app.route('/control')
def handle_control():
    wsock = get_websocket_from_request()
    log.info("websocket (control) opened")
    while True:
        try:
            message = wsock.receive()
            if message:
                log.info("Received (control): %s" % message)
                msgdict = json.loads(message)
                if msgdict.get("cmd") == "RUN":
                    log.info("RUN command received")
                    profile_obj = msgdict.get('profile')
                    if profile_obj:
                        profile_json = json.dumps(profile_obj)
                        profile = Profile(profile_json)
                    oven.run_profile(profile)
                    ovenWatcher.record(profile)
                elif msgdict.get("cmd") == "SIMULATE":
                    log.info("SIMULATE command received")
                    #profile_obj = msgdict.get('profile')
                    #if profile_obj:
                    #    profile_json = json.dumps(profile_obj)
                    #    profile = Profile(profile_json)
                    #simulated_oven = Oven(simulate=True, time_step=0.05)
                    #simulation_watcher = OvenWatcher(simulated_oven)
                    #simulation_watcher.add_observer(wsock)
                    #simulated_oven.run_profile(profile)
                    #simulation_watcher.record(profile)
                elif msgdict.get("cmd") == "STOP":
                    log.info("Stop command received")
                    oven.abort_run()
        except WebSocketError as e:
            log.error(e)
            break
    log.info("websocket (control) closed")


@app.route('/storage')
def handle_storage():
    wsock = get_websocket_from_request()
    log.info("websocket (storage) opened")
    while True:
        try:
            message = wsock.receive()
            if not message:
                break
            log.debug("websocket (storage) received: %s" % message)

            try:
                msgdict = json.loads(message)
            except:
                msgdict = {}

            if message == "GET":
                log.info("GET command received")
                wsock.send(get_profiles())
            elif msgdict.get("cmd") == "DELETE":
                log.info("DELETE command received")
                profile_obj = msgdict.get('profile')
                if delete_profile(profile_obj):
                  msgdict["resp"] = "OK"
                wsock.send(json.dumps(msgdict))
                #wsock.send(get_profiles())
            elif msgdict.get("cmd") == "PUT":
                log.info("PUT command received")
                profile_obj = msgdict.get('profile')
                #force = msgdict.get('force', False)
                force = True
                if profile_obj:
                    #del msgdict["cmd"]
                    if save_profile(profile_obj, force):
                        msgdict["resp"] = "OK"
                    else:
                        msgdict["resp"] = "FAIL"
                    log.debug("websocket (storage) sent: %s" % message)

                    wsock.send(json.dumps(msgdict))
                    wsock.send(get_profiles())
        except WebSocketError:
            break
    log.info("websocket (storage) closed")


@app.route('/config')
def handle_config():
    wsock = get_websocket_from_request()
    log.info("websocket (config) opened")
    while True:
        try:
            message = wsock.receive()
            wsock.send(get_config())
        except WebSocketError:
            break
    log.info("websocket (config) closed")


@app.route('/status')
def handle_status():
    wsock = get_websocket_from_request()
    ovenWatcher.add_observer(wsock)
    log.info("websocket (status) opened")
    while True:
        try:
            message = wsock.receive()
            wsock.send("Your message was: %r" % message)
        except WebSocketError:
            break
    log.info("websocket (status) closed")


def get_profiles():
    try:
        profile_files = os.listdir(profile_path)
    except:
        profile_files = []
    profiles = []
    for filename in profile_files:
        with open(os.path.join(profile_path, filename), 'r') as f:
            profiles.append(json.load(f))
    return json.dumps(profiles)


def save_profile(profile, force=False):
    profile_json = json.dumps(profile)
    filename = profile['name']+".json"
    filepath = os.path.join(profile_path, filename)
    if not force and os.path.exists(filepath):
        log.error("Could not write, %s already exists" % filepath)
        return False
    with open(filepath, 'w+') as f:
        f.write(profile_json)
        f.close()
    log.info("Wrote %s" % filepath)
    return True

def delete_profile(profile):
    profile_json = json.dumps(profile)
    filename = profile['name']+".json"
    filepath = os.path.join(profile_path, filename)
    os.remove(filepath)
    log.info("Deleted %s" % filepath)
    return True


def get_config():
    return json.dumps({"temp_scale": config.temp_scale,
        "time_scale_slope": config.time_scale_slope,
        "time_scale_profile": config.time_scale_profile,
        "kwh_rate": config.kwh_rate,
        "currency_type": config.currency_type})    


def main():
    ip = "0.0.0.0"
    port = config.listening_port
    log.info("listening on %s:%d" % (ip, port))

    server = WSGIServer((ip, port), app,
                        handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()


@post('/activate_cone')
def activate_cone():
    oven_watcher = oven.get_watcher()
    oven_watcher.activate_cone_mode()
    toggleConeLight(True)  # Ensure this function is defined or imported
    response.content_type = 'application/json'
    return jsonify({'status': 'Cone mode activated'})


@post('/start_cone_mode')
def start_cone_mode():
    watcher.activate_cone_mode()
    response.content_type = 'application/json'
    return jsonify({'message': 'Cone mode activated'})

# Additions for cone mode API endpoints

@app.route('/api/cone-mode/activate', method='POST')
def activate_cone_mode():
    cone_profile = request.json.get('cone_profile')
    ovenWatcher.activate_cone_mode(cone_profile)
    return {"success": True, "message": "Cone mode activated."}

@app.route('/api/cone-mode/deactivate', method='POST')
def deactivate_cone_mode():
    ovenWatcher.deactivate_cone_mode()
    return {"success": True, "message": "Cone mode deactivated."}

@post('/activate_cone')
def activate_cone():
    oven_watcher = oven.get_watcher()
    oven_watcher.activate_cone_mode()
    toggleConeLight(True)  # Ensure this function is defined or imported
    response.contlent_type = 'application/json'
    return jsonify({'status': 'Cone mode activated'})


@post('/start_cone_mode')
def start_cone_mode():
    watcher.activate_cone_mode()
    response.content_type = 'application/json'
    return jsonify({'message': 'Cone mode activated'})


# Enhanced Cone Mode Implementation
class ConeMode:
    def __init__(self, target_profile):
        self.target_profile = target_profile
        self.current_temp = 0
        self.target_temp = self.target_profile[0]  # Starting with the first temperature in the profile

    def update_temperature(self, new_temp):
        self.current_temp = new_temp
        # Logic to adjust kiln temperature based on profile

    def check_safety(self):
        # Implement safety checks
        if self.current_temp > some_safe_limit:
            self.shutdown()

    def shutdown(self):
        # Logic to safely shut down the kiln
        pass

# Note: This is a simplified representation. Actual implementation will depend on specific project requirements.

class TimerControl:
    def __init__(self):
        self.timer = 0

    def set_timer(self, time_in_seconds):
        self.timer = time_in_seconds

    def extend_timer(self, additional_time):
        self.timer += additional_time
        # Additional logic to handle extended time

class ConeModeControl:
    def __init__(self):
        self.active = False

    def activate_cone_mode(self):
        self.active = True
        # Logic to activate Cone Mode, set temperature profiles, etc.

    def deactivate_cone_mode(self):
        self.active = False
        # Logic to deactivate Cone Mode


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


# Timer mechanism
import threading
import time

class KilnTimer:
    def __init__(self):
        self.remaining_time = 0
        self.timer_thread = None
        self.timer_active = False

    def start_timer(self, duration):
        self.remaining_time = duration
        self.timer_thread = threading.Thread(target=self.countdown)
        self.timer_thread.start()
        self.timer_active = True

    def countdown(self):
        while self.remaining_time > 0:
            time.sleep(1)
            self.remaining_time -= 1
            if self.remaining_time == 60:  # One minute left
                # Trigger cone mode activation
                set_cone_mode('cone')

    def stop_timer(self):
        self.remaining_time = 0
        self.timer_active = False
        if self.timer_thread:
            self.timer_thread.join()

# Creating a timer instance
kiln_timer = KilnTimer()


from oven_watcher import ConeModeController

# Creating an instance of ConeModeController
cone_mode_controller = ConeModeController()

# Example of integrating ConeModeController methods
def initiate_cone_mode():
    additional_time = cone_mode_controller.calculate_additional_time()
    cone_mode_controller.set_cone_mode(additional_time)

# Assuming there are conditions or triggers in the code that call initiate_cone_mode

class KilnController:
    def __init__(self, oven_watcher):
        # Initialize the kiln controller
        self.current_mode = None
        self.oven_watcher = oven_watcher

    def set_cone_mode(self, selected_cone):
        # Use the existing OvenWatcher's method to get the target temperature for the selected cone
        target_temperature = self.oven_watcher.get_target_temperature_for_cone(selected_cone)
        if target_temperature == 0:
            print(f"Invalid cone mode: {selected_cone}")
            return

        # Set the kiln to the specified cone mode
        self.current_mode = selected_cone
        # Assuming there is a method to set the kiln's temperature
        # self.kiln.set_temperature(target_temperature)
        print(f"Setting kiln to cone mode: {selected_cone} at {target_temperature} degrees")

