import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from forms import PsychologistForm, RegistrationForm, LoginForm, ProfileForm, ChangePasswordForm
from flask_wtf.csrf import CSRFProtect, generate_csrf
import traceback
import json
from models import db, User, Psychologist, Availability, Appointment, BlogPost, Settings, TestResult, Session
import logging
import time
import asyncio
from webrtc_manager import webrtc_manager
from redis_manager import redis_manager
from metrics_manager import metrics_manager

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///psikoloji.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['WTF_CSRF_TIME_LIMIT'] = None
app.config['WTF_CSRF_SSL_STRICT'] = False

db.init_app(app)

# Veritabanı tablolarını oluştur
with app.app_context():
    db.create_all()
    # Test verilerini yükle
    try:
        from testdata import create_test_data
        create_test_data(db)
    except Exception as e:
        print(f"Test verileri yüklenirken hata: {str(e)}")
    
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)

# CSRF token'ı her template'e ekle
@app.context_processor
def inject_csrf_token():
    token = generate_csrf()
    return dict(csrf_token=token)

# CSRF token'ı JavaScript için kullanılabilir hale getir
@app.after_request
def add_csrf_token_to_response(response):
    if 'text/html' in response.headers.get('Content-Type', ''):
        token = generate_csrf()
        response.set_cookie('csrf_token', token)
    return response

# Test türleri ve açıklamaları
TEST_TYPES = {
    'beck_depression': {
        'name': 'Beck Depresyon Envanteri',
        'description': 'Depresyon belirtilerinin şiddetini ölçen standart test'
    },
    'hamilton_anxiety': {
        'name': 'Hamilton Anksiyete Ölçeği',
        'description': 'Anksiyete belirtilerinin şiddetini ölçen standart test'
    },
    'social_anxiety': {
        'name': 'Liebowitz Sosyal Anksiyete Ölçeği',
        'description': 'Sosyal kaygı ve kaçınma davranışlarını ölçen standart test'
    },
    'perceived_stress': {
        'name': 'Algılanan Stres Ölçeği',
        'description': 'Algılanan stres düzeyini ölçen standart test'
    },
    'sleep_quality': {
        'name': 'Pittsburgh Uyku Kalitesi İndeksi',
        'description': 'Uyku kalitesini ve bozukluklarını değerlendiren standart test'
    }
}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hizmetler')
def services():
    return render_template('services.html')

@app.route('/ekibimiz')
def team():
    psychologists = Psychologist.query.all()
    return render_template('team.html', psychologists=psychologists)

