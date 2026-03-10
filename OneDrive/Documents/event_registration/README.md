# Event Registration System

A modern, responsive Event Registration System built with Flask and styled with Bootstrap 5 and custom CSS.

## Features
- Public facing events listing with search
- Responsive registration form with validation
- Modern, clean, and vibrant UI
- Admin portal for managing events
- View attendees for each event

## Prerequisites
- Python 3.8+

## Installation & Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd event_registration
   ```

2. **(Optional but recommended) Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On macOS/Linux: source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database and Add Sample Data**
   
   Run the seed script to create the initial tables and populate them with sample events:
   ```bash
   python seed.py
   ```
   *Note: Running `seed.py` will delete any existing database data and recreate it.*

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   - Open your web browser and navigate to: `http://127.0.0.1:5000/`

## Admin Access
- **URL**: `http://127.0.0.1:5000/admin/login`
- **Default Username**: `admin`
- **Default Password**: `admin123`

## Project Structure
- `app.py`: Main Flask application with routes and logic
- `database.py`: SQLAlchemy database models configurations
- `seed.py`: Script to populate the database with sample data
- `requirements.txt`: Python package dependencies
- `static/css/style.css`: Custom styling for modern aesthetics
- `templates/`: HTML templates (Jinja2) for the frontend and admin dashboard
