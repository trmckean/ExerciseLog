# SwimLog keeps track of swimming activity

# Imports
import datetime
import mmap


# Class representing the controller for the program
class Controller:
    # Init and open/create file
    def __init__(self):
        # Create a text file on the desktop to act as a database
        # If file exists, open the file for writing
        self.swim_log = open("/Users/TylerMcKean/Desktop/swimlog.txt", "a+")

    # Create a new log entry
    def create_log(self):
        self.todays_log = DailySwimLog(self.get_date_string())

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

    # Function to make sure we haven't logged already today
    def check_duplicate_log(self):
        # Check and make sure we aren't adding data from same day
        mm = mmap.mmap(self.swim_log.fileno(), 0, access=mmap.ACCESS_READ)
        if mm.find(self.get_date_string()) != -1:
            print "Already logged swimming today"
            return False
        else:
            return True

    # Function to get data from user and add it to log entry
    def get_user_swim_data(self):
        # Prompt user for how many yards and how long
        yards = raw_input("How many yards?\n")
        # Standardize written string length for increased readability
        while len(yards) < 4:
            yards = yards + " "
        minutes = raw_input("How long did you swim for? (in minutes)\n")

        # Set data for log entry object
        self.todays_log.set_yards_minutes(yards, minutes)

        # Show user pace for daily activity
        print self.todays_log.get_pace()

    # Function to write user data to the swimLog text file
    def write_data(self):
        # Write data to file for storage
        self.swim_log.write(self.todays_log.__str__())
        print "Wrote data to log!"

    # Function to end program
    def shutdown(self):
        # Close file and end program
        print "Thank you - Exiting"
        self.swim_log.close()


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
        pace = int(self.yards) / int(self.minutes) * 60
        return "Pace: {} yards/hour".format(pace)

    # Override __str__ to allow printing of dailySwimLog object
    def __str__(self):
        return "{}    {} yards {} minutes    {}".format(self.date, self.yards, self.minutes, self.get_pace())


# Main function
def main():
    # Instantiate controller
    controller = Controller()

    # Check and see if log should be made, then gather data and write to storage
    if controller.prompt_user_initial() and controller.check_duplicate_log():
        controller.create_log()
        controller.get_user_swim_data()
        controller.write_data()

    # Shutdown
    controller.shutdown()


if __name__ == "__main__":
    main()
