from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import get_event_by_id, delete_event_by_id, update_event, get_all_admins, get_all_events, get_all_users, get_registered_users_for_event,delete_user_by_id,get_user_by_id
from .utils import login_required, superadmin_required  # Import the decorators
from bson.objectid import ObjectId

superadmin = Blueprint('superadmin', __name__)

@superadmin.route('/superadmin/view_users')
@login_required
@superadmin_required
def view_users():
    users = get_all_users()  # Fetch all users from the database
    return render_template('view_users.html', users=users)

@superadmin.route('/superadmin/view_admins')
@login_required
@superadmin_required
def view_admins():
    admins = get_all_admins()  # Fetch all admins from the database
    return render_template('view_admin.html', admins=admins)

@superadmin.route('/superadmin/view_all_events')
@login_required
@superadmin_required
def view_all_events():
    events = get_all_events()  # Fetch all events from the database
    return render_template('view_all_events.html', events=events)

@superadmin.route('/superadmin/edit_event_by_admin/<event_id>', methods=['GET', 'POST'])
@login_required
@superadmin_required
def edit_event_by_admin(event_id):
    event = get_event_by_id(event_id)  # Fetch event details by ID

    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('superadmin.view_all_events'))  # Redirect to some events listing page

    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        description = request.form.get('description')

        price_str = request.form.get('price', '0')
        total_count_str = request.form.get('total_count', '0')

        try:
            price = float(price_str) if price_str.strip() else 0.0
            total_count = int(total_count_str) if total_count_str.strip() else 0
            slots_left = total_count
        except ValueError as e:
            flash(f'Error processing the form data: {e}', 'danger')
            return redirect(url_for('superadmin.edit_event_by_admin', event_id=event_id))

        update_event(event_id, {
            'title': title,
            'date': date,
            'time': time,
            'location': location,
            'description': description,
            'price': price,
            'TotalCount': total_count,
            'SlotsLeft': slots_left,
        })

        flash('Event updated successfully.', 'success')
        return redirect(url_for('superadmin.view_all_events'))

    return render_template('edit_event_by_admin.html', event=event)

@superadmin.route('/superadmin/delete_event_by_admin/<event_id>', methods=['POST'])
@login_required
@superadmin_required
def delete_event_by_admin(event_id):
    # Logic to delete the event by event_id
    result = delete_event_by_id(event_id)  # Your function to delete the event
    if result:
        flash('Event deleted successfully.', 'success')
    else:
        flash('Error deleting event.', 'danger')
    return redirect(url_for('superadmin.view_all_events'))  # Redirect to a page showing all events

@superadmin.route('/superadmin/registered_users/<event_id>', methods=['GET'])
@login_required
@superadmin_required
def view_registered_users(event_id):
    event = get_event_by_id(ObjectId(event_id))  # Convert event_id to ObjectId

    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('superadmin.view_all_events'))

    # Fetch the registered users for the event
    registered_users = get_registered_users_for_event(ObjectId(event_id))  # Implement this function

    return render_template('registered_users.html', event=event, registered_users=registered_users)

@superadmin.route('/superadmin/delete_user_by_admin/<user_id>', methods=['POST'])
@login_required
@superadmin_required
def delete_user_by_admin(user_id):
    # Fetch the user before deleting to determine their role
    user = get_user_by_id(user_id)
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('superadmin.view_users'))  # Redirect to users view if user not found

    success = delete_user_by_id(user_id)  # Call the model function to delete the user

    if success:
        flash('User deleted successfully.', 'success')
        # Redirect to the appropriate page based on the user's role
        if user['role'] == 'admin':
            return redirect(url_for('superadmin.view_admins'))
        else:
            return redirect(url_for('superadmin.view_users'))
    else:
        flash('Error deleting user.', 'danger')
        if user['role'] == 'admin':
            return redirect(url_for('superadmin.view_admins'))
        else:
            return redirect(url_for('superadmin.view_users'))
