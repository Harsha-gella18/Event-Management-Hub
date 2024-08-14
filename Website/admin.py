from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from .models import get_events_by_organizer, get_event_by_id, delete_event, add_event, update_event
from datetime import datetime
from bson.objectid import ObjectId
from .utils import login_required, admin_required  # Import the decorators

admin = Blueprint('admin', __name__)


@admin.route('/admin/add-event', methods=['GET', 'POST'])
@login_required
@admin_required
def add_new_event():
    if request.method == 'POST':
        # Collect form data
        title = request.form.get('title')
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        description = request.form.get('description')
        organizer = session.get('username', 'Unknown')  # Default value if not found
        price = request.form.get('price')
        total_count = request.form.get('total_count')

        # Handle missing or None values
        try:
            price = float(price) if price else 0.0
            total_count = int(total_count) if total_count else 0
            slots_left = total_count  # Set slots_left equal to total_count
        except ValueError as e:
            flash(f'Error processing the form data: {e}', 'danger')
            return redirect(url_for('admin.add_new_event'))

        # Create event data dictionary
        event_data = {
            'title': title,
            'date': date,
            'time': time,
            'location': location,
            'description': description,
            'organizer': organizer,
            'price': price,
            'TotalCount': total_count,
            'SlotsLeft': total_count,
        }

        # Add new event
        add_event(event_data)

        flash('Event added successfully.', 'success')
        return redirect(url_for('auth.admin_dashboard'))

    return render_template('add_event.html')  # Ensure this template exists for adding new events

@admin.route('/admin/edit-event/<event_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_event(event_id):
    event = get_event_by_id(ObjectId(event_id))  # Convert event_id to ObjectId

    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('auth.admin_dashboard'))

    # Ensure the admin can only edit their own events
    if event.get('organizer') != session.get('username'):
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('auth.admin_dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        description = request.form.get('description')

        # Retrieve and handle the form data
        price_str = request.form.get('price', '0')  # Default to '0' if not provided
        total_count_str = request.form.get('total_count', '0')  # Default to '0' if not provided

        try:
            # Convert form data to appropriate types
            price = float(price_str) if price_str.strip() else 0.0
            total_count = int(total_count_str) if total_count_str.strip() else 0
            slots_left = total_count  # Set slots_left equal to total_count
        except ValueError as e:
            flash(f'Error processing the form data: {e}', 'danger')
            return redirect(url_for('admin.edit_event', event_id=event_id))

        # Update event
        update_event(event_id, {
            'title': title,
            'date': date,
            'time': time,
            'location': location,
            'description': description,
            'price': price,
            'TotalCount': total_count,
            'SlotsLeft': slots_left,  # Corrected field
        })

        flash('Event updated successfully.', 'success')
        return redirect(url_for('auth.admin_dashboard'))

    return render_template('edit_event.html', event=event)

@admin.route('/admin/delete-event/<event_id>', methods=['POST'])
@login_required
@admin_required
def delete_event_route(event_id):
    event = get_event_by_id(ObjectId(event_id))

    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('auth.admin_dashboard'))

    # Ensure the admin can only delete their own events
    if event.get('organizer') != session.get('username'):
        flash('You do not have permission to delete this event.', 'danger')
        return redirect(url_for('auth.admin_dashboard'))

    # Delete event
    delete_event(event_id)

    flash('Event deleted successfully.', 'success')
    return redirect(url_for('auth.admin_dashboard'))
