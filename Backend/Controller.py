# File containing controller class to control application flow

# Imports
import SQLiteDatabase
import DailySwimLog
import datetime
import os.path
from shutil import copyfile


# Class representing the controller for the program
class Controller:
    # Init and open/create sqlite database
    def __init__(self):
        self.db = SQLiteDatabase.Database()

    # Check and see if DB exists, return value
    def check_db_exists(self):
        return os.path.isfile('swim_log.db')

    # Create a new log entry
    # TODO: Fix class import/calling
    def create_log(self, date=None):
        if date is None:
            self.todays_log = DailySwimLog.DailySwimLog(self.get_date_string())
        else:
            self.todays_log = DailySwimLog.DailySwimLog(date)

        return self.todays_log

    # Function to get standardized date string
    @staticmethod
    def get_date_string():
        # Standardize date string
        now = datetime.datetime.now()
        month = "{}".format(now.month)
        while len(month) < 2:
            month = "0" + month
        day = "{}".format(now.day)
        while len(day) < 2:
            day = "0" + day
        return "{}/{}/{}".format(month, day, now.year)

    # Function to prompt user about if they have data to add
    def prompt_user_initial(self):
        # Prompt the user about any swimming done today
        print(('Did you swim today? {}'.format(self.get_date_string())))
        answer = input("Y/N\n")
        if answer.upper() == "Y":
            return True
        else:
            return False

    # Function to prompt user if they would like to backup the db
    @staticmethod
    def prompt_user_backup():
        print('Would you like to backup the database?')
        answer = input('Y/N\n')
        if answer.upper() == "Y":
            return True
        else:
            return False

    # Function to see if user wants to add a specific day
    @staticmethod
    def prompt_user_specific():
        print("Would you like to add a specific day's log?")
        answer = input("Y/N\n")
        if answer.upper() == "Y":
            return True
        else:
            return False

    # Get specific date from user
    def get_user_date(self):
        date = input("Please enter the specific day you would like to enter: (MM/DD/YYYY)\n")
        if self.validate_date(date):
            return date
        else:
            return self.get_user_date()

    # Function to make sure user date is valid
    @staticmethod
    def validate_date(date):
        try:
            datetime.datetime.strptime(date, '%m/%d/%Y')
            return True
        except ValueError:
            print("Incorrectly formatted date, try again!")
            return False

    # Function to get data from user and add it to log entry
    def get_user_swim_data(self):
        # Prompt user for how many yards and how long
        yards = input("How many yards?\n")
        # Make sure yards is a number
        while not yards.isdigit() or int(yards) == 0:
            print("Not a number, please enter something valid.")
            yards = input("How many yards?\n")
        minutes = input("How long did you swim for? (in minutes)\n")
        # Make sure minutes is a valid number
        while not minutes.isdigit() or int(minutes) == 0:
            print("Not a valid entry for minutes, please enter something valid.")
            minutes = input("How long did you swim for? (in minutes)\n")

        # Set data for log entry object
        self.todays_log.set_yards_minutes(yards, minutes)

        # Show user pace for daily activity
        print("Your pace was {}".format(self.todays_log.get_pace()))

    # Check pace and notify user if they've set a new record
    def check_pace(self):
        todays_pace = self.todays_log.get_pace()
        max_pace = self.db.get_max_pace()
        if todays_pace == max_pace:
            print("Nice work! You set a new pace record!")
        else:
            print("Nice job, but you can swim faster next time!")

    # Notify user of all yards logged
    def show_total_yards(self):
        # Sum of yards from sql query
        sum_yards = self.db.get_total_yards()
        print("Total yards logged: {}".format(sum_yards))

    # Convert yardage to miles
    def yards_to_miles(self, yards):
        # A mile is 1760 yards
        return float(yards) / 1760

    # Notify user of mileage logged
    def show_total_miles(self):
        # Sum of yards from sql query
        sum_yards = self.db.get_total_yards()
        print("Total miles logged: %.2f" % self.yards_to_miles(sum_yards))

    # Prompt user if they want to update a specific entry
    def prompt_update_entry(self):
        # Ask user if they would like to update an entry
        print("Would you like to update an entry?")
        response = input("Y/N\n")
        if response.upper() == "Y":
            return True
        else:
            return False

    # Backup the current database to a new directory called DB_Backup
    @staticmethod
    def backup_current_db():
        # Path contained in program file structure
        source = "swim_log.db"
        destination = "../DB_backup/swim_log_backup.db"
        # Copy db
        try:
            copyfile(source, destination)
        except IOError:
            print("Destination not writable")

    # Function to end program
    def shutdown(self):
        # End program
        self.db.shutdown()
        print("Thank you - Exiting")
