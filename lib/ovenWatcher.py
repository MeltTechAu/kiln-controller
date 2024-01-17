
from oven import Oven

class OvenController:
    def __init__(self, oven):
        self.oven = oven

    def start_profile_schedule(self):
        self.oven.set_target_temperature(200)  # Example target temperature
        self.oven.start_heating()

    def run_oven_cycle(self):
        while not self.oven.reached_target_temperature():
            time.sleep(1)  # Wait for the oven to reach the target temperature
            self.oven.check_and_adjust_heating()

    def pause(self):
        self.oven.stop_heating()
        self.oven.save_current_state()

# Other existing code in oven_watcher.py...
from config import CONE_MODE_ADJUSTMENT
# oven_watcher.py
import threading
import logging
import json
import time
import datetime
from bottle import route, request, run
from oven import Oven

log = logging.getLogger(__name__)
# Updated ConeModeController class
    

"""Starts a countdown for the given duration (in seconds)."""
def countdown(duration):
    remaining = duration
    while remaining > 0:
        print(f'Time remaining: {remaining} seconds')
        time.sleep(1)
        remaining -= 1
        print('Countdown finished!')

    countdown_thread = threading.Thread(target=countdown, args=(duration,))
    countdown_thread.start()






class ConeModeController:

    def set_cone_mode(self, additional_time):
        # Logic to set the cone mode
        additional_time_calculated = self.calculate_additional_time()
        self.activate_cone_mode(additional_time_calculated)
        log.info(f'Cone mode activated with additional time {additional_time_calculated}')

    
    def calculate_additional_time(self):
        # Hypothetical logic for calculating additional time
        # This might involve factors like current temperature, target temperature, remaining time in the profile, etc.

        # Example: Calculate additional time based on the difference between current and target temperatures
        current_temp = self.get_current_temperature()  # Assuming this method exists and returns the current temperature
        target_temp = self.get_target_temperature()    # Assuming this method exists and returns the target temperature

        # Example logic: additional time increases as the difference between current and target temperatures increases
        temp_difference = target_temp - current_temp
        additional_time = temp_difference * 0.5  # Hypothetical conversion factor

        return additional_time

    def activate_cone_mode(self, additional_time):
        try:
            # Check if the oven is ready for cone mode
            if not self.oven.is_ready_for_mode_change():
                log.error("Oven is not ready for mode change.")
                return False

            # Activate cone mode
            self.cone_mode_active = True
            self.oven.set_mode('cone')
            self.oven.adjust_temperature(self.cone_target_temp + additional_time)
            log.info(f"Cone mode activated with target temperature: {self.cone_target_temp + additional_time}")

            return True
        except Exception as e:
            log.error(f"Error activating cone mode: {e}")
            return False

    
    def log_lost_heatwork(self, data):
        # Logic to log lost heatwork in a CSV file
        with open('lost_heatwork.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        with open('lost_heatwork.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        # Implement logic to call this method every 14 seconds
# class attributes...
            a = 0.5  # Example value for a
            b = 1.0  # Example value for b
            c = 2.0  # Example value for c             lost_heatwork = float(last_row[2])
                 
        # Complex calculation based on lost heatwork
            a = CONE_MODE_ADJUSTMENT['a']
            b = CONE_MODE_ADJUSTMENT['b']
            c = CONE_MODE_ADJUSTMENT['c']

        # Non-linear relationship for additional time calculation
            additional_time = c + a * lost_heatwork**2 + b * lost_heatwork

        # Maximum cap for the additional time
            max_additional_time = 180  # Maximum of 180 minutes
            additional_time = min(additional_time, max_additional_time)

            return additional_time

                
        # Implementing the complex calculation based on lost heatwork
            a = CONE_MODE_ADJUSTMENT['a']  # Coefficient for heatwork's quadratic term
            b = CONE_MODE_ADJUSTMENT['b']  # Coefficient for heatwork's linear term
            c = CONE_MODE_ADJUSTMENT['c']  # Base additional time in minutes
            drop_rate = CONE_MODE_ADJUSTMENT['drop_rate']
            max_duration = CONE_MODE_ADJUSTMENT['max_duration']

        # Non-linear relationship for additional time calculation
            calculated_time = c + a * lost_heatwork**2 + b * lost_heatwork
            calculated_time *= drop_rate  # Adjusting time based on the drop rate

        # Ensuring the calculated time does not exceed the maximum
            additional_time = min(calculated_time, max_duration)
            return additional_time
        try:

            additional_time = self.calculate_additional_time(lost_heatwork)
            return additional_time
        except Exception as e:
            log.error(f'Error reading CSV file for timer extension: {e}')
            return default_additional_time

    def log_temperature_and_heatwork_to_csv(self, temperature, lost_heatwork):
        # Log the temperature and lost heatwork to a CSV file
        filename = datetime.now().strftime('heatwork_log_%Y-%m-%d.csv')
        with open(filename, "a") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now(), temperature, lost_heatwork])
    def retrieve_latest_heatwork_data(self):
        try:
            latest_csv = max(glob.glob("heatwork_log_*.csv"), key=os.path.getctime)
            with open(latest_csv, "r") as file:
                last_row = list(csv.reader(file))[-1]
                return float(last_row[2])
        except Exception as e:
            logging.error(f"Error retrieving heatwork data: {e}")
            return None
        return target_temp - current_temp  # Simplified example
        # Simple model: Additional Time = Lost Heatwork / Target Temperature
        # Calculate the additional time required to achieve the lost heatwork at target temperature
        if target_temp > 0:
            return lost_heatwork / target_temp
        else:
            return 0  # Avoid division by zero
        # This function should return additional time in seconds
    def __init__(self, oven):
        self.oven = oven
        self.cone_mode_activated = False
        self.cone_target_temp = None
        self.cone_drop_rate = 3  # 3% of the max temperature in °C
        self.cone_max_temp = None
        self.cone_start_time = None
        self.cone_heat_work_done = False
        self.cone_duration = 0  # Initialize the duration to 0 seconds
        self.cone_max_duration = 1800  # Maximum duration in seconds (e.g., 30 minutes)
        if not self.cone_mode_activated:
            self.cone_target_temp = self.get_target_temperature_for_cone(cone_type)
            self.cone_max_temp = self.oven.get_max_temperature()
            self.cone_mode_activated = True
            self.cone_start_time = time.time()
            self.oven.set_target_temperature(self.cone_target_temp)
    def deactivate_cone_mode(self):
        if self.cone_mode_activated:
            self.oven.set_target_temperature(0)  # Turn off the kiln
            self.cone_duration = 0  # Reset the duration
    def update_cone_mode(self):
            current_temp = self.oven.get_current_temperature()
            target_temp = self.cone_target_temp
            elapsed_time = time.time() - self.cone_start_time
            lost_heatwork = self.calculate_lost_heatwork(current_temp, target_temp, elapsed_time)
            additional_time = self.calculate_additional_time(lost_heatwork, target_temp)
            # Log the additional time calculation
            logging.info(f"Additional time calculated for lost heatwork: {additional_time} seconds")
            # Existing logic to update the cone mode
            # ...
            lost_heatwork = self.calculate_lost_heatwork(current_temp, target_temp)
            if current_temp >= self.cone_max_temp:
                # Kiln has reached or exceeded the maximum temperature
                self.cone_heat_work_done = True
                self.oven.set_target_temperature(current_temp)
            elif not self.cone_heat_work_done:
                # Continue heating at the maximum temperature until heat work is done
                self.oven.set_target_temperature(self.cone_max_temp)
                # Gradually reduce temperature by the drop rate
                new_target_temp = max(current_temp - self.cone_drop_rate, 0)
                self.oven.set_target_temperature(new_target_temp)
            # Update the Cone Mode duration
            self.update_duration()
    def update_duration(self):
            current_time = time.time()
            self.cone_duration = int(current_time - self.cone_start_time)
            # Check if the maximum duration has been reached
            if self.cone_duration >= self.cone_max_duration:
                # Automatically deactivate Cone Mode when the maximum duration is reached
                self.deactivate_cone_mode()
    def get_target_temperature_for_cone(self, cone_type):
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
        return cone_temperature_mapping.get(cone_type, 0)
