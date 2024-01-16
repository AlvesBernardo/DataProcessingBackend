from flask import Blueprint, render_template, request, redirect, url_for
import requests
import re
from werkzeug.security import generate_password_hash

def logIn():        
    email = request.form['email']
    password = request.form['password']

    if not is_valid_email(email):
        error_message = 'Invalid email format'
    elif not is_valid_password(password):
        error_message = 'Password must be minimum 8 characters and contain at least one uppercase letter, one lowercase letter, one number, and one special character'
    else:
        login_data = {'email': email, 'password': password}
        login_response = requests.post(f'{API_BASE_URL}/login', json=login_data)
        if login_response.status_code == 200:
            return redirect(url_for('success'))
        else:
            error_message = 'Invalid credentials'

    return render_template('logIn.html', error_message=error_message)