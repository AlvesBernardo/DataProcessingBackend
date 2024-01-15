import sys
sys.path.append("..") # added!
from utils.emailValidation import is_valid_email
from modelsv2.account_model import Account

def registerUser(name, email, password):
    try:
        hashed_password = 1111
        validatedEmail = is_valid_email(email)

        account = Account(dtFirstName=name, dtEmail=validatedEmail, dtPassword=hashed_password)
        account.save()  # Save the user to the database (implement this based on your ORM)
        return True, "User registered successfully"

    except Exception as error:
        print("Error during user registration:", error)

        if "UniqueViolation" in str(error):
            return False, "Email address is already in use"
        else:
            return False, "Failed to register user"
    