class OvenWatcher(threading.Thread):
        self.last_profile = None
        self.last_log = []
        self.started = None
        self.recording = False
        self.observers = []
        threading.Thread.__init__(self)
        self.daemon = True
        self.cone_mode = False
        self.cone_mode_controller = ConeModeController(oven)
        self.cone_mode_controller.deactivate_cone_mode()  # Ensure Cone Mode is initially deactivated
  #     Flask app for integrating with frontend
        self.flask_app = Bottle()
        self.start()
  # Flask endpoint to receive cone mode activation from frontend
        @self.flask_app.route('/activate_cone', methods=['POST'])
        def flask_activate_cone():
            self.activate_cone_mode()
            return 'Cone mode activated'
        # Flask endpoint to receive cone mode deactivation from frontend
        @self.flask_app.route('/deactivate_cone', methods=['POST'])
        def flask_deactivate_cone():
            return 'Cone mode deactivated'
        # Monitor temperature and kiln behavior
def monitor_kiln(self):
        if self.cone_mode:
            # Implement cone mode logic, including gradual temperature reduction and heat work
            # Ensure that cone_mode parameters are used for control
            if current_temp <= (target_temp - 25):
                # Kiln has reached 25 degrees below target
                self.oven.perform_heat_work()  # Implement the heat work function
            elif current_temp <= target_temp:
                # Gradually reduce temperature by turning off heating elements
                self.oven.reduce_temperature()
        self.cone_mode = True
        if not self.cone_mode:
            cone_temp = self.get_cone_temperature(cone_type)
            if cone_temp is not None:
                self.cone_target_temp = cone_temp
                log.info(f"Cone Mode activated for {cone_type}. Target temperature: {self.cone_target_temp}°C")
                log.error("Invalid cone type or temperature not available.")
        log.warning("Cone Mode is already active.")
