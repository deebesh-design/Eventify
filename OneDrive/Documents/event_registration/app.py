from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db, Admin, Event, Registration
import os

app = Flask(__name__)
app.secret_key = 'super_secret_event_key_xyz' # Change for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # Create default admin if not exists
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

# --- Routes for Public ---

@app.route('/')
def home():
    events = Event.query.order_by(Event.id.desc()).limit(3).all()
    return render_template('index.html', events=events)

@app.route('/events')
def events():
    search = request.args.get('search', '')
    if search:
        events_list = Event.query.filter(Event.event_name.ilike(f'%{search}%')).all()
    else:
        events_list = Event.query.all()
    return render_template('events.html', events=events_list, search=search)

@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
def register(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        participants = request.form.get('participants')
        
        if not name or not email or not phone or not participants:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('register', event_id=event_id))
            
        try:
            participants = int(participants)
            if participants < 1:
                flash('Participants must be at least 1.', 'danger')
                return redirect(url_for('register', event_id=event_id))
        except ValueError:
            flash('Invalid number of participants.', 'danger')
            return redirect(url_for('register', event_id=event_id))

        new_reg = Registration(
            name=name, email=email, phone=phone, 
            event_id=event_id, participants=participants
        )
        db.session.add(new_reg)
        db.session.commit()
        flash('Registration successful! We look forward to seeing you.', 'success')
        return redirect(url_for('home'))
        
    return render_template('register.html', event=event)

# --- Admin Routes ---

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            flash('Login successful', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    events_list = Event.query.order_by(Event.id.desc()).all()
    return render_template('admin/dashboard.html', events=events_list)


@app.route('/admin/events/create', methods=['GET', 'POST'])
@login_required
def admin_event_create():
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        date = request.form.get('date')
        location = request.form.get('location')
        description = request.form.get('description')
        
        if not all([event_name, date, location, description]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin_event_create'))
            
        new_event = Event(event_name=event_name, date=date, location=location, description=description)
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/create_event.html')

@app.route('/admin/events/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_event_edit(id):
    event = Event.query.get_or_404(id)
    if request.method == 'POST':
        event.event_name = request.form.get('event_name')
        event.date = request.form.get('date')
        event.location = request.form.get('location')
        event.description = request.form.get('description')
        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/edit_event.html', event=event)

@app.route('/admin/events/<int:id>/delete', methods=['POST'])
@login_required
def admin_event_delete(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/events/<int:id>/registrations')
@login_required
def admin_event_registrations(id):
    event = Event.query.get_or_404(id)
    return render_template('admin/registrations.html', event=event)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
