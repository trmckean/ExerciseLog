# SwimLog keeps track of swimming activity

# Imports
import datetime
import mmap

# Class representing a daily log object i.e. the log containing date, yards, and minutes
class DailySwimLog:

    # Init with day, yards, and minutes
    def __init__(self, date, yards, minutes):
        self.date = date
        self.yards = yards
        self.minutes = minutes

    # Override __str__ to allow printing of dailySwimLog object
    def __str__(self):
        return "{} {} yards {} minutes".format(self.date, self.yards, self.minutes)

# Create a text file on the desktop to act as a database
# If file exists, open the file for writing
swim_file = open("/Users/TylerMcKean/Desktop/swimlog.txt", "a+")

# Standardize date string
now = datetime.datetime.now()
month = "{}".format(now.month)
while len(month) < 2:
    month = "0" + month
day = "{}".format(now.day)
while len(day) < 2:
    day = "0" + day
dateString = "{}/{}/{}".format(month, day, now.year)

# Prompt the user about any swimming done today
print "Did you swim today? {}".format(dateString)
answer = raw_input("Y/N\n")

if answer == "Y":
    #Check and make sure we aren't adding data from same day
    mm = mmap.mmap(swim_file.fileno(), 0, access=mmap.ACCESS_READ)
    if mm.find(dateString) != -1:
        print "Already logged swimming today"
    else:
        # Prompt user for how many yards and how long
        yards = raw_input("How many yards?\n")

        # Standardize written string length for increased readability
        while len(yards) < 4:
            yards = yards + " "

        time = raw_input("How long did you swim for? (in minutes)\n")

        # Instantiate daily Log object
        dailyLog = DailySwimLog(dateString, yards, time)

        # Write data to file for storage
        swim_file.write("{}    {} yards {} minutes\n".format(dateString, yards, time))

# Close file and end program
print "Thank you - Exiting"
swim_file.close()