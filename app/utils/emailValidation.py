from flask import Blueprint, render_template, request, redirect, url_for
import requests
import re
from werkzeug.security import generate_password_hash

def is_valid_email(email):
    pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(pattern, email))
