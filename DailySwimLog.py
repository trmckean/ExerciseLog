# SwimLog keeps track of swimming activity

# Imports
import datetime
import mmap
import SQLiteDatabase


# Class representing a daily log object i.e. the log containing date, yards, and minutes
class DailySwimLog:
    # Init with day, yards, and minutes
    def __init__(self, date, yards=None, minutes=None):
        self.date = date
        self.yards = yards
        self.minutes = minutes

    # Function to set data if constructor w/ just date is used
    def set_yards_minutes(self, yards, minutes):
        self.yards = yards
        self.minutes = minutes

    # Function to calculate pace in yards per hour
    def get_pace(self):
        pace = float(self.yards) / int(self.minutes) * 60
        return int(pace)

    # Function to get yards
    def get_yards(self):
        return int(self.yards)

    # Function to get minutes
    def get_minutes(self):
        return int(self.minutes)

    # Override __str__ to allow printing of dailySwimLog object
    def __str__(self):
        return "{}    {} yards {} minutes    {}".format(self.date, self.yards, self.minutes, self.get_pace())