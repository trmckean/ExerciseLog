# File containing main application control flow

# Imports
import SwimLog


# Main function controlling application
def main():
    # Instantiate controller to handle application (Also handles database creation and connection)
    controller = SwimLog.Controller()

    # Prompt user if they swam today and handle logging of today's activity
    if controller.prompt_user_initial():
        # Instantiate daily log entry object
        todays_log = controller.create_log()
        # Get relevant swim data from user
        controller.get_user_swim_data()
        # Insert user data into sqlite database
        controller.db.insert(controller.get_date_string(), controller.todays_log.get_yards(),
                             controller.todays_log.get_minutes(), controller.todays_log.get_pace())
        # Check for new pace record
        controller.check_pace()



if __name__ == "__main__":
    main()