def start_flask_app(self):
    self.flask_run(debug=False, threaded=True)
    log.info("Cone Mode deactivated.")
    def get_cone_temperature(self, cone_type):
        return cone_temperature_mapping.get(cone_type)
    # ... (other methods)
    def run(self):
        while True:
            # Existing logic of the main loop...
            # Call to monitor and activate cone mode
            cone_mode_controller.monitor_and_activate_cone_mode()
    # Rest of the main loop logic...
            oven_state = self.oven.get_state()
            # Check if Cone Mode is active and adjust kiln behavior accordingly
            self.monitor_cone_mode()
            if self.cone_mode_controller.cone_mode_activated:
                self.cone_mode_controller.update_cone_mode()
            log.debug("Cone Mode is not active.")
            # ... (other monitoring logic)
            time.sleep(self.oven.time_step)
        self.cone_mode_controller.activate_cone_mode(cone_type)
        self.cone_mode_controller.deactivate_cone_mode()
    def monitor_cone_mode(self):
        if current_temp >= self.cone_target_temp:
            # Kiln has reached or exceeded the target temperature
            log.info("Cone Mode: Target temperature reached.")
            # Gradually increase temperature towards the target
            new_target_temp = min(current_temp + self.cone_temp_increase_rate, self.cone_target_temp)
