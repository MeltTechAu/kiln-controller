
import csv  # Ensure csv is imported

# oven_watcher.py
from cone import ConeModeController  # Importing ConeModeController from cone module

import threading
import logging
import json
import time
import datetime
from flask import Flask, request
from oven import Oven
from cone import ConeModeController  # Importing ConeModeController from cone module

log = logging.getLogger(__name__)

# Updated ConeModeController class



class OvenWatcher(threading.Thread):
    def init_heatwork_log(self):
        # Create the heatwork log file with headers if it doesn't exist
        try:
            with open(self.heatwork_log_file, 'x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Heatwork', 'Mode'])
        except FileExistsError:
            pass  # File already exists, no need to create

    def log_heatwork_data(self, heatwork, mode):
        # Log heatwork data to CSV with a timestamp and mode indicator
        with open(self.heatwork_log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.datetime.now(), heatwork, mode])

    def __init__(self,oven):
        self.last_profile = None
        self.last_log = []
        self.started = None
        self.recording = False
        self.observers = []
        threading.Thread.__init__(self)
        self.daemon = True
        self.oven = oven
        self.cone_mode = False
   #     self.cone_mode_controller = ConeModeController(oven)
   #     self.cone_mode_controller.deactivate_cone_mode()  # Ensure Cone Mode is initially deactivated
  #     Flask app for integrating with frontend
        self.flask_app = Flask(__name__)
        self.start()
  # Flask endpoint to receive cone mode activation from frontend
        @self.flask_app.route('/activate_cone', methods=['POST'])

        def flask_activate_cone():
            self.activate_cone_mode()
            return 'Cone mode activated'

        # Flask endpoint to receive cone mode deactivation from frontend
        @self.flask_app.route('/deactivate_cone', methods=['POST'])
        def flask_deactivate_cone():
            self.deactivate_cone_mode()
            return 'Cone mode deactivated'

    def monitor_kiln(self):
        # Monitor temperature and kiln behavior
        current_temp = self.oven.get_current_temperature()
        target_temp = self.oven.get_target_temperature()

        if self.cone_mode:
            # Implement cone mode logic, including gradual temperature reduction and heat work
            # Ensure that cone_mode parameters are used for control
            if current_temp <= (target_temp - 25):
                # Kiln has reached 25 degrees below target
                self.oven.perform_heat_work()  # Implement the heat work function
            elif current_temp <= target_temp:
                # Gradually reduce temperature by turning off heating elements
                self.oven.reduce_temperature()

    def activate_cone_mode(self):
        self.cone_mode = True

    def deactivate_cone_mode(self):
        self.cone_mode = False
    def activate_cone_mode(self, cone_type):
        if not self.cone_mode:
            cone_temp = self.get_cone_temperature(cone_type)
            if cone_temp is not None:
                self.cone_mode = True
                self.cone_target_temp = cone_temp
                log.info(f"Cone Mode activated for {cone_type}. Target temperature: {self.cone_target_temp}°C")
            else:
                log.error("Invalid cone type or temperature not available.")
        else:
            log.warning("Cone Mode is already active.")

    def start_flask_app(self):
        self.flask_app.run(debug=False, threaded=True)
    def deactivate_cone_mode(self):
        if self.cone_mode:
            self.cone_mode = False
            log.info("Cone Mode deactivated.")
        else:
            log.warning("Cone Mode is not currently active.")

    def get_cone_temperature(self, cone_type):
        # Define a mapping from cone types to target temperatures in °C
        cone_temperature_mapping = {
             "Cone 12": 1306,  # Adjust values as needed
            "Cone 11": 1294,  # Adjust values as needed
            "Cone 10": 1288,
            "Cone 9": 1260,  # Adjust values as needed
            "Cone 8": 1249,
            "Cone 7": 1239,  # Adjust values as needed
            "Cone 6": 1222,
            "Cone 5": 1186,  # Adjust values as needed
            "Cone 4": 1162,
            "Cone 3": 1152,  # Adjust values as needed
            "Cone 2": 1142,  # Adjust values as needed
            "Cone 1": 1137,
            "Cone 01": 1119,  # Adjust values as needed
            "Cone 02": 1102,
            "Cone 03": 1086,  # Adjust values as needed
            "Cone 04": 1063,
            "Cone 05": 1031,  # Adjust values as needed
            "Cone 06": 998,
            "Cone 07": 976,  # Adjust values as needed
            "Cone 08": 942,
            "Cone 09": 920,  # Adjust values as needed
            "Cone 010": 903,  # Adjust values as needed
            "Cone 011": 875,
            "Cone 012": 861,  # Adjust values as needed
            "Cone 013": 837,  # Adjust values as needed
            "Cone 014": 807,
            "Cone 015": 791,  # Adjust values as needed
            "Cone 016": 772,
            "Cone 017": 738,  # Adjust values as needed
            "Cone 018": 715,
            "Cone 019": 678,  # Adjust values as needed
            "Cone 020": 626,  # Adjust values as needed
            "Cone 021": 600,
            "Cone 022": 586,  # Adjust values as needed
            # Add more cone types and temperatures as required           
        }
        return cone_temperature_mapping.get(cone_type)

    # ... (other methods)

    def run(self):
        while True:
            oven_state = self.oven.get_state()
            # Check if Cone Mode is active and adjust kiln behavior accordingly
            if self.cone_mode:
                self.monitor_cone_mode()
            if self.cone_mode_controller.cone_mode_activated:
                self.cone_mode_controller.update_cone_mode()
            log.debug("Cone Mode is not active.")

            # ... (other monitoring logic)
            time.sleep(self.oven.time_step)



    def activate_cone_mode(self, cone_type):
        self.cone_mode_controller.activate_cone_mode(cone_type)

    def deactivate_cone_mode(self):
        self.cone_mode_controller.deactivate_cone_mode()

    def monitor_cone_mode(self):
        current_temp = self.oven.get_current_temperature()

        if current_temp >= self.cone_target_temp:
            # Kiln has reached or exceeded the target temperature
            self.oven.set_target_temperature(self.cone_target_temp)
            log.info("Cone Mode: Target temperature reached.")
        else:
            # Gradually increase temperature towards the target
            new_target_temp = min(current_temp + self.cone_temp_increase_rate, self.cone_target_temp)
            self.oven.set_target_temperature(new_target_temp)

