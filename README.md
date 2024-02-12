# Flask API with MSSQL Database and JWT Authentication

## Project Overview

This Flask project provides a RESTful API with a Microsoft SQL Server (MSSQL) database backend. It implements JSON Web Token (JWT) authentication to secure endpoints and ensure that only authorized users can access certain resources.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete records in the MSSQL database through the API.
- **JWT Authentication**: Secure API endpoints using JWT-based authentication.
- **User Registration and Login**: Allows users to register and login to access protected routes.

## Prerequisites

- Python: Before installing `pip`, ensure you have Python installed on your system. `pip` is included by default with Python 3.4 and later.
- A suitable web browser for accessing the frontend.
- Access to a Microsoft SQL Server (MSSQL) database.

## Installing Python

Python is a versatile programming language that you need to run this project. If you don't have Python installed on your system, follow these steps to install it.

### For Windows Users

1. **Download Python:**

   - Visit the official Python website at [python.org](https://www.python.org/downloads/).
   - Download the latest version of Python for Windows.

2. **Run the Installer:**

   - Open the downloaded file to start the installation.
   - **Important:** Ensure you check the box that says "Add Python to PATH" before clicking "Install Now."

3. **Verify the Installation:**
   - Open Command Prompt and type `python --version`.
   - If Python is installed correctly, you should see the version number.

### For MacOS Users

1. **Install Homebrew:**

   - Homebrew is a package manager for MacOS. Open Terminal and run:
     ```
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```

2. **Install Python using Homebrew:**

   - In Terminal, run:
     ```
     brew install python
     ```

3. **Verify the Installation:**
   - In Terminal, type `python3 --version`.
   - The version number of Python should display.

## Installing pip

`pip` is a package manager for Python that allows you to install and manage additional libraries and dependencies that are not distributed as part of the standard library.

1. **Check if pip is already installed:**
   python -m pip --version

This command will display the version of `pip` if it is already installed.

2. **Install pip (if not installed):**

- **On Windows:**
  If Python is installed, `pip` is usually included. If it's not, download `get-pip.py` by following the link: https://bootstrap.pypa.io/get-pip.py. Then, run the following command in the command prompt:

  ```
  python get-pip.py
  ```

- **On MacOS/Linux:**
  Python and `pip` are generally pre-installed. If not, you can install Python using a package manager like Homebrew (on MacOS) or apt/yum (on Linux). `pip` will be included with Python.

## Installation Of The Project

1. Clone the repository:

   ```bash
   git clone <git@github.com:AlvesBernardo/dataProcessingBackend.git>
   cd <project-directory>
   ```

2. Install the packages required:
   ```
   pip install -r requirements.txt
   ```

## Optional: Setting Up a Python Virtual Environment

Using a virtual environment is an optional but recommended approach to manage this project's Python dependencies separately from your global Python installation. It provides an isolated environment, ensuring project-specific dependencies don’t conflict with other projects.

### Working with a Virtual Environment (Optional)

It could be handy because you do not need to install on your machine all the libraries.

1. **Navigate to the Project Directory:**

   - Open your terminal or command prompt and navigate to the root of the cloned project directory.

2. **Create a Virtual Environment:**
   - Run the following command to create a new virtual environment named `venv` within your project folder:
     ```
     python -m venv venv
     ```

### Activating the Virtual Environment

- **On Windows:**
  .\venv\Scripts\activate

- **On MacOS/Linux:**
  source venv/bin/activate

### Installing Dependencies in the Virtual Environment (Optional)

- With the virtual environment activated, install the project-specific dependencies:
  pip install -r requirements.txt

## Running the project for the first time

1. The project is run using the following command :

   ```
      Using the preferred code editor run the app/app.py file

   ```

2. In order to use the login system, the user must login from the frontend.

### Libraries used

- blinker==1.7.0
- certifi==2023.11.17
- charset-normalizer==3.3.2
- click==8.1.7
- colorama==0.4.6
- Flask==3.0.0
- Flask-Cors==4.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-Testing==0.8.1
- greenlet==3.0.3
- idna==3.6
- itsdangerous==2.1.2
- Jinja2==3.1.3
- mailjet-rest==1.3.4
- MarkupSafe==2.1.3
- PyJWT==2.8.0
- pyodbc==5.0.1
- python-dateutil==2.8.2
- python-dotenv==1.0.0
- requests==2.31.0
- six==1.16.0
- SQLAlchemy==2.0.25
- typing_extensions==4.9.0
- urllib3==2.1.0
- Werkzeug==3.0.1
- Xmlify==0.1.1