@app.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/iletisim', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Burada form verilerini işleyebilirsiniz (örn: e-posta gönderme, veritabanına kaydetme)
        flash('Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

@app.route('/randevu', methods=['GET', 'POST'])
@login_required
def appointment():
    psychologists = Psychologist.query.all()  # Fetch psychologists
    if request.method == 'POST':
        new_appointment = Appointment(
            psychologist_id=request.form['psychologist_id'],
            client_name=request.form['name'],
            client_email=request.form['email'],
            client_phone=request.form['phone'],
            appointment_date=datetime.strptime(request.form['date'], '%Y-%m-%d')
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Yeni randevu eklendi!')
        return redirect(url_for('manage_appointments'))
    return render_template('appointment.html', psychologists=psychologists)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # LoginForm'u import ettim ve kullandım
    if form.validate_on_submit():  # Form validasyonunu ekledim
        username = form.username.data
        password = form.password.data
        
        if not username or not password:
            flash('Lütfen kullanıcı adı ve şifre giriniz', 'error')  # Flash mesajlarına kategori ekledim
            return redirect(url_for('login'))
            
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Başarıyla giriş yaptınız!', 'success')  # Flash mesajlarına kategori ekledim
            return redirect(url_for('admin_dashboard_panel'))
        flash('Geçersiz kullanıcı adı veya şifre', 'error')  # Flash mesajlarına kategori ekledim
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'error')
        return redirect(url_for('home'))
    return redirect(url_for('admin_dashboard_panel'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard_panel():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'error')
        return redirect(url_for('home'))
        
    # İstatistikleri hesapla
    total_appointments = Appointment.query.count()
    pending_appointments = Appointment.query.filter_by(status='pending').count()
    total_psychologists = Psychologist.query.count()
    total_posts = BlogPost.query.count()
    
    # Son randevuları al
    recent_appointments = Appointment.query.order_by(
        Appointment.date_requested.desc()
    ).limit(5).all()
    
    # Bugünün randevularını al
    today = datetime.now().date()
    today_appointments = Appointment.query.filter(
        db.func.date(Appointment.appointment_date) == today
    ).all()
    
    return render_template(
        'admin/dashboard.html',
        stats={
            'total_appointments': total_appointments,
            'pending_appointments': pending_appointments,
            'total_psychologists': total_psychologists,
            'total_posts': total_posts
        },
        recent_appointments=recent_appointments,
        today_appointments=today_appointments
    )

@app.route('/admin/appointments/pending')
@login_required
def pending_appointments():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'error')
        return redirect(url_for('home'))
        
    appointments = Appointment.query.filter_by(status='pending').order_by(
        Appointment.date_requested.desc()
    ).all()
    return render_template('admin/pending_appointments.html', appointments=appointments)

@app.route('/admin/appointment/update-status/<int:id>', methods=['POST'])
@login_required
def update_appointment_status(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkiniz yok'}), 403
        
    appointment = Appointment.query.get_or_404(id)
    status = request.form.get('status')
    
    if status not in ['confirmed', 'cancelled', 'completed']:
        return jsonify({'error': 'Geçersiz durum'}), 400
        
    try:
        appointment.status = status
        db.session.commit()
        
        # E-posta bildirimi gönder
        if status == 'confirmed':
            # TODO: Send confirmation email
            pass
        elif status == 'cancelled':
            # TODO: Send cancellation email
            pass
            
        return jsonify({
            'success': True,
            'message': 'Randevu durumu güncellendi'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/admin/reports')
@login_required
def admin_reports():
    # Aylık randevu istatistikleri
    month_stats = []
    psychologist_stats = []
    status_stats = []
    
    appointments = Appointment.query.all()
    if appointments:
        # Aylık istatistikler
        month_counts = {}
        for appt in appointments:
            month_key = appt.appointment_date.strftime('%Y-%m')
            month_counts[month_key] = month_counts.get(month_key, 0) + 1
        
        month_stats = [{'month': k, 'count': v} for k, v in month_counts.items()]
        month_stats.sort(key=lambda x: x['month'])

        # Psikolog bazlı istatistikler
        psych_counts = {}
        for appt in appointments:
            psych = Psychologist.query.get(appt.psychologist_id)
            if psych:
                psych_counts[psych.name] = psych_counts.get(psych.name, 0) + 1
        
        psychologist_stats = [{'name': k, 'count': v} for k, v in psych_counts.items()]
        psychologist_stats.sort(key=lambda x: x['count'], reverse=True)

        # Durum bazlı istatistikler
        status_counts = {}
        for appt in appointments:
            status_counts[appt.status] = status_counts.get(appt.status, 0) + 1
        
        status_stats = [{'status': k, 'count': v} for k, v in status_counts.items()]

    return render_template('admin/reports.html', 
                         month_stats=month_stats,
                         psychologist_stats=psychologist_stats,
                         status_stats=status_stats)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'error')
        return redirect(url_for('index'))

    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':
        if 'current_password' in request.form:
            # Şifre değiştirme işlemi
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if not check_password_hash(current_user.password_hash, current_password):
                flash('Mevcut şifre yanlış.', 'error')
            elif new_password != confirm_password:
                flash('Yeni şifreler eşleşmiyor.', 'error')
            else:
                current_user.password_hash = generate_password_hash(new_password)
                db.session.commit()
                flash('Şifreniz başarıyla güncellendi.', 'success')
        else:
            # Bildirim ayarları güncelleme
            settings.email_enabled = 'email_enabled' in request.form
            settings.sms_enabled = 'sms_enabled' in request.form
            settings.smtp_server = request.form.get('smtp_server')
            settings.smtp_port = int(request.form.get('smtp_port', 587))
            settings.smtp_username = request.form.get('smtp_username')
            
            # SMTP şifresi sadece değiştirilmek istenirse güncelle
            new_smtp_password = request.form.get('smtp_password')
            if new_smtp_password:
                settings.smtp_password = new_smtp_password
                
            settings.sms_api_key = request.form.get('sms_api_key')
            settings.notification_template = request.form.get('notification_template')
            
            db.session.commit()
            flash('Ayarlar başarıyla güncellendi.', 'success')

    return render_template('admin/settings.html', settings=settings)

@app.route('/admin/psychologists')
@login_required
def admin_psychologists():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'error')
        return redirect(url_for('home'))
        
    psychologists = Psychologist.query.all()
    return render_template('admin/psychologists.html', psychologists=psychologists)

@app.route('/admin/psychologist/add', methods=['GET', 'POST'])
@login_required
def add_psychologist():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'error')
        return redirect(url_for('home'))
        
    form = PsychologistForm()
    
    if form.validate_on_submit():
        try:
            psychologist = Psychologist(
                name=form.name.data,
                title=form.title.data,
                specialization=form.specialization.data,
                about=form.about.data,
                email=form.email.data,
                phone=form.phone.data
            )
            
            if form.photo.data:
                file = form.photo.data
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    psychologist.photo = filename
            
            db.session.add(psychologist)
            db.session.commit()
            
            flash('Psikolog başarıyla eklendi.', 'success')
            return redirect(url_for('admin_psychologists'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Bir hata oluştu: {str(e)}', 'error')
            
    return render_template('admin/add_psychologist.html', form=form)

@app.route('/admin/psychologist/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_psychologist(id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'error')
        return redirect(url_for('home'))
        
    psychologist = Psychologist.query.get_or_404(id)
    form = PsychologistForm(obj=psychologist)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(psychologist)
            
            if form.photo.data:
                file = form.photo.data
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    psychologist.photo = filename
            
            db.session.commit()
            flash('Psikolog bilgileri güncellendi.', 'success')
            return redirect(url_for('admin_psychologists'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Bir hata oluştu: {str(e)}', 'error')
    
    return render_template('admin/edit_psychologist.html', form=form, psychologist=psychologist)

@app.route('/admin/psychologist/delete/<int:id>', methods=['POST'])
@login_required
def delete_psychologist(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkiniz yok'}), 403
        
    try:
        psychologist = Psychologist.query.get_or_404(id)
        
        # Önce psikoloğa ait randevuları sil
        Appointment.query.filter_by(psychologist_id=id).delete()
        
        # Sonra psikoloğu sil
        db.session.delete(psychologist)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Psikolog başarıyla silindi'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/admin/blog', methods=['GET', 'POST'])
@login_required
def manage_blog():
    posts = BlogPost.query.all()
    if request.method == 'POST':
        new_post = BlogPost(
            title=request.form['title'],
            content=request.form['content'],
            image_url=request.form.get('image_url', '')
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Yeni blog yazısı eklendi!')
        return redirect(url_for('manage_blog'))
    return render_template('admin/manage_blog.html', posts=posts)

@app.route('/admin/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    if request.method == 'POST':
        new_post = BlogPost(
            title=request.form['title'],
            content=request.form['content'],
            image_url=request.form.get('image_url', '')
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Yeni blog yazısı eklendi!')
        return redirect(url_for('manage_blog'))
    return render_template('admin/new_blog.html')

@app.route('/admin/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.image_url = request.form.get('image_url', post.image_url)
        db.session.commit()
        flash('Blog yazısı güncellendi!')
        return redirect(url_for('manage_blog'))
    return render_template('admin/edit_blog.html', post=post)

@app.route('/admin/blog/delete/<int:id>', methods=['POST'])
@login_required
def delete_blog(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Blog yazısı silindi!')
    return redirect(url_for('manage_blog'))

# Admin Appointment Management
@app.route('/admin/appointments')
@login_required
def manage_appointments():
    appointments = Appointment.query.all()
    return render_template('admin/manage_appointments.html', appointments=appointments)

@app.route('/admin/appointment/delete/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Randevu silindi!')
    return redirect(url_for('manage_appointments'))

@app.route('/admin/appointment/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    psychologists = Psychologist.query.all()
    if request.method == 'POST':
        appointment.client_name = request.form['client_name']
        appointment.client_email = request.form['client_email']
        appointment.client_phone = request.form['client_phone']
        appointment.psychologist_id = request.form['psychologist_id']
        appointment.status = request.form['status']
        db.session.commit()
        flash('Randevu güncellendi!')
        return redirect(url_for('manage_appointments'))
    return render_template('admin/edit_appointment.html', appointment=appointment, psychologists=psychologists)

# API Routes
@app.route('/api/psychologists')
def get_psychologists():
    """Get list of all psychologists"""
    psychologists = Psychologist.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'title': p.title,
        'specialization': p.specialization
    } for p in psychologists])

@app.route('/api/message', methods=['POST'])
def send_message():
    """Send a contact message"""
    data = request.get_json() or request.form
    try:
        # Here you would typically implement email sending logic
        # For now, we'll just return a success message
        return jsonify({'success': True, 'message': 'Message sent successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/psychologist/<int:psychologist_id>/availability')
def get_availability(psychologist_id):
    """Get a psychologist's availability information"""
    # Get base availability
    psychologist = Psychologist.query.get_or_404(psychologist_id)
    availabilities = []
    for availability in psychologist.availabilities:
        availabilities.append({
            'day': availability.day_of_week,
            'start': availability.start_time.strftime('%H:%M'),
            'end': availability.end_time.strftime('%H:%M')
        })

    # Get appointments if date range is provided
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    if start_date and end_date:
        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            
            appointments = Appointment.query.filter(
                Appointment.psychologist_id == psychologist_id,
                Appointment.appointment_date.between(start, end)
            ).all()
            
            # Convert appointments to events
            events = []
            for apt in appointments:
                events.append({
                    'title': 'Dolu',
                    'start': apt.appointment_date.isoformat(),
                    'color': '#ff9999',
                    'available': False
                })
                
            return jsonify({
                'availabilities': availabilities,
                'appointments': events
            })
            
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    
    return jsonify(availabilities)

@app.route('/api/availability/calendar/<int:psychologist_id>')
def get_availability_calendar(psychologist_id):
    """Get calendar view of psychologist availability"""
    # Get date range from query parameters
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    if not start_date or not end_date:
        # Default to 30 days from today if no range specified
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
    else:
        try:
            start_date = datetime.fromisoformat(start_date)
            end_date = datetime.fromisoformat(end_date)
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    
    events = []
    current_date = start_date
    
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            events.append({
                'start': current_date.strftime('%Y-%m-%d'),
                'title': 'Müsait Değil',
                'available': False
            })
            current_date += timedelta(days=1)
            continue
        
        # Check appointments for this day
        day_appointments = Appointment.query.filter(
            Appointment.psychologist_id == psychologist_id,
            Appointment.appointment_date >= datetime.combine(current_date, datetime.min.time()),
            Appointment.appointment_date < datetime.combine(current_date + timedelta(days=1), datetime.min.time())
        ).count()
        
        # Maximum 8 appointments per day
        if day_appointments >= 8:
            events.append({
                'start': current_date.strftime('%Y-%m-%d'),
                'title': 'Dolu',
                'available': False
            })
        else:
            events.append({
                'start': current_date.strftime('%Y-%m-%d'),
                'title': 'Müsait',
                'available': True
            })
        
        current_date += timedelta(days=1)
    
    return jsonify({'events': events})

@app.route('/get-timeslots')
def get_timeslots():
    """Get available time slots for a specific date"""
    try:
        psychologist_id = request.args.get('psikolog_id')
        date_str = request.args.get('date')
        
        if not psychologist_id or not date_str:
            return jsonify({'error': 'Psikolog ID ve tarih gerekli'}), 400
            
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Geçersiz tarih formatı'}), 400
    
    # Get psychologist's availability for this day of week
    day_of_week = target_date.weekday()  # 0 = Monday, 6 = Sunday
    availability = Availability.query.filter_by(
        psychologist_id=psychologist_id,
        day_of_week=day_of_week
    ).first()
    
    if not availability:
        return jsonify({'timeSlots': []})  # Psikolog bu gün müsait değil
    
    # Get all appointments for this day
    day_appointments = Appointment.query.filter(
        Appointment.psychologist_id == psychologist_id,
        Appointment.appointment_date >= datetime.combine(target_date, datetime.min.time()),
        Appointment.appointment_date < datetime.combine(target_date + timedelta(days=1), datetime.min.time())
    ).all()
    
    # Generate time slots based on availability
    start_time = availability.start_time
    end_time = availability.end_time
    slot_duration = timedelta(hours=1)  # 1 saat aralıklarla
    
    current_slot = datetime.combine(target_date, start_time)
    end_datetime = datetime.combine(target_date, end_time)
    
    all_slots = []
    while current_slot < end_datetime:
        all_slots.append(current_slot.strftime('%H:%M'))
        current_slot += slot_duration
    
    # Remove booked times
    booked_times = [apt.appointment_date.strftime('%H:%M') for apt in day_appointments]
    available_slots = [slot for slot in all_slots if slot not in booked_times]
    
    return jsonify({'timeSlots': available_slots})

@app.route('/api/availability/timeslots/<int:psychologist_id>/<date>')
def get_timeslots_api(psychologist_id, date):
    """Get available time slots for a specific date"""
    try:
        target_date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Get all appointments for this day
    day_appointments = Appointment.query.filter(
        Appointment.psychologist_id == psychologist_id,
        Appointment.appointment_date >= datetime.combine(target_date, datetime.min.time()),
        Appointment.appointment_date < datetime.combine(target_date + timedelta(days=1), datetime.min.time())
    ).all()
    
    # All possible time slots
    all_slots = [
        '09:00', '10:00', '11:00', '12:00',
        '14:00', '15:00', '16:00', '17:00'
    ]
    
    # Remove booked times
    booked_times = [apt.appointment_date.strftime('%H:%M') for apt in day_appointments]
    available_slots = [slot for slot in all_slots if slot not in booked_times]
    
    return jsonify({'timeSlots': available_slots})

@app.route('/create-appointment', methods=['POST'])
def create_appointment():
    """Create a new appointment"""
    data = request.get_json() or request.form
    try:
        # Parse appointment date from ISO format
        date_str = data['date']
        if 'T' not in date_str:  # If time is not included
            return jsonify({'success': False, 'error': 'Lütfen randevu saatini seçin'}), 400
            
        appointment_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        
        # Check if slot is available
        existing = Appointment.query.filter_by(
            psychologist_id=int(data['psikolog_id']),
            appointment_date=appointment_date
        ).first()
        
        if existing:
            return jsonify({'success': False, 'error': 'Bu randevu saati dolu'}), 400
            
        # Create new appointment
        appointment = Appointment(
            psychologist_id=int(data['psikolog_id']),
            client_name=data['name'],
            client_email=data['email'],
            client_phone=data['phone'],
            appointment_date=appointment_date,
            status='pending'
        )
        db.session.add(appointment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Randevunuz başarıyla oluşturuldu',
            'id': appointment.id
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Geçersiz tarih formatı: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/appointment/create', methods=['POST'])
def api_create_appointment():
    """Create a new appointment"""
    data = request.get_json() or request.form
    try:
        # Parse appointment date
        if 'time' in data:
            # Handle separate date and time fields
            appointment_date = datetime.strptime(
                f"{data['date']} {data['time']}", 
                '%Y-%m-%d %H:%M'
            )
        else:
            # Handle combined datetime field
            appointment_date = datetime.fromisoformat(data['appointment_date'])
        
        # Check if slot is available
        existing = Appointment.query.filter_by(
            psychologist_id=int(data['psychologist_id']),
            appointment_date=appointment_date
        ).first()
        
        if existing:
            return jsonify({'error': 'This time slot is already booked'}), 400
            
        # Create new appointment
        appointment = Appointment(
            psychologist_id=int(data['psychologist_id']),
            client_name=data['client_name'] or data.get('name'),
            client_email=data.get('client_email') or data.get('email'),
            client_phone=data.get('client_phone') or data.get('phone'),
            appointment_date=appointment_date,
            status='pending'
        )
        db.session.add(appointment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Appointment created successfully',
            'id': appointment.id
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/tests')
@login_required
def tests():
    return render_template('tests.html')

@app.route('/submit_test', methods=['POST'])
@login_required
def submit_test():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Veri bulunamadı'}), 400
            
        test_type = data.get('test_type')
        answers = data.get('answers')
        score = data.get('score')
        
        if not all([test_type, answers, score is not None]):
            return jsonify({'error': 'Eksik veri'}), 400
            
        if test_type not in TEST_TYPES:
            return jsonify({'error': f'Geçersiz test türü: {test_type}'}), 400
            
        # Test sonucunu kaydet
        test_result = TestResult(
            user_id=current_user.id,
            test_type=test_type,
            answers=json.dumps(answers),
            score=score,
            created_at=datetime.utcnow()
        )
        
        db.session.add(test_result)
        db.session.commit()
        
        return jsonify({'message': 'Test sonuçları başarıyla kaydedildi'})
        
    except Exception as e:
        app.logger.error(f'Test sonuçları kaydedilirken hata: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/test_results')
@login_required
def test_results():
    try:
        # Kullanıcının test sonuçlarını al
        user_results = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.created_at.desc()).all()
        
        # Sonuçları formatla
        formatted_results = []
        for result in user_results:
            test_info = TEST_TYPES.get(result.test_type, {})
            formatted_result = {
                'test_name': test_info.get('title', result.test_type),
                'description': test_info.get('description', ''),
                'score': result.score,
                'date': result.created_at.strftime('%d.%m.%Y %H:%M'),
                'answers': result.answers
            }
            formatted_results.append(formatted_result)
        
        return render_template('test_results.html', results=formatted_results)
    except Exception as e:
        app.logger.error(f"Error in test_results route: {str(e)}")
        flash('Test sonuçları görüntülenirken bir hata oluştu.', 'error')
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.password_hash = generate_password_hash(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Hesap oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.', 'danger')
    
    return render_template('register.html', form=form)

def save_profile_picture(form_picture):
    if form_picture:
        filename = secure_filename(form_picture.filename)
        # Generate unique filename
        _, ext = os.path.splitext(filename)
        picture_filename = f'profile_{current_user.id}{ext}'
        picture_path = os.path.join(app.root_path, 'static/uploads/profile_pics', picture_filename)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(picture_path), exist_ok=True)
        
        # Save the file
        form_picture.save(picture_path)
        return f'uploads/profile_pics/{picture_filename}'
    return None

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile_form = ProfileForm(current_user.username, current_user.email)
    password_form = ChangePasswordForm()
    today = datetime.now()
    
    # Tüm randevuları al
    appointments = Appointment.query.all()
    
    if profile_form.submit.data and profile_form.validate_on_submit():
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        
        if profile_form.profile_picture.data:
            picture_file = save_profile_picture(profile_form.profile_picture.data)
            if picture_file:
                current_user.profile_picture = picture_file
        
        db.session.commit()
        flash('Profil bilgileriniz güncellendi.', 'success')
        return redirect(url_for('profile'))
        
    elif password_form.submit.data and password_form.validate_on_submit():
        if current_user.check_password(password_form.current_password.data):
            current_user.password_hash = generate_password_hash(password_form.new_password.data)
            db.session.commit()
            flash('Şifreniz başarıyla değiştirildi.', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Mevcut şifreniz yanlış.', 'danger')
    
    # Pre-fill the profile form with current data
    if request.method == 'GET':
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
    
    return render_template('profile.html', 
                         profile_form=profile_form,
                         password_form=password_form,
                         today=today,
                         appointments=appointments)  # Tüm randevuları gönder

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/sessions')
@login_required
def sessions():
    return render_template('sessions.html')

@app.route('/get_appointments/<int:psychologist_id>')
@login_required
def get_appointments(psychologist_id):
    try:
        # Psikoloğun randevularını getir
        appointments = Appointment.query.filter_by(
            psychologist_id=psychologist_id
        ).all()
        
        events = []
        for appointment in appointments:
            # Her randevu için bir event oluştur
            event = {
                'start': appointment.appointment_date.strftime('%Y-%m-%d %H:%M:00'),
                'end': (appointment.appointment_date + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:00')
            }
            events.append(event)
        
        return jsonify(events)
    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify([])

@app.route('/save_appointment', methods=['POST'])
@login_required
def save_appointment():
    try:
        data = request.get_json()
        
        print("Gelen veri:", data)  # Debug için veriyi yazdır
        
        # Tarih ve saat bilgisini birleştir
        date_str = data.get('date')
        time_str = data.get('time')
        print(f"Tarih: {date_str}, Saat: {time_str}")  # Debug için yazdır
        
        if not date_str or not time_str:
            return jsonify({
                'success': False,
                'message': 'Tarih ve saat bilgisi eksik!'
            }), 400
            
        try:
            appointment_datetime = datetime.strptime(
                f"{date_str} {time_str}", 
                '%Y-%m-%d %H:%M'
            )
        except ValueError as e:
            print(f"Tarih parse hatası: {str(e)}")  # Debug için yazdır
            return jsonify({
                'success': False,
                'message': 'Geçersiz tarih veya saat formatı!'
            }), 400
        
        # Aynı tarih ve saatte başka randevu var mı kontrol et
        existing_appointment = Appointment.query.filter_by(
            appointment_date=appointment_datetime
        ).first()
        
        if existing_appointment:
            return jsonify({
                'success': False,
                'message': 'Bu tarih ve saat için randevu dolu!'
            })
        
        psychologist_id = data.get('psychologist_id')  
        if not psychologist_id:
            return jsonify({
                'success': False,
                'message': 'Psikolog seçimi yapılmadı!'
            }), 400
            
        # Yeni randevu oluştur
        new_appointment = Appointment(
            user_id=current_user.id,
            psychologist_id=psychologist_id,  
            client_name=current_user.username,  
            client_email=current_user.email,  
            appointment_date=appointment_datetime,
            appointment_type=data.get('appointment_type'),  # Görüşme türünü ekle
            status='pending'  
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Randevu başarıyla kaydedildi.'
        })
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Hata: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'Randevu kaydedilirken bir hata oluştu: {str(e)}'
        }), 500

# Global değişkenler
active_rooms = {}
client_rooms = {}

# SocketIO yapılandırması
socketio = SocketIO(
    app,
    async_mode='eventlet',
    ping_timeout=60,
    ping_interval=25,
    cors_allowed_origins="*",
    manage_session=False,
    logger=logger,
    engineio_logger=logger,
    max_http_buffer_size=5e8,  # 500MB
    async_handlers=True
)

# Initialize managers
def setup_managers():
    try:
        redis_manager.init()
        logger.info("Managers initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize managers: {e}")
        raise

# Call setup_managers when app starts
with app.app_context():
    setup_managers()

@socketio.on('connect')
def handle_connect():
    logger.info(f"Client connected: {request.sid}")
    metrics_manager.participant_joined.inc()

@socketio.on('disconnect')
def handle_disconnect():
    try:
        sid = request.sid
        room_data = redis_manager.get_participant_status(None, sid)
        if room_data and 'room_id' in room_data:
            webrtc_manager.remove_participant(room_data['room_id'], sid)
            metrics_manager.active_participants.dec()
        logger.info(f"Client disconnected: {sid}")
    except Exception as e:
        logger.error(f"Error in disconnect handler: {e}")
        metrics_manager.record_error("disconnect_error")

@socketio.on('join')
def join_session(data):
    with metrics_manager.track_connection_setup():
        try:
            room_id = data['room']
            sid = request.sid
            
            # Create or get room
            room = webrtc_manager.get_room(room_id)
            if not room:
                room = webrtc_manager.create_room(room_id)
                metrics_manager.room_created.inc()
            
            # Add participant
            participant = webrtc_manager.add_participant(room_id, sid)
            
            # Update Redis
            redis_manager.set_participant_status(room_id, sid, {
                'joined_at': time.time(),
                'room_id': room_id
            })
            
            # Update metrics
            metrics_manager.active_participants.inc()
            metrics_manager.active_rooms.set(len(webrtc_manager.rooms))
            
            # Join room
            join_room(room_id)
            
            # Get existing participants
            participants = webrtc_manager.get_room_participants(room_id)
            participant_list = [{'id': p.id, 'is_publisher': p.is_publisher} 
                              for p in participants.values() if p.id != sid]
            
            # Notify room
            emit('room_join', {
                'room': room_id,
                'count': len(participants),
                'participants': participant_list,
                'you': {'id': sid, 'is_publisher': False}
            }, room=room_id)
            
            logger.info(f"Client {sid} joined room {room_id}")
            
        except Exception as e:
            logger.error(f"Error in join_session: {e}")
            metrics_manager.record_error("join_error")
            emit('error', {'message': 'Failed to join session'})

@socketio.on('leave')
def leave_session(data):
    try:
        room_id = data['room']
        sid = request.sid
        
        webrtc_manager.remove_participant(room_id, sid)
        redis_manager.remove_participant_status(room_id, sid)
        
        leave_room(room_id)
        metrics_manager.active_participants.dec()
        
        emit('participant_left', {'participant_id': sid}, room=room_id)
        logger.info(f"Client {sid} left room {room_id}")
        
    except Exception as e:
        logger.error(f"Error in leave_session: {e}")
        metrics_manager.record_error("leave_error")

@socketio.on('signal')
def handle_signal(data):
    try:
        room_id = data['room']
        target_id = data['target']
        signal_data = data['signal']
        
        # Forward signal to target participant
        emit('signal', {
            'from': request.sid,
            'signal': signal_data
        }, room=target_id)
        
    except Exception as e:
        logger.error(f"Error handling signal: {e}")
        metrics_manager.record_error("signal_error")

@socketio.on('ping')
def handle_ping():
    try:
        sid = request.sid
        room_data = redis_manager.get_participant_status(None, sid)
        if room_data and 'room_id' in room_data:
            webrtc_manager.update_participant_ping(room_data['room_id'], sid)
            redis_manager.update_participant_status(room_data['room_id'], sid, {'last_ping': time.time()})
    except Exception as e:
        logger.error(f"Error handling ping: {e}")
        metrics_manager.record_error("ping_error")

@socketio.on('offer')
def handle_offer(data):
    try:
        room_id = data['room']
        sid = request.sid
        offer = data['offer']
        
        # Process WebRTC offer
        answer = webrtc_manager.process_offer(room_id, sid, offer)
        
        # Update participant status
        redis_manager.set_participant_status(room_id, sid, {
            'last_offer': time.time()
        })
        
        # Send answer back
        emit('answer', {'answer': answer.sdp})
        
    except Exception as e:
        logger.error(f"Error processing offer: {e}")
        metrics_manager.record_error("offer_error")
        emit('error', {'message': 'Failed to process offer'})

@socketio.on('ice-candidate')
def handle_ice_candidate(data):
    try:
        room_id = data['room']
        candidate = data['candidate']
        
        room = webrtc_manager.get_room(room_id)
        if room:
            # Forward candidate to other participants
            for participant_id in room.participants:
                if participant_id != request.sid:
                    emit('ice-candidate', {
                        'candidate': candidate
                    }, room=participant_id)
    except Exception as e:
        logger.error(f"Error handling ICE candidate: {e}")
        metrics_manager.record_error("ice_error")

@socketio.on('chat-message')
def on_chat_message(data):
    room_id = data['room']
    emit('chat-message', {'message': data['message']}, room=room_id, include_self=False)

@app.route('/session/<appointment_id>')
@login_required
def video_session(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Kullanıcının bu seansa erişim yetkisi var mı kontrol et
    if current_user.is_psychologist:
        # Terapistin email'i ile appointment'taki psikolog email'i eşleşmeli
        psychologist = Psychologist.query.filter_by(email=current_user.email).first()
        if not psychologist:
            flash('Psikolog kaydı bulunamadı.', 'error')
            return redirect(url_for('profile'))
        has_access = psychologist.id == appointment.psychologist_id
    else:
        has_access = current_user.id == appointment.user_id
        
    if not has_access:
        flash('Bu seansa erişim yetkiniz yok.', 'error')
        return redirect(url_for('profile'))
    
    # Oda ID'si oluştur
    room_id = f"session_{appointment_id}"
    
    # Kullanıcı terapist mi yoksa danışan mı kontrol et
    is_host = current_user.is_psychologist
    
    return render_template('video_session.html', 
                         room_id=room_id, 
                         is_host=is_host,
                         appointment=appointment)

@app.route('/health')
def health_check():
    try:
        # Redis bağlantısını kontrol et
        redis_ok = redis_manager.ping()
        
        # Metrics servisini kontrol et
        metrics_ok = metrics_manager.active_rooms.collect() is not None
        
        health_status = {
            'status': 'healthy' if redis_ok and metrics_ok else 'unhealthy',
            'redis': 'ok' if redis_ok else 'error',
            'metrics': 'ok' if metrics_ok else 'error',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(health_status), 200 if health_status['status'] == 'healthy' else 503
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503

if __name__ == '__main__':
    socketio.run(app, debug=True)
