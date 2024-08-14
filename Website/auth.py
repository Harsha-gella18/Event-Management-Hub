from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import get_user, create_user, get_events, get_events_by_organizer, get_event_by_id, update_event, register_user_for_event, unregister_user_from_event, get_user_by_email, reset_user_password
from .utils import send_otp_email, verification, login_required, admin_required, user_required
from datetime import datetime
from bson.objectid import ObjectId

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')
        role = request.form.get('role')  # Role is selected from radio buttons

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('auth.register'))

        # Check if username already exists
        if get_user(username):
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Send OTP email
        if not send_otp_email(email):
            flash('Failed to send OTP. Please try again.', 'danger')
            return redirect(url_for('auth.register'))

        # Store user data in session
        session['email'] = email
        session['username'] = username
        session['password'] = password
        session['role'] = role

        return redirect(url_for('auth.verify_signup_otp'))

    return render_template('signup.html')

@auth.route('/verify_password_reset_otp', methods=['GET', 'POST'])
def verify_password_reset_otp():
    if request.method == 'POST':
        otp = request.form.get('otp')
        print(f"Entered OTP for Password Reset: {otp}")

        if verification(otp):
            return redirect(url_for('auth.reset_password'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('verify_otp.html', action_url=url_for('auth.verify_password_reset_otp'))

@auth.route('/verify_signup_otp', methods=['GET', 'POST'])
def verify_signup_otp():
    if request.method == 'POST':
        otp = request.form.get('otp')
        print(f"Entered OTP for Signup: {otp}")

        if verification(otp):
            if all(key in session for key in ['username', 'password', 'email', 'role']):
                hashed_password = generate_password_hash(session['password'], method='pbkdf2:sha256')
                create_user(session['username'], hashed_password, session['email'], session['role'])
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Missing session data for signup. Please try again.', 'danger')
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('verify_otp.html', action_url=url_for('auth.verify_signup_otp'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user is in the user collection
        user = get_user(username)
        if user:
            if check_password_hash(user['password'], password):
                session['username'] = username
                session['role'] = user['role']
                session['isLogin'] = True  # Track login status

                return redirect(url_for('auth.dashboard'))  # Redirect to user dashboard

            else:
                flash('Invalid username or password. Please try again.', 'danger')
                session['isLogin'] = False
        else:
            flash('User not found. Please try again.', 'danger')
            session['isLogin'] = False

    return render_template('login.html')

@auth.route('/dashboard')
@login_required
def dashboard():
    if session['role'] == 'user':
        return redirect(url_for('auth.user_dashboard'))
    elif session['role'] == 'super_admin':
        return redirect(url_for('auth.superadmin_dashboard'))
    elif session['role'] == 'admin':
        return redirect(url_for('auth.admin_dashboard'))
    else:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    session.pop('isLogin', None)
    flash('You have been logged out.', 'info')
    print("Session after logout:", session)  # Debug statement
    return redirect(url_for('auth.login'))

@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# Define admin routes with admin_required decorator
@auth.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    events = get_events_by_organizer(session['username'])
    for event in events:
        if 'date' in event and event['date']:
            try:
                event['date'] = datetime.strptime(event['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                event['date'] = 'Invalid date format'

    return render_template('admin_daashboard.html', events=events)

# Define user routes with user_required decorator
@auth.route('/user_dashboard')
@user_required
def user_dashboard():
    events = get_events()
    user = get_user(session['username'])
    
    if user:
        registered_events = [str(event_id) for event_id in user.get('registered_events', [])]
    else:
        registered_events = []
    
    print("Registered Events:", registered_events)  # Debug print
    
    return render_template('user_dashboard.html', events=events, registered_events=registered_events)

@auth.route('/superadmin_dashboard')
def superadmin_dashboard():
    return render_template('super_admin_dashboard.html')

@auth.route('/register_event', methods=['POST'])
@user_required
def register_event():
    event_id = request.form.get('event_id')
    user_id = get_user(session['username'])['_id']
    print(event_id)
    print(user_id)

    if register_user_for_event(event_id, user_id):
        flash('Successfully registered for the event.', 'success')
        print("Success")
    else:
        event = get_event_by_id(event_id)
        if event:
            if event['SlotsLeft'] <= 0:
                flash('No slots available for this event.', 'danger')
            elif user_id in event.get('registered_users', []):
                flash('You are already registered for this event.', 'warning')
        else:
            flash('Event not found.', 'danger')

    return redirect(url_for('auth.user_dashboard'))

@auth.route('/unregister_event', methods=['POST'])
@user_required
def unregister_event():
    event_id = request.form.get('event_id')
    username = session.get('username')
    user = get_user(username)
    
    if user:
        user_id = user['_id']
        if unregister_user_from_event(event_id, user_id):
            flash('You have successfully unregistered from the event.', 'success')
        else:
            flash('Failed to unregister from the event.', 'danger')
    else:
        flash('User not found.', 'danger')
    
    return redirect(url_for('auth.user_dashboard'))

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        session['email'] = email
        user = get_user_by_email(email)  # Fetch user by email
        if user:
            # Send OTP to user’s email
            send_otp_email(email)

            return redirect(url_for('auth.verify_password_reset_otp', email=email))
        else:
            flash('Email not found.', 'danger')
    return render_template('forgot_password.html')

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        email = session.get('email')

        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
        else:
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            if reset_user_password(email, hashed_password):
                flash('Password reset successful. You can now log in with your new password.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Failed to reset password. Please try again.', 'danger')

    return render_template('reset_password.html')