# FIXME - need to save runs of schedules in near-real-time
# FIXME - this will enable re-start in case of power outage
# FIXME - re-start also requires safety start (pausing at the beginning
# until a temp is reached)
# FIXME - re-start requires a time setting in minutes.  if power has been
# out more than N minutes, don't restart
# FIXME - this should not be done in the Watcher, but in the Oven class

    def run(self):
        while True:
            oven_state = self.oven.get_state()
           
            # record state for any new clients that join
            if oven_state.get("state") == "RUNNING":
                self.last_log.append(oven_state)
            else:
                self.recording = False
            self.notify_all(oven_state)
            time.sleep(self.oven.time_step)
   
    def lastlog_subset(self,maxpts=50):
        '''send about maxpts from lastlog by skipping unwanted data'''
        totalpts = len(self.last_log)
        if (totalpts <= maxpts):
            return self.last_log
        every_nth = int(totalpts / (maxpts - 1))
        return self.last_log[::every_nth]

    def record(self, profile):
        self.last_profile = profile
        self.last_log = []
        self.started = datetime.datetime.now()
        self.recording = True
        #we just turned on, add first state for nice graph
        self.last_log.append(self.oven.get_state())

    def add_observer(self,observer):
        if self.last_profile:
            p = {
                "name": self.last_profile.name,
                "data": self.last_profile.data, 
                "type" : "profile"
            }
        else:
            p = None
        
        backlog = {
            'type': "backlog",
            'profile': p,
            'log': self.lastlog_subset(),
            #'started': self.started
        }
        print(backlog)
        backlog_json = json.dumps(backlog)
        try:
            print(backlog_json)
            observer.send(backlog_json)
        except:
            log.error("Could not send backlog to new observer")
        
        self.observers.append(observer)

    def notify_all(self,message):
        message_json = json.dumps(message)
        log.debug("sending to %d clients: %s"%(len(self.observers),message_json))
        for wsock in self.observers:
            if wsock:
                try:
                    wsock.send(message_json)
                except:
                    log.error("could not write to socket %s"%wsock)
                    self.observers.remove(wsock)
            else:
                self.observers.remove(wsock)


    def start_heatwork_logging(self):
        self.heatwork_file = open('lost_heatwork_log.csv', 'w', newline='')
        self.heatwork_writer = csv.writer(self.heatwork_file)
        self.heatwork_writer.writerow(['Time', 'Temp', 'Lost Heatwork Cone Number', 'Additional Info'])

    def stop_heatwork_logging(self):
        self.heatwork_file.close()

    def log_heatwork(self, cone_number, additional_info=''):
        self.heatwork_writer.writerow([datetime.datetime.now(), self.oven.get_current_temperature(), cone_number, additional_info])
        log.info(f"Heatwork data logged for cone {cone_number}")


