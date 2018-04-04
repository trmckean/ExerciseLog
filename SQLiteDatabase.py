# Database using SQLite to store swim logs

# Imports
import Controller
import sqlite3


# Class holding SQLite database
class Database:
    # Init and open/create DB file
    def __init__(self):
        self.connection = sqlite3.connect("swim_log.db")
        self.cursor = self.connection.cursor()

    # Create initial table
    def create_swim_log_table(self):
        self.cursor.execute("""CREATE TABLE swim_logs
                              (date TEXT, yards INTEGER, time INTEGER )
                              """)

    # Insert data into table
    def insert(self, date, yards, time, pace):
        log_entry = (date, yards, time, pace)
        self.cursor.execute("INSERT INTO swim_logs VALUES (?, ?, ?, ?)", log_entry)
        self.connection.commit()

    # Print all entries in db
    def get_all_entries(self):
        sql = "SELECT * FROM swim_logs"
        self.cursor.execute(sql)
        print self.cursor.fetchall()

    # Return a list of all dates stored
    def get_previous_dates(self):
        sql = "SELECT date FROM swim_logs"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # Return the maximum pace logged
    def get_max_pace(self):
        sql = "SELECT MAX(pace) FROM swim_logs"
        self.cursor.execute(sql)
        return self.cursor.fetchone()

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


# Main function to execute test program
def main():
    # Testing implementation
    db = Database()

    controller = Controller.Controller()
    while controller.prompt_user_specific():
        controller.create_log(controller.get_user_date())
        # TODO: Make below functionality into function and clean up breaks
        dates = db.get_previous_dates()
        for date in dates:
            if not date[0] in controller.todays_log.date:
                controller.get_user_swim_data()
                db.insert(controller.todays_log.date, controller.todays_log.get_yards(),
                          controller.todays_log.get_minutes(), controller.todays_log.get_pace())
                break
            else:
                print "Can't update previously written daily logs at this point"
                break

    if controller.prompt_user_initial():
        controller.create_log()
        controller.get_user_swim_data()
        db.insert(controller.get_date_string(), controller.todays_log.get_yards(),
                  controller.todays_log.get_minutes(), controller.todays_log.get_pace())


if __name__ == "__main__":
    main()
