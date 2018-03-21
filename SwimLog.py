# SwimLog keeps track of swimming activity

# Create a text file on the desktop to act as a database
# If file exists, open the file for writing
import datetime

swim_file = open("/Users/TylerMcKean/Desktop/swimlog.txt", "w+")

# Prompt the user about any swimming done today
now = datetime.datetime.now()
month = now.month
day = now.day
year = now.year

print "Did you swim today? {}/{}/{}".format(month, day, year)



