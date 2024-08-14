import random
import smtplib
from email.mime.text import MIMEText
from flask import current_app, session, flash, redirect, url_for
from functools import wraps
from .models import get_user_by_id  
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

def send_otp_email(mail):
    otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
    session['otp'] = otp  # Store the OTP in session for verification

    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = mail
    subject = 'Your OTP Code'
    body = f'Your OTP code is {otp}'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, os.getenv('EMAIL_PASSWORD'))
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        flash(f'Error sending OTP: {e}', 'danger')
        return False


def verification(input_otp):
    actual_otp = session.get('otp')
    return input_otp == actual_otp

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'user':
            flash('Access denied. Users only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session.get('role') != 'super_admin':
            flash('Access denied. Superadmins only.', 'danger')
            return redirect(url_for('auth.login'))  # Redirect to login if not superadmin
        return f(*args, **kwargs)
    return decorated_function
