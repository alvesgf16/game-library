from mysql.connector import Error, errorcode


def create_exception_message(an_error: Error) -> None:
    if an_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("There is something wrong with the username or password")
    elif an_error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table already exists")
    else:
        print(an_error)
