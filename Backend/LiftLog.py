# Module containing class for a weight lifting log
# First iteration only supports specific weight lifting program

# Standard imports
import datetime


class LiftLog:
    # Init function. Only split_type of leg, push, or pull is supported at this time.
    def __init__(self, date, split_type):
        if split_type is not "legs" or split_type is not "push" or split_type is not "pull":
            print "Invalid type - Only supporting Leg, Pull, and Push at this time"
        else:
            self.split_type = split_type
            self.date = date