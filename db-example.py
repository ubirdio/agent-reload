import ai_dev

@ai_dev.in_ai_dev()
def user_signup(email, username):
    pass
    # At this entry point, we have access to the DB and the form data.
    #
    # We need to check that the user email is not already used and nor is the username.
    #
    # Then we need to save to the database.
    # In the first iteration we have a bug in our SQL query.
    #
    # The error is returned to the AI.
    # It updates the SQL query.
    # And restarts from the entrypoint (so we have a tight development loop).
    #
    # Finally, we exit.
