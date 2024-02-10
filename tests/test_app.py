"""
    # test_app.py
    Contains unit testing for functions used in the project
"""
import cv2
import sys
import unittest
from datetime import datetime, date, timedelta, time

sys.path.append('..')
import Detector

class TestMySurveillance(unittest.TestCase):
    def setUp(self):
        self.cap = cv2.VideoCapture(0)
        self.Surveillance = Detector.Detector_2A2S(self.cap)

    def test_get_curr_date_time(self):
        # call function
        curr_date, curr_time = self.Surveillance.get_curr_date_time()

        # find actual time
        expected_curr_date = date.today()
        expected_curr_time = datetime.now().strftime("%H:%M:%S")

        # compare the result
        self.assertEqual(curr_date, expected_curr_date)
        self.assertEqual(curr_time, expected_curr_time)

    def test_write_motion_logs(self):
        # set dummy data
        self.Surveillance.last_log_time = datetime.now() - timedelta(minutes=2)
        self.Surveillance.motion_logs_path = "./logs/motion_log.txt"
        
        # call the function
        self.Surveillance.write_motion_logs()

        # Assert that the motion log was written
        with open("./logs/motion_log.txt", "r") as f:
            motion_log_entry = f.readline()
            self.assertRegex(motion_log_entry, r"Motion detected at \d{2}:\d{2}:\d{2} on \d{4}-\d{2}-\d{2}\n")
        
        # Check that the last_log_time was updated correctly
        current_time = datetime.now()
        self.assertGreaterEqual(current_time, self.Surveillance.last_log_time)

    def test_check_time_for_alert(self):
        alert_time_start = time(hour=20, minute=0)
        alert_time_end = time(hour=8, minute=0)
    
        # Get current time (for testing, set it at 01:00)
        current_time = time(hour=1, minute=0)

        print(alert_time_start)
        print(alert_time_end)

        # Check if the current time falls within the alert time bracket
        result = alert_time_start <= current_time <= alert_time_end

        print(f"result: {result}")

        # Assert the result 
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()