# FIXME - need to save runs of schedules in near-real-time
# FIXME - this will enable re-start in case of power outage
# FIXME - re-start also requires safety start (pausing at the beginning
# until a temp is reached)
# FIXME - re-start requires a time setting in minutes.  if power has been
# out more than N minutes, don't restart
# FIXME - this should not be done in the Watcher, but in the Oven class
            # record state for any new clients that join
            if oven_state.get("state") == "RUNNING":
                self.last_log.append(oven_state)
            self.notify_all(oven_state)
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
                    wsock.send(message_json)
                    log.error("could not write to socket %s"%wsock)
                    self.observers.remove(wsock)
    # Additional methods for automatic cone mode activation in countdown
    def check_timer_and_activate_cone_mode(self):
        self.activate_cone_mode(self.current_cone_profile)
        # Implement logic to check if the timer has only 1 minute remaining
        return self.remaining_time <= 60  # Assuming remaining_time is in seconds
    def perform_safety_checks(self):
    # Checks for over-temperature and other safety concerns
        if self.get_current_temperature() > self.max_safe_temperature:
            self.trigger_emergency_shutdown()
    def optimize_energy_usage(self):
    # Adjust heating elements based on real-time temperature data for efficiency
        desired_temp = self.calculate_optimal_temperature()
        self.adjust_heating_elements(desired_temp)
    def check_maintenance_needs(self):
    # Predictive alerts based on usage patterns and operational data
        if self.needs_maintenance():
            self.notify_maintenance_department()
    def send_status_update(self):
    # Send notifications about the status, especially for long operations
        self.notify_users("Current status: " + self.get_operation_status())
    def log_operational_data(self):
    # Enhanced data logging for analysis
        self.data_logger.log(self.collect_operational_data())
# Placeholder for remote monitoring and control features
    def create_or_modify_profile(self, profile_data):
    # Allow users to create or modify operational profiles
        self.profile_manager.save_profile(profile_data)
    # Logic to activate cone mode based on specific oven conditions
        if self.check_conditions_for_cone_mode(profile):
            self.adjust_settings_for_cone_mode()
            self.log_cone_mode_activation()
    def handle_end_of_profile(self):
    # Actions to perform at the end of a profile
        self.initiate_cooldown_procedure()
        self.log_profile_completion()
        self.send_end_of_profile_notification()
def check_conditions_for_cone_mode(self, profile):
    # Check specific safety and efficiency conditions for cone mode
    return self.is_temperature_within_range(profile) and not self.is_any_safety_alert_active()
def log_cone_mode_activation(self):
    # Log detailed information during cone mode for analysis
    self.data_logger.log({"event": "cone_mode_activated", "timestamp": self.get_current_time()})
def create_or_modify_cone_mode_profile(self, profile_data):
    # Allow users to create or modify cone mode profiles
    self.cone_mode_profile_manager.save_profile(profile_data)
    def estimate_lost_heatwork(self):
    # Fallback mechanism to estimate lost heatwork when log file can't be read
        # Attempt to read from the lost heatwork log file
        return self.read_from_heatwork_log()
#####?????except IOError:
        # Fallback estimation if log file is inaccessible
        return self.calculate_heatwork_from_temp_and_time()
def read_from_heatwork_log(self):
        """Reads the last entry from the lost heatwork log file.Returns the heatwork value from the last entry."""
        with open('heatwork_log.csv', 'r') as file:
            last_line = file.readlines()[-1]
            heatwork = float(last_line.split(',')[1])  # Assuming heatwork is in the second column
        return heatwork
        log.error(f"Error reading heatwork log: {e}")
    # Logic to read the last entry from the lost heatwork log file
        """heatwork entry from the specified log file.Assumes heatwork is in the second column."""
        try:
            with open(log_filename, 'r') as file:
                last_line = list(csv.reader(file))[-1]
                return float(last_line[1])  # Second column for heatwork
        except Exception as e:
            log.error(f'Error reading heatwork log: {e}')
            return None  # Or handle the error as needed
        pause_mode = PauseMode(oven)

