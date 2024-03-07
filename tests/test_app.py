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
        _, frame = self.cap.read()
        self.Surveillance.write_motion_logs(frame)

        # Assert that the motion log was written
        with open("./logs/motion_log.txt", "r") as f:
            motion_log_entry = f.readline()
            self.assertRegex(motion_log_entry, r"Motion detected at \d{2}:\d{2}:\d{2} on \d{4}-\d{2}-\d{2}\n")
        
        # Check that the last_log_time was updated correctly
        current_time = datetime.now()
        self.assertGreaterEqual(current_time, self.Surveillance.last_log_time)

    # PICKUP HERE
    def test_check_isSendingAlert(self):
        self.Surveillance.alert_time_start = "21:00"
        self.Surveillance.alert_time_end = "07:00"

        # create a mock 'now' time, then assert True
        mock_now = time(hour=23, minute=30, second=00)
        result = self.Surveillance.check_isSendingAlerts(mock_now)
        self.assertTrue(result)

        # create a mock time, then assert False
        mock_now = time(hour=19, minute=30, second=00)
        result = self.Surveillance.check_isSendingAlerts(mock_now)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()