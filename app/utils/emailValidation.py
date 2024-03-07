from flask import Blueprint, render_template, request, redirect, url_for
import requests
import re
from werkzeug.security import generate_password_hash

def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False