class Oven:
    # ... existing methods and attributes

 #   def start_profile_schedule(self):
        # Realistic logic to start the profile schedule
        # ...

 #   def run_oven_cycle(self):
        # Realistic logic for running the oven cycle
        # ...


    def calculate_heatwork_from_temp_and_time(self):
        """ Estimates heatwork based on temperature and time.
        This is a placeholder logic and should be replacedwith an actual calculation."""
    elapsed_time = time.time() - self.cone_start_time  # Assuming cone_start_time is the start time
    estimated_heatwork = current_temp * elapsed_time * 0.1  # Example formula
    return estimated_heatwork
    """Estimation logic based on temperature, time, and existing mappings
        Estimates heatwork based on temperature and time.
        This is an example logic using a basic formula."""
    current_temp = self.get_current_temperature()  # Assuming this method exists to get current temperature
    elapsed_time = time.time() - self.cone_start_time  # Time since cone mode started
    estimated_heatwork = current_temp * elapsed_time * 0.1  # Example formula
    return estimated_heatwork

    def adjust_temperature_gradually(self, target_temp):
        """
        Gradually increase the temperature to the target for cone mode.
        """
        while self.get_current_temperature() < target_temp:
            self.increase_temperature_step()  # Assuming this method increases the temperature by a step
            time.sleep(self.temperature_increase_interval)  # Wait for the specified interval

    def decrease_temperature_gradually(self, target_temp):
        """
        Gradually decrease the temperature to the target.
        """
        while self.get_current_temperature() > target_temp:
            self.decrease_temperature_step()  # Assuming this method decreases the temperature by a step
            time.sleep(self.temperature_decrease_interval)  # Wait for the specified interval

    # Gradually increase the temperature to the target for cone mode
    while self.get_current_temperature() < target_temp:
        self.increase_temperature_step()
        time.sleep(self.temperature_increase_interval)
    # Gradually decrease the temperature to the target
    while self.get_current_temperature() > target_temp:
        self.decrease_temperature_step()
        time.sleep(self.temperature_decrease_interval)
    # Error handling for file reading
        # Assuming heatwork is the second value in the CSV
        return float(last_line.split(',')[1])
        log.error('Error reading heatwork log: {}'.format(e))
        return float(last_line.split(',')[1])  # Assuming heatwork is the second value in the CSV
    elapsed_time = self.get_elapsed_time()  # Assuming a method to get elapsed time exists
    # Simple estimation formula; replace with actual logic as needed
    estimated_heatwork = current_temp * elapsed_time
    return lost_heatwork * 10  # Simplified example
    # Placeholder for file reading logic
    # Placeholder for estimation logic
        # Preventing overshooting the target temperature
    if self.get_current_temperature() >= target_temp:
            break
    if self.get_current_temperature() <= target_temp:

        @route('/extend-timer', methods=['POST'])
        def extend_timer():
            additional_time = request.json.get('time')
            kiln_controller.timer_control.extend_timer(additional_time)
            return jsonify({'status': 'Timer extended'})



import logging

