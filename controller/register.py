from flask import Blueprint, render_template, request, redirect, url_for
import requests
import re
from werkzeug.security import generate_password_hash
import sys
sys.path.append("..")
from utils.emailValidation import is_valid_email
from modelsv2.account_model import Account


def registerUSer(name, email, password):
    try:
        hashed_password = generate_password_hash(password)

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

    return render_template('register.html', success_message=success_message, error_message=error_message)
