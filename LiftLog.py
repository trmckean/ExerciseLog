# Module containing class for a weight lifting log
# First iteration only supports specific weight lifting program

# Standard imports
import datetime


class LiftLog:
    def __init__(self, type):
        if type is not "leg" or type is not "push" or type is not "pull":
            print "Invalid type - Only supporting Leg, Pull, and Push at this time"
