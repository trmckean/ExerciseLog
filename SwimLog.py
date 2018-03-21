# SwimLog keeps track of swimming activity


# Create a text file on the desktop to act as a database
# If file exists, open the file for writing
import datetime

swim_file = open("/Users/TylerMcKean/Desktop/swimlog.txt", "a+")

# Prompt the user about any swimming done today
now = datetime.datetime.now()

# Standardize date string
month = "{}".format(now.month)
while len(month) < 2:
    month = "0" + month
day = "{}".format(now.day)
while len(day) < 2:
    day = "0" + day
dateString = "{}/{}/{}".format(month, day, now.year)

print "Did you swim today? {}".format(dateString)
answer = raw_input("Y/N\n")

if answer == "Y":
    # Prompt user for how many yards and how long
    yards = raw_input("How many yards?\n")

    # Standardize written string length for increased readability
    while len(yards) < 4:
        yards = yards + " "

    time = raw_input("How long did you swim for? (in minutes)\n")

    # Write data to file for storage
    swim_file.write("{}    {} yards {} minutes\n".format(dateString, yards, time))

# Close file and end program
print "Thank you - Exiting"
swim_file.close()