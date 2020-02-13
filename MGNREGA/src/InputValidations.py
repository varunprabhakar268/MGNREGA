from datetime import datetime
import re


def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        print("\tInvalid date. Please try again. ")
        return False


def validate_end_date(start_date, end_date):
    a = datetime.strptime(start_date, '%Y-%m-%d')
    b = datetime.strptime(end_date, '%Y-%m-%d')
    if b > a :
        return True
    else:
        print("\tInvalid End Date. Please try again.")
        return False


def validate_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        print("Invalid Email")
        return False
