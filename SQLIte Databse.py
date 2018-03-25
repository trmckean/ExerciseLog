# Database using SQLite to store swim logs

# Imports
import SwimLog
import sqlite3


# Class holding SQLite database
class database:

    # Init and open/create DB file
    def __init__(self):
        self.connection = sqlite3.connect("swim_log.db")
        self.cursor = self.connection.cursor()

