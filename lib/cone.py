import threading
import time
import datetime

class ConeModeController:
    def __init__(self, oven, max_duration=1800):  # default max_duration set to 1800 seconds
        self.oven = oven
        self.cone_mode_activated = False
        self.cone_target_temp = None
        self.cone_drop_rate = 3  # 3% of the max temperature in °C
        self.cone_max_temp = None
        self.cone_start_time = None
        self.cone_heat_work_done = False
        self.cone_duration = 0  # Initialize the duration to 0 seconds
        self.cone_max_duration = max_duration
        self.target_heatwork = 0
        self.current_heatwork = 0
        self.max_duration = max_duration
        self.heatwork_thread = None
        self.max_duration_thread = None

    def activate_cone_mode(self, target_heatwork):
        self.target_heatwork = target_heatwork
        self.heatwork_thread = threading.Thread(target=self.monitor_heatwork)
        self.max_duration_thread = threading.Thread(target=self.monitor_max_duration)
        self.heatwork_thread.start()
        self.max_duration_thread.start()

    def monitor_heatwork(self):
        while self.oven.heat_elements_active:
            self.current_heatwork += self.calculate_heatwork_increment()
            time.sleep(60)  # Monitor every 60 seconds
            if self.current_heatwork >= self.target_heatwork:
                self.oven.stop_oven()
                break

    def monitor_max_duration(self):
        start_time = time.time()
        while time.time() - start_time < self.max_duration:
            time.sleep(60)  # Check every 60 seconds
        if self.oven.heat_elements_active:
            self.oven.stop_oven()

    def calculate_heatwork_increment(self):
        temperature_factor = 0.1  # Example factor
        return self.oven.temperature * temperature_factor  # Simplified calculation

    def adjust_for_lost_heatwork(self):
        # Adjustment logic for lost heatwork
        pass
    def start_countdown(self, duration):
       # """Starts a countdown for the given duration (in seconds).""nj
        remaining = duration
        while remaining > 0:
            print(f"Time remaining: {remaining} seconds")
            time.sleep(1)
            remaining -= 1
        print("Countdown finished!")

        countdown_thread = threading.Thread(target=countdown)
        countdown_thread.start()

    
    # Existing class attributes...
    a = 0.5  # Example value for a
    b = 1.0  # Example value for b
    c = 2.0  # Example value for c
    max_additional_time = 180  # Example value for max additional time in minutes
    def log_heatwork_data(self, heatwork, mode):
        # Log heatwork data to CSV with a timestamp and mode indicator
        filename = 'heatwork_log.csv'
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now(), heatwork, mode])

    def log_before_cone_mode(self, heatwork):
        self.log_heatwork_data(heatwork, 'Before Cone Mode')

    def log_after_cone_mode(self, heatwork):
        self.log_heatwork_data(heatwork, 'After Cone Mode')


    def determine_additional_time_based_on_heatwork(self):
        # Read the latest CSV file to get the lost heatwork data
        try:
            latest_csv = max(glob.glob('log_*.csv'), key=os.path.getctime)
            with open(latest_csv, 'r') as file:
                last_row = list(csv.reader(file))[-1]
                lost_heatwork = float(last_row[2])
                # 
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

            additional_time = self.calculate_additional_time(lost_heatwork)
            return additional_time
        except Exception as e:
            log.error(f'Error reading CSV file for timer extension: {e}')
            return default_additional_time

    def log_temperature_and_heatwork_to_csv(self, temperature, lost_heatwork):
        # Log the temperature and lost heatwork to a CSV file
        filename = datetime.now().strftime('heatwork_log_%Y-%m-%d.csv')
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now(), temperature, lost_heatwork])

    def retrieve_latest_heatwork_data(self):
        # Retrieve the latest lost heatwork data from the most recent CSV file
        try:
            latest_csv = max(glob.glob('heatwork_log_*.csv'), key=os.path.getctime)
            with open(latest_csv, 'r') as file:
                last_row = list(csv.reader(file))[-1]
                return float(last_row[2])
        except Exception as e:
            log.error(f'Error retrieving heatwork data from CSV: {e}')
            return None
        
    def calculate_lost_heatwork(self, current_temp, target_temp, elapsed_time):
        # Simple model: Heatwork = Temperature * Time
        # Calculate the expected heatwork at target temperature
        expected_heatwork = target_temp * elapsed_time
        # Calculate the actual heatwork at current temperature
        actual_heatwork = current_temp * elapsed_time
        # The lost heatwork is the difference
        return expected_heatwork - actual_heatwork

        # This function should return the heatwork lost due to temperature lag
        return target_temp - current_temp  # Simplified example
        
    def calculate_additional_time(self, lost_heatwork, target_temp):
        # Simple model: Additional Time = Lost Heatwork / Target Temperature
        # Calculate the additional time required to achieve the lost heatwork at target temperature
        if target_temp > 0:
            return lost_heatwork / target_temp
        else:
            return 0  # Avoid division by zero

        # This function should return additional time in seconds
        return lost_heatwork * 10  # Simplified example

    



    def deactivate_cone_mode(self):
        # Example implementation of deactivating cone mode
        # This can be modified based on specific requirements
        self.cone_mode_activated = False
        print("Cone mode deactivated.")

    def activate_cone_mode(self, cone_type):
        if not self.cone_mode_activated:
            self.cone_target_temp = self.get_target_temperature_for_cone(cone_type)
            self.cone_max_temp = self.oven.get_max_temperature()
            self.cone_mode_activated = True
            self.cone_start_time = time.time()
            self.oven.set_target_temperature(self.cone_target_temp)

    def deactivate_cone_mode(self):
        if self.cone_mode_activated:
            self.oven.set_target_temperature(0)  # Turn off the kiln
            self.cone_mode_activated = False
            self.cone_target_temp = None
            self.cone_max_temp = None
            self.cone_start_time = None
            self.cone_heat_work_done = False
            self.cone_duration = 0  # Reset the duration

    
    def update_cone_mode(self):
        if self.cone_mode_activated:
            current_temp = self.oven.get_current_temperature()
            target_temp = self.cone_target_temp
            elapsed_time = time.time() - self.cone_start_time
            lost_heatwork = self.calculate_lost_heatwork(current_temp, target_temp, elapsed_time)
            additional_time = self.calculate_additional_time(lost_heatwork, target_temp)

            # Log the additional time calculation
            logging.info(f"Additional time calculated for lost heatwork: {additional_time} seconds")

            # Existing logic to update the cone mode
            # ...

            if self.cone_mode_activated:
                current_temp = self.oven.get_current_temperature()
                target_temp = self.cone_target_temp
                lost_heatwork = self.calculate_lost_heatwork(current_temp, target_temp)
                additional_time = self.calculate_additional_time(lost_heatwork)

                # Log the additional time calculation
                logging.info(f"Additional time calculated for lost heatwork: {additional_time} seconds")

                # Existing logic to update the cone mode
                # ...
        
        if self.cone_mode_activated:
            current_temp = self.oven.get_current_temperature()

            if current_temp >= self.cone_max_temp:
                # Kiln has reached or exceeded the maximum temperature
                self.cone_heat_work_done = True
                self.oven.set_target_temperature(current_temp)
            elif not self.cone_heat_work_done:
                # Continue heating at the maximum temperature until heat work is done
                self.oven.set_target_temperature(self.cone_max_temp)
            else:
                # Gradually reduce temperature by the drop rate
                new_target_temp = max(current_temp - self.cone_drop_rate, 0)
                self.oven.set_target_temperature(new_target_temp)

            # Update the Cone Mode duration
            self.update_duration()

    def update_duration(self):
        if self.cone_mode_activated:
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



# New Functionalities




    def check_and_activate_cone_mode(self):
        remaining_time = self.oven.get_remaining_profile_time()
        if remaining_time <= 60 and not self.cone_mode_activated:
            self.activate_cone_mode()

    def activate_cone_mode(self):
        # Implement activation logic here
        self.cone_mode_activated = True
        log.info("Cone mode activated with 1 minute remaining")

    def check_and_perform_cone_drop(self):
        remaining_time = self.oven.get_remaining_profile_time()
        if remaining_time <= 10 and not self.cone_drop_performed:
            self.perform_cone_drop()

    def perform_cone_drop(self):
        # Implement cone drop logic here
        self.cone_drop_performed = True
        log.info("Cone drop performed with 10 seconds remaining")

    def log_heatwork(self, cone_number, additional_info=''):
        with open('lost_heatwork_log.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.datetime.now(), self.oven.get_current_temperature(), cone_number, additional_info])
            log.info(f"Heatwork data logged for cone {cone_number}")
