"""
    # test_app.py
    Contains unit testing for functions used in the project
"""
import cv2
import sys
import unittest
from datetime import datetime, date, timedelta, time
import tkinter as tk

sys.path.append('..')
import Detector
from  GUI import GUI_2A2S
import Email_Alert

class TestMySurveillance(unittest.TestCase):
    def setUp(self):
        """
        Return: Void
        """
        # Detector testing setup
        self.cap = cv2.VideoCapture(0)
        self.mock_Detector = Detector.Detector_2A2S(self.cap)

        # GUI testing setup
        self.root = tk.Tk()
        self.mock_GUI = GUI_2A2S(self.root)
        self.root.mainloop()

        # email_alert_system testing system
        self.mock_email_alert_system = Email_Alert.email_alert_system

    # DETECTOR functions ================================================================================================
    def test_get_curr_date_time(self):
        """
        Return: Void
        """
        # call function
        curr_date, curr_time = self.mock_Detector.get_curr_date_time()

        # find actual time
        expected_curr_date = date.today()
        expected_curr_time = datetime.now().strftime("%H:%M:%S")

        # compare the result
        self.assertEqual(curr_date, expected_curr_date)
        self.assertEqual(curr_time, expected_curr_time)

    def test_write_motion_logs(self):
        """
        Return: Void
        """
        # set dummy data
        self.mock_Detector.last_log_time = datetime.now() - timedelta(minutes=2)
        self.mock_Detector.motion_logs_path = "./logs/motion_log.txt"
        
        # call the function
        _, frame = self.cap.read()
        self.mock_Detector.write_motion_logs(frame)

        # Assert that the motion log was written
        with open("./logs/motion_log.txt", "r") as f:
            motion_log_entry = f.readline()
            self.assertRegex(motion_log_entry, r"Motion detected at \d{2}:\d{2}:\d{2} on \d{4}-\d{2}-\d{2}\n")
        
        # Check that the last_log_time was updated correctly
        current_time = datetime.now()
        self.assertGreaterEqual(current_time, self.mock_Detector.last_log_time)

    
    def test_check_isSendingAlert(self):
        """
        Return: Void
        """
        self.mock_Detector.alert_time_start = "21:00"
        self.mock_Detector.alert_time_end = "07:00"

        # create a mock 'now' time, then assert True
        mock_now = time(hour=23, minute=30, second=00)
        result = self.mock_Detector.check_isSendingAlerts(mock_now)
        self.assertTrue(result)

        # create a mock time, then assert False
        mock_now = time(hour=19, minute=30, second=00)
        result = self.mock_Detector.check_isSendingAlerts(mock_now)
        self.assertFalse(result)

    # Email Alert functions
    def test_send_alert_cli_invalid_flag(self):
        """Tests the function against an invalid argument"""
        with self.assertRaises(ValueError):
            self.mock_email_alert_system.send_alert_cli("invalid", "2024-03-08 15:30:00")

    #def test_send_alert_cli(self):
        #self.mock_email_alert_system.send_alert_cli("motion", "21:30:13")

        #expected_output = ""

    # GUI functions ================================================================================================
    # ISSUE: NOT TESTED
    def test_GUI_toggle_object_detection(self):
        """
        Tests GUI.toggle_object_detection() by checking if the value changes after the func call
        Return: Void
        """
        initial_val = self.mock_GUI.set_objectDetectionIsON
        updated_val = self.mock_GUI.toggle_object_detection()
        self.assertFalse(initial_val == updated_val)
    
    # TODOS
    def check_update_min_contour(self):
        """
        Return: Void
        """

    def check_update_obj_scan_duration(self):
        pass
    
    def check_update_frame_diff_threshold(self):
        pass
    
    def check_update_bg_subtractor(self):
        pass

if __name__ == "__main__":
    unittest.main()