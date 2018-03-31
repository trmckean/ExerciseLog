# File containing controller class to control application flow

# Imports
import SQLiteDatabase
import DailySwimLog
import datetime


# Class representing the controller for the program
class Controller:
    # Init and open/create sqlite database
    def __init__(self):
        self.db = SQLiteDatabase.Database()

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
        print "Did you swim today? {}".format(self.get_date_string())
        answer = raw_input("Y/N\n")
        if answer.upper() == "Y":
            return True
        else:
            return False

    # Function to see if user wants to add a specific day
    @staticmethod
    def prompt_user_specific():
        print "Would you like to add a specific day's log?"
        answer = raw_input("Y/N\n")
        return answer.upper() == "Y"

    # Get specific date from user
    @staticmethod
    def get_user_date():
        return raw_input("Please enter the specific day you would like to enter: (MM/DD/YYYY)\n")

    # Function to make sure we haven't logged already today
    def check_duplicate_log(self):
        # # Check and make sure we aren't adding data from same day
        # mm = mmap.mmap(self.swim_log.fileno(), 0, access=mmap.ACCESS_READ)
        # if mm.find(self.get_date_string()) != -1:
            print "Already logged swimming today"
        #     return False
        # else:
        #     return True

    # Function to get data from user and add it to log entry
    def get_user_swim_data(self):
        # Prompt user for how many yards and how long
        yards = raw_input("How many yards?\n")
        # Make sure yards is a number
        while not yards.isdigit() or int(yards) == 0:
            print "Not a number, please enter something valid."
            yards = raw_input("How many yards?\n")
        # Standardize written string length for increased readability
        while len(yards) < 4:
            yards = yards + " "
        minutes = raw_input("How long did you swim for? (in minutes)\n")
        # Make sure minutes is a valid number
        while not minutes.isdigit() or int(minutes) == 0:
            print "Not a valid entry for minutes, please enter something valid."
            minutes = raw_input("How long did you swim for? (in minutes)\n")

        # Set data for log entry object
        self.todays_log.set_yards_minutes(yards, minutes)

        # Show user pace for daily activity
        print "Your pace today was {}".format(self.todays_log.get_pace())

    # Function to write user data to the swimLog text file
    def write_data(self):
        # # Write data to file for storage
        # self.swim_log.write(self.todays_log.__str__())
         print "Wrote data to log!"

    # Check pace and notify user if they've set a new record
    def check_pace(self):
        todays_pace = self.todays_log.get_pace()
        max_pace = self.db.get_max_pace()[0]
        if todays_pace > max_pace:
            print "Nice work! You set a new pace record!"
        elif todays_pace == max_pace:
            print "Nice work! You matched your fastest pace!"
        else:
            print "Nice job, but you can swim faster next time!"

    # Function to end program
    def shutdown(self):
        # # Close file and end program
         print "Thank you - Exiting"
        # self.swim_log.close()
