# Database using SQLite to store swim logs

# Imports
import Controller
import sqlite3


# Class holding SQLite database
class Database:
    # Init and open/create DB file
    def __init__(self, path=None):
        if path is None:
            self.connection = sqlite3.connect("swim_log.db")
        else:
            self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

        # Check and see if default table exists, if not create it
        if not self.check_swim_log_table_exits():
            self.create_swim_log_table()

    # Create initial table
    def create_swim_log_table(self):
        self.cursor.execute("""CREATE TABLE swim_logs
                              (date TEXT, yards INTEGER, time INTEGER, pace INTEGER )
                              """)

    # Check and see if swim_log table exists
    def check_swim_log_table_exits(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='swim_logs'"
        self.cursor.execute(sql)
        if self.cursor.fetchone() is not None:
            return True
        else:
            return False

    # Insert data into table
    def insert(self, date, yards, time, pace):
        log_entry = (date, yards, time, pace)
        self.cursor.execute("INSERT INTO swim_logs VALUES (?, ?, ?, ?)", log_entry)
        self.connection.commit()

    # Print all entries in db
    def get_all_entries(self):
        sql = "SELECT * FROM swim_logs"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # Return a list of all dates stored
    def get_previous_dates(self):
        sql = "SELECT date FROM swim_logs"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # Return the maximum pace logged
    def get_max_pace(self):
        sql = "SELECT MAX(pace) FROM swim_logs"
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    # Return the maximum yardage logged
    def get_max_yards(self):
        sql = "SELECT MAX(yards) FROM swim_logs"
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    # Return a total of all yards logged
    def get_total_yards(self):
        sql = "SELECT SUM(yards) FROM swim_logs"
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    # Return whether or not a record exists given the date
    def check_log_entry_exists(self, datestring):
        # SQL statement returns 0 if not previously logged, and 1 if it exists
        date = (datestring, )
        sql = "SELECT count(1) FROM swim_logs WHERE date =?"
        self.cursor.execute(sql, date)
        return self.cursor.fetchone()[0]

    # Update an existing entry in the database based on date with provided yards, time, and pace
    def update_previous_date(self, date_string, yards, time, pace):
        date = (date_string,)
        # TODO: Find out if the below string formatting is secure
        sql = "UPDATE swim_logs SET yards = {}, time = {}, pace = {} WHERE date =?".format(yards, time, pace)
        self.cursor.execute(sql, date)
        self.connection.commit()

    # Close the cursor connection to db
    def shutdown(self):
        self.connection.close()

