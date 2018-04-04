# File containing main application control flow

# Imports
import Controller


# Main function controlling application
def main():
    # Instantiate controller to handle application (Also handles database creation and connection)
    controller = Controller.Controller()

    # Prompt user if they swam today and handle logging of today's activity
    if controller.prompt_user_initial():
        # Instantiate daily log entry object
        controller.create_log()
        # Get relevant swim data from user
        controller.get_user_swim_data()
        # Insert user data into sqlite database
        controller.db.insert(controller.get_date_string(), controller.todays_log.get_yards(),
                             controller.todays_log.get_minutes(), controller.todays_log.get_pace())
        # Check for new pace record
        controller.check_pace()

    # Prompt user if they would like to add a specific day and allow them to keep doing so
    # TODO: Add update support
    # TODO: Figure out whether to allow overwriting previously written date
    while controller.prompt_user_specific():
        # Prompt user for specific date
        date = controller.get_user_date()
        # Instantiate new log entry object
        controller.create_log(date)
        # Get relevant swim data for date
        controller.get_user_swim_data()
        # Insert data into database
        controller.db.insert(controller.todays_log.date, controller.todays_log.get_yards(),
                             controller.todays_log.get_minutes(), controller.todays_log.get_pace())

    # Show user how many swim yards/miles logged
    controller.show_total_yards()


    # Shutdown message
    controller.shutdown()


if __name__ == "__main__":
    main()
