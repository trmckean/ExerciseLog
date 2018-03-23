# SwimLog keeps track of swimming activity

# Imports
import datetime
import mmap

# Class representing the controller for the program
class Controller:
    # Init and open/create file
    def __init__(self):
        self.swim_log = open("/Users/TylerMcKean/Desktop/swimlog.txt", "a+")


# Class representing a daily log object i.e. the log containing date, yards, and minutes
class DailySwimLog:
    # Init with day, yards, and minutes
    def __init__(self, date, yards, minutes):
        self.date = date
        self.yards = yards
        self.minutes = minutes

    # Init w/ just date
    def __init__(self, date):
        self.date = date

    # Function to set data if constructor w/ just date is used
    def set_yards_minutes(self, yards, minutes):
        self.yards = yards
        self.minutes = minutes

    # Override __str__ to allow printing of dailySwimLog object
    def __str__(self):
        return "{} {} yards {} minutes".format(self.date, self.yards, self.minutes)


# Function to get standardized date string
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
def prompt_user_initial(date_string):
    # Prompt the user about any swimming done today
    print "Did you swim today? {}".format(date_string)
    answer = raw_input("Y/N\n")
    if answer.upper() == "Y":
        return True
    else:
        return False


# Function to make sure we haven't logged already today
def check_duplicate_log(date_string, swim_file):
    # Check and make sure we aren't adding data from same day
    mm = mmap.mmap(swim_file.fileno(), 0, access=mmap.ACCESS_READ)
    if mm.find(date_string) != -1:
        print "Already logged swimming today"
        return False
    else:
        return True


# Function to write user data to the swimLog text file
def write_data(swim_file, daily_log):
    # Write data to file for storage
    swim_file.write("{}    {} yards {} minutes\n".format(daily_log.date, daily_log.yards, daily_log.minutes))
    print "Wrote data to log!"


# Function to handle user prompting and input if there's data to add
def get_user_swim_data():
    # Prompt user for how many yards and how long
    yards = raw_input("How many yards?\n")

    # Standardize written string length for increased readability
    while len(yards) < 4:
        yards = yards + " "

    minutes = raw_input("How long did you swim for? (in minutes)\n")

    # Dictionary to hold user data
    data = {"yards": yards, "minutes": minutes}

    return data


# Main function
def main():
    # Create a text file on the desktop to act as a database
    # If file exists, open the file for writing
    swim_file = open("/Users/TylerMcKean/Desktop/swimlog.txt", "a+")

    # Instantiate daily log object
    daily_log = DailySwimLog(get_date_string())

    # Prompt user about swimming
    if prompt_user_initial(daily_log.date) and check_duplicate_log(daily_log.date, swim_file):
        # Get data from user
        data = get_user_swim_data()
        # Add data to log object
        daily_log.set_yards_minutes(data["yards"], data["minutes"])
        # Write user data to log file
        write_data(swim_file, daily_log)

    # Close file and end program
    print "Thank you - Exiting"
    swim_file.close()

if __name__ == "__main__":
    main()
