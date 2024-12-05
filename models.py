from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    profile_picture = db.Column(db.String(255), default='default_profile.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_psychologist = db.Column(db.Boolean, default=False)  # Terapist mi değil mi?
    test_results = db.relationship('TestResult', backref='user', lazy=True)
    sessions = db.relationship('Session', backref='user', lazy=True)
    
    # Ana randevu ilişkisi
    appointments = db.relationship('Appointment',
                                 backref='client',
                                 lazy=True,
                                 foreign_keys='Appointment.user_id')
    
    # İkincil randevu ilişkisi (viewonly)
    user_appointments = db.relationship('Appointment',
                                      lazy=True,
                                      foreign_keys='Appointment.user_id',
                                      overlaps="appointments,client",
                                      viewonly=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Psychologist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))
    specialization = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    
    # Ana randevu ilişkisi
    appointments = db.relationship('Appointment',
                                 backref='psychologist',
                                 lazy=True,
                                 foreign_keys='Appointment.psychologist_id')
    
    # İkincil randevu ilişkisi (viewonly)
    therapist_appointments = db.relationship('Appointment',
                                           lazy=True,
                                           foreign_keys='Appointment.psychologist_id',
                                           overlaps="appointments,psychologist",
                                           viewonly=True)

    def __repr__(self):
        return f'<Psychologist {self.name}>'

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    psychologist_id = db.Column(db.Integer, db.ForeignKey('psychologist.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    psychologist_id = db.Column(db.Integer, db.ForeignKey('psychologist.id'), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    appointment_type = db.Column(db.String(50), nullable=False)
    is_online = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')
    date_requested = db.Column(db.DateTime, default=datetime.utcnow)

    # Sadece foreign key ilişkileri
    therapist = db.relationship('Psychologist', 
                              foreign_keys=[psychologist_id],
                              overlaps="appointments,psychologist")
    
    user = db.relationship('User', 
                         foreign_keys=[user_id],
                         overlaps="appointments,client")

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200))

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_enabled = db.Column(db.Boolean, default=False)
    sms_enabled = db.Column(db.Boolean, default=False)
    smtp_server = db.Column(db.String(100))
    smtp_port = db.Column(db.Integer, default=587)
    smtp_username = db.Column(db.String(100))
    smtp_password = db.Column(db.String(100))
    sms_api_key = db.Column(db.String(100))
    notification_template = db.Column(db.Text)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    answers = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<TestResult {self.id} - User {self.user_id} - Type {self.test_type}>'

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    therapist_name = db.Column(db.String(100), nullable=False)
    session_date = db.Column(db.DateTime, nullable=False)
    session_type = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
