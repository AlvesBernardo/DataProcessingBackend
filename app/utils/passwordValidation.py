def is_valid_password(password):
    # Minimum 8 characters, at least one uppercase letter, one lowercase letter, one number, and one special character
    pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    return bool(re.match(pattern, password))