
# Event Management System

An intuitive web application for managing and tracking events. This system allows users to register for events, admins to manage event details, and superadmins to oversee the entire platform.

## Features

- **User Roles:**
  - **User**: Can view and register for events.
  - **Admin**: Can manage events, including adding, updating, and deleting events.
  - **Superadmin**: Can manage all users and admins, and oversee the entire system.

## Tools & Technologies

- **Flask**: A lightweight WSGI web application framework in Python.
- **MongoDB**: NoSQL database used for storing user and event data.
- **Python**: Programming language used for backend development.
- **HTML**: Markup language for creating web pages.
- **Tailwind CSS**: Utility-first CSS framework for designing responsive, modern web interfaces.
  
## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Harsha-gella18/Event-Management-Hub.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd Event-Management-Hub
   ```

3. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. **Install the required packages:**

   ```bash
   pip install Flask pymongo python-dotenv
   ```

6. **Set up environment variables:**

   Create a `.env` file in the root directory and add the following:

   ```
   MONGO_URI=mongodb://localhost:27017
   SENDER_EMAIL=your_email
   EMAIL_PASSWORD=your_email_password
   ```

7. **Run the application:**

   Execute the `main.py` file to start the application:

   ```bash
   python main.py
   ```

   The application will be accessible at `http://127.0.0.1:5000` by default.

## Application Overview

- **User Dashboard**: Users can view and register for events. The dashboard also includes a profile section and a logout button.
  
- **Admin Dashboard**: Admins can view all events, manage event details, and perform CRUD operations.

- **Superadmin Dashboard**: Superadmins have access to all functionalities, including managing users and admins.

## Directory Structure

- `Website/`: Contains the main application code including routes, models, and database interactions.
  - `__init__.py`: Initializes the Flask application.
  - `auth.py`: Handles authentication and user routes.
  - `models.py`: Defines database models and functions.
  - `database.py`: Sets up MongoDB connections and operations.

## Contributing

Feel free to fork the repository and submit pull requests. For any issues or feature requests, please open an issue on GitHub.


```