class OvenWatcher:
    # Assuming other initialization and methods already exist

        logging.info("Attempting to activate cone mode...")

        # Check current mode of the oven
        if self.oven.get_mode() == 'cone':
            logging.info("Cone mode is already active.")
            return

        # Validate cone target temperature
        if not self.is_valid_temperature(self.cone_target_temp):
            logging.error(f"Invalid cone target temperature: {self.cone_target_temp}")
            # Set to a default value or handle the error as required
            return

        # Try to set the oven to cone mode
        try:
            self.oven.set_mode('cone')
        except Exception as e:
            logging.error(f"Failed to set oven mode to cone: {e}")
            return

        # Confirm mode change
        if self.oven.get_mode() != 'cone':
            logging.error("Failed to change to cone mode.")
            return

        # Adjust temperature gradually to the target temperature
        try:
            self.oven.adjust_temperature_gradually(self.cone_target_temp)
        except Exception as e:
            logging.error(f"Failed to adjust temperature: {e}")
            return

        # Verify if the temperature reaches and stabilizes at the target temperature
        if not self.is_temperature_stabilized(self.cone_target_temp):
            logging.warning("Temperature not stabilized at target value for cone mode.")

        self.cone_mode_active = True
        logging.info(f"Cone mode activated with target temperature: {self.cone_target_temp}")

        def is_valid_temperature(self, temp):
        # Placeholder for temperature validation logic
        # Example: check if the temperature is within an acceptable range
            min_temp, max_temp = 100, 500  # Example range, adjust as needed
            return min_temp <= temp <= max_temp

        def is_temperature_stabilized(self, target_temp):
        # Placeholder for checking temperature stabilization
        # This might involve reading temperature over a period and ensuring it's consistent
            current_temp = self.oven.get_current_temperature()
            temp_diff_threshold = 5  # Example threshold, adjust as needed
            return abs(current_temp - target_temp) <= temp_diff_threshold

    # ...rest of the OvenWatcher class...

class HeatworkLogger:

    def __init__(self):
        # Realistic initialization logic
        self.log_file = 'heatwork_log.csv'
        # Other necessary initializations

    def log_heatwork(self, cone_number, heatwork, time, temp):
        # Realistic logging logic
        with open(self.log_file, 'a') as log:
            log.write(f'{cone_number},{heatwork},{time},{temp}\n')
    # Implementation of HeatworkLogger...
    pass

    def start_profile_schedule(self):

        # Realistic logic to start the profile schedule
        # Example: Set initial conditions, start timers, etc.
        # Implementation of start_profile_schedule...
        pass

    def run_oven_cycle(self):

        # Realistic logic for running the oven cycle
        # Example: Monitor temperature, update state, etc.
        # Implementation of run_oven_cycle...
        pass

    def pause(self):

        # Realistic logic to pause the oven
        # Example: Stop timers, maintain state, etc.
        # Implementation of pause feature...
        pass

# Pause Button functionality
def pause_button_pressed():
    # Logic executed when the pause button is pressed
    # Example: Call the pause method of the oven
    oven.pause()


class PauseMode:
    def __init__(self, oven):
        self.oven = oven
        self.paused_state = None
        self.is_paused = False

    def pause(self):
        if self.is_paused:
            return False  # Already paused
        self.paused_state = self.oven.save_state()  # Save the current state of the oven
        self.oven.pause_heating()  # Pause heating
        self.oven.stop_timers()  # Stop timers
        self.is_paused = True
        return True

    def resume(self):
        if not self.is_paused:
            return False  # Not in paused state
        self.oven.restore_state(self.paused_state)  # Restore the oven to its saved state
        self.oven.start_timers()  # Start timers
        self.is_paused = False
        return True

class Oven:
    # ... existing methods and attributes

 #   def start_profile_schedule(self):
        # Realistic logic to start the profile schedule
        # ...

    #def run_oven_cycle(self):
        # Realistic logic for running the oven cycle
        # ...
class OvenController:
    def __init__(self, oven):
        self.oven = oven

    def start_profile_schedule(self):
        self.oven.set_target_temperature(200)  # Example target temperature
        self.oven.start_heating()

    def run_oven_cycle(self):
        while not self.oven.reached_target_temperature():
            time.sleep(1)  # Wait for the oven to reach the target temperature
            self.oven.check_and_adjust_heating()

    def pause(self):
        self.oven.stop_heating()
        self.oven.save_current_state()

# Mocking any external dependencies for testing
class MockOven:
    def set_target_temperature(self, temp):
        pass
    def start_heating(self):
        pass
    def reached_target_temperature(self):
        return True
    def check_and_adjust_heating(self):
        pass
    def stop_heating(self):
        
    def save_current_state(self):
    def monitor_kiln(self):
    pass
